#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["pytest>=8,<10", "pydantic>=2,<3", "typer>=0.16,<1", "pillow>=11,<13"]
# ///
# How to run: uv run --with pytest --with pydantic --with typer --with pillow python3 -m pytest -q scripts/test_planexpert_counter_import.py
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest
from PIL import Image

SCRIPT = Path(__file__).with_name("planexpert_counter_import.py")
QPL = b'''\xef\xbb\xbf<?xml version="1.0" encoding="utf-8"?>\r\n<QuoterPlanSession>
<Project Name="Preserve &amp; retain"/><Workspace><ActivePlan Name="A"/></Workspace>
<Plans><Plan Name="A" FileName="current.png"><Scale Value="17.5"/>
<Layers><Layer Index="0" Name="A &gt; B"><Line GroupID="7"><Element X1="1" X2="3"/></Line>
</Layer></Layers></Plan></Plans><Reports><!--keep exactly--></Reports></QuoterPlanSession>'''


@pytest.fixture
def project(tmp_path: Path) -> Path:
    (tmp_path / "source.qpl").write_bytes(QPL)
    Image.new("RGB", (800, 400)).save(tmp_path / "current.png")
    (tmp_path / "points.csv").write_text(
        "sheet,label,x_pt,y_pt,occurrence_id,status\nS1,Luminaire,25,50,a,confirmed\n"
        "S1,Luminaire,100,100,b,review\n", encoding="utf-8"
    )
    (tmp_path / "mapping.json").write_text(json.dumps({"sheets": [{
        "sheet": "S1", "plan_name": "A", "layer_index": "0",
        "page_width_pt": 200, "page_height_pt": 100,
    }]}), encoding="utf-8")
    return tmp_path


def invoke(project: Path, options: tuple[str, ...] = ()) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(project / "source.qpl"),
         str(project / "points.csv"), str(project / "mapping.json"),
         str(project / "result.qpl"), *options], capture_output=True, text=True, check=False,
    )


def test_append_when_valid_preserves_original_and_measurements(project: Path) -> None:
    result = invoke(project)
    assert result.returncode == 0, result.stderr
    output = (project / "result.qpl").read_bytes()
    tree = ET.fromstring(output)
    counter = tree.find("./Plans/Plan/Layers/Layer/Counter")
    assert counter is not None
    assert counter.attrib["GroupID"] == "8"
    assert [(point.get("X"), point.get("Y")) for point in counter] == [("100", "200"), ("400", "400")]
    start, end = output.index(b"<Counter "), output.index(b"</Counter>") + len(b"</Counter>")
    assert output[:start] + output[end:] == QPL
    assert (project / "source.qpl").read_bytes() == QPL
    audit = json.loads((project / "result.qpl.audit.json").read_text())
    assert audit["count_by_sheet_label"] == {"S1": {"Luminaire": 2}}
    assert audit["occurrences"] == 2 and audit["new_line_count"] == 0 and audit["new_area_count"] == 0
    assert audit["unique_occurrence_ids"] == 2
    assert audit["points"][1]["status"] == "review"


@pytest.mark.parametrize("fault", ["duplicate", "bounds", "nan", "sheet", "background", "layer", "group_id", "exists", "audit_exists", "same_input", "empty"])
def test_reject_when_source_contract_invalid(project: Path, fault: str) -> None:
    # Given one invalid boundary and an unchanged source file.
    csv_path, qpl_path = project / "points.csv", project / "source.qpl"
    modifications = {
        "duplicate": lambda: csv_path.write_text(csv_path.read_text().replace(",b,", ",a,")),
        "bounds": lambda: csv_path.write_text(csv_path.read_text().replace(",25,", ",201,")),
        "nan": lambda: csv_path.write_text(csv_path.read_text().replace(",25,", ",NaN,")),
        "sheet": lambda: csv_path.write_text(csv_path.read_text().replace("S1,", "missing,")),
        "background": lambda: (project / "current.png").unlink(),
        "layer": lambda: qpl_path.write_bytes(QPL.replace(b'Index="0"', b'Index="1"')),
        "group_id": lambda: qpl_path.write_bytes(QPL.replace(b"</Layer>", b'<Counter GroupID="7"/></Layer>')),
        "exists": lambda: (project / "result.qpl").write_bytes(b"owned"),
        "audit_exists": lambda: (project / "result.qpl.audit.json").write_bytes(b"owned"),
        "same_input": lambda: (project / "result.qpl").symlink_to(qpl_path),
        "empty": lambda: csv_path.write_text("sheet,label,x_pt,y_pt\n"),
    }
    modifications[fault]()
    before = qpl_path.read_bytes()
    result = invoke(project)
    # Then no source mutation or successful partial import is possible.
    assert result.returncode != 0
    assert qpl_path.read_bytes() == before
    if fault == "exists":
        assert (project / "result.qpl").read_bytes() == b"owned"
    elif fault != "same_input":
        assert not (project / "result.qpl").exists()


def test_append_when_empty_layer_and_no_explicit_ids(project: Path) -> None:
    # Given an empty layer and coincident objects, which may be distinct equipment.
    (project / "source.qpl").write_bytes(b'<QuoterPlanSession><Plans><Plan Name="A" FileName="current.png"><Layers><Layer Index="0"/></Layers></Plan></Plans></QuoterPlanSession>')
    (project / "points.csv").write_text("sheet,label,x_pt,y_pt\nS1,A & B,0,0\nS1,A & B,0,0\n")
    result = invoke(project)
    # Then both occurrences survive and XML escaping roundtrips.
    assert result.returncode == 0, result.stderr
    tree = ET.parse(project / "result.qpl")
    assert len(tree.findall(".//Counter/Element")) == 2
    assert tree.find(".//Counter").get("Name") == "A & B"


def test_append_when_real_compatibility_specimen(tmp_path: Path) -> None:
    # Given a local specimen supplied by the operator, never checked into git.
    source = os.environ.get("PLANEXPERT_SPECIMEN")
    if source is None:
        pytest.skip("Set PLANEXPERT_SPECIMEN for the local real-file integration check")
    original = Path(source)
    shutil.copyfile(original, tmp_path / "source.qpl")
    shutil.copyfile(original.with_name("TEST-GRILLE.png"), tmp_path / "TEST-GRILLE.png")
    (tmp_path / "points.csv").write_text("sheet,label,x_pt,y_pt\nTEST,Import test,800,500\n")
    (tmp_path / "mapping.json").write_text(json.dumps({"sheets": [{
        "sheet": "TEST", "plan_name": "TEST-GRILLE", "layer_index": "0",
        "page_width_pt": 1600, "page_height_pt": 1000,
    }]}))
    before = original.read_bytes()
    result = invoke(tmp_path)
    # Then real legacy Line/Area objects survive byte-for-byte.
    assert result.returncode == 0, result.stderr
    output = (tmp_path / "result.qpl").read_bytes()
    tree = ET.fromstring(output)
    assert len(tree.findall(".//Counter/Element")) == 2
    assert len(tree.findall(".//Line")) == 1 and len(tree.findall(".//Area")) == 1
    assert original.read_bytes() == before


@pytest.mark.parametrize("authorize", [False, True])
def test_create_layer_when_empty_requires_explicit_flag(project: Path, authorize: bool) -> None:
    # Given the actual current-save shape: Layers exists but has no saved Layer.
    source = b'<QuoterPlanSession><Plans><Plan Name="A" FileName="current.png"><Scale Value="0"/><Layers>\n</Layers></Plan></Plans></QuoterPlanSession>'
    (project / "source.qpl").write_bytes(source)
    result = invoke(project, ("--create-missing-layer",) if authorize else ())
    # Then the explicit option controls creation, while original zero scale survives.
    if authorize:
        assert result.returncode == 0, result.stderr
        output = (project / "result.qpl").read_bytes()
        start, end = output.index(b"<Layer "), output.index(b"</Layer>") + len(b"</Layer>")
        assert output[:start] + output[end:] == source
        tree = ET.fromstring(output)
        assert tree.find(".//Layer").attrib == {"Active": "True", "Index": "0", "Name": "Releve autonome", "Opacity": "150", "Visible": "True"}
        assert len(tree.findall(".//Counter/Element")) == 2
    else:
        assert result.returncode != 0
        assert not (project / "result.qpl").exists()


@pytest.mark.parametrize("share", [False, True])
def test_aggregate_group_when_exact_label_across_different_plans(project: Path, share: bool) -> None:
    # Given two native plans, one exact shared label, and a distinct label.
    source = '<QuoterPlanSession><Plans>' + ''.join(
        f'<Plan Name="{name}" FileName="current.png"><Layers><Layer Index="0"/></Layers></Plan>'
        for name in ("A", "B")
    ) + '</Plans></QuoterPlanSession>'
    (project / "source.qpl").write_text(source)
    (project / "points.csv").write_text("sheet,label,x_pt,y_pt\nS1,DR5,25,50\nS2,DR5,20,10\nS2,DR51,25,50\n")
    (project / "mapping.json").write_text(json.dumps({"sheets": [
        {"sheet": sheet, "plan_name": plan, "page_width_pt": 200, "page_height_pt": 100}
        for sheet, plan in (("S1", "A"), ("S2", "B"))
    ]}))
    result = invoke(project, ("--share-groups-by-label",) if share else ())
    # Then native report identity can aggregate DR5 while keeping DR51 separate.
    assert result.returncode == 0, result.stderr
    counters = ET.parse(project / "result.qpl").findall(".//Counter")
    identities = [counter.get("GroupID") for counter in counters]
    assert (identities[0] == identities[1]) is share
    assert identities[2] not in identities[:2]
    assert len({identity for identity in identities}) == (2 if share else 3)


@pytest.mark.parametrize("conflict", ["none", "same_plan", "name", "style"])
def test_accept_shared_source_id_only_when_identity_consistent(project: Path, conflict: str) -> None:
    # Given a shared existing group, optionally conflicting in plan, label or style.
    counter = '<Counter GroupID="7" Name="Saved" Color="-65536"/>'
    second = counter.replace('Name="Saved"', 'Name="Other"') if conflict == "name" else counter
    second = second.replace('Color="-65536"', 'Color="0"') if conflict == "style" else second
    first = counter + second if conflict == "same_plan" else counter
    source = '<QuoterPlanSession><Plans>' + ''.join(
        f'<Plan Name="{name}" FileName="current.png"><Layers><Layer Index="0">{nodes}</Layer></Layers></Plan>'
        for name, nodes in (("A", first), ("B", second))
    ) + '</Plans></QuoterPlanSession>'
    (project / "source.qpl").write_text(source)
    result = invoke(project, ("--share-groups-by-label",))
    # Then only the same style/name identity across distinct plans is accepted.
    assert (result.returncode == 0) is (conflict == "none"), result.stderr

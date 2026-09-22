"""
Import de compteurs dans un .qpl Plan Expert existant — le cœur du socle
(docs/pipeline-qpl.md §1 étape 6 et §4.1).

Porté depuis planexpert-s1857-saint-michel/tools/import/planexpert_counter_import.py
(voir docs/consolidation.md). Seule adaptation : la CLI `typer` est
remplacée par `argparse` (dépendance en moins) ; la logique, les modèles
pydantic et tous les garde-fous sont inchangés :

  python -m src.qpl.import_counters SOURCE.qpl OCCURRENCES.csv MAPPING.json SORTIE.qpl \
      [--create-missing-layer] [--share-groups-by-label]

La sortie doit être un FRÈRE NOUVEAU de la source (les rasters sont
référencés en relatif) ; son audit est SORTIE.qpl.audit.json.
CSV : sheet,label,x_pt,y_pt[,occurrence_id,status] — coordonnées en
points PDF, origine haut-gauche.
Mapping : {"sheets":[{"sheet":"E001","plan_name":"E001","layer_index":"0",
  "page_width_pt":2383.92,"page_height_pt":1683.72}]}
Les dimensions de page viennent du PDF correspondant ; les dimensions du
raster sont lues dans le PNG, jamais supposées.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from dataclasses import dataclass
from pathlib import Path, PureWindowsPath
from typing import Final
from xml.parsers import expat

from PIL import Image
from pydantic import BaseModel, ConfigDict, Field, ValidationError


class FrozenModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True, allow_inf_nan=False)


class Occurrence(FrozenModel):
    sheet: str = Field(min_length=1)
    label: str = Field(min_length=1)
    x_pt: float = Field(ge=0)
    y_pt: float = Field(ge=0)
    occurrence_id: str = ""
    status: str = ""


class Sheet(FrozenModel):
    sheet: str = Field(min_length=1)
    plan_name: str = Field(min_length=1)
    layer_index: str = "0"
    page_width_pt: float = Field(gt=0)
    page_height_pt: float = Field(gt=0)


class Mapping(FrozenModel):
    sheets: tuple[Sheet, ...] = Field(min_length=1)


class PointAudit(Occurrence):
    x_px: int
    y_px: int


@dataclass(frozen=True, slots=True)
class ImportFiles:
    source: Path
    occurrences: Path
    mapping: Path
    output: Path
    create_missing_layer: bool = False
    share_groups_by_label: bool = False


@dataclass(frozen=True, slots=True)
class ImportRejected(Exception):
    reason: str

    def __str__(self) -> str:
        return self.reason


COUNTER_ATTRIBUTES: Final = {
    "Color": "-65536", "DefaultSize": "20", "FillColor": "-65536", "PenType": "Generic",
    "PenWidth": "2", "Shape": "1", "ShowMeasure": "True", "Text": "1", "Visible": "True",
}


def read_occurrences(path: Path) -> tuple[Occurrence, ...]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames is None or len(set(reader.fieldnames)) != len(reader.fieldnames):
            raise ImportRejected("CSV headers are missing or duplicated")
        items = tuple(Occurrence.model_validate(row) for row in reader)
    resolved = tuple(item.model_copy(update={"occurrence_id": item.occurrence_id or f"csv-row-{index}"})
                     for index, item in enumerate(items, start=2))
    if not resolved or len({item.occurrence_id for item in resolved}) != len(resolved):
        raise ImportRejected("CSV must contain occurrences with unique occurrence IDs")
    return resolved


def element_spans(data: bytes, element_path: tuple[str, ...]) -> tuple[tuple[int, int], ...]:
    """Return byte spans so appending counters preserves unrelated original XML exactly."""
    parser = expat.ParserCreate()
    stack: list[str] = []
    starts: list[int] = []
    spans: list[tuple[int, int]] = []

    def start(name: str, _attributes: dict[str, str]) -> None:
        stack.append(name)
        if tuple(stack) == element_path:
            starts.append(parser.CurrentByteIndex)

    def end(_name: str) -> None:
        if tuple(stack) == element_path:
            spans.append((starts.pop(), parser.CurrentByteIndex))
        stack.pop()

    parser.StartElementHandler, parser.EndElementHandler = start, end
    parser.Parse(data, True)
    return tuple(spans)


def raster_path(plan: ET.Element, source: Path) -> Path:
    filename = plan.get("FileName", "")
    if not filename:
        raise ImportRejected("Target plan has no background FileName")
    windows = PureWindowsPath(filename)
    if sys.platform != "win32" and windows.drive:
        if len(windows.drive) != 2:
            raise ImportRejected("UNC background paths require an accessible local QPL copy")
        return Path("/mnt", windows.drive[0].lower(), *windows.parts[1:])
    return source.parent / Path(filename.replace("\\", "/"))


def validate_group_ids(root: ET.Element, shared: bool) -> tuple[int, ...]:
    identities: dict[int, tuple[str, tuple[tuple[str, str], ...]]] = {}
    memberships: set[tuple[int, int]] = set()
    plan_indices = {node: index for index, plan in enumerate(root.findall("./Plans/Plan")) for node in plan.iter()}
    groups: list[int] = []
    for node in (node for node in root.iter() if "GroupID" in node.attrib):
        group = int(node.attrib["GroupID"])
        if node not in plan_indices or group < 0:
            raise ImportRejected("GroupID must be nonnegative and belong to a plan")
        membership = (plan_indices[node], group)
        signature = (node.tag, tuple(sorted((key, value) for key, value in node.attrib.items() if key != "GroupID")))
        if membership in memberships or (not shared and group in identities):
            raise ImportRejected("Duplicate GroupID in its permitted scope")
        if group in identities and identities[group] != signature:
            raise ImportRejected("Shared GroupID conflicts in name, kind or style")
        memberships.add(membership)
        identities[group] = signature
        groups.append(group)
    return tuple(groups)


def import_counters(files: ImportFiles) -> Path:
    source, output = files.source.resolve(), files.output.resolve()
    audit_path = output.with_name(output.name + ".audit.json")
    if source == output or source.parent != output.parent:
        raise ImportRejected("Output must be a different sibling QPL to preserve background references")
    if files.output.exists() or files.output.is_symlink() or audit_path.exists() or audit_path.is_symlink():
        raise ImportRejected("Output or audit already exists; refusing overwrite")
    data = source.read_bytes()
    data.decode("utf-8-sig")
    if b"<!DOCTYPE" in data or b"<!ENTITY" in data:
        raise ImportRejected("DTD/entity declarations are unsupported")
    root = ET.fromstring(data)
    if root.tag != "QuoterPlanSession":
        raise ImportRejected("Expected QuoterPlanSession XML root")
    groups = validate_group_ids(root, files.share_groups_by_label)
    rows = read_occurrences(files.occurrences)
    mapping = Mapping.model_validate_json(files.mapping.read_bytes())
    sheets = {sheet.sheet: sheet for sheet in mapping.sheets}
    if len(sheets) != len(mapping.sheets) or len({(s.plan_name, s.layer_index) for s in mapping.sheets}) != len(sheets):
        raise ImportRejected("Sheet mapping contains duplicate sheet or target layer")
    if {row.sheet for row in rows} - sheets.keys():
        raise ImportRejected("An occurrence has no explicit sheet mapping")
    layers = root.findall("./Plans/Plan/Layers/Layer")
    containers = root.findall("./Plans/Plan/Layers")
    container_path = ("QuoterPlanSession", "Plans", "Plan", "Layers")
    spans = dict(zip(layers, element_spans(data, (*container_path, "Layer")), strict=True))
    spans.update(zip(containers, element_spans(data, container_path), strict=True))
    insertions: list[tuple[int, int, bytes]] = []
    points: list[PointAudit] = []
    counts: dict[str, dict[str, int]] = {}
    dimensions: dict[str, tuple[int, int]] = {}
    created_layers: list[str] = []
    label_ids: dict[str, int] = {}
    new_memberships: set[tuple[str, str]] = set()
    group_id = max(groups, default=0)
    for sheet in mapping.sheets:
        plans = [plan for plan in root.findall("./Plans/Plan") if plan.get("Name") == sheet.plan_name]
        if len(plans) != 1:
            raise ImportRejected(f"Missing or ambiguous plan: {sheet.plan_name}")
        candidates = [layer for layer in plans[0].findall("./Layers/Layer") if layer.get("Index") == sheet.layer_index]
        create_layer = False
        if not candidates and files.create_missing_layer and sheet.layer_index == "0":
            candidates = [container for container in plans[0].findall("./Layers") if len(container) == 0]
            create_layer = True
        if len(candidates) != 1:
            raise ImportRejected(f"Missing or ambiguous layer: {sheet.sheet}")
        with Image.open(raster_path(plans[0], source)) as image:
            width, height = image.size
            image.verify()
        dimensions[sheet.sheet] = width, height
        labels: dict[str, list[PointAudit]] = {}
        for row in (row for row in rows if row.sheet == sheet.sheet):
            if row.x_pt > sheet.page_width_pt or row.y_pt > sheet.page_height_pt:
                raise ImportRejected(f"Occurrence outside PDF page: {row.occurrence_id}")
            point = PointAudit(**row.model_dump(), x_px=round(row.x_pt * width / sheet.page_width_pt),
                               y_px=round(row.y_pt * height / sheet.page_height_pt))
            points.append(point)
            labels.setdefault(row.label, []).append(point)
        fragments: list[bytes] = []
        for label, occurrences in labels.items():
            membership = (sheet.plan_name, label)
            if files.share_groups_by_label and membership in new_memberships:
                raise ImportRejected("Shared label occurs in multiple layers of the same plan")
            new_memberships.add(membership)
            if not files.share_groups_by_label or label not in label_ids:
                group_id += 1
                label_ids[label] = group_id
            counter = ET.Element("Counter", {**COUNTER_ATTRIBUTES, "GroupID": str(label_ids[label]), "Name": label})
            for occurrence in occurrences:
                ET.SubElement(counter, "Element", Height="20", Width="20", X=str(occurrence.x_px), Y=str(occurrence.y_px))
            fragments.append(ET.tostring(counter, encoding="utf-8"))
        counts[sheet.sheet] = dict(Counter(point.label for occurrences in labels.values() for point in occurrences))
        if fragments:
            start, end = spans[candidates[0]]
            tag = candidates[0].tag.encode("ascii")
            opening = re.match(b"<" + tag + rb'\b(?:[^>"\x27]|"[^"]*"|\x27[^\x27]*\x27)*>', data[start:])
            if opening is None:
                raise ImportRejected("Cannot locate target layer opening tag")
            fragment = b"".join(fragments)
            if create_layer:
                fragment = b'<Layer Active="True" Index="0" Name="Releve autonome" Opacity="150" Visible="True">' + fragment + b"</Layer>"
                created_layers.append(sheet.sheet)
            if opening[0].endswith(b"/>"):
                position = start + len(opening[0]) - 2
                insertions.append((position, position + 2, b">" + fragment + b"</" + tag + b">"))
            else:
                insertions.append((end, end, fragment))
    result = data
    for start, end, fragment in sorted(insertions, reverse=True):
        result = result[:start] + fragment + result[end:]
    validate_group_ids(ET.fromstring(result), files.share_groups_by_label)
    audit = {
        "source_sha256": hashlib.sha256(data).hexdigest(), "output_sha256": hashlib.sha256(result).hexdigest(),
        "source": str(source), "output": str(output), "occurrences": len(points),
        "count_by_sheet_label": counts, "unique_occurrence_ids": len({point.occurrence_id for point in points}),
        "new_counter_groups": group_id - max(groups, default=0), "new_group_ids": list(range(max(groups, default=0) + 1, group_id + 1)),
        "new_line_count": 0, "new_area_count": 0, "bounds_valid": True, "original_xml_preserved": True,
        "coordinate_origin": "top-left", "coordinate_units": "PDF points to raster pixels, nearest integer",
        "raster_dimensions": dimensions, "mapping": mapping.model_dump(), "points": [point.model_dump() for point in points],
        "created_layers": created_layers,
        "share_groups_by_label": files.share_groups_by_label, "new_counter_nodes": sum(len(labels) for labels in counts.values()),
    }
    audit_bytes = (json.dumps(audit, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with output.open("xb") as stream, audit_path.open("xb") as audit_stream:
        stream.write(result)
        audit_stream.write(audit_bytes)
    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m src.qpl.import_counters",
        description="Importe des occurrences CSV comme compteurs dans une copie d'un .qpl.",
    )
    parser.add_argument("source", type=Path, help=".qpl source (non modifié)")
    parser.add_argument("occurrences", type=Path, help="CSV : sheet,label,x_pt,y_pt[,occurrence_id,status]")
    parser.add_argument("mapping", type=Path, help="JSON de correspondance feuilles/plans/dimensions")
    parser.add_argument("sortie", type=Path, help="nouveau .qpl frère de la source")
    parser.add_argument("--create-missing-layer", action="store_true",
                        help="Créer le calque 0 audité, seulement dans un Layers vide")
    parser.add_argument("--share-groups-by-label", action="store_true",
                        help="Partager le GroupID d'un libellé identique entre plans différents")
    args = parser.parse_args(argv)
    try:
        output = import_counters(
            ImportFiles(args.source, args.occurrences, args.mapping, args.sortie,
                        args.create_missing_layer, args.share_groups_by_label)
        )
    except (ImportRejected, OSError, ValueError, ValidationError, ET.ParseError, expat.ExpatError) as error:
        print(f"Import refusé : {error}", file=sys.stderr)
        return 2
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

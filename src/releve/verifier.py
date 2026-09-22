"""
Sous-commande `verifier` — relit un .qpl Plan Expert et sort le décompte
(compteurs, éléments, lignes, GroupID) + le hachage SHA-256, tel que défini
dans docs/pipeline-qpl.md §5.2 (« on peut remonter la chaîne d'un
livrable »).

Avec `--export-plans` / `--export-counters`, écrit aussi les deux JSON du
même schéma que `qpl_build.py` attend en entrée : ça permet l'aller-retour
qpl -> verifier -> qpl exigé par la consigne (comparer la sortie regénérée
à l'original).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _parse(path: Path) -> ET.Element:
    # Les .qpl Plan Expert sont en UTF-8 avec BOM (PIPELINE §2.1) ;
    # utf-8-sig l'enlève proprement avant de passer le texte à ElementTree.
    text = Path(path).read_text(encoding="utf-8-sig")
    return ET.fromstring(text)


def _to_bool(value: str | None) -> bool | None:
    if value is None:
        return None
    return value == "True"


def _to_int(value: str | None):
    return int(value) if value is not None else None


# --------------------------------------------------------------------- #
# Décompte (ce que la consigne demande au minimum)
# --------------------------------------------------------------------- #

def compute_counts(root: ET.Element) -> dict:
    plans_el = root.find("Plans")
    plans = plans_el.findall("Plan") if plans_el is not None else []

    n_counters = 0
    n_counter_elements = 0
    n_lines = 0
    n_line_segments = 0
    counter_group_ids: set[int] = set()
    line_group_ids: set[int] = set()
    shapes: dict[int, int] = {}

    for plan in plans:
        for layer in plan.findall("./Layers/Layer"):
            for counter in layer.findall("Counter"):
                n_counters += 1
                counter_group_ids.add(int(counter.attrib["GroupID"]))
                shape = int(counter.attrib.get("Shape", -1))
                shapes[shape] = shapes.get(shape, 0) + 1
                n_counter_elements += len(counter.findall("Element"))
            for line in layer.findall("Line"):
                n_lines += 1
                line_group_ids.add(int(line.attrib["GroupID"]))
                n_line_segments += len(line.findall("Element"))

    overlap = counter_group_ids & line_group_ids
    return {
        "n_plans": len(plans),
        "n_counters": n_counters,
        "n_counter_elements": n_counter_elements,
        "n_lines": n_lines,
        "n_line_segments": n_line_segments,
        "n_distinct_group_ids_counters": len(counter_group_ids),
        "n_distinct_group_ids_lines": len(line_group_ids),
        "n_distinct_group_ids_total": len(counter_group_ids | line_group_ids),
        "group_ids_partages_compteur_et_ligne": sorted(overlap),
        "compteurs_par_forme": shapes,
    }


# --------------------------------------------------------------------- #
# Export du modèle complet — même schéma que qpl_build.py, pour l'essai
# d'aller-retour (verifier --export-* puis `qpl` puis verifier à nouveau)
# --------------------------------------------------------------------- #

def export_model(root: ET.Element) -> tuple[dict, dict]:
    project_el = root.find("Project")
    project = {}
    if project_el is not None:
        project = {
            "name": project_el.attrib.get("Name", ""),
            "description": (project_el.findtext("Description") or ""),
            "contact_name": (project_el.findtext("ContactName") or ""),
            "contact_info": (project_el.findtext("ContactInfo") or ""),
            "job_number": (project_el.findtext("JobNumber") or ""),
            "comment": (project_el.findtext("Comment") or ""),
            "creation_date": (project_el.findtext("CreationDate") or ""),
            "last_modified": (project_el.findtext("LastModified") or ""),
            "display_results_for_all_plans": _to_bool(
                project_el.findtext("DisplayResultsForAllPlans")
            ),
        }

    workspace_el = root.find("Workspace")
    active_plan = None
    recent_plans: list[str] = []
    if workspace_el is not None:
        active_el = workspace_el.find("ActivePlan")
        if active_el is not None:
            active_plan = active_el.attrib.get("Name")
        recent_plans = [
            p.attrib["Name"] for p in workspace_el.findall("./RecentPlans/Plan")
        ]

    plans_out: list[dict] = []
    counters_by_gid: dict[int, dict] = {}
    lines_by_gid: dict[int, dict] = {}

    for plan in root.findall("./Plans/Plan"):
        sheet = plan.attrib["Name"]
        scale_el = plan.find("Scale")
        scale = None
        if scale_el is not None:
            scale = {
                "value": _to_int(scale_el.attrib.get("Value")),
                "type": _to_int(scale_el.attrib.get("Type")),
                "precision": _to_int(scale_el.attrib.get("Precision")),
                "set_manually": _to_bool(scale_el.attrib.get("SetManually")),
                "engineering": _to_bool(scale_el.attrib.get("Engineering")),
            }
        bookmark_el = plan.find("./Bookmarks/Bookmark")
        bookmark = None
        if bookmark_el is not None:
            bookmark = {
                "zoom": _to_int(bookmark_el.attrib.get("Zoom")),
                "x": _to_int(bookmark_el.attrib.get("X")),
                "y": _to_int(bookmark_el.attrib.get("Y")),
            }
        layer_el = plan.find("./Layers/Layer")
        legend = None
        layer_name = None
        opacity = None
        if layer_el is not None:
            layer_name = layer_el.attrib.get("Name")
            opacity = _to_int(layer_el.attrib.get("Opacity"))
            legend_el = layer_el.find("Legend")
            if legend_el is not None:
                legend = {
                    "x": _to_int(legend_el.attrib.get("X")),
                    "y": _to_int(legend_el.attrib.get("Y")),
                    "font_size": _to_int(legend_el.attrib.get("FontSize")),
                    "max_rows": _to_int(legend_el.attrib.get("MaxRows")),
                }

        thumb_el = plan.find("Thumbnail")
        thumbnail = thumb_el.attrib.get("FileName") if thumb_el is not None else None

        plans_out.append(
            {
                "sheet": sheet,
                "file_name": plan.attrib.get("FileName", ""),
                "thumbnail": thumbnail,
                "scale": scale,
                "bookmark": bookmark,
                "layer_name": layer_name,
                "opacity": opacity,
                "legend": legend,
            }
        )

        if layer_el is None:
            continue
        for counter in layer_el.findall("Counter"):
            gid = int(counter.attrib["GroupID"])
            entry = counters_by_gid.setdefault(
                gid,
                {
                    "group_id": gid,
                    "name": counter.attrib.get("Name", ""),
                    "shape": _to_int(counter.attrib.get("Shape")),
                    "default_size": _to_int(counter.attrib.get("DefaultSize")),
                    "color": _to_int(counter.attrib.get("Color")),
                    "fill_color": _to_int(counter.attrib.get("FillColor")),
                    "pen_width": _to_int(counter.attrib.get("PenWidth")),
                    "pen_type": counter.attrib.get("PenType", "Generic"),
                    "text": counter.attrib.get("Text", "1"),
                    "show_measure": _to_bool(counter.attrib.get("ShowMeasure")),
                    "visible": _to_bool(counter.attrib.get("Visible")),
                    "elements": [],
                },
            )
            for el in counter.findall("Element"):
                entry["elements"].append(
                    {
                        "sheet": sheet,
                        "x": _to_int(el.attrib.get("X")),
                        "y": _to_int(el.attrib.get("Y")),
                        "width": _to_int(el.attrib.get("Width")),
                        "height": _to_int(el.attrib.get("Height")),
                    }
                )
        for line in layer_el.findall("Line"):
            gid = int(line.attrib["GroupID"])
            entry = lines_by_gid.setdefault(
                gid,
                {
                    "group_id": gid,
                    "name": line.attrib.get("Name", ""),
                    "color": _to_int(line.attrib.get("Color")),
                    "pen_width": _to_int(line.attrib.get("PenWidth")),
                    "pen_type": line.attrib.get("PenType", "Generic"),
                    "show_measure": _to_bool(line.attrib.get("ShowMeasure")),
                    "visible": _to_bool(line.attrib.get("Visible")),
                    "segments": [],
                },
            )
            for el in line.findall("Element"):
                entry["segments"].append(
                    {
                        "sheet": sheet,
                        "x1": _to_int(el.attrib.get("X1")),
                        "y1": _to_int(el.attrib.get("Y1")),
                        "x2": _to_int(el.attrib.get("X2")),
                        "y2": _to_int(el.attrib.get("Y2")),
                    }
                )

    plans_model = {
        "project": project,
        "active_plan": active_plan,
        "recent_plans": recent_plans,
        "plans": plans_out,
    }
    counters_model = {
        "counters": [counters_by_gid[g] for g in sorted(counters_by_gid)],
        "lines": [lines_by_gid[g] for g in sorted(lines_by_gid)],
    }
    return plans_model, counters_model


# --------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------- #

def add_arguments(sub: argparse.ArgumentParser) -> None:
    sub.add_argument("qpl", type=Path, help="Fichier .qpl à relire")
    sub.add_argument("--json", type=Path, help="Écrire le décompte JSON ici (sinon stdout)")
    sub.add_argument("--export-plans", type=Path, help="Écrire le JSON de plans extrait")
    sub.add_argument("--export-counters", type=Path, help="Écrire le JSON de compteurs extrait")


def run(args: argparse.Namespace) -> int:
    root = _parse(args.qpl)
    counts = compute_counts(root)
    counts["fichier"] = str(args.qpl)
    counts["taille_octets"] = Path(args.qpl).stat().st_size
    counts["sha256"] = _sha256(args.qpl)

    payload = json.dumps(counts, ensure_ascii=False, indent=2)
    if args.json:
        Path(args.json).write_text(payload, encoding="utf-8")
        print(f"Décompte écrit dans {args.json}")
    else:
        print(payload)

    if args.export_plans or args.export_counters:
        plans_model, counters_model = export_model(root)
        if args.export_plans:
            Path(args.export_plans).write_text(
                json.dumps(plans_model, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            print(f"Plans exportés dans {args.export_plans}")
        if args.export_counters:
            Path(args.export_counters).write_text(
                json.dumps(counters_model, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            print(f"Compteurs exportés dans {args.export_counters}")
    return 0

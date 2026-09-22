"""
Sous-commande `qpl` — construit un .qpl Plan Expert valide à partir de deux
fichiers JSON : un JSON de compteurs (familles + marques) et un JSON de
plans (feuilles + échelle + légende). Voir docs/pipeline-qpl.md §2 pour le
schéma XML et §7 pour la liste des paramètres à isoler par soumission.

Schéma du JSON de PLANS (plans.json) :
{
  "project": {                       # tous les champs sont optionnels
    "name": "maison st-michel test",
    "description": "", "contact_name": "", "contact_info": "",
    "job_number": "", "comment": "",
    "creation_date": "2026/9/8", "last_modified": "2026/9/8",
    "display_results_for_all_plans": true
  },
  "active_plan": "E406_Rev0",        # optionnel, sinon 1re feuille listée
  "recent_plans": ["E409_Rev0", ...],# optionnel, sinon les 10 dernières
  "plans": [
    {
      "sheet": "E409_Rev0",          # identifiant = <Plan Name="...">
      "file_name": "E409_Rev0.png",  # PNG relatif, à côté du .qpl (§3.4)
      "thumbnail": "<guid>",         # optionnel, sinon généré
      "raster_width_px": 5694,       # optionnel, sert de garde-fou
      "raster_height_px": 4022,      # optionnel, sert de garde-fou
      "scale": {"value": 100, "type": 0, "precision": 2,
                "set_manually": false, "engineering": false},
      "bookmark": {"zoom": 10, "x": 0, "y": 0},
      "layer_name": "Releve autonome", "opacity": 150,
      "legend": {"x": 4250, "y": 1350, "font_size": 45, "max_rows": 25}
    }
  ]
}
Feuille non calibrée (§2.3) : omettre "scale" -> Value=0 Type=1 Precision=0.

Schéma du JSON de COMPTEURS (counters.json) :
{
  "counters": [
    {
      "group_id": 1, "name": "Panneau principal P-P1 600A",
      "shape": 1, "default_size": 20,
      "color": -65536, "fill_color": -65536,   # Color == FillColor (§2.5)
      "pen_width": 2, "pen_type": "Generic", "text": "1",
      "show_measure": true, "visible": true,
      "elements": [{"sheet": "E200_Rev0", "x": 2389, "y": 1805,
                    "width": 20, "height": 20}]
    }
  ],
  "lines": [
    {
      "group_id": 123, "name": "CTRL-ECHELLE-BA-E400",
      "color": -16776961, "pen_width": 6, "pen_type": "Generic",
      "show_measure": true, "visible": true,
      "segments": [{"sheet": "E400_Rev0", "x1": 501, "y1": 3048,
                    "x2": 501, "y2": 3485}]
    }
  ]
}
GroupID des compteurs et des lignes : **même espace de numérotation**
(§2.6) — un GroupID ne doit apparaître qu'une seule fois, compteur ou ligne.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import qplschema as sch


class QplBuildError(ValueError):
    """Erreur de données refusée avant toute écriture (garde-fous §2.6)."""


# --------------------------------------------------------------------- #
# Chargement + validation des deux JSON d'entrée
# --------------------------------------------------------------------- #

def load_counters(path: Path) -> tuple[list[dict], list[dict]]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    counters = data.get("counters", [])
    lines = data.get("lines", [])

    seen_ids: dict[int, tuple[str, str]] = {}
    for kind, items in (("Counter", counters), ("Line", lines)):
        for item in items:
            gid = int(item["group_id"])
            if gid < 0:
                raise QplBuildError(f"GroupID négatif refusé : {item!r}")
            if gid in seen_ids:
                autre_kind, autre_nom = seen_ids[gid]
                raise QplBuildError(
                    f"GroupID {gid} dupliqué : « {autre_nom} » ({autre_kind}) "
                    f"et « {item['name']} » ({kind}) partagent le même "
                    "espace de numérotation (PIPELINE §2.6)"
                )
            seen_ids[gid] = (kind, item["name"])
    return counters, lines


def load_plans(path: Path) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    plans = data.get("plans", [])
    if not plans:
        raise QplBuildError("plans.json ne contient aucune feuille")

    seen_sheets: set[str] = set()
    for plan in plans:
        sheet = plan["sheet"]
        if sheet in seen_sheets:
            raise QplBuildError(f"Feuille dupliquée dans plans.json : {sheet}")
        seen_sheets.add(sheet)
    data["plans"] = plans
    data.setdefault("project", {})
    return data


def _check_sheet_known(sheet: str, known: set[str], where: str) -> None:
    if sheet not in known:
        raise QplBuildError(
            f"{where} référence la feuille « {sheet} », absente de "
            "plans.json (garde-fou équivalent à import_counters.py)"
        )


def _check_in_page(sheet: str, x: float, y: float, plan_by_sheet: dict) -> None:
    plan = plan_by_sheet[sheet]
    w = plan.get("raster_width_px")
    h = plan.get("raster_height_px")
    if w is not None and not (0 <= x <= w):
        raise QplBuildError(f"{sheet} : X={x} hors du raster (largeur {w} px)")
    if h is not None and not (0 <= y <= h):
        raise QplBuildError(f"{sheet} : Y={y} hors du raster (hauteur {h} px)")


# --------------------------------------------------------------------- #
# Construction du XML — sérialisation manuelle pour coller exactement au
# format observé (BOM, pas de déclaration d'encodage, tabulations, CRLF,
# balises vides non-autofermantes pour Comment/Description, cf. §2.1-2.9).
# --------------------------------------------------------------------- #

def _project_block(project: dict) -> str:
    name = sch.esc(project.get("name", ""))
    fields = [
        ("Description", project.get("description", "")),
        ("ContactName", project.get("contact_name", "")),
        ("ContactInfo", project.get("contact_info", "")),
        ("JobNumber", project.get("job_number", "")),
        ("Comment", project.get("comment", "")),
    ]
    lines = [f'\t<Project Name="{name}">']
    for tag, value in fields:
        lines.append(f"\t\t<{tag}>{sch.esc(value)}</{tag}>")
    creation = project.get("creation_date", "")
    modified = project.get("last_modified", creation)
    lines.append(f"\t\t<CreationDate>{sch.esc(creation)}</CreationDate>")
    lines.append(f"\t\t<LastModified>{sch.esc(modified)}</LastModified>")
    show_all = sch.bool_str(project.get("display_results_for_all_plans", True))
    lines.append(f"\t\t<DisplayResultsForAllPlans>{show_all}</DisplayResultsForAllPlans>")
    lines.append("\t</Project>")
    return sch.CRLF.join(lines)


def _workspace_block(active_plan: str, recent_plans: list[str]) -> str:
    lines = ["\t<Workspace>", f'\t\t<ActivePlan Name="{sch.esc(active_plan)}"/>']
    if recent_plans:
        lines.append("\t\t<RecentPlans>")
        for name in recent_plans[:10]:
            lines.append(f'\t\t\t<Plan Name="{sch.esc(name)}"/>')
        lines.append("\t\t</RecentPlans>")
    lines.append("\t</Workspace>")
    return sch.CRLF.join(lines)


def _legend_line(legend: dict | None) -> str:
    leg = legend or {}
    x = leg.get("x", 0)
    y = leg.get("y", 0)
    font_size = leg.get("font_size", sch.LEGEND_FONT_SIZE)
    max_rows = leg.get("max_rows", sch.LEGEND_MAX_ROWS)
    return (
        f'\t\t\t\t\t<Legend Name="Légende" X="{x}" Y="{y}" '
        f'FontSize="{font_size}" MaxRows="{max_rows}" '
        f'Color="{sch.LEGEND_FILL_COLOR}" PenWidth="{sch.LEGEND_PEN_WIDTH}" '
        f'PenType="Generic" FillColor="{sch.LEGEND_FILL_COLOR}" '
        f'ShowMeasure="True" Visible="True"/>'
    )


def _counter_block(counter: dict, elements_on_sheet: list[dict]) -> str:
    attrs = (
        f'Name="{sch.esc(counter["name"])}" GroupID="{int(counter["group_id"])}" '
        f'Shape="{int(counter.get("shape", 1))}" '
        f'DefaultSize="{int(counter.get("default_size", 20))}" '
        f'Text="{sch.esc(counter.get("text", "1"))}" '
        f'Color="{int(counter["color"])}" '
        f'PenWidth="{int(counter.get("pen_width", 2))}" '
        f'PenType="{sch.esc(counter.get("pen_type", "Generic"))}" '
        f'FillColor="{int(counter.get("fill_color", counter["color"]))}" '
        f'ShowMeasure="{sch.bool_str(counter.get("show_measure", True))}" '
        f'Visible="{sch.bool_str(counter.get("visible", True))}"'
    )
    lines = [f"\t\t\t\t\t<Counter {attrs}>"]
    for el in elements_on_sheet:
        lines.append(
            f'\t\t\t\t\t\t<Element X="{int(el["x"])}" Y="{int(el["y"])}" '
            f'Width="{int(el.get("width", counter.get("default_size", 20)))}" '
            f'Height="{int(el.get("height", counter.get("default_size", 20)))}"/>'
        )
    lines.append("\t\t\t\t\t</Counter>")
    return sch.CRLF.join(lines)


def _line_block(line: dict, segments_on_sheet: list[dict]) -> str:
    attrs = (
        f'Name="{sch.esc(line["name"])}" GroupID="{int(line["group_id"])}" '
        f'Color="{int(line["color"])}" '
        f'PenWidth="{int(line.get("pen_width", 6))}" '
        f'PenType="{sch.esc(line.get("pen_type", "Generic"))}" '
        f'ShowMeasure="{sch.bool_str(line.get("show_measure", True))}" '
        f'Visible="{sch.bool_str(line.get("visible", True))}"'
    )
    lines = [f"\t\t\t\t\t<Line {attrs}>"]
    for seg in segments_on_sheet:
        lines.append(
            f'\t\t\t\t\t\t<Element X1="{int(seg["x1"])}" Y1="{int(seg["y1"])}" '
            f'X2="{int(seg["x2"])}" Y2="{int(seg["y2"])}"/>'
        )
    lines.append("\t\t\t\t\t</Line>")
    return sch.CRLF.join(lines)


def _plan_block(plan: dict, counters: list[dict], lines_: list[dict]) -> str:
    sheet = plan["sheet"]
    file_name = plan.get("file_name", f"{sheet}.png")
    thumb = plan.get("thumbnail") or sch.new_thumbnail()
    scale = plan.get("scale")
    if scale:
        scale_attrs = (
            f'Value="{scale.get("value", 0)}" Type="{scale.get("type", 0)}" '
            f'Precision="{scale.get("precision", 0)}" '
            f'SetManually="{sch.bool_str(scale.get("set_manually", False))}" '
            f'Engineering="{sch.bool_str(scale.get("engineering", False))}"'
        )
    else:
        scale_attrs = 'Value="0" Type="1" Precision="0" SetManually="False" Engineering="False"'
    bookmark = plan.get("bookmark", {})
    zoom = bookmark.get("zoom", -1)
    bx = bookmark.get("x", 0)
    by = bookmark.get("y", 0)
    layer_name = plan.get("layer_name", "Calque par défaut")
    opacity = plan.get("opacity", 150)

    out = [
        f'\t\t<Plan Name="{sch.esc(sheet)}" FileName="{sch.esc(file_name)}">',
        f'\t\t\t<Thumbnail FileName="{thumb}"/>',
        f"\t\t\t<Scale {scale_attrs}/>",
        "\t\t\t<Bookmarks>",
        f'\t\t\t\t<Bookmark Name="Default" LayerIndex="0" Zoom="{zoom}" X="{bx}" Y="{by}"/>',
        "\t\t\t</Bookmarks>",
        f'\t\t\t<Comment>{sch.esc(plan.get("comment", ""))}</Comment>',
        "\t\t\t<Layers>",
        f'\t\t\t\t<Layer Index="0" Name="{sch.esc(layer_name)}" Opacity="{opacity}" '
        'Visible="True" Active="True">',
        _legend_line(plan.get("legend")),
    ]
    for counter in counters:
        elements_on_sheet = [e for e in counter["elements"] if e["sheet"] == sheet]
        if elements_on_sheet:
            out.append(_counter_block(counter, elements_on_sheet))
    for line in lines_:
        segments_on_sheet = [s for s in line["segments"] if s["sheet"] == sheet]
        if segments_on_sheet:
            out.append(_line_block(line, segments_on_sheet))
    out.append("\t\t\t\t</Layer>")
    out.append("\t\t\t</Layers>")
    out.append("\t\t</Plan>")
    return sch.CRLF.join(out)


def _prices_block(counters: list[dict], lines_: list[dict]) -> str:
    out = ["\t<Prices>"]
    for counter in counters:
        gid = int(counter["group_id"])
        out.append(f'\t\t<Price Key="{gid};;Counter;" CostEach="0" MarkupEach="0" SystemType="2"/>')
    for line in lines_:
        gid = int(line["group_id"])
        out.append(f'\t\t<Price Key="{gid};;Line;" CostEach="0" MarkupEach="0" SystemType="2"/>')
    out.append("\t</Prices>")
    return sch.CRLF.join(out)


def _reports_block() -> str:
    out = ['\t<Reports>', '\t\t<Report Name="Default" Order="1" ScaleType="1" Precision="0">']
    for name, value in sch.REPORT_PROPERTIES:
        out.append(f'\t\t\t<Property Name="{name}" Value="{sch.esc(value)}"/>')
    out.append("\t\t</Report>")
    out.append("\t</Reports>")
    return sch.CRLF.join(out)


def build_qpl_text(plans_model: dict, counters: list[dict], lines_: list[dict]) -> str:
    """Assemble le XML complet (str, avec CRLF) — sans BOM ni prologue,
    ajoutés seulement à l'écriture (`write_qpl`)."""
    plans = plans_model["plans"]
    sheets = {p["sheet"] for p in plans}
    plan_by_sheet = {p["sheet"]: p for p in plans}

    for counter in counters:
        for el in counter.get("elements", []):
            _check_sheet_known(el["sheet"], sheets, f'Compteur « {counter["name"]} »')
            _check_in_page(el["sheet"], el["x"], el["y"], plan_by_sheet)
    for line in lines_:
        for seg in line.get("segments", []):
            _check_sheet_known(seg["sheet"], sheets, f'Ligne « {line["name"]} »')

    active_plan = plans_model.get("active_plan") or plans[0]["sheet"]
    recent_plans = plans_model.get("recent_plans")
    if not recent_plans:
        recent_plans = list(reversed([p["sheet"] for p in plans]))[:10]

    body = [
        sch.XML_DECL,
        "<QuoterPlanSession>",
        _project_block(plans_model.get("project", {})),
        _workspace_block(active_plan, recent_plans),
        "\t<Plans>",
    ]
    for plan in plans:
        body.append(_plan_block(plan, counters, lines_))
    body.append("\t</Plans>")
    body.append(_prices_block(counters, lines_))
    body.append(_reports_block())
    body.append("</QuoterPlanSession>")
    body.append("")  # ligne finale, comme dans les fichiers réels
    return sch.CRLF.join(body)


def write_qpl(path: Path, xml_text: str, *, force: bool = False) -> None:
    path = Path(path)
    if path.exists() and not force:
        raise QplBuildError(
            f"{path} existe déjà (refus, comme import_counters.py "
            "qui écrit en mode 'xb' — utiliser --force pour écraser explicitement)"
        )
    # BOM UTF-8 + pas de déclaration d'encodage dans le prologue (§2.1) :
    # on encode nous-mêmes en utf-8-sig plutôt que de laisser un writer XML
    # générique choisir l'encodage.
    path.write_bytes(("﻿" + xml_text).encode("utf-8"))


# --------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------- #

def add_arguments(sub: argparse.ArgumentParser) -> None:
    sub.add_argument("plans_json", type=Path, help="JSON de plans (feuilles, échelle, légende)")
    sub.add_argument("counters_json", type=Path, help="JSON de compteurs (familles + marques)")
    sub.add_argument("sortie", type=Path, help="Chemin du .qpl à écrire")
    sub.add_argument("--force", action="store_true", help="Écraser la sortie si elle existe déjà")


def run(args: argparse.Namespace) -> int:
    plans_model = load_plans(args.plans_json)
    counters, lines_ = load_counters(args.counters_json)
    xml_text = build_qpl_text(plans_model, counters, lines_)
    write_qpl(args.sortie, xml_text, force=args.force)
    n_elements = sum(len(c.get("elements", [])) for c in counters)
    n_segments = sum(len(l.get("segments", [])) for l in lines_)
    print(
        f"OK : {args.sortie} — {len(counters)} compteurs / {n_elements} éléments, "
        f"{len(lines_)} lignes / {n_segments} segments, {len(plans_model['plans'])} plans"
    )
    return 0

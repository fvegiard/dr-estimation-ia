"""Write an estimate (Store.estimate output) to an Excel quote with a review flag per line."""
from __future__ import annotations

from datetime import date
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

OUT = Path(__file__).resolve().parents[1] / "eewin" / "catalogue-llm" / "out"
FLAG = PatternFill("solid", fgColor="FFF2CC")
HEAD = PatternFill("solid", fgColor="DDEBF7")


def _text(row) -> None:
    """User text starting with '=' stays text: openpyxl would otherwise store it as a formula."""
    for c in row:
        if c.data_type == "f":
            c.data_type = "s"


def write_quote(est: dict, title: str, path: Path | str | None = None) -> Path:
    if not path:
        OUT.mkdir(exist_ok=True)
    safe = "".join(c if c.isalnum() or c in " -_" else "_" for c in title).strip() or "estimate"
    path = Path(path) if path else OUT / f"{date.today():%Y-%m-%d} {safe}.xlsx"
    wb = Workbook()
    ws = wb.active
    assert ws is not None
    ws.title = "Estimation"
    t = est["totals"]
    ws.append([title]); ws["A1"].font = Font(bold=True, size=14); _text(ws[1])
    ws.append([f"Prix au {est.get('prices_as_of', '')} - taux main-d'oeuvre {t['labor_rate']:.2f} $/h - "
               f"généré le {date.today():%Y-%m-%d} - À RÉVISER avant envoi"])
    ws.append([])
    cols = ["#", "Code", "Description", "Type", "Qté", "Unité", "Sections", "Matériel $", "Heures",
            "Main-d'oeuvre $", "Total $", "À vérifier", "Note"]
    ws.append(cols)
    for c in ws[4]:
        c.font = Font(bold=True); c.fill = HEAD
    for ln in est["lines"]:
        ws.append([ln["line"], ln["code"], ln["description"], ln["kind"], ln["qty"], ln["unit"], ln["sections"] or None,
                   ln["material"], ln["hours"], ln["labor_cost"], ln["total"], "; ".join(ln["warnings"]), ln["note"]])
        _text(ws[ws.max_row])
        if ln["warnings"]:
            for c in ws[ws.max_row]:
                c.fill = FLAG
    first, last = 5, ws.max_row
    ws.append([])
    r0 = ws.max_row + 1  # totals: label in C, value in K
    totals = [
        ("Total matériel", f"=SUM(H{first}:H{last})"),
        ("Total heures", f"=SUM(I{first}:I{last})"),
        ("Taux horaire $/h", t["labor_rate"]),
        ("Total main-d'oeuvre", f"=K{r0 + 1}*K{r0 + 2}"),
        ("Coût total", f"=K{r0}+K{r0 + 3}"),
        ("Majoration matériel %", t["material_markup_pct"]),
        ("Majoration main-d'oeuvre %", t["labor_markup_pct"]),
        ("Prix de vente", f"=K{r0}*(1+K{r0 + 5}/100)+K{r0 + 3}*(1+K{r0 + 6}/100)"),
    ]
    for i, (label, val) in enumerate(totals):
        ws.cell(r0 + i, 3, label).font = Font(bold=True)
        c = ws.cell(r0 + i, 11, val)
        c.number_format = "0.00" if i in (1, 5, 6) else '#,##0.00 "$"'
        c.font = Font(bold=i in (4, 7))
    for col, w in zip("ABCDEFGHIJKLM", [4, 22, 48, 9, 8, 6, 8, 12, 8, 14, 12, 40, 30]):
        ws.column_dimensions[col].width = w
    for row in ws.iter_rows(min_row=first, max_row=last):
        for i in (7, 9, 10):
            row[i].number_format = '#,##0.00 "$"'
        row[8].number_format = "0.00"
    ws.freeze_panes = "A5"

    det = wb.create_sheet("Détail assemblages")
    det.append(["Ligne", "Assemblage", "Composant", "Description", "Qté", "Unité", "Matériel $", "Heures", "À vérifier"])
    for c in det[1]:
        c.font = Font(bold=True); c.fill = HEAD
    for ln in est["lines"]:
        for comp in ln["components"]:
            det.append([ln["line"], ln["code"], comp["code"], comp["description"], comp["qty"], comp["unit"],
                        comp["material"], comp["hours"], "; ".join(comp["warnings"])])
            _text(det[det.max_row])
    for i, w in enumerate([6, 22, 12, 48, 10, 6, 12, 8, 30], 1):
        det.column_dimensions[get_column_letter(i)].width = w

    warn = wb.create_sheet("Avertissements")
    warn.append(["Avertissement"]); warn["A1"].font = Font(bold=True)
    for w in est["warnings"] or ["Aucun"]:
        warn.append([w]); _text(warn[warn.max_row])
    warn.column_dimensions["A"].width = 100
    wb.save(path)
    return path

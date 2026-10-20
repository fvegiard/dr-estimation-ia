#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Classeur de chiffrage (méthode Dupuis) — mise en page imprimable DR, formules Excel. Générique : lit chiffrage.json + soumission.json."""
import json, os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.page import PageMargins
from openpyxl.drawing.image import Image as XLImage
LOGO=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logo_dr.png')
fillZ = PatternFill('solid', fgColor='FAFAFA')

import sys, os
if len(sys.argv) != 4:
    sys.exit('Usage: python build_xlsx.py <chiffrage.json> <soumission.json> <sortie.xlsx>')
C = json.load(open(sys.argv[1], encoding='utf-8'))
V = json.load(open(sys.argv[2], encoding='utf-8'))['ventilation']
OUT = sys.argv[3]

BORD = '6B1A1A'; ROSE = 'F5E6E6'; GRIS = 'F2F2F2'; JAUNE = 'FFF2CC'
F = 'Arial'
fTitle = Font(name=F, bold=True, size=14, color=BORD)
fSub = Font(name=F, size=9, italic=True, color='555555')
fHdr = Font(name=F, bold=True, size=9, color='FFFFFF')
fSec = Font(name=F, bold=True, size=10, color=BORD)
fB = Font(name=F, bold=True, size=9)
fN = Font(name=F, size=9)
fBlue = Font(name=F, size=9, color='0000FF')
fTot = Font(name=F, bold=True, size=11, color=BORD)
fillH = PatternFill('solid', fgColor=BORD)
fillSec = PatternFill('solid', fgColor=ROSE)
fillG = PatternFill('solid', fgColor=GRIS)
fillY = PatternFill('solid', fgColor=JAUNE)
thin = Side(style='thin', color='BFBFBF'); med = Side(style='medium', color=BORD)
box = Border(top=thin, bottom=thin, left=thin, right=thin)
wrap = Alignment(wrap_text=True, vertical='center')
center = Alignment(horizontal='center', vertical='center', wrap_text=True)
right = Alignment(horizontal='right', vertical='center')
CUR = '#,##0.00 $;-#,##0.00 $;"-"'
CUR0 = '#,##0 $;-#,##0 $;"-"'
HRS = '#,##0.00;-#,##0.00;"-"'

def setup_print(ws, landscape, title_rows, widths):
    ws.page_setup.orientation = 'landscape' if landscape else 'portrait'
    ws.page_setup.paperSize = ws.PAPERSIZE_LETTER
    ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_title_rows = title_rows
    ws.page_margins = PageMargins(left=0.4, right=0.4, top=0.6, bottom=0.6, header=0.3, footer=0.3)
    ws.oddHeader.left.text = '&"Arial,Bold"&9Le Groupe DR Électrique inc. — S-1902 Bibliothèque Georgette-Lepage'
    ws.oddHeader.right.text = '&9Chiffrage méthode Dupuis — 2026-10-20'
    ws.oddFooter.left.text = '&8DR Électrique inc. | Merci de votre confiance'
    ws.oddFooter.right.text = '&8Page &P de &N'
    ws.sheet_view.showGridLines = False
    for i, w in enumerate(widths, 1): ws.column_dimensions[get_column_letter(i)].width = w

def banner(ws, title, subtitle, ncols):
    """Bandeau titre : logo DR (A1:A2), titre bordeaux sur fond rose, sous-titre."""
    img = XLImage(LOGO); img.height = 52; img.width = int(52 * 398 / 420); ws.add_image(img, 'A1')
    ws.row_dimensions[1].height = 24; ws.row_dimensions[2].height = 18
    for r in (1, 2):
        for j in range(1, ncols + 1): ws.cell(r, j).fill = fillSec
    c = ws.cell(1, 2, title); c.font = Font(name=F, bold=True, size=14, color=BORD); c.alignment = Alignment(vertical='center')
    c = ws.cell(2, 2, subtitle); c.font = Font(name=F, size=9, italic=True, color='555555'); c.alignment = Alignment(vertical='center')
    ws.merge_cells(start_row=1, start_column=2, end_row=1, end_column=ncols); ws.merge_cells(start_row=2, start_column=2, end_row=2, end_column=ncols)
    for j in range(1, ncols + 1): ws.cell(3, j).border = Border(bottom=Side(style='medium', color=BORD))

def header_row(ws, r, labels, cols=None):
    for j, lab in enumerate(labels, 1):
        c = ws.cell(r, j, lab); c.font = fHdr; c.fill = fillH; c.alignment = center; c.border = box
    ws.row_dimensions[r].height = 28

wb = Workbook()

# ============================ DÉTAIL ============================
D = wb.create_sheet('Détail')
setup_print(D, True, '1:4', [10, 56, 8, 7, 12, 10, 9, 13, 10, 58])
banner(D, 'S-1902 — DÉTAIL DU CHIFFRAGE (méthode Dupuis / ACCEO)',
       'Chaque ligne = quantité × prix vendant d’assemblage de M. Dupuis (dernier prix de ses relevés 2026) et quantité × son temps unitaire.  Bleu = intrant · Jaune = heures de jugement · Noir = formule.', 10)
header_row(D, 4, ['Code', 'Description', 'Qté', 'Unité', 'Prix unit.\nvendant ($)', 'Temps unit.\n(h)', 'Article\nbordereau', 'Matériel ($)', 'Heures', 'Source (catalogue Dupuis / allocation)'])
sections = [('A', '5.19 / 3.22 — DÉMANTÈLEMENT, RELOCALISATION, TRAVAUX TEMPORAIRES', ('A-',)),
            ('B', '3.24 à 3.26 — DISTRIBUTION, PANNEAU PP-3, DISJONCTEURS, MCC', ('B-',)),
            ('C', '3.23 — RACCORDEMENTS DES ÉQUIPEMENTS MÉCANIQUES', ('C-',)),
            ('D', '3.27 à 3.34 — SERVICES REZ-DE-CHAUSSÉE ET ÉTAGE', ('D-', 'E-')),
            ('F', '3.35 — ÉCLAIRAGE, ÉCLAIRAGE D’URGENCE ET CONTRÔLE', ('F-',)),
            ('G', '3.36 à 3.38 — ALARME INCENDIE', ('G-',)),
            ('H', 'FRAIS DE CHANTIER (répartis sur 3.31)', ('H-',))]
r = 5; sub_rows = []
for sec, title, prefixes in sections:
    c = D.cell(r, 1, title); c.font = fSec; c.fill = fillSec
    for j in range(1, 11): D.cell(r, j).fill = fillSec; D.cell(r, j).border = box
    D.merge_cells(start_row=r, start_column=1, end_row=r, end_column=10); r += 1
    first = r
    for x in C['lignes']:
        if not x['code'].startswith(prefixes): continue
        vals = [x['code'], x['desc'], round(x['q'], 2), x['u'], x['p'], x['h'], x['art'], f'=C{r}*E{r}', f'=C{r}*F{r}', x['src']]
        for j, v in enumerate(vals, 1):
            c = D.cell(r, j, v); c.font = fN; c.border = box; c.alignment = wrap if j in (2, 10) else (center if j in (1, 4, 7) else right)
        D.cell(r, 3).font = fBlue; D.cell(r, 5).font = fBlue; D.cell(r, 6).font = fBlue
        D.cell(r, 5).number_format = CUR; D.cell(r, 6).number_format = '0.000'; D.cell(r, 8).number_format = CUR; D.cell(r, 9).number_format = HRS
        if 'jugement' in x['src']:
            D.cell(r, 5).fill = fillY; D.cell(r, 6).fill = fillY
        if (r - first) % 2 == 1:
            for j in range(1, 11):
                if D.cell(r, j).fill.fgColor.rgb in (None, '00000000'): D.cell(r, j).fill = fillZ
        D.row_dimensions[r].height = 24 if len(x['desc']) < 70 else 36
        r += 1
    last = r - 1
    D.cell(r, 2, f'Sous-total section {sec}').font = fB
    D.cell(r, 8, f'=SUM(H{first}:H{last})').number_format = CUR; D.cell(r, 9, f'=SUM(I{first}:I{last})').number_format = HRS
    for j in range(1, 11): D.cell(r, j).fill = fillG; D.cell(r, j).border = box; D.cell(r, j).font = fB
    D.cell(r, 8).alignment = right; D.cell(r, 9).alignment = right
    sub_rows.append(r); r += 2
D.cell(r, 2, 'TOTAL MATÉRIEL / LOTS ET HEURES RELEVÉES').font = fTot
D.cell(r, 8, '=' + '+'.join(f'H{s}' for s in sub_rows)).number_format = CUR
D.cell(r, 9, '=' + '+'.join(f'I{s}' for s in sub_rows)).number_format = HRS
for j in range(1, 11):
    D.cell(r, j).border = Border(top=med, bottom=med, left=thin, right=thin); D.cell(r, j).fill = fillSec
D.cell(r, 8).font = fTot; D.cell(r, 9).font = fTot; D.cell(r, 8).alignment = right; D.cell(r, 9).alignment = right
TOT_ROW = r
D.freeze_panes = 'A5'

# ============================ SOMMAIRE ============================
S = wb.active; S.title = 'Sommaire'
setup_print(S, False, '1:3', [50, 22, 56])
banner(S, 'S-1902 — SOMMAIRE DU CHIFFRAGE',
       'Bibliothèque Georgette-Lepage (Brossard) — RFID — AO SP-GTER-26-0080 — R.D.J. E-26-75-GE', 3)
PRIX_SOUMIS = sum(m for _, _, m in V)
tot_mat = C['materiel']; tot_h = C['heures_relevees']; tot_hc = C['heures_chargees']; tot_acceo = C['total_acceo']

def section_title(ws, r, txt, ncols=3):
    c = ws.cell(r, 1, txt); c.font = fSec; c.alignment = Alignment(vertical='center', indent=0)
    for j in range(1, ncols + 1): ws.cell(r, j).border = Border(bottom=Side(style='medium', color=BORD))
    ws.row_dimensions[r].height = 20

def kpi(ws, r, j, label, value, fmt, big=True):
    a = ws.cell(r, j, label); a.font = Font(name=F, bold=True, size=8, color=BORD); a.alignment = Alignment(horizontal='center', vertical='bottom'); a.fill = fillSec
    b = ws.cell(r + 1, j, value); b.number_format = fmt; b.font = Font(name=F, bold=True, size=16 if big else 13, color=BORD if big else INK_C); b.alignment = Alignment(horizontal='center', vertical='top'); b.fill = fillSec
    for rr in (r, r + 1): ws.cell(rr, j).border = box

INK_C = '1F1F1F'
# --- bandeau KPI (ligne 4-5) ---
r = 4
kpi(S, r, 1, 'PRIX SOUMIS (avant taxes)', PRIX_SOUMIS, CUR0, True)
kpi(S, r, 2, 'HEURES CHARGÉES', tot_hc, '#,##0 "h"', False)
kpi(S, r, 3, 'SOMMAIRE ACCEO (matériel + MO, admin/profit 0 %)', tot_acceo, CUR0, False)
S.row_dimensions[4].height = 14; S.row_dimensions[5].height = 26
r = 7

def table(ws, r, headers, rows, fmts, bold_last=False):
    """rows: list de tuples (col1, col2, col3) ; fmts: format de la colonne 2 ; retourne la ligne suivante."""
    header_row(ws, r, headers); ws.row_dimensions[r].height = 18; r += 1
    for i, (a, b, c3) in enumerate(rows):
        last = bold_last and i == len(rows) - 1
        ca = ws.cell(r, 1, a); ca.font = fB if last else fN
        cb = ws.cell(r, 2, b); cb.number_format = fmts[i] if isinstance(fmts, list) else fmts; cb.font = fTot if last else (fBlue if isinstance(b, (int, float)) and str(a).startswith(('Taux', 'Facteur')) else fN)
        cc = ws.cell(r, 3, c3); cc.font = fSub
        for j in range(1, 4):
            cell = ws.cell(r, j); cell.border = box
            cell.alignment = Alignment(vertical='center', horizontal='right' if j == 2 else 'left', indent=1 if j != 2 else 0, wrap_text=(j == 3))
            if last: cell.fill = fillSec
            elif i % 2 == 1: cell.fill = fillZ
        ws.row_dimensions[r].height = 17
        r += 1
    return r + 1

# --- 1. Calcul ---
section_title(S, r, '1. CALCUL (méthode Dupuis — Expert Estimateur / ACCEO)'); r += 1
rows = [('Taux horaire', 85, 'Dupuis, août–oct. 2026 : S-1797, S-1835, S-1854, S-1881'),
        ('Matériel + lots fournisseur (prix vendant Dupuis)', f"=Détail!H{TOT_ROW}", 'Feuille Détail — dernière valeur du catalogue par article'),
        ('Heures relevées', f"=Détail!I{TOT_ROW}", 'Feuille Détail — temps unitaires Dupuis'),
        ('Heures chargées (arrondi vers le haut, multiple de 10)', '=CEILING(B11,10)', 'Pratique Dupuis (S-1881 : 4 128,6 → 4 150 h)'),
        ("Main-d'œuvre = heures chargées × taux", '=B12*B9', ''),
        ('Sommaire ACCEO = matériel + main-d\'œuvre', '=B10+B13', 'Admin/profit 0 % — équivalent de son « Grand total » ; part MO ' + f'{C["main_doeuvre"]/C["total_acceo"]:.0%}' + ' (Dupuis : 30–69 %)'),
        ('Facteur de passage au prix de vente', 1.244, 'S-1844 : prix remis 238 744 $ ÷ sommaire ACCEO 191 909,19 $'),
        ('Prix de vente calculé', '=ROUND(B14*B15,0)', ''),
        ('PRIX SOUMIS (arrondi au millier)', PRIX_SOUMIS, 'Somme des articles de la soumission (PDF)')]
fm = [CUR, CUR, HRS, '#,##0', CUR, CUR, '0.000', CUR0, CUR0]
r = table(S, r, ['Poste', 'Valeur', 'Source / preuve'], rows, fm, bold_last=True)

# --- 2. Comparaisons ---
section_title(S, r, '2. COMPARAISONS'); r += 1
rows = [('Estimation_2 — Léna AI, 2026-10-08', 112381.39, '719,5 h × 124 $ + Lumen 23 160 $ ; sans FG, profit ni sous-traitance'),
        ('v2 — 2026-10-20 (midi)', 158296, '745 h × 113,50 $ pondéré + matériel + allocations'),
        ('v3 — méthode Dupuis, médianes conduits', 183000, '990 h ; conduits aux valeurs médianes du catalogue'),
        ('v4 — méthode Dupuis, dernières valeurs (ce classeur)', PRIX_SOUMIS, 'Ses temps et prix « dernier », 85 $/h, × 1,244')]
r = table(S, r, ['Version', 'Prix avant taxes', 'Base'], rows, CUR0, bold_last=True)

# --- 3. Lots ---
section_title(S, r, '3. LOTS FOURNISSEUR INCLUS (prix confirmés par Frank, 2026-10-20)'); r += 1
rows = [('Luminaires A1 ×11, Axis SL1 ×33 + trousses, E ×3, Z6 ×3', 11 * 185 + 12 * 290 + 15 * 230 + 6 * 110 + 1500 + 3 * 475 + 3 * 161.60, 'Gerrie prix réguliers / agents'),
        ('Panneau NF 225 A 42 cct + disjoncteurs EDB/EJB', 6200, 'Schneider NF + EDB 1P ×20 + EJB 3P ×3'),
        ('Services JCI/Simplex + 2 détecteurs adressables', 8000, 'Bypass, programmation 4007ES, annonciateur, vérification ULC-S537'),
        ('Scan GPR de la dalle', 1250, 'Dupuis « SCAN DALLE BETON »')]
r = table(S, r, ['Poste', 'Montant ($)', 'Note'], rows, CUR0)

# --- 4. Ventilation ---
section_title(S, r, '4. VENTILATION PAR ARTICLE DU BORDEREAU (Annexe 2.00, prix soumis avant taxes)'); r += 1
rows = []
for a, d, m in V:
    pa = C['par_article'][a]
    rows.append((f"{a} — {d}", m, f"{pa['materiel']:,.0f} $ matériel · {pa['heures']:,.1f} h".replace(',', ' ')))
rows.append(('TOTAL ÉLECTRICITÉ, avant taxes', f'=SUM(B{r+1}:B{r+len(V)})', ''))
r = table(S, r, ['Article — description (bordereau R.D.J.)', 'Prix soumis ($)', 'Base ACCEO'], rows, CUR0, bold_last=True)

# ============================ PAR ARTICLE ============================
A = wb.create_sheet('Par article')
setup_print(A, False, '1:3', [9, 52, 14, 10, 14, 15, 15])
banner(A, 'S-1902 — VENTILATION PAR ARTICLE DU BORDEREAU (Annexe 2.00)',
       'Total ACCEO par article = matériel + heures × taux (arrondi réparti au prorata) ; prix soumis = total × 1,244 arrondi au dollar ; 3.31 absorbe l’arrondi du total.', 7)
header_row(A, 3, ['Article', 'Description (bordereau R.D.J.)', 'Matériel ($)', 'Heures', 'Main-d’œuvre ($)', 'Total ACCEO ($)', 'Prix soumis ($)'])
desc = {a: d for a, d, _ in V}; sold = {a: m for a, _, m in V}
r = 4; first = r
for a, v in C['par_article'].items():
    vals = [a, desc[a], v['materiel'], v['heures'], v['mo'], v['total'], sold[a]]
    for j, val in enumerate(vals, 1):
        c = A.cell(r, j, val); c.font = fN; c.border = box; c.alignment = center if j == 1 else (wrap if j == 2 else right)
    for j in (3, 5, 6, 7): A.cell(r, j).number_format = CUR0
    A.cell(r, 4).number_format = HRS; A.cell(r, 7).font = fB
    if (r - first) % 2 == 1:
        for j in range(1, 8): A.cell(r, j).fill = fillZ
    A.row_dimensions[r].height = 20; r += 1
last = r - 1
A.cell(r, 2, 'TOTAL ÉLECTRICITÉ (avant taxes)').font = fTot
for j, col in zip((3, 4, 5, 6, 7), 'CDEFG'):
    c = A.cell(r, j, f'=SUM({col}{first}:{col}{last})'); c.font = fTot; c.alignment = right; c.number_format = HRS if col == 'D' else CUR0
for j in range(1, 8): A.cell(r, j).fill = fillSec; A.cell(r, j).border = Border(top=med, bottom=med, left=thin, right=thin)
r += 1
A.cell(r, 2, 'TPS 5 %').font = fN; A.cell(r, 7, f'=ROUND(G{r-1}*0.05,2)').number_format = CUR; r += 1
A.cell(r, 2, 'TVQ 9,975 %').font = fN; A.cell(r, 7, f'=ROUND(G{r-2}*0.09975,2)').number_format = CUR; r += 1
A.cell(r, 2, 'TOTAL TAXES INCLUSES').font = fB; A.cell(r, 7, f'=G{r-3}+G{r-2}+G{r-1}').number_format = CUR; A.cell(r, 7).font = fB
for rr in range(r - 2, r + 1):
    for j in range(1, 8): A.cell(rr, j).border = box
    A.cell(rr, 7).alignment = right
A.freeze_panes = 'A4'

wb.move_sheet('Sommaire', offset=-2)
wb.save(OUT); print('saved', OUT, 'TOT_ROW', TOT_ROW)

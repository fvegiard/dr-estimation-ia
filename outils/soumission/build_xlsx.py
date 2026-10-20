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
setup_print(S, False, '1:3', [54, 20, 54])
banner(S, 'S-1902 — SOMMAIRE DU CHIFFRAGE',
       'Bibliothèque Georgette-Lepage (Brossard) — RFID, RDC et étage — AO SP-GTER-26-0080 — R.D.J. E-26-75-GE', 3)
S['A3'] = ('Méthode de M. Dupuis (Expert Estimateur / ACCEO) : matériel au prix vendant de son catalogue, administration et profit 0 % dans le sommaire, '
           'main-d’œuvre = heures relevées arrondies vers le haut × taux horaire, puis facteur de passage au prix de vente observé sur S-1844.')
S['A3'].font = fSub; S.merge_cells('A3:C3'); S['A3'].alignment = Alignment(wrap_text=True, vertical='center'); S.row_dimensions[3].height = 34
header_row(S, 5, ['Poste', 'Valeur', 'Source / preuve'])
rows = [
    ('Taux horaire ($/h)', 85, CUR, 'Dupuis, août–oct. 2026 : S-1797, S-1835, S-1854, S-1881', True),
    ('Matériel + lots fournisseur (prix vendant Dupuis + allocations)', f"=Détail!H{TOT_ROW}", CUR, 'Feuille Détail', False),
    ('Heures relevées', f"=Détail!I{TOT_ROW}", HRS, 'Feuille Détail (temps unitaires Dupuis)', False),
    ('Heures chargées (arrondi vers le haut, multiple de 10)', '=CEILING(B8,10)', HRS, 'Pratique Dupuis (S-1881 : 4 128,6 → 4 150 h)', False),
    ('Main-d’œuvre = heures chargées × taux', '=B9*B6', CUR, '', False),
    ('TOTAL SOMMAIRE ACCEO (admin/profit 0 %, comme Dupuis)', '=B7+B10', CUR, 'Équivalent de son « Grand total »', False),
    ('Part main-d’œuvre du sommaire', '=B10/B11', '0.0%', 'Dupuis : 30–69 %, médiane ≈ 45 % (S-1783 : 50,5 %)', False),
    ('Facteur de passage au prix de vente', 1.244, '0.000', 'S-1844 : prix remis 238 744 $ ÷ sommaire ACCEO 191 909,19 $', True),
    ('Prix de vente calculé', '=ROUND(B11*B13,0)', CUR0, '', False),
    ('PRIX SOUMIS (arrondi au millier)', 183000, CUR0, 'Soumission_S-1902_Georgette-Lepage.pdf', True),
    ('Heures par 100 k$ de prix', '=B9/(B15/100000)', '#,##0', 'Dupuis : ≈ 450–520 h / 100 k$ (S-1783, S-1775, S-1857, S-1881)', False),
]
r = 6
for lab, val, fmt, src, blue in rows:
    S.cell(r, 1, lab).font = fN; c = S.cell(r, 2, val); c.number_format = fmt; c.font = fBlue if blue else fN; c.alignment = right
    S.cell(r, 3, src).font = fSub
    for j in range(1, 4): S.cell(r, j).border = box; S.cell(r, j).alignment = Alignment(wrap_text=True, vertical='center', horizontal='right' if j == 2 else 'left')
    S.row_dimensions[r].height = 22
    if lab.startswith('TOTAL') or lab.startswith('PRIX SOUMIS'):
        for j in range(1, 4): S.cell(r, j).fill = fillSec; S.cell(r, j).font = fTot if j == 2 else fB
    r += 1
r += 1
S.cell(r, 1, 'COMPARAISONS').font = fSec; r += 1
header_row(S, r, ['Version', 'Prix avant taxes', 'Base']); r += 1
for lab, val, src in [('Estimation_2 — Léna AI, 2026-10-08', 112381.39, '719,5 h × 124 $ + Lumen 23 160 $ ; sans FG, profit ni sous-traitance'),
                      ('v2 — 2026-10-20 (midi)', 158296, '745 h × 113,50 $ pondéré + matériel + allocations'),
                      ('v3 — méthode Dupuis (ce classeur)', '=B15', 'Ses temps, ses prix d’assemblage, 85 $/h, × 1,244')]:
    S.cell(r, 1, lab).font = fN; c = S.cell(r, 2, val); c.number_format = CUR0; c.alignment = right; c.font = fN; S.cell(r, 3, src).font = fSub
    for j in range(1, 4): S.cell(r, j).border = box
    r += 1
r += 1
S.cell(r, 1, 'LOTS FOURNISSEUR INCLUS (prix confirmés par Frank, 2026-10-20)').font = fSec; r += 1
header_row(S, r, ['Poste', 'Montant ($)', 'Note']); r += 1
for lab, val, st in [('Luminaires A1 ×11, Axis SL1 (4′×12, 3′×15, 1′×6) + trousses, E ×3, Z6 ×3', 11 * 185 + 12 * 290 + 15 * 230 + 6 * 110 + 1500 + 3 * 475 + 3 * 161.60, 'Prix retenus (Gerrie prix réguliers / agents) — confirmés'),
                     ('Panneau NF 225 A 42 cct + disjoncteurs EDB/EJB', 6200, 'Schneider NF 225 A 42 cct + EDB/EJB — confirmé'),
                     ('Services JCI/Simplex + 2 détecteurs adressables', 8000, 'Services JCI + 2 détecteurs 4098-9714 — confirmé'),
                     ('Scan GPR de la dalle', 1250, 'Dupuis « SCAN DALLE BETON » 1 250 $')]:
    S.cell(r, 1, lab).font = fN; c = S.cell(r, 2, val); c.number_format = CUR0; c.alignment = right; c.font = fN; S.cell(r, 3, st).font = fSub
    for j in range(1, 4): S.cell(r, j).border = box; S.cell(r, j).alignment = Alignment(wrap_text=True, vertical='center', horizontal='right' if j == 2 else 'left')
    S.row_dimensions[r].height = 26; r += 1

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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Soumission DR Électrique — gabarit officiel (ReportLab, bordeaux/rose, logo DR).
Usage: python gen_soumission.py <donnees.json> <sortie.pdf>
Le prix forfaitaire = somme des articles de la ventilation (jamais saisi à la main)."""
import json, sys
from decimal import Decimal, ROUND_HALF_UP
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
                                KeepTogether, ListFlowable, ListItem)
from num2words import num2words

BORDEAUX = colors.HexColor('#6B1A1A')
ROSE = colors.HexColor('#F5E6E6')
GRIS = colors.HexColor('#F2F2F2')
INK = colors.HexColor('#1F1F1F')
GREY = colors.HexColor('#555555')
LINE = colors.HexColor('#C9C9C9')

W, H = letter
import os
LOGO = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logo_dr.png')
ML = MR = 16 * mm
MT = 30 * mm
MB = 18 * mm

def money(d: Decimal) -> str:
    q = d.quantize(Decimal('0.01'), ROUND_HALF_UP)
    s = f"{q:,.2f}".replace(',', ' ').replace('.', ',')
    return s + ' $'

def words(d: Decimal) -> str:
    q = d.quantize(Decimal('0.01'), ROUND_HALF_UP)
    dollars = int(q); cents = int((q - dollars) * 100)
    t = num2words(dollars, lang='fr') + (' dollars' if dollars > 1 else ' dollar')
    if cents:
        t += ' et ' + num2words(cents, lang='fr') + (' cents' if cents > 1 else ' cent')
    return t[0].upper() + t[1:]

base = ParagraphStyle('base', fontName='Helvetica', fontSize=9, leading=12, textColor=INK)
small = ParagraphStyle('small', parent=base, fontSize=8, leading=10.5)
bold = ParagraphStyle('bold', parent=base, fontName='Helvetica-Bold')
ital = ParagraphStyle('ital', parent=base, fontName='Helvetica-Oblique', textColor=GREY)
h1 = ParagraphStyle('h1', parent=base, fontName='Helvetica-Bold', fontSize=15, leading=18, textColor=BORDEAUX)
bar = ParagraphStyle('bar', parent=base, fontName='Helvetica-Bold', fontSize=9.5, textColor=colors.white, leading=12)
price = ParagraphStyle('price', parent=base, fontName='Helvetica-Bold', fontSize=22, leading=26, textColor=BORDEAUX, alignment=TA_CENTER)
pwords = ParagraphStyle('pwords', parent=ital, alignment=TA_CENTER)
ptitle = ParagraphStyle('ptitle', parent=base, fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=BORDEAUX, alignment=TA_CENTER)
psub = ParagraphStyle('psub', parent=base, fontName='Helvetica-Bold', fontSize=10.5, alignment=TA_CENTER)
lbl = ParagraphStyle('lbl', parent=base, fontName='Helvetica-Bold', fontSize=8.5, textColor=BORDEAUX)
right = ParagraphStyle('right', parent=base, alignment=TA_RIGHT)
rightb = ParagraphStyle('rightb', parent=bold, alignment=TA_RIGHT)
cond = ParagraphStyle('cond', parent=small, leftIndent=0)

CONDITIONS = [
    "La soumission est valide pour {validite}",
    "Un délai de dix (10) jours ouvrables est nécessaire à la planification de la date des travaux, suite à l'acceptation de la soumission",
    "La tarification soumise par la présente offre ne tient pas compte de la TPS et la TVQ",
    "Termes de paiement, net 30 jours",
    "Intérêt de 2% par mois (24% par année) sur les comptes passés dû",
    "Les travaux seront effectués durant les heures normales de bureau",
    "Frais supplémentaire dû aux conditions hivernales non-incluses",
    "Une facturation partielle pourrait être émise selon l'avancement des travaux",
    "Tout retard non raisonnable et non imputable à notre personnel sera facturé en supplément",
    "Les réparations, autres que spécifiées, ne sont pas comprises et pourront être effectuées en supplément à votre demande",
]
VOLATILITE = ("<b>Clause de volatilité des matériaux :</b> le prix des matériaux de base sont très volatiles en ce moment et peuvent "
              "nécessiter un ajustement sans préavis de la part de nos fournisseurs. Nous ne pouvons donc garantir les prix des matériaux "
              "qui sont inclus dans la soumission. Dans ce cas, une charge additionnelle vous sera facturée avec justification et "
              "explication. Les matériaux concernés sont les suivants : conduits et boîtes métalliques, conduits de PVC et câbles en "
              "cuivre et aluminium.")

def section_bar(txt):
    t = Table([[Paragraph(txt, bar)]], colWidths=[W - ML - MR])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), BORDEAUX), ('LEFTPADDING', (0, 0), (-1, -1), 6),
                           ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]))
    return t

def bullets(items, style=base):
    return ListFlowable([ListItem(Paragraph(i, style), leftIndent=10, value='•') for i in items],
                        bulletType='bullet', start='•', leftIndent=12, bulletFontSize=8, spaceBefore=0)

def header_footer(canvas, doc, D):
    canvas.saveState()
    # bandeau bordeaux
    canvas.setFillColor(BORDEAUX); canvas.rect(0, H - 18 * mm, W, 18 * mm, stroke=0, fill=1)
    # logo officiel (soumissions-brand/assets/logo_dr.png) dans un cartouche blanc
    canvas.setFillColor(colors.white); canvas.roundRect(ML, H - 16.5 * mm, 46 * mm, 15 * mm, 2 * mm, stroke=0, fill=1)
    lh = 13 * mm; lw = lh * 398 / 420
    canvas.drawImage(LOGO, ML + 2 * mm, H - 15.5 * mm, width=lw, height=lh, mask='auto')
    canvas.setFillColor(INK); canvas.setFont('Helvetica-Bold', 9.5); canvas.drawString(ML + lw + 5 * mm, H - 8.5 * mm, 'LE GROUPE DR')
    canvas.setFillColor(BORDEAUX); canvas.setFont('Helvetica-Bold', 8); canvas.drawString(ML + lw + 5 * mm, H - 12.5 * mm, 'Électrique inc.')
    canvas.setFillColor(colors.white); canvas.setFont('Helvetica-Bold', 8)
    canvas.drawRightString(W - MR, H - 7 * mm, '1420, boul. Lionel-Boulet, Varennes (Québec)')
    canvas.setFont('Helvetica', 7.5)
    canvas.drawRightString(W - MR, H - 10.5 * mm, 'drservice@drelectrique.com')
    canvas.drawRightString(W - MR, H - 14 * mm, 'RBQ : 5587-4812-01')
    # pied
    canvas.setStrokeColor(LINE); canvas.setLineWidth(0.5); canvas.line(ML, MB - 4 * mm, W - MR, MB - 4 * mm)
    canvas.setFillColor(GREY); canvas.setFont('Helvetica', 7)
    canvas.drawCentredString(W / 2, MB - 8 * mm, f"DR Électrique inc.  |  Merci de votre confiance  |  Soumission {D['no']}  Page {doc.page}")
    canvas.restoreState()

def build(D, out):
    doc = BaseDocTemplate(out, pagesize=letter, leftMargin=ML, rightMargin=MR, topMargin=MT, bottomMargin=MB,
                          title=f"Soumission {D['no']} - {D['titre_court']}", author='Le Groupe DR Électrique inc.')
    frame = Frame(ML, MB, W - ML - MR, H - MT - MB, id='f', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id='p', frames=[frame], onPage=lambda c, d: header_footer(c, d, D))])
    S = []
    cw = W - ML - MR

    # Titre + date
    t = Table([[Paragraph(f"SOUMISSION {D['no']}", h1), Paragraph(D['date_ligne'], right)]], colWidths=[cw * 0.6, cw * 0.4])
    t.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('LINEBELOW', (0, 0), (-1, 0), 1.2, BORDEAUX),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 5), ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0)]))
    S += [t, Spacer(1, 5 * mm)]

    # CLIENT / DÉTAILS
    cl = [Paragraph('CLIENT', lbl)] + [Paragraph(x, base) for x in D['client']]
    dt = [Paragraph('DÉTAILS', lbl)] + [Paragraph(x, base) for x in D['details']]
    t = Table([[cl, dt]], colWidths=[cw / 2, cw / 2])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), ROSE), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                           ('LINEBEFORE', (1, 0), (1, 0), 1, BORDEAUX), ('LEFTPADDING', (0, 0), (-1, -1), 8), ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                           ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6)]))
    S += [t, Spacer(1, 5 * mm)]

    # Prix
    total = sum(Decimal(str(x[2])) for x in D['ventilation'])
    D['_total'] = total
    pb = [Paragraph(money(total), price), Paragraph(f"({words(total)}) — taxes en sus", pwords), Spacer(1, 2 * mm),
          Paragraph('PRIX FORFAITAIRE', ptitle), Paragraph(D['prix_sous_titre'], psub)]
    t = Table([[pb]], colWidths=[cw])
    t.setStyle(TableStyle([('LINEABOVE', (0, 0), (-1, 0), 1, BORDEAUX), ('LINEBELOW', (0, 0), (-1, 0), 1, BORDEAUX),
                           ('TOPPADDING', (0, 0), (-1, -1), 8), ('BOTTOMPADDING', (0, 0), (-1, -1), 8)]))
    S += [t, Spacer(1, 3 * mm), Paragraph(D['prix_note'], ital), Spacer(1, 4 * mm)]

    # Ventilation bordereau
    S += [section_bar(D['ventilation_titre']), Spacer(1, 2 * mm)]
    rows = [[Paragraph('<b>Article</b>', small), Paragraph('<b>Description (bordereau de prix)</b>', small), Paragraph('<b>Montant</b>', ParagraphStyle('x', parent=small, alignment=TA_RIGHT))]]
    for art, desc, amt in D['ventilation']:
        rows.append([Paragraph(art, small), Paragraph(desc, small), Paragraph(money(Decimal(str(amt))), ParagraphStyle('y', parent=small, alignment=TA_RIGHT))])
    rows.append(['', Paragraph('<b>TOTAL ÉLECTRICITÉ (avant taxes)</b>', small), Paragraph(f'<b>{money(total)}</b>', ParagraphStyle('z', parent=small, alignment=TA_RIGHT))])
    t = Table(rows, colWidths=[18 * mm, cw - 18 * mm - 32 * mm, 32 * mm], repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), GRIS), ('LINEBELOW', (0, 0), (-1, -2), 0.4, LINE),
                           ('BACKGROUND', (0, -1), (-1, -1), ROSE), ('TEXTCOLOR', (0, -1), (-1, -1), BORDEAUX),
                           ('TOPPADDING', (0, 0), (-1, -1), 2.5), ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
    S += [t, Spacer(1, 1.5 * mm), Paragraph(D['ventilation_note'], ParagraphStyle('vn', parent=ital, fontSize=7.5, leading=9.5)), Spacer(1, 4 * mm)]

    # Fournir et installer
    S += [section_bar('FOURNIR ET INSTALLER'), Spacer(1, 2 * mm), bullets(D['travaux']), Spacer(1, 4 * mm)]

    # Prix séparés
    if D.get('prix_separes'):
        S += [section_bar('PRIX SÉPARÉS (non inclus au prix forfaitaire)'), Spacer(1, 2 * mm)]
        rows = [[Paragraph('<b>Code</b>', small), Paragraph('<b>Description</b>', small), Paragraph('<b>Montant avant taxes</b>', ParagraphStyle('x', parent=small, alignment=TA_RIGHT))]]
        for code, desc, amt in D['prix_separes']:
            rows.append([Paragraph(code, small), Paragraph(desc, small), Paragraph(amt, ParagraphStyle('y', parent=small, alignment=TA_RIGHT))])
        t = Table(rows, colWidths=[16 * mm, cw - 16 * mm - 40 * mm, 40 * mm], repeatRows=1)
        t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), GRIS), ('LINEBELOW', (0, 0), (-1, -1), 0.4, LINE),
                               ('TOPPADDING', (0, 0), (-1, -1), 2.5), ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
        S += [t, Spacer(1, 4 * mm)]

    # Exclusions
    S += [section_bar('EXCLUSIONS'), Spacer(1, 2 * mm), bullets(D['exclusions']), Spacer(1, 4 * mm)]

    # Conditions
    conds = [Paragraph(f"{i + 1})&nbsp;&nbsp;{c.format(validite=D['validite'])}", cond) for i, c in enumerate(CONDITIONS)]
    S += [KeepTogether([section_bar('CONDITIONS'), Spacer(1, 2 * mm)] + conds), Spacer(1, 3 * mm),
          Paragraph(VOLATILITE, ParagraphStyle('vol', parent=small, leftIndent=14)), Spacer(1, 6 * mm),
          Paragraph("Nous vous remercions de la confiance que vous nous témoignez et demeurons à votre disposition pour toute question.", base),
          Spacer(1, 10 * mm)]

    # Signature
    sig = [Paragraph('__________________________________', base)] + [Paragraph(x, bold if i == 0 else base) for i, x in enumerate(D['signataire'])]
    S += [KeepTogether(sig), Spacer(1, 8 * mm)]

    # Approbation
    ap = [Paragraph('APPROBATION / BON DE COMMANDE', ParagraphStyle('apt', parent=bold, textColor=BORDEAUX)), Spacer(1, 3 * mm),
          Paragraph(f"Par la présente, nous acceptons la soumission {D['no']} au montant forfaitaire de {money(total)} (taxes en sus) et autorisons DR Électrique inc. à procéder aux travaux décrits ci-dessus.", base),
          Spacer(1, 5 * mm),
          Paragraph('Nom : ______________________________  Titre : ______________________________', base), Spacer(1, 3 * mm),
          Paragraph('Signature : _________________________  Date : _______________________________', base), Spacer(1, 3 * mm),
          Paragraph('N° de bon de commande : ______________________', base)]
    t = Table([[ap]], colWidths=[cw])
    t.setStyle(TableStyle([('BOX', (0, 0), (-1, -1), 1.2, BORDEAUX), ('BACKGROUND', (0, 0), (0, 0), colors.white),
                           ('LEFTPADDING', (0, 0), (-1, -1), 8), ('RIGHTPADDING', (0, 0), (-1, -1), 8), ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 8)]))
    # bandeau rose titre dans l'encadré : simplifié, titre en bordeaux
    S += [KeepTogether([t])]
    doc.build(S)
    return total

if __name__ == '__main__':
    D = json.load(open(sys.argv[1], encoding='utf-8'))
    total = build(D, sys.argv[2])
    print(f"OK {sys.argv[2]} total={money(total)}")

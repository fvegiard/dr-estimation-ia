#!/usr/bin/env python3
"""Générateur de soumissions / lettres brandées (DR, SIP, BR ou toute compagnie dans brands.json).

Usage:
  python generate.py --brand br --data examples/soumission_EP2026-079.json --out out/soum_br.pdf
  python generate.py --brand dr --data examples/lettre_E2026-XX.json --out out/lettre_dr.pdf
  python generate.py --all --data examples/soumission_EP2026-079.json --outdir out/   (une PDF par marque)

Le type (soumission | lettre) est lu dans le JSON ("type"). La palette est dérivée de brands.json :
  primary -> bandes, titres, lignes ; tint (primary mélangé 90 % blanc) -> bloc CLIENT/DÉTAILS ; gris #F2F2F2 -> en-têtes de tableau.
"""
import argparse
import json
import os
from pathlib import Path

from num2words import num2words
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, Frame, Image, KeepTogether, ListFlowable, ListItem, PageBreak,
                                PageTemplate, Paragraph, Spacer, Table, TableStyle)

ROOT = Path(__file__).resolve().parent
GREY = colors.HexColor("#F2F2F2")
RULE = colors.HexColor("#BDBDBD")
INK = colors.HexColor("#1F1F1F")
INK2 = colors.HexColor("#444444")

CONDITIONS = [
    "La soumission est valide pour 30 jours",
    "Un délai de dix (10) jours ouvrables est nécessaire à la planification de la date des travaux, suite à l'acceptation de la soumission",
    "La tarification soumise par la présente offre ne tient pas compte de la TPS et la TVQ",
    "Termes de paiement, net 30 jours",
    "Intérêt de 2% par mois (24% par année) sur les comptes passés dû",
    "Les travaux seront effectués durant les heures normales de bureau",
    "Frais supplémentaire dû aux conditions hivernales non-incluses",
    "Une facturation partielle pourrait être émise selon l'avancement des travaux",
    "Tout retard non raisonnable et non imputable à notre personnel sera facturé en supplément",
    "Les réparations, autres que spécifiées, ne sont pas comprises et pourront être effectuées en supplément à votre demande.",
]
VOLATILITE = ("Le prix des matériaux de base sont très volatiles en ce moment et peuvent nécessiter un ajustement sans préavis "
              "de la part de nos fournisseurs. Nous ne pouvons donc garantir les prix des matériaux qui sont inclus dans la "
              "soumission. Dans ce cas, une charge additionnelle vous sera facturée avec justification et explication. Les "
              "matériaux concernés sont les suivants : conduits et boîtes métalliques, conduits de PVC et câbles en cuivre et aluminium.")


# ---------- helpers ----------
def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def mix(a, b, t):
    ra, rb = hex2rgb(a), hex2rgb(b)
    return "#%02X%02X%02X" % tuple(round(x + (y - x) * t) for x, y in zip(ra, rb))


def luminance(h):
    r, g, b = (c / 255 for c in hex2rgb(h))
    lin = lambda c: c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4
    return .2126 * lin(r) + .7152 * lin(g) + .0722 * lin(b)


def palette(brand):
    """Palette dérivée du logo. Une primaire claire (jaune, cyan…) garde le texte lisible :
    la bande prend un texte foncé et les titres sur blanc utilisent la variante foncée."""
    p = brand["primary"]
    dark = mix(p, "#000000", .25)
    light = luminance(p) > .45
    return {"brand": colors.HexColor(p), "dark": colors.HexColor(dark),
            "tint": colors.HexColor(mix(p, "#FFFFFF", .90)), "secondary": colors.HexColor(brand.get("secondary", p)),
            "on_brand": INK if light else colors.white,
            "text": colors.HexColor(mix(p, "#000000", .45)) if light else colors.HexColor(p),
            "text_hex": mix(p, "#000000", .45) if light else p}


def money(v):
    s = f"{v:,.2f}".replace(",", " ").replace(".", ",")
    return f"{s} $"


def en_lettres(v):
    # Même quantification que money() : total en cents, puis dollars/cents — jamais d'arrondi du dollar seul.
    d, c = divmod(int(round(float(v) * 100)), 100)
    w = num2words(d, lang="fr")
    w = w[0].upper() + w[1:]
    return f"{w} dollars" + (f" et {num2words(c, lang='fr')} cents" if c else "")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def signer_for(data, brand_key, brand):
    """`signer` peut être une liste (un seul signataire) ou un dict par marque {"br": [...], "dr": [...]}.
    Sans entrée pour la marque demandée : placeholder neutre — jamais le personnel d'une autre compagnie."""
    sg = data.get("signer")
    if isinstance(sg, dict):
        sg = sg.get(brand_key)
    if not sg:
        sg = ["Nom du signataire", "", f"{brand['short']}"]
    return sg


def salutation(data):
    return data.get("salutation", "Madame, Monsieur")


def load_brands():
    return {k: v for k, v in json.load(open(ROOT / "brands.json", encoding="utf-8")).items() if not k.startswith("_")}


# ---------- styles ----------
def styles(P):
    base = ParagraphStyle("base", fontName="Helvetica", fontSize=9.2, leading=12.5, textColor=INK)
    return {
        "base": base,
        "small": ParagraphStyle("small", parent=base, fontSize=8, leading=10.5, textColor=INK2),
        "lbl": ParagraphStyle("lbl", parent=base, fontName="Helvetica-Bold", fontSize=8, textColor=P["text"], spaceAfter=2),
        "h4": ParagraphStyle("h4", parent=base, fontName="Helvetica-Bold", fontSize=9.5, textColor=P["text"], spaceAfter=3),
        "band": ParagraphStyle("band", parent=base, fontName="Helvetica-Bold", fontSize=9.5, textColor=P["on_brand"]),
        "th": ParagraphStyle("th", parent=base, fontName="Helvetica-Bold", fontSize=8.5),
        "thr": ParagraphStyle("thr", parent=base, fontName="Helvetica-Bold", fontSize=8.5, alignment=TA_RIGHT),
        "tdr": ParagraphStyle("tdr", parent=base, alignment=TA_RIGHT),
        "tdc": ParagraphStyle("tdc", parent=base, alignment=TA_CENTER, textColor=INK2),
        "tot": ParagraphStyle("tot", parent=base, fontName="Helvetica-Bold", textColor=P["text"]),
        "totr": ParagraphStyle("totr", parent=base, fontName="Helvetica-Bold", textColor=P["text"], alignment=TA_RIGHT),
        "pk": ParagraphStyle("pk", parent=base, fontName="Helvetica-Bold", fontSize=11, textColor=P["text"], alignment=TA_CENTER),
        "pv": ParagraphStyle("pv", parent=base, fontName="Helvetica-Bold", fontSize=20, leading=24, textColor=P["text"], alignment=TA_CENTER),
        "pw": ParagraphStyle("pw", parent=base, fontName="Helvetica-Oblique", alignment=TA_CENTER, textColor=INK2),
        "pn": ParagraphStyle("pn", parent=base, fontName="Helvetica-Oblique", fontSize=7.5, alignment=TA_CENTER, textColor=INK2),
        "vol": ParagraphStyle("vol", parent=base, fontName="Helvetica-Oblique", fontSize=8.8, textColor=INK2),
        "sig": ParagraphStyle("sig", parent=base, fontName="Helvetica-Bold"),
        "title": ParagraphStyle("title", parent=base, fontName="Helvetica-Bold", fontSize=14, leading=16, alignment=TA_RIGHT),
        "hr": ParagraphStyle("hr", parent=base, fontSize=8.5, leading=11, alignment=TA_RIGHT, textColor=INK2),
        "amt": ParagraphStyle("amt", parent=base, fontName="Helvetica-Bold", fontSize=14, leading=18, textColor=P["text"], alignment=TA_CENTER),
        "amtw": ParagraphStyle("amtw", parent=base, fontName="Helvetica-BoldOblique", alignment=TA_CENTER, textColor=INK2),
        "obj": ParagraphStyle("obj", parent=base, fontName="Helvetica-Bold"),
    }


# ---------- page furniture ----------
def make_doc(out, brand, P, kind, no=""):
    W, H = letter
    lm, rm, tm, bm = 17 * mm, 17 * mm, 34 * mm, 18 * mm
    logo_h = brand.get("logo_height_mm", 18) * mm
    logo_path = ROOT / brand["logo"]
    im = Image(str(logo_path))
    ratio = im.imageWidth / im.imageHeight
    footer_left = brand["short"] + (f"  ·  {brand['rbq']}" if brand.get("rbq") else "")

    def on_page(c, d):
        c.saveState()
        # logo
        c.drawImage(str(logo_path), lm, H - 12 * mm - logo_h, width=logo_h * ratio, height=logo_h, mask="auto", preserveAspectRatio=True, anchor="sw")
        # right header
        c.setFillColor(INK)
        if kind == "soumission":
            c.setFont("Helvetica-Bold", 14); c.drawRightString(W - rm, H - 16 * mm, "SOUMISSION")
            c.setFont("Helvetica", 8.5); c.setFillColor(INK2)
            c.drawRightString(W - rm, H - 21 * mm, f"N° {no}")
            c.drawRightString(W - rm, H - 25 * mm, d.date_str)
        else:
            c.setFont("Helvetica", 8.5); c.setFillColor(INK2)
            y = H - 16 * mm
            for line in [brand["name"], brand.get("address", ""), brand.get("rbq", "")]:
                if line:
                    c.drawRightString(W - rm, y, line); y -= 4 * mm
        # brand rule
        c.setStrokeColor(P["brand"]); c.setLineWidth(2.2)
        c.line(lm, H - 13 * mm - logo_h - 2 * mm, W - rm, H - 13 * mm - logo_h - 2 * mm)
        # footer
        c.setStrokeColor(RULE); c.setLineWidth(.5); c.line(lm, bm - 4 * mm, W - rm, bm - 4 * mm)
        c.setFont("Helvetica", 7.5); c.setFillColor(INK2)
        c.drawString(lm, bm - 8 * mm, footer_left)
        c.drawCentredString(W / 2, bm - 8 * mm, "Merci de votre confiance")
        right = (f"Soumission {no}  ·  Page {d.page}" if kind == "soumission" else f"Page {d.page}")
        c.drawRightString(W - rm, bm - 8 * mm, right)
        c.restoreState()

    doc = BaseDocTemplate(out, pagesize=letter, leftMargin=lm, rightMargin=rm, topMargin=tm + logo_h - 10 * mm, bottomMargin=bm,
                          title=f"Soumission {no}" if no else "Lettre", author=brand["name"])
    fr = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="p", frames=[fr], onPage=on_page)])
    doc.date_str = ""
    return doc


def band(text, P, S, width):
    t = Table([[Paragraph(text, S["band"])]], colWidths=[width])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), P["brand"]), ("LEFTPADDING", (0, 0), (-1, -1), 8),
                           ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    return t


def numbered(items, S, start=1):
    return ListFlowable([ListItem(Paragraph(esc(x), S["base"]), leftIndent=14) for x in items],
                        bulletType="1", start=start, bulletFontName="Helvetica-Bold", bulletFontSize=9, leftIndent=14)


def bullets(items, S):
    return ListFlowable([ListItem(Paragraph(esc(x), S["base"]), leftIndent=12) for x in items],
                        bulletType="bullet", bulletFontSize=7, leftIndent=12)


# ---------- SOUMISSION ----------
def build_soumission(data, brand, out, brand_key=""):
    P = palette(brand); S = styles(P)
    doc = make_doc(out, brand, P, "soumission", data["no"])
    doc.date_str = data["date"]
    W = doc.width
    total = sum(float(i[1]) for i in data["items"])
    el = []

    # CLIENT / DÉTAILS (bloc teinté, séparateur vertical)
    left = [Paragraph("CLIENT", S["lbl"])] + [Paragraph(esc(l), S["base"]) for l in data["client"]]
    right = [Paragraph("DÉTAILS DU PROJET", S["lbl"])] + [Paragraph(esc(l), S["base"]) for l in data["projet"]]
    blk = Table([[left, right]], colWidths=[W / 2, W / 2])
    blk.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), P["tint"]), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                             ("LINEAFTER", (0, 0), (0, 0), .8, P["brand"]),
                             ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                             ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 9)]))
    el += [blk, Spacer(1, 7 * mm)]

    # PRIX entre deux lignes
    prix = Table([[[Paragraph("PRIX FORFAITAIRE DES TRAVAUX (Taxes en sus)", S["pk"]), Paragraph(money(total), S["pv"]),
                    Paragraph(esc(en_lettres(total)), S["pw"]), Paragraph("Nos frais d'administration et profit sont inclus.", S["pn"])]]],
                 colWidths=[W])
    prix.setStyle(TableStyle([("LINEABOVE", (0, 0), (-1, 0), 1.2, P["brand"]), ("LINEBELOW", (0, 0), (-1, 0), 1.2, P["brand"]),
                              ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
    el += [prix, Spacer(1, 7 * mm)]

    # TRAVAUX
    rows = [[Paragraph("#", S["th"]), Paragraph("Description des travaux", S["th"]), Paragraph("Prix", S["thr"])]]
    for i, (desc, price) in enumerate(data["items"], 1):
        rows.append([Paragraph(str(i), S["tdc"]), Paragraph(esc(desc), S["base"]), Paragraph(money(float(price)), S["tdr"])])
    rows.append([Paragraph("TOTAL (avant taxes)", S["tot"]), "", Paragraph(money(total), S["totr"])])
    t = Table(rows, colWidths=[9 * mm, W - 9 * mm - 26 * mm, 26 * mm], repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), GREY), ("LINEBELOW", (0, 0), (-1, 0), .6, RULE),
                           ("LINEBELOW", (0, 1), (-1, -2), .4, colors.HexColor("#E6E6E6")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("SPAN", (0, -1), (1, -1)), ("BACKGROUND", (0, -1), (-1, -1), P["tint"]),
                           ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    el += [band("TRAVAUX", P, S, W), t, Spacer(1, 6 * mm)]

    # EXCLUSIONS
    if data.get("exclusions"):
        el += [KeepTogether([Paragraph("EXCLUSIONS / NOTES", S["h4"]), bullets(data["exclusions"], S)]), Spacer(1, 6 * mm)]

    # CONDITIONS (10) + volatilité
    el += [band("CONDITIONS", P, S, W), Spacer(1, 2 * mm), numbered(CONDITIONS, S), Spacer(1, 5 * mm),
           KeepTogether([Paragraph("VOLATILITÉ DES PRIX DES MATÉRIAUX", S["h4"]), Paragraph(esc(VOLATILITE), S["vol"])]), Spacer(1, 6 * mm)]

    # salutations + signature
    sg = signer_for(data, brand_key, brand)
    el += [Paragraph("Nous espérons le tout à votre entière satisfaction. N'hésitez pas à communiquer avec nous pour toute information additionnelle.", S["base"]),
           Spacer(1, 2 * mm), Paragraph(f"Nous vous prions d'agréer, {esc(salutation(data))}, nos sincères salutations.", S["base"]), Spacer(1, 8 * mm),
           KeepTogether([Paragraph(esc(sg[0]), S["sig"])] + [Paragraph(esc(x), S["base"]) for x in sg[1:]]), Spacer(1, 10 * mm)]

    # APPROBATION / BON DE COMMANDE (encadré)
    ap = Table([[Paragraph("APPROBATION / BON DE COMMANDE", ParagraphStyle("apl", parent=S["lbl"], fontSize=9.5)), ""],
                [Paragraph("Signature : ______________________________", S["base"]), Paragraph("Date : __________________", S["base"])],
                [Paragraph("Nom (lettres moulées) : ______________________________", S["base"]), Paragraph("Bon de commande # : __________________", S["base"])]],
               colWidths=[W * .58, W * .42])
    ap.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 1.5, P["brand"]), ("SPAN", (0, 0), (1, 0)),
                            ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                            ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    el += [KeepTogether([ap])]
    doc.build(el)


# ---------- LETTRE ----------
def build_lettre(data, brand, out, brand_key=""):
    P = palette(brand); S = styles(P)
    doc = make_doc(out, brand, P, "lettre")
    W = doc.width
    el = [Paragraph(esc(data["lieu_date"]), S["base"]), Spacer(1, 5 * mm)]
    el += [Paragraph(esc(l), S["base"]) for l in data["attention"]]
    el += [Spacer(1, 5 * mm), Paragraph(f"<font color='{P['text_hex']}'>PROJET :</font> {esc(data['projet'])}", S["obj"]),
           Paragraph(f"<font color='{P['text_hex']}'>OBJET :</font> {esc(data['objet'])}", S["obj"]), Spacer(1, 5 * mm),
           Paragraph(esc(salutation(data)) + ",", S["base"]), Spacer(1, 3 * mm),
           Paragraph("Pour le projet mentionné en rubrique, nous avons le plaisir de vous soumettre notre prix budgétaire pour la réalisation des travaux d'électricité, établi comme suit :", S["base"]),
           Spacer(1, 4 * mm)]
    m = float(data["montant"])
    amt = Table([[[Paragraph(money(m).replace(" $", "$") + " + taxes applicables", S["amt"]), Paragraph(esc(en_lettres(m)), S["amtw"])]]], colWidths=[W])
    amt.setStyle(TableStyle([("LINEABOVE", (0, 0), (-1, 0), .8, P["brand"]), ("LINEBELOW", (0, 0), (-1, 0), .8, P["brand"]),
                             ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    el += [amt, Spacer(1, 4 * mm)]
    for title, key in [("Soumission selon les documents suivants :", "documents"), ("Inclusions prévues dans la soumission :", "inclusions"), ("Exclusions :", "exclusions")]:
        if data.get(key):
            el += [Paragraph(title, S["h4"]), bullets(data[key], S), Spacer(1, 3 * mm)]
    el += [Spacer(1, 2 * mm), Paragraph("En espérant le tout à votre entière satisfaction, nous vous prions d'agréer l'expression de nos meilleurs sentiments.", S["base"]),
           Spacer(1, 12 * mm)]
    sg = signer_for(data, brand_key, brand)
    sig = Table([[[Paragraph(esc(sg[0]), S["sig"])] + [Paragraph(esc(x), S["base"]) for x in sg[1:]],
                  Paragraph(f"<i>{esc(data.get('validite', 'Période de validité : 30 jours'))}</i>", ParagraphStyle("v", parent=S["base"], alignment=TA_RIGHT))]],
                colWidths=[W * .6, W * .4])
    sig.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "BOTTOM"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0)]))
    el += [sig]
    doc.build(el)


def generate(brand_key, data, out, brands=None):
    brands = brands or load_brands()
    if brand_key not in brands:
        raise SystemExit(f"Marque inconnue '{brand_key}'. Disponibles : {', '.join(brands)}")
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    (build_lettre if data.get("type") == "lettre" else build_soumission)(data, brands[brand_key], out, brand_key)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--brand", help="clé dans brands.json (dr | sip | br | ...)")
    ap.add_argument("--all", action="store_true", help="génère une PDF par marque")
    ap.add_argument("--data", required=True)
    ap.add_argument("--out")
    ap.add_argument("--outdir", default="out")
    a = ap.parse_args()
    data = json.load(open(a.data, encoding="utf-8"))
    brands = load_brands()
    stem = Path(a.data).stem
    if a.all:
        if not isinstance(data.get("signer"), dict):
            print("Avertissement : `signer` n'est pas un dict par marque — les PDF des autres marques auront un signataire placeholder.")
        for k in brands:
            print("->", generate(k, data, os.path.join(a.outdir, f"{stem}_{k}.pdf"), brands))
    else:
        if not a.brand:
            raise SystemExit("--brand requis (ou --all)")
        print("->", generate(a.brand, data, a.out or os.path.join(a.outdir, f"{stem}_{a.brand}.pdf"), brands))

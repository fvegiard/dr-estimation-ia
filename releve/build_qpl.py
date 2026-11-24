# /// script
# requires-python = ">=3.12"
# dependencies = ["pillow>=10"]
# ///
"""Étape 3 (déterministe) : occurrences + nomenclature → projet Plan Expert (.qpl) + rasters à côté.

Usage : uv run releve/build_qpl.py WORKDIR NOM_PROJET SORTIE_DIR
Produit SORTIE_DIR/<NOM_PROJET>.qpl et copie les rasters <feuille>.png à côté (Plan Expert les référence en relatif).
Format XML observé sur les fichiers natifs Plan Expert 3.0.17 (voir HANDOFF §3b, REPRODUCTION.md §2) :
  <Counter Name GroupID Shape DefaultSize Text Color PenWidth PenType FillColor ShowMeasure Visible> + <Element X Y Width Height/>
  Couleurs = ARGB signé 32 bits ; pixels = points PDF × largeur_raster / largeur_page_pt ; Element X,Y = coin haut-gauche.
"""
import os, sys, shutil, uuid, json, datetime, collections
from pathlib import Path
from xml.sax.saxutils import escape
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from commun import load_nomenclature, load_occurrences, load_feuilles, argb, sha256
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

def q(s):  # attribut XML
    return escape(str(s), {'"': "&quot;"})

def canoniser(nom, occ):
    """Opt-in (RELEVE_LIBELLES_CANONIQUES=1): rename labels to the canonical Plan Expert labels learnt from
    the 2021-2026 corpus (src/qpl/normalisation.py) and drop noise labels. Lossy (PRISE GFI -> PRISE):
    off by default so the estimator keeps the detailed label unless asked."""
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.qpl.normalisation import canonique, nettoyer
    def c(label):  # None = noise; unchanged if only case/accents/spaces differ; else the canonical label
        k = canonique(label)
        return label if k is not None and k == nettoyer(label) else k
    nom2 = {}
    for label, v in nom.items():
        k = c(label)
        if k is not None:
            nom2.setdefault(k, v)
    occ2 = [dict(o, label=c(o["label"])) for o in occ if c(o["label"]) is not None]
    return nom2, occ2

def main(work, name, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    nom = load_nomenclature(work); occ = load_occurrences(work); feuilles = load_feuilles(work)
    if os.environ.get("RELEVE_LIBELLES_CANONIQUES") == "1":
        nom, occ = canoniser(nom, occ)
    labels = sorted({o["label"] for o in occ})
    unknown = [l for l in labels if l not in nom]
    if unknown:
        sys.exit("labels absents de nomenclature.csv : " + ", ".join(unknown))
    gid = {l: i + 1 for i, l in enumerate(labels)}
    by_sheet = collections.defaultdict(lambda: collections.defaultdict(list))
    for o in occ:
        by_sheet[o["feuille"]][o["label"]].append(o)
    order = sorted(feuilles, key=lambda f: (feuilles[f].get("type") != "plan", f))
    inv = Path(work) / "inventaire.json"
    ident = ":".join(sorted(e["sha256"] for e in json.loads(inv.read_text(encoding="utf-8"))["fichiers"])) if inv.is_file() else name
    # La date de génération est configurable pour un rejeu octet à octet.
    today = datetime.date.fromisoformat(os.environ["RELEVE_DATE"]) if os.environ.get("RELEVE_DATE") else datetime.date.today()
    longueurs = Path(work) / "metre-longueurs.json"
    lignes = collections.defaultdict(list)
    if longueurs.is_file():
        for r in json.loads(longueurs.read_text(encoding="utf-8"))["lignes"]:
            if r["feuille"] not in feuilles:
                raise ValueError(f"Métré : feuille {r['feuille']} introuvable")
            lignes[r["feuille"]].append(r)
    prochain_gid = len(gid) + 1
    L = ['﻿<?xml version="1.0"?>', "<QuoterPlanSession>", f'\t<Project Name="{q(name)}">', "\t\t<Description/>", "\t\t<ContactName/>",
         "\t\t<ContactInfo/>", "\t\t<JobNumber/>", "\t\t<Comment/>",
         f"\t\t<CreationDate>{today.year}/{today.month}/{today.day}</CreationDate>", f"\t\t<LastModified>{today.year}/{today.month}/{today.day}</LastModified>",
         "\t\t<DisplayResultsForAllPlans>True</DisplayResultsForAllPlans>", "\t</Project>", "\t<Workspace>"]
    marked = [f for f in order if by_sheet.get(f)]
    L.append(f'\t\t<ActivePlan Name="{q(feuilles[marked[0] if marked else order[0]]["nom"])}"/>')
    L.append("\t\t<RecentPlans>")
    for f in marked[:10]:
        L.append(f'\t\t\t<Plan Name="{q(feuilles[f]["nom"])}"/>')
    L += ["\t\t</RecentPlans>", "\t</Workspace>", "\t<Plans>"]
    stats = {}
    missing_rasters = [f for f in order if (by_sheet.get(f) or lignes.get(f)) and not os.path.exists(os.path.join(work, "rasters", f + ".png"))]
    if missing_rasters:
        sys.exit("rasters absents pour feuilles marquées : " + ", ".join(missing_rasters))
    for f in order:
        info = feuilles[f]
        src = os.path.join(work, "rasters", f + ".png")
        if not os.path.exists(src):
            continue
        dst = os.path.join(out_dir, f + ".png")
        with Image.open(src) as im:
            rw, rh = im.size
            if lignes[f]:
                dpi = rw * 72 / float(info["largeur_pt"])
                im.save(dst, dpi=(dpi, dpi))
            else:
                shutil.copy2(src, dst)
        W = float(info["largeur_pt"]); k = rw / W
        ech = str(lignes[f][0]["echelle"]) if lignes[f] else info.get("echelle", "")
        scale = f'<Scale Value="{int(ech)}" Type="0" Precision="2" SetManually="False" Engineering="False"/>' if ech.isdigit() else '<Scale Value="0" Type="1" Precision="0" SetManually="False" Engineering="False"/>'
        vignette = uuid.uuid5(uuid.NAMESPACE_URL, f"dr-estimation/{name}/{ident}/{f}")
        L += [f'\t\t<Plan Name="{q(info["nom"])}" FileName="{q(f)}.png">', f'\t\t\t<Thumbnail FileName="{vignette}"/>', "\t\t\t" + scale,
              "\t\t\t<Bookmarks>", '\t\t\t\t<Bookmark Name="Default" LayerIndex="0" Zoom="10" X="0" Y="0"/>', "\t\t\t</Bookmarks>", "\t\t\t<Comment/>",
              "\t\t\t<Layers>", '\t\t\t\t<Layer Index="0" Name="Releve automatique" Opacity="150" Visible="True" Active="True">']
        lx, ly = (int(rw * 0.746), int(rh * 0.336)) if by_sheet.get(f) else (100, 100)
        L.append(f'\t\t\t\t\t<Legend Name="Légende" X="{lx}" Y="{ly}" FontSize="45" MaxRows="25" Color="-657931" PenWidth="6" PenType="Generic" FillColor="-657931" ShowMeasure="True" Visible="True"/>&#13;')
        for label in sorted(by_sheet.get(f, {})):
            n = nom[label]; col = argb(n["rgb"]); size = n["taille"]
            L.append(f'\t\t\t\t\t<Counter Name="{q(label)}" GroupID="{gid[label]}" Shape="{n["forme"]}" DefaultSize="{size}" Text="1" Color="{col}" PenWidth="2" PenType="Generic" FillColor="{col}" ShowMeasure="True" Visible="True">&#13;')
            for o in by_sheet[f][label]:
                x = int(round(o["x"] * k - size / 2)); y = int(round(o["y"] * k - size / 2))
                L.append(f'\t\t\t\t\t\t<Element X="{x}" Y="{y}" Width="{size}" Height="{size}"/>&#13;')
                stats.setdefault(f, collections.Counter())[label] += 1
            L.append("\t\t\t\t\t</Counter>&#13;")
        for r in lignes[f]:
            nom_ligne = f"{r['famille']} — {r['id']} ({r['longueur_m']:.2f} m tracés, partiel)"
            L.append(f'\t\t\t\t\t<Line Name="{q(nom_ligne)}" GroupID="{prochain_gid}" Color="-29696" PenWidth="4" PenType="Generic" ShowMeasure="False" Visible="True">')
            prochain_gid += 1
            pixels = [(round(x * k), round(y * k)) for x, y in r["points_pt"]]
            for (x1, y1), (x2, y2) in zip(pixels, pixels[1:]):
                L.append(f'\t\t\t\t\t\t<Element X1="{x1}" Y1="{y1}" X2="{x2}" Y2="{y2}"/>')
            L.append("\t\t\t\t\t</Line>")
        L += ["\t\t\t\t</Layer>", "\t\t\t</Layers>", "\t\t</Plan>"]
    L += ["\t</Plans>", "\t<Prices>"]
    for label in labels:
        L.append(f'\t\t<Price Key="{gid[label]};;Counter;" CostEach="0" MarkupEach="0" SystemType="2"/>')
    L += ["\t</Prices>", "\t<Reports>", '\t\t<Report Name="Default" Order="1" ScaleType="1" Precision="0">']
    for p in ("ShowProjectInfo", "ShowComments", "ShowInvisibleObjects", "ApplyFilter", "EstimatingShowProjectInfo", "EstimatingShowComments",
              "EstimatingShowInvisibleObjects", "EstimatingApplyFilter", "QuoteShowProjectInfo", "QuoteShowComments", "QuoteShowInvisibleObjects", "QuoteApplyFilter"):
        L.append(f'\t\t\t<Property Name="{p}" Value="True"/>')
    L += ['\t\t\t<Property Name="OrderByObjectsFilter" Value=""/>', '\t\t\t<Property Name="OrderByPlansFilter" Value=""/>',
          '\t\t\t<Property Name="ReportSortBy" Value="0"/>', '\t\t\t<Property Name="QuoteReportSortBy" Value="0"/>', "\t\t</Report>", "\t</Reports>", "</QuoterPlanSession>", ""]
    out = os.path.join(out_dir, name + ".qpl")
    with open(out, "w", encoding="utf-8", newline="\r\n") as fh:
        fh.write("\n".join(L))
    total = sum(sum(c.values()) for c in stats.values())
    audit = {"qpl": out, "sha256": sha256(out), "octets": os.path.getsize(out), "plans": len(order), "compteurs": sum(len(c) for c in stats.values()),
             "marques": total, "libelles": len(labels), "par_feuille": {f: dict(c) for f, c in stats.items()},
             "traces_metres": prochain_gid - len(gid) - 1}
    json.dump(audit, open(out + ".audit.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"{out} : {len(order)} plans, {audit['compteurs']} compteurs, {total} marques, {len(labels)} libellés, sha256 {audit['sha256']}")

if __name__ == "__main__":
    main(*sys.argv[1:4])

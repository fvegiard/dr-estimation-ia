"""Lien humain ↔ plan : relier LE DOCUMENT REÇU à CE QUE L'ESTIMATEUR EN A FAIT dans Plan Expert.

Deux choses distinctes :
  1. le document reçu  — le PDF des plans du client (« 01-PLANS.pdf », « Document d'appel d'offres_Addenda 1 »…) ;
  2. ce qu'on en fait  — le projet Plan Expert (.qpl) : Plan Expert rastérise chaque page du PDF en PNG
     « <document> - <page>.png » à côté du .qpl, et l'estimateur y clique une marque par appareil compté
     (Counter = libellé, Element = X, Y en pixels de ce PNG, coin haut-gauche).

Le nom du PNG redonne donc (document reçu, page) et la marque redonne (libellé, position) : on découpe exactement
ce que l'humain voyait quand il a compté. C'est ce que le LLM doit reproduire sur un document neuf.

Sorties (--sortie, défaut apprentissage/lien-humain) :
  connaissance.json   par libellé canonique : occurrences, projets, variantes, catégorie, marque Plan Expert
                      (forme/couleur/taille), voisins habituels, exemples (projet, document, page, x, y)
  documents.json      par projet : documents reçus → pages marquées / pages ignorées, marques par page
  galerie/<slug>.jpg  planche de 8 découpes max (projets différents), anneau rouge = point cliqué par l'humain
  PRATIQUES.md        résumé lisible (servi au LLM par le serveur MCP : estimateur://pratiques-humaines)

Sources — les deux liens publics, lus directement en ligne (ni Z:, ni G:, ni synchro) :
  * OneDrive « Mes projets » (Daniel Dupuis) : ce qu'on fait dans Plan Expert (.qpl + PNG des pages).
    Seuls les .qpl sont copiés (cache) ; chaque page PNG utile à une découpe est téléchargée puis effacée.
  * Google Drive « original » : les documents reçus, reliés au projet par le numéro S-xxxx → recus.json.

    python -m src.apprentissage.lien_humain                     # les deux liens publics (défaut)
    python -m src.apprentissage.lien_humain --no-onedrive --racine <dossier .qpl+PNG>   # essai hors ligne
"""
from __future__ import annotations

import argparse
import json
import math
import os
import random
import re
import unicodedata
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
APPR = RACINE / "apprentissage" / "qpl-2021-2026"
COTE = 144
PAR_LIBELLE = 8
MIN_PROJETS = 2
MIN_PROJETS_GALERIE = 4
PNG_RE = re.compile(r"^(?P<doc>.+?) - (?P<page>\d+)(?: \(\d+\))?(?: - Copie(?: \(\d+\))?)?\.png$", re.I)


def cle(texte: str) -> str:
    t = unicodedata.normalize("NFKD", texte or "").encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", t).strip().upper()


def slug(texte: str) -> str:
    return re.sub(r"[^A-Z0-9]+", "-", cle(texte)).strip("-")[:60] or "SANS-NOM"


def document_page(nom_png: str) -> tuple[str, int]:
    """« 01-PLANS - 14 (3).png » → (« 01-PLANS », 14) : le document reçu et sa page."""
    m = PNG_RE.match(nom_png)
    return (m.group("doc"), int(m.group("page"))) if m else (Path(nom_png).stem, 0)


class Canon:
    """Libellé brut → libellé canonique (normalisation.json + dictionnaire-symboles.json)."""

    def __init__(self, appr: Path = APPR):
        norm = json.loads((appr / "normalisation.json").read_text(encoding="utf-8")) \
            if (appr / "normalisation.json").exists() else {}
        self.fusion = {cle(k): cle(v) for k, v in norm.get("fusion", {}).items()}
        self.rebut = {cle(x) for x in norm.get("rebut", [])}
        self.dico = {}
        dico = appr / "dictionnaire-symboles.json"
        for s in (json.loads(dico.read_text(encoding="utf-8"))["symboles"] if dico.exists() else []):
            self.dico[cle(s["label"])] = s
            for v in s.get("variantes", []):
                self.fusion.setdefault(cle(v), cle(s["label"]))

    def __call__(self, brut: str) -> str | None:
        k = cle(brut)
        if not k or k in self.rebut:
            return None
        vus = set()
        while k in self.fusion and k not in vus:
            vus.add(k)
            k = self.fusion[k]
        return k


def lire_qpl(p: Path):
    b = p.read_bytes()
    for enc in ("utf-8-sig", "utf-16", "latin-1"):
        try:
            return ET.fromstring(b.decode(enc).lstrip("\ufeff").encode("utf-8"))
        except (UnicodeDecodeError, ET.ParseError):
            continue
    return None


def couleur(argb) -> str:
    try:
        return f"#{int(argb) & 0xFFFFFF:06X}"
    except (TypeError, ValueError):
        return ""


def _racines(racine) -> list[Path]:
    return [Path(r) for r in racine] if isinstance(racine, (list, tuple)) else [Path(racine)]


def projets_uniques(racine) -> list[Path]:
    """Un .qpl par dossier de projet : on écarte les « - Copie » quand l'original existe.
    Plusieurs racines possibles (Z:, copie Drive de « Mes projets »…) : un même nom de dossier n'est lu qu'une fois."""
    par_dossier = defaultdict(list)
    vus = {}
    for r in _racines(racine):
        for q in r.rglob("*.qpl"):
            if vus.setdefault(q.parent.name, q.parent) == q.parent:
                par_dossier[q.parent].append(q)
    out = []
    for qs in par_dossier.values():
        vrais = [q for q in qs if "copie" not in q.stem.lower()] or qs
        out.append(max(vrais, key=lambda q: q.stat().st_mtime))
    return sorted(out)


def collecter(racine, canon: Canon, journal=print, distants: dict | None = None):
    """Toutes les marques dont la page PNG est présente à côté du .qpl (sur disque ou en ligne),
    + le bilan document reçu → pages."""
    distants = distants or {}
    marques = []   # (canon, brut, projet, png, x, y, taille)
    formes, couleurs = defaultdict(Counter), defaultdict(Counter)
    documents = {}
    qpls = projets_uniques(racine)
    for i, q in enumerate(qpls, 1):
        r = lire_qpl(q)
        if r is None:
            continue
        projet = q.parent.name
        docs = defaultdict(lambda: {"pages_marquees": {}, "pages_sans_marque": []})
        for plan in r.findall("./Plans/Plan"):
            nom_png = plan.get("FileName") or ""
            doc, page = document_page(nom_png)
            png = q.parent / nom_png
            elements = [(c, e) for c in plan.iter("Counter") for e in c.findall("Element")]
            if not elements:
                docs[doc]["pages_sans_marque"].append(page)
                continue
            docs[doc]["pages_marquees"][str(page)] = len(elements)
            if not (png.is_file() or png in distants):
                continue
            for c, e in elements:
                k = canon(c.get("Name", ""))
                if not k:
                    continue
                try:
                    t = float(e.get("Width") or c.get("DefaultSize") or 38)
                    h = float(e.get("Height") or t)
                    # Plan Expert stocke le coin haut-gauche de la marque : le symbole est au centre
                    x, y = float(e.get("X")) + t / 2, float(e.get("Y")) + h / 2
                except (TypeError, ValueError):
                    continue
                marques.append((k, cle(c.get("Name", "")), projet, png, x, y, t))
                formes[k][c.get("Shape", "")] += 1
                couleurs[k][couleur(c.get("Color"))] += 1
        for d in docs.values():
            d["pages_sans_marque"].sort()
        documents[projet] = dict(docs)
        if i % 50 == 0:
            journal(f"  {i}/{len(qpls)} projets, {len(marques)} marques")
    return marques, formes, couleurs, documents


def voisins(marques, rayon_facteur=3.0):
    """Libellés comptés juste à côté (≤ 3 tailles de marque) : habitudes de l'estimateur."""
    par_page = defaultdict(list)
    for m in marques:
        par_page[m[3]].append(m)
    v = defaultdict(Counter)
    for pts in par_page.values():
        pts.sort(key=lambda m: m[4])
        for i, a in enumerate(pts):
            r = rayon_facteur * a[6]
            for b in pts[i + 1:]:
                if b[4] - a[4] > r:
                    break
                if b[0] != a[0] and abs(b[5] - a[5]) <= r:
                    v[a[0]][b[0]] += 1
                    v[b[0]][a[0]] += 1
    return v


def choisir_exemples(marques_label, n, alea):
    """n exemples de projets différents (puis d'autres marques si pas assez de projets)."""
    par_projet = defaultdict(list)
    for m in marques_label:
        par_projet[m[2]].append(m)
    projets = sorted(par_projet)
    alea.shuffle(projets)
    choix = [alea.choice(par_projet[p]) for p in projets[:n]]
    if len(choix) < n:
        reste = [m for m in marques_label if m not in choix]
        alea.shuffle(reste)
        choix += reste[: n - len(choix)]
    return choix


def decouper(png: Path, pts):
    from PIL import Image, ImageDraw

    Image.MAX_IMAGE_PIXELS = None
    out = {}
    with Image.open(png) as im:
        im = im.convert("RGB")
        for (x, y, t, cle_ex) in pts:
            demi = max(60, 3 * t)
            tuile = im.crop((int(x - demi), int(y - demi), int(x + demi), int(y + demi))).resize((COTE, COTE))
            d = ImageDraw.Draw(tuile)
            r = max(6, t / 2 * COTE / (2 * demi) + 3)
            c = COTE / 2
            d.ellipse((c - r, c - r, c + r, c + r), outline=(230, 0, 0), width=2)
            out[cle_ex] = tuile
    return out


def planche(tuiles, titre):
    from PIL import Image, ImageDraw

    cols = 4
    lignes = max(1, math.ceil(len(tuiles) / cols))
    m = Image.new("RGB", (cols * (COTE + 4), 22 + lignes * (COTE + 18)), "white")
    d = ImageDraw.Draw(m)
    d.text((4, 4), titre[:90], fill=(0, 0, 0))
    for i, (legende, t) in enumerate(tuiles):
        x, y = (i % cols) * (COTE + 4), 22 + (i // cols) * (COTE + 18)
        m.paste(t, (x, y))
        d.text((x + 2, y + COTE + 2), legende[:30], fill=(90, 90, 90))
    return m


def construire(racine, sortie: Path, par_libelle=PAR_LIBELLE, min_projets=MIN_PROJETS, fils=6,
               appr: Path = APPR, journal=print, galerie_min=MIN_PROJETS_GALERIE, distants: dict | None = None,
               telecharger=None):
    """`distants` : {chemin local attendu du PNG : ref distante} ; `telecharger(ref, dest)` rapatrie une page
    dans un fichier temporaire, effacé dès la découpe faite."""
    canon = Canon(appr)
    distants = distants or {}
    journal(f"lecture des .qpl sous {racine}")
    marques, formes, couleurs, documents = collecter(racine, canon, journal, distants)
    journal(f"{len(marques)} marques avec image, {len(documents)} projets")
    par_label = defaultdict(list)
    for m in marques:
        par_label[m[0]].append(m)
    retenus = {k: v for k, v in par_label.items() if len({m[2] for m in v}) >= min_projets}
    vois = voisins(marques)
    alea = random.Random(2026)
    exemples = {k: choisir_exemples(v, par_libelle, alea) for k, v in sorted(retenus.items())}

    a_couper = defaultdict(list)
    for k, ex in exemples.items():
        if len({m[2] for m in par_label[k]}) < galerie_min:
            continue
        for j, m in enumerate(ex):
            a_couper[m[3]].append((m[4], m[5], m[6], (k, j)))
    journal(f"{len(retenus)} libellés (≥ {min_projets} projets), {sum(map(len, a_couper.values()))} découpes "
            f"dans {len(a_couper)} pages")
    tuiles = {}

    def tache(item):
        png, pts = item
        tmp = None
        try:
            if not png.is_file() and png in distants:
                import tempfile
                fd, nom = tempfile.mkstemp(suffix=".png")
                os.close(fd)
                tmp = Path(nom)
                telecharger(distants[png], tmp)
            return decouper(tmp or png, pts)
        except Exception as e:  # page illisible : on garde les autres
            journal(f"  page illisible {png.name} : {e}")
            return {}
        finally:
            if tmp is not None:
                tmp.unlink(missing_ok=True)

    with ThreadPoolExecutor(fils) as ex:
        for i, res in enumerate(ex.map(tache, a_couper.items()), 1):
            tuiles.update(res)
            if i % 100 == 0:
                journal(f"  {i}/{len(a_couper)} pages découpées")

    (sortie / "galerie").mkdir(parents=True, exist_ok=True)
    connaissance = {}
    for k, ex in exemples.items():
        v = par_label[k]
        projets = {m[2] for m in v}
        d = canon.dico.get(k, {})
        tu = [(m[2][:28], tuiles[(k, j)]) for j, m in enumerate(ex) if (k, j) in tuiles]
        fichier = f"galerie/{slug(k)}.jpg"
        if tu:
            planche(tu, f"{k} - {len(v)} marques / {len(projets)} projets").save(sortie / fichier, quality=70)
        tailles = sorted(m[6] for m in v)
        connaissance[k] = {
            "libelle": k,
            "categorie": d.get("categorie", ""),
            "sous_type": d.get("sous_type", ""),
            "occurrences": len(v),
            "projets": len(projets),
            "variantes": [b for b, _ in Counter(m[1] for m in v).most_common(12)],
            "marque_planexpert": {"forme": formes[k].most_common(1)[0][0], "couleur": couleurs[k].most_common(1)[0][0],
                                  "taille_px_mediane": tailles[len(tailles) // 2]},
            "voisins": [{"libelle": n, "fois": c} for n, c in vois[k].most_common(6)],
            "galerie": fichier if tu else "",
            "exemples": [dict(zip(("projet", "document", "page"), (m[2], *document_page(m[3].name))), x=m[4], y=m[5])
                         for m in ex],
        }
    (sortie / "connaissance.json").write_text(json.dumps({
        "source": [str(r) for r in _racines(racine)], "marques": len(marques), "projets": len(documents), "libelles": len(connaissance),
        "note": "document = PDF reçu, page = sa page ; x, y en pixels du PNG Plan Expert de cette page "
                "(coin haut-gauche) ; galerie : anneau rouge = clic de l'estimateur",
        "symboles": sorted(connaissance.values(), key=lambda s: -s["occurrences"])}, ensure_ascii=False, indent=1),
        encoding="utf-8")
    (sortie / "documents.json").write_text(json.dumps(documents, ensure_ascii=False, indent=1), encoding="utf-8")
    (sortie / "PRATIQUES.md").write_text(pratiques_md(connaissance, documents, len(marques), min_projets),
                                         encoding="utf-8")
    journal(f"écrit {sortie}")
    return connaissance


def pratiques_md(conn: dict, documents: dict, n_marques: int, min_projets: int = MIN_PROJETS) -> str:
    pages_m = sum(len(d["pages_marquees"]) for p in documents.values() for d in p.values())
    pages_v = sum(len(d["pages_sans_marque"]) for p in documents.values() for d in p.values())
    par_cat = defaultdict(list)
    for s in conn.values():
        par_cat[s["categorie"] or "non classe"].append(s)
    lignes = ["# Pratiques des estimateurs DR Électrique (projets Plan Expert réels)", "",
              "Deux choses à ne pas confondre : **le document reçu** (PDF des plans du client) et **ce que "
              "l'estimateur en fait dans Plan Expert** (une marque par appareil, posée sur la page de ce PDF).", "",
              f"{len(documents)} projets, {n_marques} marques relues sur les pages mêmes où l'estimateur a cliqué. "
              f"Pages de documents reçus marquées : {pages_m} ; pages reçues sans aucune marque (devis, détails, "
              f"autres disciplines) : {pages_v}. {len(conn)} libellés présents dans au moins {min_projets} projets.", "",
              "Utilisation : nommer chaque article de nomenclature avec le libellé canonique ci-dessous, appeler "
              "`exemples_humains(libelle)` pour voir comment l'humain l'a repéré sur de vrais plans, et vérifier "
              "les « voisins » (ce que l'humain compte habituellement juste à côté).", ""]
    for cat in sorted(par_cat, key=lambda c: -sum(s["occurrences"] for s in par_cat[c])):
        lignes += [f"## {cat}", "", "| Libellé | Marques | Projets | Variantes | Voisins habituels |",
                   "|---|---|---|---|---|"]
        for s in sorted(par_cat[cat], key=lambda s: -s["occurrences"])[:60]:
            var = ", ".join(v for v in s["variantes"][:4] if v != s["libelle"])
            voi = ", ".join(v["libelle"] for v in s["voisins"][:3])
            lignes.append(f"| {s['libelle']} | {s['occurrences']} | {s['projets']} | {var} | {voi} |")
        lignes.append("")
    return "\n".join(lignes)


NUM_RE = re.compile(r"(?<![A-Za-z0-9])[sS]\s?-?\s?(\d{3,5})(?!\d)")
EXT_RECUS = {".pdf", ".jpg", ".jpeg", ".png", ".tif", ".tiff", ".docx", ".doc", ".xlsx", ".xls", ".dwg", ".zip"}


def numero(nom: str) -> str | None:
    m = NUM_RE.search(nom)
    return str(int(m.group(1))) if m else None


def lier_recus(documents: dict, drive, racine_id: str, journal=print) -> dict:
    """Relie chaque projet Plan Expert (OneDrive) au dossier des documents reçus (Google Drive, lu en ligne) par
    son numéro S-xxxx, puis chaque document du .qpl au fichier reçu qui porte le même nom."""
    import difflib

    par_num = defaultdict(list)
    for d in drive.lister(racine_id):
        if d["dossier"] and (n := numero(d["nom"])):
            par_num[n].append(d)
    lien = {}
    for projet, docs in sorted(documents.items()):
        n = numero(projet)
        if not n or n not in par_num:
            continue
        fichiers = []
        for d in par_num[n]:
            try:
                fichiers += [{**f, "chemin": f"{d['nom']}/{f['chemin']}"} for f in drive.fichiers(d["id"])]
            except Exception as e:  # noqa: BLE001
                journal(f"  Drive {d['nom']} illisible : {e}")
        fichiers = [f for f in fichiers if Path(f["nom"]).suffix.lower() in EXT_RECUS]
        cles = {cle(Path(f["nom"]).stem): f for f in fichiers}
        corr = {}
        for doc in docs:
            k = cle(doc)
            f = cles.get(k) or next((v for c, v in cles.items() if k and (k in c or c in k)), None)
            if f is None and cles:
                m = difflib.get_close_matches(k, list(cles), n=1, cutoff=0.6)
                f = cles[m[0]] if m else None
            corr[doc] = {"fichier": f["chemin"], "url": f["url"]} if f else None
        lien[projet] = {"dossiers_recus": [{"nom": d["nom"], "url": d["url"]} for d in par_num[n]],
                        "fichiers_recus": sorted(f["chemin"] for f in fichiers),
                        "document_qpl_vers_recu": corr}
    journal(f"documents reçus (Google Drive) reliés : {len(lien)} projets / {len(documents)}, "
            f"{sum(v is not None for p in lien.values() for v in p['document_qpl_vers_recu'].values())} documents")
    return lien


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m src.apprentissage.lien_humain", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--onedrive", action=argparse.BooleanOptionalAction, default=True,
                    help="lire « Mes projets » (qpl + pages PNG) par le lien public OneDrive (défaut : oui)")
    ap.add_argument("--cache-qpl", type=Path, default=Path(os.environ.get("TEMP", "/tmp")) / "dr-mes-projets-qpl",
                    help="où garder les seuls .qpl (≈ 90 Mo) ; les PNG ne sont jamais copiés en entier")
    ap.add_argument("--racine", type=Path, nargs="*", default=[],
                    help="dossiers supplémentaires de projets Plan Expert (.qpl + PNG), facultatif")
    ap.add_argument("--drive", default=os.environ.get("DR_DRIVE_RECUS", "13JWszeHOEIM41Gf6GnNO0o4sOtWZHOW7"),
                    help="identifiant du dossier Google Drive public des documents reçus (« original ») ; "
                         "vide = ne pas relier")
    ap.add_argument("--sortie", type=Path, default=RACINE / "apprentissage" / "lien-humain")
    ap.add_argument("--par-libelle", type=int, default=PAR_LIBELLE)
    ap.add_argument("--min-projets", type=int, default=MIN_PROJETS)
    ap.add_argument("--fils", type=int, default=6)
    a = ap.parse_args(argv)
    journal = lambda s: print(s, flush=True)  # noqa: E731
    racines, distants, telecharger = list(a.racine), {}, None
    if a.onedrive:
        from src.apprentissage.sharepoint import MesProjets, miroir_qpl

        mp = MesProjets()
        distants = miroir_qpl(a.cache_qpl, a.fils, journal, mp)
        racines.insert(0, a.cache_qpl)
        telecharger = lambda ref, dest: mp.telecharger(ref[0], dest, -1)  # noqa: E731
    construire(racines, a.sortie, a.par_libelle, a.min_projets, a.fils, journal=journal, distants=distants,
               telecharger=telecharger)
    if a.drive:
        from src.apprentissage.gdrive import DossierDrive

        documents = json.loads((a.sortie / "documents.json").read_text(encoding="utf-8"))
        lien = lier_recus(documents, DossierDrive(), a.drive, journal)
        (a.sortie / "recus.json").write_text(json.dumps(lien, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

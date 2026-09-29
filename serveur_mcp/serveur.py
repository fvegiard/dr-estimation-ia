"""Serveur MCP « Expert estimateur » (Groupe DR Électrique).

N'importe quel LLM compatible MCP (Claude, GPT, Gemini, modèle local…) se branche ici et fait le relevé de quantités
électrique d'un plan PDF brut, sans Plan Expert ni machine virtuelle :

  deposer_fichier / preparer_dossier  → pages, tuiles, mots (releve/prepare.py)
  voir_image / zoomer / nature_traits → le LLM lit la légende et les plans (jugement visuel)
  ecrire_fichier                      → classement, nomenclature, occurrences, réserves (méthode : ressource
                                        estimateur://methode, gabarit : prompt releve_planexpert)
  extraire_occurrences / verifier_releve
  produire_livrables                  → <S>-RELEVE.pdf au format de l'exemplaire HR26-14 (pastilles, encadré
                                        « RELEVE <feuille> - MATERIEL », bordereau 8 colonnes, réserves) + projet
                                        Plan Expert .qpl + rapport de métré
  comparer_estimateur                 → écart marque par marque avec le projet de l'estimateur

Lancement :
  python -m serveur_mcp                                   # stdio (client local)
  python -m serveur_mcp --transport http --port 8765      # Streamable HTTP sur /mcp (nuage)
Variables : ESTIMATEUR_BASE (dossiers de travail, défaut <dépôt>/travail-mcp), ESTIMATEUR_MCP_CLE (clé Bearer,
obligatoire dès que l'hôte n'est pas local).
"""
from __future__ import annotations

import argparse
import base64
import csv
import hmac
import io
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

from mcp.server import MCPServer
from mcp.server.mcpserver import Image
from mcp.server.mcpserver.exceptions import ToolError

RACINE = Path(__file__).resolve().parents[1]
RELEVE = RACINE / "releve"
METHODE = RACINE / ".claude" / "skills" / "releve-planexpert" / "SKILL.md"
STANDARD = RACINE / "apprentissage" / "hr26-14-exemplaire" / "STANDARD-RELEVE.md"
LIBELLES = RACINE / "apprentissage" / "qpl-2021-2026" / "dictionnaire-symboles.json"
NOM_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
FEUILLE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
ECRITURE_PERMISE = {
    "feuilles-classement.csv", "nomenclature.csv", "occurrences-texte.csv", "occurrences-visuel.csv",
    "reserves.md", "rapport-releve.md", "comparaison-estimateur.md",
}
TAILLE_MAX_DEPOT = 200 * 1024 * 1024
TAILLE_MAX_LIVRABLE = 25 * 1024 * 1024
MORCEAU = 60_000

INSTRUCTIONS = """Tu es l'expert estimateur électrique du Groupe DR Électrique. Tu fais le relevé de quantités d'un
dossier de plans PDF brut et tu livres le PDF annoté au format de l'exemplaire HR26-14.
Déroulement : deposer_fichier (ou preparer_dossier avec chemin_source) → preparer_dossier → lire la ressource
estimateur://methode et l'appliquer (voir_image des aperçus/tuiles, zoomer, ecrire_fichier) → extraire_occurrences →
verifier_releve jusqu'à « pret »: true → produire_livrables → voir_image du rendu pour te contrôler toi-même →
comparer_estimateur si une référence existe. Rien n'est inventé : chaque quantité vient d'un symbole vu, d'une
étiquette, d'une cédule ou d'une note ; le doute va dans reserves.md."""

mcp = MCPServer("expert-estimateur", instructions=INSTRUCTIONS, version="0.1.0")


# ---------------------------------------------------------------- chemins
def base() -> Path:
    b = Path(os.environ.get("ESTIMATEUR_BASE") or RACINE / "travail-mcp").resolve()
    b.mkdir(parents=True, exist_ok=True)
    return b


def dossier_de(nom: str, creer: bool = False) -> Path:
    if not NOM_RE.match(nom or ""):
        raise ToolError(f"nom de dossier invalide : {nom!r} (lettres, chiffres, . _ -)")
    d = base() / nom
    if creer:
        for s in ("entree", "travail", "sortie", "reference"):
            (d / s).mkdir(parents=True, exist_ok=True)
    elif not d.is_dir():
        raise ToolError(f"dossier inconnu : {nom} (utiliser deposer_fichier ou preparer_dossier)")
    return d


def sous_chemin(racine: Path, relatif: str) -> Path:
    p = (racine / relatif).resolve()
    if p != racine.resolve() and racine.resolve() not in p.parents:
        raise ToolError(f"chemin hors du dossier : {relatif}")
    return p


def lancer(script: str, *args: str, delai: int = 1800) -> str:
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    r = subprocess.run([sys.executable, str(RELEVE / script), *args], cwd=RACINE, env=env,
                           stdin=subprocess.DEVNULL, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=delai)
    sortie = (r.stdout + ("\n" + r.stderr if r.stderr.strip() else "")).strip()
    if r.returncode != 0:
        raise ToolError(f"{script} a échoué (code {r.returncode}) :\n{sortie[-4000:]}")
    return sortie[-4000:]


def lire_csv(p: Path) -> list[dict]:
    if not p.exists():
        return []
    with open(p, encoding="utf-8-sig", newline="") as fh:
        return [{(k or "").strip(): (v or "").strip() for k, v in r.items()} for r in csv.DictReader(fh)]


# ---------------------------------------------------------------- outils : dossiers et fichiers
@mcp.tool()
def lister_dossiers() -> list[dict]:
    """Liste les dossiers de soumission du serveur avec leur état (préparé, relevé prêt, livrables)."""
    out = []
    for d in sorted(p for p in base().iterdir() if p.is_dir()):
        t = d / "travail"
        out.append({
            "dossier": d.name,
            "pdf_entree": sorted(p.name for p in (d / "entree").glob("*.pdf")),
            "prepare": (t / "feuilles.csv").exists(),
            "nomenclature": (t / "nomenclature.csv").exists(),
            "livrables": sorted(p.name for p in (d / "sortie").glob("*") if p.is_file()),
        })
    return out


@mcp.tool()
def deposer_fichier(dossier: str, nom_fichier: str, contenu_base64: str, sous_dossier: str = "entree") -> dict:
    """Dépose un fichier (PDF de plans, addenda, ou projet de l'estimateur) encodé en base64.

    sous_dossier : « entree » pour les plans à relever, « reference » pour le projet Plan Expert de l'estimateur
    (<S>-Dupuis-PlanExpert.qpl + dupuis-png-dimensions.txt)."""
    if sous_dossier not in ("entree", "reference"):
        raise ToolError("sous_dossier doit être « entree » ou « reference »")
    if not NOM_RE.match(nom_fichier or "") or nom_fichier.startswith("."):
        raise ToolError(f"nom de fichier invalide : {nom_fichier!r}")
    data = base64.b64decode(contenu_base64, validate=True)
    if len(data) > TAILLE_MAX_DEPOT:
        raise ToolError("fichier trop gros (200 Mo max)")
    d = dossier_de(dossier, creer=True)
    p = sous_chemin(d / sous_dossier, nom_fichier)
    p.write_bytes(data)
    return {"fichier": f"{sous_dossier}/{nom_fichier}", "octets": len(data)}


@mcp.tool()
def preparer_dossier(dossier: str, chemin_source: str = "") -> dict:
    """Prépare le dossier : une page par feuille, rasters, tuiles 3×4 graduées en points PDF, mots positionnés,
    aperçus et MANIFESTE.md. chemin_source (facultatif, serveur local seulement) : dossier ou PDF à copier dans
    entree/ avant la préparation."""
    d = dossier_de(dossier, creer=True)
    if chemin_source:
        src = Path(chemin_source).expanduser().resolve()
        pdfs = [src] if src.is_file() else sorted(src.glob("*.pdf"))
        if not pdfs:
            raise ToolError(f"aucun PDF dans {src}")
        for p in pdfs:
            (d / "entree" / p.name).write_bytes(p.read_bytes())
    if not list((d / "entree").glob("*.pdf")):
        raise ToolError("entree/ ne contient aucun PDF")
    log = lancer("prepare.py", str(d / "entree"), str(d / "travail"))
    feuilles = lire_csv(d / "travail" / "feuilles.csv")
    return {"feuilles": [{k: f.get(k) for k in ("feuille", "fichier", "page", "titre", "nb_mots")} for f in feuilles],
            "manifeste": "travail/MANIFESTE.md", "journal": log[-1500:],
            "suite": "Lire estimateur://methode puis classer les feuilles (voir_image travail/apercus/<F>.png)."}


@mcp.tool()
def lister_fichiers(dossier: str, sous_chemin_relatif: str = "travail", motif: str = "*") -> list[dict]:
    """Liste les fichiers d'un sous-dossier (ex. « travail/tuiles/E101 », « sortie »)."""
    d = dossier_de(dossier)
    r = sous_chemin(d, sous_chemin_relatif)
    if not r.is_dir():
        raise ToolError(f"pas un dossier : {sous_chemin_relatif}")
    return [{"chemin": p.relative_to(d).as_posix(), "octets": p.stat().st_size}
            for p in sorted(r.glob(motif)) if p.is_file()][:2000]


@mcp.tool()
def lire_fichier(dossier: str, chemin: str, debut: int = 0) -> dict:
    """Lit un fichier texte du dossier (CSV, MD, JSON) par morceaux de 60 000 caractères à partir de `debut`."""
    p = sous_chemin(dossier_de(dossier), chemin)
    texte = p.read_text(encoding="utf-8", errors="replace")
    morceau = texte[debut:debut + MORCEAU]
    fin = debut + len(morceau)
    return {"chemin": chemin, "texte": morceau, "suite": fin if fin < len(texte) else None, "taille": len(texte)}


@mcp.tool()
def ecrire_fichier(dossier: str, nom: str, contenu: str) -> dict:
    """Écrit un fichier du relevé dans travail/. Noms permis : feuilles-classement.csv, nomenclature.csv,
    occurrences-texte.csv, occurrences-visuel.csv, reserves.md, rapport-releve.md, comparaison-estimateur.md."""
    if nom not in ECRITURE_PERMISE:
        raise ToolError(f"nom non permis : {nom} (permis : {', '.join(sorted(ECRITURE_PERMISE))})")
    p = dossier_de(dossier) / "travail" / nom
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(contenu if contenu.endswith("\n") else contenu + "\n", encoding="utf-8")
    lignes = contenu.count("\n") + (0 if contenu.endswith("\n") else 1)
    return {"ecrit": f"travail/{nom}", "lignes": lignes}


@mcp.tool()
def voir_image(dossier: str, chemin: str, largeur_max: int = 1600) -> Image:
    """Renvoie une image du dossier (aperçu, tuile, zoom, rendu) réduite à largeur_max pixels.
    Pour voir une page d'un PDF de sortie : chemin « sortie/<fichier>.pdf#<page> » (page 1 = première)."""
    from PIL import Image as PILImage

    d = dossier_de(dossier)
    page = None
    if "#" in chemin:
        chemin, page = chemin.split("#", 1)
    p = sous_chemin(d, chemin)
    if page is not None or p.suffix.lower() == ".pdf":
        import pymupdf

        with pymupdf.open(p) as doc:
            pg = doc[int(page or 1) - 1]
            zoom = min(4.0, max(0.2, largeur_max / pg.rect.width))
            return Image(data=pg.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom)).tobytes("png"), format="png")
    im = PILImage.open(p)
    if im.width > largeur_max:
        im = im.resize((largeur_max, round(im.height * largeur_max / im.width)))
    buf = io.BytesIO()
    im.convert("RGB").save(buf, "PNG", optimize=True)
    return Image(data=buf.getvalue(), format="png")


# ---------------------------------------------------------------- outils : lecture fine
def _feuille(d: Path, feuille: str) -> None:
    if not FEUILLE_RE.match(feuille or "") or not (d / "travail" / "feuilles" / f"{feuille}.pdf").exists():
        raise ToolError(f"feuille inconnue : {feuille}")


@mcp.tool()
def zoomer(dossier: str, feuille: str, x0: float, y0: float, x1: float, y1: float, px: int = 1600,
           sans_marques: bool = False) -> Image:
    """Zoom vectoriel d'une zone de feuille (coordonnées en points PDF), avec règle graduée et les occurrences déjà
    relevées marquées (sauf sans_marques). Sert à confirmer un symbole dense ou douteux."""
    d = dossier_de(dossier)
    _feuille(d, feuille)
    args = [str(d / "travail"), feuille, *(f"{v:g}" for v in (x0, y0, x1, y1)), "--px", str(int(px))]
    if sans_marques:
        args.append("--sans-marques")
    lancer("zoom.py", *args, delai=300)
    zooms = sorted((d / "travail" / "zooms").glob(f"{feuille}_*.png"), key=lambda p: p.stat().st_mtime)
    if not zooms:
        raise ToolError("zoom.py n'a produit aucune image")
    return Image(data=zooms[-1].read_bytes(), format="png")


@mcp.tool()
def nature_traits(dossier: str, feuille: str, x: float, y: float, rayon: float = 12) -> str:
    """Décrit les traits vectoriels autour d'un point (cercle, carré, arc, texte…) pour distinguer un vrai symbole
    d'un texte, d'une cote ou d'un trait d'architecture."""
    d = dossier_de(dossier)
    _feuille(d, feuille)
    return lancer("traits.py", str(d / "travail"), feuille, f"{x:g}", f"{y:g}", f"{rayon:g}", delai=300)


@mcp.tool()
def extraire_occurrences(dossier: str) -> dict:
    """Applique nomenclature.csv (jeton_regex) aux mots des feuilles « plan » → occurrences-texte.csv."""
    d = dossier_de(dossier)
    log = lancer("extract_occurrences.py", str(d / "travail"))
    occ = lire_csv(d / "travail" / "occurrences-texte.csv")
    return {"occurrences": len(occ), "par_label": dict(Counter(o["label"] for o in occ).most_common()),
            "journal": log[-1500:]}


# ---------------------------------------------------------------- contrôle du relevé
def controler(travail: Path) -> dict:
    """Contrôles déterministes avant livraison : rien ne sort d'un relevé incohérent."""
    erreurs, alertes = [], []
    requis = ["feuilles.csv", "feuilles-classement.csv", "nomenclature.csv", "reserves.md"]
    for f in requis:
        if not (travail / f).exists():
            erreurs.append(f"fichier manquant : {f}")
    feuilles = {r["feuille"]: r for r in lire_csv(travail / "feuilles.csv")}
    classes = {r["feuille"]: r.get("type", "") for r in lire_csv(travail / "feuilles-classement.csv")}
    non_classees = sorted(set(feuilles) - set(classes))
    if non_classees:
        erreurs.append(f"feuilles non classées : {', '.join(non_classees)}")
    nomen = lire_csv(travail / "nomenclature.csv")
    labels = {r.get("label", "") for r in nomen}
    for r in nomen:
        if not r.get("label"):
            erreurs.append("nomenclature : ligne sans label")
        if r.get("jeton_regex"):
            try:
                re.compile(r["jeton_regex"])
            except re.error as e:
                erreurs.append(f"nomenclature {r.get('label')} : jeton_regex invalide ({e})")
    occ = []
    for nom in ("occurrences-texte.csv", "occurrences-visuel.csv"):
        for i, o in enumerate(lire_csv(travail / nom), start=2):
            if o.get("exclure") == "1":
                continue
            o["_fichier"], o["_ligne"] = nom, i
            occ.append(o)
    if not occ:
        erreurs.append("aucune occurrence (occurrences-texte.csv / occurrences-visuel.csv vides)")
    hors_nomen, hors_page, feuille_inconnue, pas_plan = Counter(), [], Counter(), Counter()
    for o in occ:
        f = o.get("feuille", "")
        if o.get("label") not in labels:
            hors_nomen[o.get("label")] += 1
        if f not in feuilles:
            feuille_inconnue[f] += 1
            continue
        if classes.get(f) and classes[f] != "plan":
            pas_plan[f] += 1
        try:
            x, y = float(o["x_pt"]), float(o["y_pt"])
            L, H = float(feuilles[f]["largeur_pt"]), float(feuilles[f]["hauteur_pt"])
            if not (0 <= x <= L and 0 <= y <= H):
                hors_page.append(f"{o['_fichier']}:{o['_ligne']} ({f} {x:g},{y:g})")
        except (KeyError, ValueError):
            hors_page.append(f"{o['_fichier']}:{o['_ligne']} coordonnées illisibles")
    if hors_nomen:
        erreurs.append(f"labels absents de nomenclature.csv : {dict(hors_nomen)}")
    if feuille_inconnue:
        erreurs.append(f"feuilles inconnues dans les occurrences : {dict(feuille_inconnue)}")
    if hors_page:
        erreurs.append(f"{len(hors_page)} occurrence(s) hors de la page : {hors_page[:10]}")
    if pas_plan:
        alertes.append(f"occurrences sur des feuilles non « plan » : {dict(pas_plan)}")
    # doublons : même label à moins de 4 pt sur la même feuille (1 symbole = 1 repère)
    par = defaultdict(list)
    for o in occ:
        try:
            par[(o["feuille"], o["label"])].append((float(o["x_pt"]), float(o["y_pt"]), o))
        except (KeyError, ValueError):
            pass
    doublons = []
    for (f, lab), pts in par.items():
        pts.sort()
        for i, (x, y, o) in enumerate(pts):
            for x2, y2, o2 in pts[i + 1:]:
                if x2 - x > 4:
                    break
                if abs(y2 - y) <= 4:
                    doublons.append(f"{f} {lab} ({x:g},{y:g}) {o['_fichier']}:{o['_ligne']} ~ {o2['_fichier']}:{o2['_ligne']}")
    if doublons:
        erreurs.append(f"{len(doublons)} doublon(s) à moins de 4 pt : {doublons[:10]}")
    reserves = (travail / "reserves.md").read_text(encoding="utf-8") if (travail / "reserves.md").exists() else ""
    n_res = len(set(re.findall(r"R-\d{3}", reserves)))
    comptes = defaultdict(Counter)
    familles = {r.get("label"): r.get("famille", "") for r in nomen}
    for o in occ:
        comptes[o.get("feuille", "?")][familles.get(o.get("label"), "?")] += 1
    return {"pret": not erreurs, "erreurs": erreurs, "alertes": alertes, "occurrences": len(occ),
            "reserves": n_res, "par_feuille": {f: dict(c) for f, c in sorted(comptes.items())},
            "feuilles_plan": sorted(f for f, t in classes.items() if t == "plan")}


@mcp.tool()
def verifier_releve(dossier: str) -> dict:
    """Contrôle le relevé (fichiers, classement, labels, coordonnées, doublons < 4 pt, réserves) et donne les
    comptes par feuille et famille. « pret »: true est exigé par produire_livrables."""
    return controler(dossier_de(dossier) / "travail")


@mcp.tool()
def produire_livrables(dossier: str, nom: str = "") -> dict:
    """Produit les livrables dans sortie/ : <S>-RELEVE.pdf au format de l'exemplaire (plans annotés + bordereau
    matériel + réserves), <S>.qpl (projet Plan Expert), Plans-annotes.pdf, Rapport-de-metre.pdf/.md,
    Dossier-complet.pdf. Refuse si verifier_releve n'est pas « pret »."""
    from .exemple import rendre

    d = dossier_de(dossier)
    nom = nom or dossier
    if not NOM_RE.match(nom):
        raise ToolError(f"nom invalide : {nom!r}")
    ctl = controler(d / "travail")
    if not ctl["pret"]:
        return {"produit": False, "raison": "relevé non prêt", "erreurs": ctl["erreurs"]}
    sortie = d / "sortie"
    journal = [lancer("build_qpl.py", str(d / "travail"), nom, str(sortie)),
               lancer("render_pdf.py", str(d / "travail"), nom, str(sortie))]
    rapport = rendre(d / "travail", sortie, nom)
    return {"produit": True, "releve_pdf": f"sortie/{nom}-RELEVE.pdf", "pages": rapport["pages"],
            "reperes": rapport["reperes"],
            "feuilles": [{k: s[k] for k in ("sheet", "plan_page", "reperes", "familles", "res", "box_in_free_space")}
                         for s in rapport["sheets"]],
            "fichiers": sorted(p.name for p in sortie.iterdir() if p.is_file()),
            "journal": "\n".join(journal)[-2000:],
            "controle": "Regarder chaque page de plan avec voir_image('sortie/<S>-RELEVE.pdf#<page>')."}


@mcp.tool()
def recuperer_livrable(dossier: str, chemin: str) -> dict:
    """Renvoie un fichier de sortie/ en base64 (25 Mo max) pour le client distant."""
    d = dossier_de(dossier)
    p = sous_chemin(d / "sortie", chemin.removeprefix("sortie/"))
    data = p.read_bytes()
    if len(data) > TAILLE_MAX_LIVRABLE:
        raise ToolError("fichier trop gros pour un transfert MCP (25 Mo max)")
    return {"nom": p.name, "octets": len(data), "contenu_base64": base64.b64encode(data).decode("ascii")}


@mcp.tool()
def comparer_estimateur(dossier: str) -> dict:
    """Compare le .qpl produit au projet Plan Expert de l'estimateur (reference/<S>-Dupuis-PlanExpert.qpl +
    dupuis-png-dimensions.txt, dans le dossier ou dans dossiers/<S>/reference du dépôt), marque par marque."""
    if str(RACINE) not in sys.path:
        sys.path.insert(0, str(RACINE))
    from src.validation import compare_qpl as cq

    d = dossier_de(dossier)
    ref = next((r for r in (d / "reference", RACINE / "dossiers" / dossier / "reference")
                if (r / f"{dossier}-Dupuis-PlanExpert.qpl").exists()), None)
    if ref is None:
        raise ToolError("aucun projet de l'estimateur trouvé (reference/<S>-Dupuis-PlanExpert.qpl)")
    ia_qpl = d / "sortie" / f"{dossier}.qpl"
    if not ia_qpl.exists():
        raise ToolError("lancer produire_livrables d'abord")
    from src.validation.jeu_reference import accord_categories

    sortie = d / "sortie" / "comparaison-estimateur"
    sortie.mkdir(parents=True, exist_ok=True)
    qpl_h = ref / f"{dossier}-Dupuis-PlanExpert.qpl"
    humains = cq.lire_qpl(qpl_h, "humain")
    cq.preparer_humain(humains, cq.lire_dimensions(ref / "dupuis-png-dimensions.txt", dossier))
    ias = cq.lire_qpl(ia_qpl, "ia")
    anomalies = cq.preparer_ia(ias, cq.lire_feuilles(d / "travail" / "feuilles.csv"), d / "sortie")
    comp = cq.comparer(humains, ias, anomalies)
    tot = cq.ecrire_sorties(comp, sortie, {"dossier": dossier, "humain": qpl_h.name, "ia": ia_qpl.name,
                                          "dims": "dupuis-png-dimensions.txt", "feuilles": "travail/feuilles.csv"})
    h, ia, a = tot["humaines"], tot["ia"], tot["appariees"]
    cat = accord_categories(comp)
    return {"sortie": "sortie/comparaison-estimateur", "humaines": h, "ia": ia, "appariees": a,
            "rappel": round(100 * a / h, 1) if h else 0.0, "precision": round(100 * a / ia, 1) if ia else 0.0,
            "accord_categories": cat["pourcentage"],
            "confusions": [{"humain": x, "ia": y, "n": n} for (x, y), n in cat["confusions"].most_common(10)]}


# ---------------------------------------------------------------- savoir exposé au LLM
def _methode() -> str:
    t = METHODE.read_text(encoding="utf-8")
    t = re.sub(r"\A---.*?---\s*", "", t, flags=re.S)
    remplacements = {
        r"uv run releve/prepare\.py[^\n`]*": "preparer_dossier",
        r"uv run releve/extract_occurrences\.py[^\n`]*": "extraire_occurrences",
        r"uv run releve/zoom\.py[^\n`]*": "zoomer",
        r"uv run releve/traits\.py[^\n`]*": "nature_traits",
        r"uv run releve/build_qpl\.py[^\n`]*": "produire_livrables",
        r"uv run releve/render_pdf\.py[^\n`]*": "produire_livrables",
    }
    for motif, outil in remplacements.items():
        t = re.sub(motif, outil, t)
    entete = ("# Méthode de relevé (serveur MCP)\n\nOutils : preparer_dossier, voir_image (aperçus, tuiles), zoomer, "
              "nature_traits, ecrire_fichier (fichiers de travail/), extraire_occurrences, verifier_releve, "
              "produire_livrables, comparer_estimateur. Là où la méthode dit « lire » ou « Read », utiliser "
              "voir_image ou lire_fichier ; « écrire » = ecrire_fichier.\n\n")
    return entete + t


@mcp.resource("estimateur://methode", mime_type="text/markdown",
              description="Méthode complète du relevé (classement, légende, occurrences, réserves).")
def ressource_methode() -> str:
    return _methode()


@mcp.resource("estimateur://standard", mime_type="text/markdown",
              description="Standard de présentation de l'exemplaire HR26-14 (encadré, pastilles, bordereau, portées).")
def ressource_standard() -> str:
    return STANDARD.read_text(encoding="utf-8")


@mcp.resource("estimateur://libelles", mime_type="application/json",
              description="Libellés Plan Expert appris des projets humains 2021-2026 (orthographe à reprendre).")
def ressource_libelles() -> str:
    return LIBELLES.read_text(encoding="utf-8") if LIBELLES.exists() else "{}"


@mcp.prompt(name="releve_planexpert", description="Faire le relevé complet d'un dossier de plans.")
def prompt_releve(dossier: str) -> str:
    return (f"Fais le relevé de quantités électrique complet du dossier « {dossier} ».\n\n{INSTRUCTIONS}\n\n"
            f"Méthode à suivre à la lettre :\n\n{_methode()}")


# ---------------------------------------------------------------- transport HTTP protégé
class CleBearer:
    """Middleware ASGI : exige « Authorization: Bearer <ESTIMATEUR_MCP_CLE> » sur chaque requête HTTP."""

    def __init__(self, app, cle: str):
        self.app, self.cle = app, cle.encode()

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            entetes = dict(scope.get("headers") or [])
            fourni = entetes.get(b"authorization", b"")
            if not (fourni.startswith(b"Bearer ") and hmac.compare_digest(fourni[7:].strip(), self.cle)):
                await send({"type": "http.response.start", "status": 401,
                            "headers": [(b"content-type", b"application/json"), (b"www-authenticate", b"Bearer")]})
                await send({"type": "http.response.body", "body": b'{"erreur":"cle absente ou invalide"}'})
                return
        await self.app(scope, receive, send)


def application_http(hote: str = "127.0.0.1", hotes_permis: list[str] | None = None, cle: str | None = None):
    from mcp.server.transport_security import TransportSecuritySettings

    cle = cle if cle is not None else os.environ.get("ESTIMATEUR_MCP_CLE", "")
    local = hote in ("127.0.0.1", "localhost", "::1")
    if not local and len(cle) < 24:
        raise SystemExit("ESTIMATEUR_MCP_CLE (24 caractères min.) est obligatoire hors de l'hôte local")
    permis = [x for h in (hotes_permis or []) for x in (h, f"{h}:*")] + ["127.0.0.1:*", "localhost:*", "[::1]:*"]
    securite = TransportSecuritySettings(enable_dns_rebinding_protection=True, allowed_hosts=permis,
                                         allowed_origins=[f"{s}://{h}" for h in permis for s in ("http", "https")])
    app = mcp.streamable_http_app(host=hote, transport_security=securite)
    return CleBearer(app, cle) if cle else app


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m serveur_mcp", description="Serveur MCP Expert estimateur")
    ap.add_argument("--transport", choices=["stdio", "http"], default="stdio")
    ap.add_argument("--hote", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--hote-permis", action="append", default=[], help="nom d'hôte public accepté (ex. estim.exemple.ca)")
    a = ap.parse_args(argv)
    if a.transport == "stdio":
        mcp.run("stdio")
        return 0
    import uvicorn

    uvicorn.run(application_http(a.hote, a.hote_permis), host=a.hote, port=a.port)
    return 0


if __name__ == "__main__":
    sys.exit(main())

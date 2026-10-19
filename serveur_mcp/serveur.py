"""Serveur MCP « Expert estimateur » (Groupe DR Électrique).

N'importe quel LLM compatible MCP (Claude, GPT, Gemini, modèle local…) se branche ici et fait le relevé de quantités
électrique d'un plan PDF brut, sans Plan Expert ni machine virtuelle :

  deposer_fichier / preparer_dossier  → pages, tuiles, mots (releve/prepare.py)
  voir_image / zoomer / nature_traits → le LLM lit la légende et les plans (jugement visuel)
  ecrire_fichier                      → classement, nomenclature, occurrences, réserves (méthode : ressource
                                        estimateur://methode, gabarit : prompt releve_planexpert)
  extraire_occurrences / verifier_releve
  quantites                           → repères × multiplicateurs.csv (unités types) = quantités à soumissionner
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
import shutil
import subprocess
import sys
import zipfile
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
BIBLIOTHEQUE = Path(os.environ.get("ESTIMATEUR_BIBLIOTHEQUE") or RELEVE / "bibliotheque-blocs.csv")
LIEN_HUMAIN = Path(os.environ.get("ESTIMATEUR_LIEN_HUMAIN") or RACINE / "apprentissage" / "lien-humain")
NOM_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
FEUILLE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
ECRITURE_PERMISE = {
    "feuilles-classement.csv", "nomenclature.csv", "occurrences-texte.csv", "occurrences-visuel.csv",
    "reserves.md", "rapport-releve.md", "comparaison-estimateur.md", "multiplicateurs.csv",
}
TAILLE_MAX_DEPOT = 200 * 1024 * 1024
TAILLE_MAX_LIVRABLE = 25 * 1024 * 1024
MORCEAU = 60_000

INSTRUCTIONS = """Tu es l'expert estimateur électrique du Groupe DR Électrique. Tu fais le relevé de quantités d'un
dossier de plans PDF brut et tu livres le PDF annoté au format de l'exemplaire HR26-14.
PARCOURS STANDARD (toujours celui-ci : même PDF = même résultat, quel que soit le Claude qui appelle) :
1. relever_automatique(dossier="<no de soumission, ex. S-1902>", url_source="<lien Google Drive du PDF ou du dossier
   de plans>") — ou chemin_source="<chemin local>" sur le poste. Ne rien passer d'autre.
2. Si « produit »: true → donner à l'utilisateur lien_zip et lien_releve_pdf (ou zip / releve_pdf), le nombre de
   repères par feuille et les réserves ; montrer voir_image("sortie/<S>-RELEVE.pdf#1"). Ne jamais modifier le relevé.
3. Si a_etiqueter.inconnues n'est pas vide (bureau d'ingénieurs encore inconnu) : voir_image de chaque planche,
   etiqueter_signatures (vrais appareils seulement, IGNORER pour le reste, rien deviné : dans le doute ne pas
   étiqueter), puis relever_automatique(dossier, reprendre=True). Une fois appris, ce bureau sort seul pour tous.
Déroulement manuel (seulement si l'utilisateur le demande) : deposer_fichier (ou preparer_dossier avec chemin_source) → preparer_dossier → lire la ressource
estimateur://methode et l'appliquer (voir_image des aperçus/tuiles, zoomer, ecrire_fichier) → extraire_occurrences →
multiplicateurs.csv si une feuille montre des unités types (logements, chambres, salles « TYPE ») : facteur = nombre
d'unités réelles, avec sa source (cartouche, liste des logements, note) → verifier_releve jusqu'à « pret »: true →
quantites (repères × multiplicateur = quantités à soumissionner) → produire_livrables → voir_image du rendu pour te contrôler toi-même →
comparer_estimateur si une référence existe. Avant de nommer un article de nomenclature : chercher_libelle (nom
employé par les estimateurs) puis exemples_humains (comment ils l'ont repéré sur leurs plans). Rien n'est inventé :
chaque quantité vient d'un symbole vu, d'une étiquette, d'une cédule ou d'une note ; le doute va dans reserves.md."""

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


def lancer(script: str, *args: str, delai: int = 1800, codes_ok: tuple[int, ...] = (0,)) -> str:
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    r = subprocess.run([sys.executable, str(RELEVE / script), *args], cwd=RACINE, env=env,
                           stdin=subprocess.DEVNULL, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=delai)
    sortie = (r.stdout + ("\n" + r.stderr if r.stderr.strip() else "")).strip()
    if r.returncode not in codes_ok:
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


def _jpeg(im, qualite: int = 85) -> Image:
    """Image PIL -> JPEG (plus léger que PNG pour les plans ; préférence de Francis)."""
    buf = io.BytesIO()
    im.convert("RGB").save(buf, "JPEG", quality=qualite, optimize=True)
    return Image(data=buf.getvalue(), format="jpeg")


@mcp.tool()
def voir_image(dossier: str, chemin: str, largeur_max: int = 1600) -> Image:
    """Renvoie une image JPEG du dossier (aperçu, tuile, zoom, rendu) réduite à largeur_max pixels.
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
            pix = pg.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom))
            return _jpeg(PILImage.frombytes("RGB", (pix.width, pix.height), pix.samples))
    im = PILImage.open(p)
    if im.width > largeur_max:
        im = im.resize((largeur_max, round(im.height * largeur_max / im.width)))
    return _jpeg(im)


# ---------------------------------------------------------------- outils : savoir des estimateurs (projets Plan Expert)
_CONNAISSANCE: dict | None = None


def connaissance() -> dict:
    """apprentissage/lien-humain/connaissance.json : ce que les estimateurs ont fait des documents reçus."""
    global _CONNAISSANCE
    if _CONNAISSANCE is None:
        p = LIEN_HUMAIN / "connaissance.json"
        if not p.exists():
            raise ToolError("base humaine absente : lancer python -m src.apprentissage.lien_humain")
        _CONNAISSANCE = {s["libelle"]: s for s in json.loads(p.read_text(encoding="utf-8"))["symboles"]}
    return _CONNAISSANCE


def _pli(t: str) -> str:
    import unicodedata

    t = unicodedata.normalize("NFKD", t or "").encode("ascii", "ignore").decode("ascii").upper()
    return re.sub(r"[^A-Z0-9]+", " ", t).strip()


@mcp.tool()
def chercher_libelle(texte: str, n: int = 8) -> list[dict]:
    """Trouve les libellés que les estimateurs DR emploient dans Plan Expert pour un texte de légende ou un nom
    d'appareil (ex. « prise duplex DDFT », « détecteur de fumée »). Renvoie libellé canonique, variantes, catégorie,
    nombre de marques et de projets. Reprendre ce libellé dans nomenclature.csv."""
    import difflib

    q = _pli(texte)
    mots = set(q.split())
    res = []
    for lab, s in connaissance().items():
        noms = [lab, *s.get("variantes", [])]
        ratio = max(difflib.SequenceMatcher(None, q, _pli(v)).ratio() for v in noms)
        commun = max(len(mots & set(_pli(v).split())) / max(1, len(mots)) for v in noms)
        score = max(ratio, commun) + min(0.1, s["projets"] / 2000)
        res.append((score, s))
    res.sort(key=lambda r: -r[0])
    return [{"libelle": s["libelle"], "score": round(sc, 3), "categorie": s.get("categorie", ""),
             "variantes": s.get("variantes", [])[:6], "marques": s["occurrences"], "projets": s["projets"]}
            for sc, s in res[:max(1, min(n, 30))]]


@mcp.tool()
def exemples_humains(libelle: str) -> list:
    """Montre comment les estimateurs ont repéré ce libellé sur les documents reçus : planche de découpes des pages
    mêmes où ils ont cliqué dans Plan Expert (anneau rouge = marque humaine), + statistiques (marques, projets,
    forme/couleur Plan Expert, libellés comptés juste à côté, exemples document/page)."""
    c = connaissance()
    import unicodedata

    k = re.sub(r"\s+", " ", unicodedata.normalize("NFKD", libelle or "").encode("ascii", "ignore").decode("ascii"))
    s = c.get(k.strip().upper()) or next((v for kk, v in c.items() if _pli(kk) == _pli(libelle)), None)
    if s is None:
        proches = chercher_libelle(libelle, 5)
        raise ToolError(f"libellé inconnu : {libelle} ; proches : {[p['libelle'] for p in proches]}")
    infos = {k: s[k] for k in ("libelle", "categorie", "sous_type", "occurrences", "projets", "variantes",
                               "marque_planexpert", "voisins", "exemples") if k in s}
    out = [json.dumps(infos, ensure_ascii=False)]
    if s.get("galerie") and (LIEN_HUMAIN / s["galerie"]).exists():
        out.append(Image(data=(LIEN_HUMAIN / s["galerie"]).read_bytes(), format="jpeg"))
    return out


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
    from PIL import Image as PILImage
    return _jpeg(PILImage.open(zooms[-1]))


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


# ---------------------------------------------------------------- multiplicateurs (unités / logements / chambres types)
TYPIQUE_RE = re.compile(r"\bTYP(E|ES|IQUE|IQUES|ICAL)\b", re.I)


def lire_multiplicateurs(travail: Path) -> list[dict]:
    """multiplicateurs.csv : feuille,facteur,x0_pt,y0_pt,x1_pt,y1_pt,source.
    Zone vide = toute la feuille. Une occurrence prend le facteur de la zone la plus petite qui la contient."""
    regles = []
    for i, r in enumerate(lire_csv(travail / "multiplicateurs.csv"), start=2):
        try:
            fac = float(r.get("facteur") or "")
        except ValueError:
            raise ToolError(f"multiplicateurs.csv:{i} facteur illisible : {r.get('facteur')!r}")
        z = [r.get(k, "").strip() for k in ("x0_pt", "y0_pt", "x1_pt", "y1_pt")]
        zone = tuple(float(v) for v in z) if all(z) else None
        regles.append({"feuille": r.get("feuille", ""), "facteur": fac, "zone": zone,
                       "source": r.get("source", "").strip(), "_ligne": i})
    return regles


def facteur_de(regles: list[dict], feuille: str, x: float, y: float) -> float:
    """Zone explicite la plus petite qui contient le point, sinon règle « toute la feuille », sinon 1."""
    feuille_entiere, meilleur, aire = None, None, float("inf")
    for r in regles:
        if r["feuille"] != feuille:
            continue
        if r["zone"] is None:
            feuille_entiere = r["facteur"]
            continue
        x0, y0, x1, y1 = r["zone"]
        if min(x0, x1) <= x <= max(x0, x1) and min(y0, y1) <= y <= max(y0, y1):
            a = abs(x1 - x0) * abs(y1 - y0)
            if a < aire:
                meilleur, aire = r["facteur"], a
    if meilleur is not None:
        return meilleur
    return feuille_entiere if feuille_entiere is not None else 1.0


def controle_multiplicateurs(travail: Path, classement: list[dict]) -> tuple[list[str], list[str]]:
    """Bloquant : une feuille « plan » dont le cartouche/la note dit TYPE/TYPIQUE sans ligne dans
    multiplicateurs.csv (cause de S-1695 : chambres types non multipliées, -64 % luminaires).
    Facteur 1 accepté s'il est justifié (source)."""
    erreurs, alertes = [], []
    try:
        regles = lire_multiplicateurs(travail)
    except ToolError as e:
        return [str(e)], []
    avec = {r["feuille"] for r in regles}
    for r in regles:
        if not r["source"]:
            erreurs.append(f"multiplicateurs.csv:{r['_ligne']} sans source (dire d'où vient le facteur : "
                           "nombre de logements, liste des chambres, note de plan…)")
        if r["facteur"] <= 0:
            erreurs.append(f"multiplicateurs.csv:{r['_ligne']} facteur <= 0")
    for c in classement:
        if c.get("type") == "plan" and TYPIQUE_RE.search(c.get("note", "")) and c["feuille"] not in avec:
            msg = (f"feuille {c['feuille']} : unités types (« {c.get('note', '')[:80]} ») sans "
                   "multiplicateur — ajouter une ligne dans multiplicateurs.csv (facteur 1 si justifié)")
            # route automatique : la note est un extrait brut du cartouche (« Type D3-N » d'un appareil) → à vérifier
            (alertes if c.get("note", "").startswith("cartouche=") else erreurs).append(msg)
    return erreurs, alertes


@mcp.tool()
def quantites(dossier: str) -> dict:
    """Quantités à soumissionner : repères représentés × multiplicateur (unités/logements/chambres types).
    Écrit sortie/quantites.csv (label, code, famille, represente, total) et renvoie le détail par feuille."""
    d = dossier_de(dossier)
    t = d / "travail"
    regles = lire_multiplicateurs(t)
    nomen = {r.get("label"): r for r in lire_csv(t / "nomenclature.csv")}
    plans = {r["feuille"] for r in lire_csv(t / "feuilles-classement.csv") if r.get("type") == "plan"}
    rep, tot = Counter(), defaultdict(float)
    detail = defaultdict(lambda: defaultdict(lambda: [0, 0.0]))
    vus = set()
    for nom in ("occurrences-texte.csv", "occurrences-visuel.csv"):
        for o in lire_csv(t / nom):
            if o.get("exclure") == "1" or o.get("feuille") not in plans:
                continue
            try:
                x, y = float(o["x_pt"]), float(o["y_pt"])
            except (KeyError, ValueError):
                continue
            cle = (o["feuille"], o["label"], round(x), round(y))
            if cle in vus:
                continue
            vus.add(cle)
            f = facteur_de(regles, o["feuille"], x, y)
            rep[o["label"]] += 1
            tot[o["label"]] += f
            detail[o["feuille"]][o["label"]][0] += 1
            detail[o["feuille"]][o["label"]][1] += f
    lignes = []
    for lab in sorted(rep, key=lambda l: (nomen.get(l, {}).get("famille", ""), l)):
        n = nomen.get(lab, {})
        total = tot[lab]
        lignes.append({"label": lab, "code": n.get("code", ""), "famille": n.get("famille", ""),
                       "represente": rep[lab], "total": int(total) if total == int(total) else round(total, 2)})
    sortie = d / "sortie"
    sortie.mkdir(exist_ok=True)
    with (sortie / "quantites.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["label", "code", "famille", "represente", "total"])
        w.writeheader()
        w.writerows(lignes)
    return {"ecrit": "sortie/quantites.csv", "represente": sum(rep.values()),
            "total": round(sum(tot.values()), 2), "lignes": lignes,
            "multiplicateurs": [{k: v for k, v in r.items() if k != "_ligne"} for r in regles],
            "par_feuille": {f: {l: {"represente": a, "total": b} for l, (a, b) in v.items()} for f, v in detail.items()}}


# ---------------------------------------------------------------- contrôle du relevé
def _controle_legende(travail: Path, nomen: list[dict], occ: list[dict], classes: dict) -> list[str]:
    import importlib.util
    spec = importlib.util.spec_from_file_location("controle_qualite", Path(__file__).resolve().parents[1] / "releve" / "controle_qualite.py")
    cq = importlib.util.module_from_spec(spec); spec.loader.exec_module(cq)
    plans = {f for f, t in classes.items() if t == "plan"}
    comptes = Counter(o.get("label") for o in occ if o.get("feuille") in plans)
    classement = [{"feuille": f, "type": t} for f, t in classes.items()]
    return cq.controler_legende(str(travail), nomen, comptes, classement, [])


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
    # Q11-Q14 de releve/controle_qualite.py (légende, une famille par symbole, modèle du devis, code du vocabulaire) :
    # la méthode exposée renvoie « controle_qualite » vers verifier_releve, qui doit donc les appliquer aussi.
    erreurs += _controle_legende(travail, nomen, occ, classes)
    e_mult, a_mult = controle_multiplicateurs(travail, lire_csv(travail / "feuilles-classement.csv"))
    erreurs += e_mult
    alertes += a_mult
    return {"pret": not erreurs, "erreurs": erreurs, "alertes": alertes, "occurrences": len(occ),
            "reserves": n_res, "par_feuille": {f: dict(c) for f, c in sorted(comptes.items())},
            "feuilles_plan": sorted(f for f, t in classes.items() if t == "plan")}


@mcp.tool()
def verifier_releve(dossier: str) -> dict:
    """Contrôle le relevé (fichiers, classement, labels, coordonnées, doublons < 4 pt, réserves) et donne les
    comptes par feuille et famille. « pret »: true est exigé par produire_livrables."""
    return controler(dossier_de(dossier) / "travail")


def _etiqueter_signatures_vision(travail: Path, sig_dir: Path) -> int:
    """Quand blocs_familles_auto laisse des signatures inconnues et que GEMINI_API_KEY (ou auth.json) est disponible,
    demande à Gemini Vision (gemini-3.8-flash) d'identifier les symboles d'appareils sur signatures-*.png et complète
    blocs-familles.csv."""
    p_inc = travail / "blocs-a-etiqueter.json"
    if not p_inc.exists():
        return 0
    inc = json.loads(p_inc.read_text(encoding="utf-8")).get("inconnues") or []
    if not inc:
        return 0
    planches = sorted(sig_dir.glob("signatures-*.png"))
    if not planches:
        return 0
    cle = os.environ.get("GEMINI_API_KEY") or ""
    if not cle:
        p_auth = Path.home() / ".omo" / "agent" / "auth.json"
        if p_auth.exists():
            try:
                cle = json.loads(p_auth.read_text(encoding="utf-8")).get("google", {}).get("key", "")
            except Exception:
                pass
    if not cle:
        return 0
    import urllib.request
    b64 = base64.b64encode(planches[0].read_bytes()).decode("ascii")
    sids = [r["sig_id"] for r in inc[:15]]
    prompt = (
        f"Voici la planche de vignettes de symboles CAO ({', '.join(sids)}) extraits d'un plan électrique. "
        "Pour chaque vignette (S001, S002...) qui montre un VRAI boîtier ou symbole d'appareil électrique (par ex. boîtier "
        "avec code DP1, DP2, PP1, SO3, SO4, SW1, SW5, prise, luminaire, détecteur — PAS un bout de câble, ni un numéro "
        "de détail dans un grand cercle, ni une légende de fil), renvoie un tableau JSON d'objets : "
        "[{\"sig_id\": \"S002\", \"label\": \"APPAREIL NLIGHT DP1\", \"famille\": \"commande\", \"forme\": \"carre\", "
        "\"code\": \"DP1\", \"materiel\": \"APPAREIL DE CONTROLE NLIGHT DP1\"}]. Réponds UNIQUEMENT par le tableau JSON."
    )
    corps = {
        "model": "gemini-3.8-flash",
        # 16000 et non 4000 : la réflexion du modèle compte dans max_tokens ; à 4000 la réponse revenait tronquée
        # (finish_reason « length », JSON illisible) et l'étiquetage rendait 0 en silence (TEST-JO-02, 2026-10-19).
        "max_tokens": 16000,
        "temperature": 0,
        "messages": [{"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": "data:image/png;base64," + b64}},
        ]}],
    }
    try:
        req = urllib.request.Request(
            "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
            data=json.dumps(corps).encode("utf-8"),
            headers={"Authorization": "Bearer " + cle, "Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.load(resp)
        texte = data["choices"][0]["message"]["content"] or ""
        m = re.search(r"\[.*\]", texte, re.S)
        if not m:
            raise ValueError(f"pas de tableau JSON (finish_reason={data['choices'][0].get('finish_reason')}) : {texte[:300]!r}")
        items = json.loads(m.group(0))
    except Exception as e:   # jamais silencieux : la raison reste lisible dans travail/vision-gemini.log
        (travail / "vision-gemini.log").write_text(type(e).__name__ + ": " + str(e)[:1500], encoding="utf-8")
        return 0
    if not isinstance(items, list) or not items:
        return 0
    items = [it for it in items if isinstance(it, dict) and str(it.get("sig_id") or "").strip().upper() in sids]   # jamais une règle existante
    return _ajouter_etiquettes(travail, items, "vision-gemini", "étiqueté par Gemini Vision sur signatures-01.png")["ajoutees"]


COLS_FAMILLES = ["sig_id", "label", "famille", "forme", "code", "materiel", "legende_no", "diam_min", "diam_max", "feuilles",
                 "portee", "reserve", "origine", "feuilles_auto", "note"]


def _ajouter_etiquettes(travail: Path, items: list, origine: str, note: str) -> dict:
    """Écrit des règles de signatures dans blocs-familles.csv (origine ≠ auto : blocs_familles_auto.py ne les écrase
    jamais). Une règle existante du même sig_id dont la plage diam_min–diam_max chevauche la nouvelle est remplacée
    (correction) ; les autres plages restent (S002 sortie data ≤ 6,5 pt ET boîtier DP1 à 16 pt). label IGNORER = vu,
    pas un appareil."""
    if str(RELEVE) not in sys.path:
        sys.path.insert(0, str(RELEVE))
    from legende import code_attendu
    connus = {r["sig_id"] for r in lire_csv(travail / "blocs-index.csv")}
    ids = travail / "blocs-ids.json"
    if ids.exists():
        connus |= set(json.loads(ids.read_text(encoding="utf-8")).values())
    p_fam = travail / "blocs-familles.csv"
    existantes = lire_csv(p_fam)
    code_de = {r["materiel"]: r["code"] for r in existantes if r.get("code") and r.get("label") != "IGNORER"}

    def code_pour(materiel: str, propose: str) -> str:
        """Vocabulaire d'abord (contrôle Q14), puis le code lu sur le symbole, puis Mnn libre — jamais un code déjà
        porté par un autre matériel du dossier (les repères DP1/DP2 se mélangeraient)."""
        if materiel in code_de:
            return code_de[materiel]
        pris = {c for m, c in code_de.items() if m != materiel}
        for c in (code_attendu(materiel), re.sub(r"[^A-Z0-9]", "", propose.upper())[:4]):
            if c and c not in pris:
                break
        else:
            c = next(f"M{i:02d}" for i in range(1, 100) if f"M{i:02d}" not in pris)
        code_de[materiel] = c
        return c

    nouvelles, refusees = {}, []
    for it in items if isinstance(items, list) else []:
        sid = str((it or {}).get("sig_id") or "").strip().upper()
        label = str(it.get("label") or "").strip().upper()
        if not sid or sid not in connus or not label:
            refusees.append({"sig_id": sid, "raison": "sig_id inconnu de blocs-index.csv" if sid else "sig_id vide"} if label
                            else {"sig_id": sid, "raison": "label vide"})
            continue
        materiel = str(it.get("materiel") or label).strip().upper()
        nouvelles[sid] = {
            "sig_id": sid, "label": label, "famille": str(it.get("famille") or "commande").strip().lower(),
            "forme": str(it.get("forme") or "carre").strip().lower(),
            "code": "" if label == "IGNORER" else code_pour(materiel, str(it.get("code") or "")), "materiel": materiel,
            "legende_no": str(it.get("legende_no") or ""), "diam_min": str(it.get("diam_min") or "0"),
            "diam_max": str(it.get("diam_max") or "99"), "feuilles": str(it.get("feuilles") or ""),
            "portee": str(it.get("portee") or "").upper(), "reserve": str(it.get("reserve") or ""),
            "origine": origine, "feuilles_auto": "", "note": str(it.get("note") or note)}
    def chevauche(r: dict, n: dict) -> bool:
        return float(r.get("diam_min") or 0) <= float(n["diam_max"]) and float(n["diam_min"]) <= float(r.get("diam_max") or 99)
    gardees = [r for r in existantes if not (r.get("sig_id") in nouvelles and chevauche(r, nouvelles[r["sig_id"]]))]
    with open(p_fam, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS_FAMILLES, extrasaction="ignore")
        w.writeheader()
        w.writerows(gardees + list(nouvelles.values()))
    return {"ajoutees": len(nouvelles), "refusees": refusees, "regles": list(nouvelles.values())}


def _signatures_a_etiqueter(d: Path) -> dict:
    """Ce que le LLM doit regarder quand la bibliothèque ne connaît pas les blocs de ce bureau d'ingénieurs."""
    p = d / "travail" / "blocs-a-etiqueter.json"
    inc = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    return {"inconnues": [{k: r.get(k) for k in ("sig_id", "n_plans", "par_feuille", "exemple")} for r in inc.get("inconnues") or []],
            "ambigues": [r.get("sig_id") for r in inc.get("ambigues") or []],
            "planches": [f"sortie/signatures/{p.name}" for p in sorted((d / "sortie" / "signatures").glob("signatures-*.png"))]}


@mcp.tool()
def etiqueter_signatures(dossier: str, etiquettes: list[dict], apprendre: bool = True) -> dict:
    """Étiquette les signatures de blocs CAO inconnues (vues sur sortie/signatures/signatures-NN.png avec voir_image).
    etiquettes : [{"sig_id": "S002", "label": "APPAREIL NLIGHT DP1", "famille": "commande", "forme": "carre",
    "materiel": "APPAREIL DE CONTROLE NLIGHT DP1"}, ...] ; facultatif : code, diam_min, diam_max, feuilles, portee,
    reserve, note. label "IGNORER" pour un bloc qui n'est pas un appareil (fil, trame, texte, numéro de détail).
    apprendre (défaut oui) : chaque signature encore absente de releve/bibliotheque-blocs.csv y est ajoutée — même
    bureau d'ingénieurs = mêmes blocs, le prochain dossier sort sans rien étiqueter. Une signature déjà connue de la
    bibliothèque avec une autre règle n'y est jamais réécrite (la règle reste propre au dossier).
    Ensuite : relever_automatique(dossier, reprendre=True)."""
    d = dossier_de(dossier)
    if not (d / "travail" / "blocs-index.csv").exists():
        raise ToolError("blocs-index.csv absent : lancer relever_automatique d'abord")
    res = _ajouter_etiquettes(d / "travail", etiquettes, "llm-mcp", "étiqueté par le LLM client MCP sur les planches de signatures")
    appris, non_appris = _apprendre(d / "travail", res.pop("regles"), dossier) if apprendre else ([], [])
    return {**res, "appris_bibliotheque": appris, "non_appris": non_appris,
            "suite": "relever_automatique(dossier, reprendre=True)"}


COLS_BIBLIOTHEQUE = ["signature", "label", "famille", "forme", "code", "materiel", "legende_no", "diam_min", "diam_max",
                     "feuilles_regex", "portee", "tolerance", "source", "note"]


def _apprendre(travail: Path, regles: list[dict], dossier: str) -> tuple[list[str], list[dict]]:
    """Ajoute à la bibliothèque les règles dont la signature y est absente (jamais d'écrasement). Une signature déjà
    connue (forme générique : un rectangle est un mur chez un bureau, un boîtier DP2 chez un autre) reste une règle du
    dossier seulement : elle est rendue dans non_appris, à étiqueter de nouveau sur le prochain dossier."""
    sig_de = {r["sig_id"]: r["signature"] for r in lire_csv(travail / "blocs-index.csv")}
    ids = travail / "blocs-ids.json"
    if ids.exists():
        sig_de.update({v: k for k, v in json.loads(ids.read_text(encoding="utf-8")).items()})
    connues = {r["signature"] for r in lire_csv(BIBLIOTHEQUE)}
    nouvelles, non_appris = [], []
    for r in regles:
        sg = sig_de.get(r["sig_id"])
        if not sg or sg in connues:
            if r["label"] != "IGNORER":
                non_appris.append({"sig_id": r["sig_id"], "raison": "signature générique déjà dans la bibliothèque "
                                   "avec une autre règle : règle gardée pour ce dossier seulement"})
            continue
        connues.add(sg)
        nouvelles.append({**{k: r.get(k, "") for k in COLS_BIBLIOTHEQUE}, "signature": sg, "feuilles_regex": "",
                          "tolerance": "0", "source": f"{dossier} {r['sig_id']} (LLM client MCP)"})
    if nouvelles:
        neuf = not BIBLIOTHEQUE.exists()
        with open(BIBLIOTHEQUE, "a", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=COLS_BIBLIOTHEQUE, extrasaction="ignore")
            if neuf:
                w.writeheader()
            w.writerows(nouvelles)
    return [r["source"].split()[1] for r in nouvelles], non_appris


def _empaqueter_zip_png(travail: Path, sortie: Path, nom: str, rapport: dict) -> dict:
    """Exporte chaque feuille et bordereau en PNG (<F>_annote.png, <F>_calque.png, <F>_bordereau_NN.png) + BOM (.csv, .xlsx)
    et empaquette le tout dans sortie/<nom>-LIVRABLES-PNG.zip."""
    png_dir = sortie / "png"
    shutil.rmtree(png_dir, ignore_errors=True)
    png_dir.mkdir(parents=True, exist_ok=True)
    annote_pdf = sortie / f"{nom}-Plans-annotes.pdf"
    sheets = rapport.get("sheets") or []
    total_pages = int(rapport.get("pages") or 0)
    for idx, sh in enumerate(sheets):
        f_nom = str(sh.get("sheet"))
        p_plan = int(sh.get("plan_page") or 1)
        p_suiv = int(sheets[idx + 1]["plan_page"]) if idx + 1 < len(sheets) else (total_pages + 1)
        nb_bord = max(0, p_suiv - p_plan - 1)
        lancer("calque_png.py", str(annote_pdf), str(png_dir), "--page", str(p_plan), "--nom", f_nom, "--bordereaux", str(nb_bord))
    # Export BOM CSV + XLSX
    bom_csv = sortie / "vecteur" / "bordereau.csv"
    if bom_csv.exists():
        shutil.copyfile(bom_csv, png_dir / f"{nom}-BOM.csv")
    try:
        from src.releve.xlsx_export import main as xlsx_main
        occ_files = [travail / f for f in ("occurrences-visuel.csv", "occurrences-texte.csv") if (travail / f).exists() and (travail / f).stat().st_size > 35]
        if occ_files:
            xlsx_main([str(occ_files[0]), "--sortie", str(png_dir / f"{nom}-BOM.xlsx"), "--nomenclature", str(travail / "nomenclature.csv")])
    except Exception:
        pass
    zip_path = sortie / f"{nom}-LIVRABLES-PNG.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(png_dir.glob("*")):
            if p.is_file():
                zf.write(p, arcname=p.name)
        for extra in ("nomenclature.csv", "occurrences-visuel.csv", "occurrences-texte.csv", "reserves.md"):
            ep = travail / extra
            if ep.exists():
                zf.write(ep, arcname=f"releve/{extra}")
    return {
        "zip": f"sortie/{zip_path.name}",
        "zip_chemin_absolu": str(zip_path.resolve()),
        "png_fichiers": sorted(p.name for p in png_dir.glob("*.png")),
        "bom_fichiers": sorted(p.name for p in png_dir.glob("*-BOM.*")),
    }


_DRIVE_DOSSIER = re.compile(r"/folders/([\w-]{20,})")
_DRIVE_FICHIER = re.compile(r"(?:/file/d/|/d/|[?&]id=)([\w-]{20,})")
# jamais la réponse de l'estimateur ni les prix comme entrée de relevé (CLAUDE.md, critère d'acceptation étape 1)
_EXCLU = re.compile(r"prix|soumission|take ?off|relev|estimat|\.qpl", re.I)


def _telecharger_source(url: str, dest: Path) -> list[str]:
    """Télécharge le PDF (ou les PDF d'un dossier) d'un lien Google Drive public ou d'une URL directe dans dest/."""
    import requests

    s = requests.Session()
    cibles = []
    m = _DRIVE_DOSSIER.search(url)
    if m and "google.com" in url:
        from src.apprentissage.gdrive import DossierDrive

        for f in DossierDrive(s).fichiers(m.group(1)):
            if f["nom"].lower().endswith(".pdf") and not _EXCLU.search(f["chemin"]):
                cibles.append((f"https://drive.usercontent.google.com/download?id={f['id']}&export=download&confirm=t",
                               f["nom"]))
    else:
        m = _DRIVE_FICHIER.search(url) if "google.com" in url else None
        cibles.append((f"https://drive.usercontent.google.com/download?id={m.group(1)}&export=download&confirm=t"
                       if m else url, ""))
    if not cibles:
        raise ToolError(f"aucun PDF de plans dans {url}")
    noms = []
    for u, nom in cibles:
        r = s.get(u, timeout=600)
        r.raise_for_status()
        if not r.content.startswith(b"%PDF"):
            raise ToolError(f"{nom or u} n'est pas un PDF lisible (lien privé ? le partager « toute personne disposant "
                            "du lien »)")
        if not nom:
            cd = re.search(r'filename\*?=(?:UTF-8\'\')?"?([^";]+)', r.headers.get("content-disposition", ""))
            from urllib.parse import unquote
            nom = unquote(cd.group(1)) if cd else (Path(u.split("?")[0]).name or "plans.pdf")
        nom = re.sub(r"[^\w.\- ()]", "_", nom)[:120]
        nom = nom if nom.lower().endswith(".pdf") else nom + ".pdf"
        if len(r.content) > TAILLE_MAX_DEPOT:
            raise ToolError(f"{nom} : plus de 200 Mo")
        (dest / nom).write_bytes(r.content)
        noms.append(nom)
    return noms


def _jeton(chemin: str) -> str:
    """Jeton de téléchargement d'un livrable : HMAC de la clé du serveur, la clé elle-même ne sort jamais."""
    return hmac.new(os.environ.get("ESTIMATEUR_MCP_CLE", "").encode(), chemin.encode(), "sha256").hexdigest()[:32]


def _liens(dossier: str, liv: dict) -> dict:
    """Liens cliquables (ESTIMATEUR_URL_PUBLIQUE) vers le ZIP et le PDF de relevé, pour un Claude distant."""
    racine = os.environ.get("ESTIMATEUR_URL_PUBLIQUE", "").rstrip("/")
    if not racine:
        return {}
    out = {}
    for cle, champ in (("lien_zip", "zip"), ("lien_releve_pdf", "releve_pdf")):
        if liv.get(champ):
            rel = f"{dossier}/{liv[champ].removeprefix('sortie/')}"
            out[cle] = f"{racine}/livrables/{rel}?jeton={_jeton(rel)}"
    return out


@mcp.tool()
def relever_automatique(dossier: str, url_source: str = "", chemin_source: str = "", feuille_unique: str = "",
                        verification_vision: bool = False, reprendre: bool = False) -> dict:
    """Pipeline automatique de bout en bout (PDF -> PNG -> relevé des symboles + calque coloré + BOM -> ZIP de PNG + BOM).
    Accepte un PDF ou un dossier de PDFs via `chemin_source` (ou déjà déposé dans `entree/`), prépare les PNG,
    extrait et étiquette les symboles page par page (route blocs CAO + texte, avec repli vision Gemini/NVIDIA),
    génère les calques PNG (<feuille>_annote.png, <feuille>_calque.png, <feuille>_bordereau_01.png) et la BOM,
    et retourne le chemin du fichier ZIP final prêt à livrer.
    Signatures inconnues de la bibliothèque (autre bureau d'ingénieurs) : la réponse liste `a_etiqueter` et les
    planches ; les regarder (voir_image), appeler etiqueter_signatures, puis relancer avec reprendre=True (garde la
    préparation et les blocs déjà extraits, refait seulement familles → relevé → livrables).
    url_source : lien du PDF ou du DOSSIER de plans (Google Drive « toute personne disposant du lien », ou URL
    directe) — le serveur le télécharge lui-même ; c'est l'entrée normale depuis un Claude distant.
    verification_vision (défaut non) : modèles de vision Gemini/NVIDIA du serveur ; non déterministe, donc hors du
    parcours standard (même PDF = même résultat, quel que soit le Claude qui appelle)."""
    d = dossier_de(dossier, creer=not reprendre)
    if not reprendre:
        if url_source:
            shutil.rmtree(d / "entree", ignore_errors=True)
            (d / "entree").mkdir(parents=True)
            _telecharger_source(url_source, d / "entree")
        preparer_dossier(dossier, chemin_source=chemin_source)
    elif not (d / "travail" / "blocs-index.csv").exists():
        raise ToolError("rien à reprendre : lancer relever_automatique sans reprendre d'abord")
    travail = d / "travail"
    sortie = d / "sortie"
    pdfs = sorted((d / "entree").glob("*.pdf"))
    if not pdfs:
        raise ToolError("aucun PDF dans entree/")
    pdf_princ = max(pdfs, key=lambda p: p.stat().st_size)
    # Si feuille_unique est demandé, restreindre feuilles.csv à cette feuille
    if feuille_unique:
        lignes_f = lire_csv(travail / "feuilles.csv")
        gardees = [r for r in lignes_f if r.get("feuille") == feuille_unique]
        if not gardees:
            raise ToolError(f"feuille {feuille_unique!r} absente de feuilles.csv ({[r.get('feuille') for r in lignes_f]})")
        with open(travail / "feuilles.csv", "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(gardees[0].keys()))
            w.writeheader()
            w.writerows(gardees)
    sig_dir = sortie / "signatures"
    if not reprendre:
        lancer("blocs_vectoriels.py", str(travail), str(pdf_princ))
        lancer("blocs_vignettes.py", str(travail), str(pdf_princ), str(sig_dir), "--min", "1")
    lancer("blocs_familles_auto.py", str(travail), "--bibliotheque", str(BIBLIOTHEQUE))
    vision = _etiqueter_signatures_vision(travail, sig_dir) if verification_vision else 0
    if vision:   # nouvelles règles : les inconnues restantes sont recalculées
        lancer("blocs_familles_auto.py", str(travail), "--bibliotheque", str(BIBLIOTHEQUE))
    lancer("blocs_vers_releve.py", str(travail), str(pdf_princ), "--modele", "automatique-mcp")
    a_etiqueter = _signatures_a_etiqueter(d)
    liv = produire_livrables(dossier, nom=dossier)
    liv["a_etiqueter"] = a_etiqueter
    liv["etiquetees_vision"] = vision
    if not liv.get("produit"):
        liv["suite"] = ("Aucun bloc reconnu par la bibliothèque : voir_image chaque planche de a_etiqueter.planches, "
                        "etiqueter_signatures(dossier, [...]) pour les vrais appareils (IGNORER pour le reste), "
                        "puis relever_automatique(dossier, reprendre=True).")
        return liv
    if a_etiqueter["inconnues"]:
        liv["suite"] = ("Livré avec des signatures non étiquetées (en réserve R-008) : etiqueter_signatures puis "
                        "relever_automatique(dossier, reprendre=True) pour les compter.")
    if verification_vision and (os.environ.get("GEMINI_API_KEY") or os.environ.get("NVIDIA_API_KEY")):
        try:
            lancer("verif_visuelle.py", str(sortie), dossier, "--max-marques", "25", codes_ok=(0, 2, 4))
            rapport = json.loads((sortie / f"{dossier}-rendu-rapport.json").read_text(encoding="utf-8"))
            liv.update(_empaqueter_zip_png(travail, sortie, dossier, rapport))
        except Exception as e:
            liv["verification_vision_note"] = str(e)[:300]
    liv.update(_liens(dossier, liv))
    return liv


@mcp.tool()
def produire_livrables(dossier: str, nom: str = "") -> dict:
    """Produit les livrables dans sortie/ : <S>-RELEVE.pdf au format de l'exemplaire (plans annotés + bordereau
    matériel + réserves), <S>.qpl (projet Plan Expert), Plans-annotes.pdf, Rapport-de-metre.pdf/.md,
    Dossier-complet.pdf. Refuse si verifier_releve n'est pas « pret ». `produit: true` signifie que les
    fichiers existent, PAS qu'ils sont validés visuellement — voir `a_verifier` et `controle`."""
    d = dossier_de(dossier)
    nom = nom or dossier
    if not NOM_RE.match(nom):
        raise ToolError(f"nom invalide : {nom!r}")
    ctl = controler(d / "travail")
    if not ctl["pret"]:
        return {"produit": False, "raison": "relevé non prêt", "erreurs": ctl["erreurs"]}
    sortie = d / "sortie"
    journal = [lancer("build_qpl.py", str(d / "travail"), nom, str(sortie)),
               lancer("render_vectoriel.py", str(d / "travail"), nom, str(sortie)),
               lancer("render_pdf.py", str(d / "travail"), nom, str(sortie))]
    # render_vectoriel.py a déjà fait build()+render() (sortie/vecteur/, <nom>-Plans-annotes.pdf) : ne pas
    # refaire le même rendu une seconde fois (sortie/format-exemple/) pour produire -RELEVE.pdf, juste copier
    # le PDF et relire son rapport déjà écrit sur disque.
    rapport = json.loads((sortie / f"{nom}-rendu-rapport.json").read_text(encoding="utf-8"))
    releve_pdf = sortie / f"{nom}-RELEVE.pdf"
    shutil.copyfile(sortie / f"{nom}-Plans-annotes.pdf", releve_pdf)
    a_verifier = rapport.get("conformite", {}).get("encadre_hors_espace_libre") or []
    controle = "Regarder chaque page de plan avec voir_image('sortie/<S>-RELEVE.pdf#<page>')."
    if a_verifier:
        controle += (f" ATTENTION : encadré RELEVE-MATERIEL hors de l'espace libre du plan sur "
                     f"{', '.join(a_verifier)} — valider visuellement avant de considérer ce relevé terminé.")
    zip_info = _empaqueter_zip_png(d / "travail", sortie, nom, rapport)
    return {"produit": True, **zip_info, "releve_pdf": f"sortie/{nom}-RELEVE.pdf", "pages": rapport["pages"],
            "reperes": rapport["reperes"],
            "feuilles": [{k: s[k] for k in ("sheet", "plan_page", "reperes", "familles", "res", "box_in_free_space")}
                         for s in rapport["sheets"]],
            "a_verifier": a_verifier,
            "fichiers": sorted(p.name for p in sortie.iterdir() if p.is_file()),
            "journal": "\n".join(journal)[-2000:],
            "controle": controle}


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
        r"uv run releve/controle_qualite\.py[^\n`]*": "verifier_releve",
        r"uv run releve/build_qpl\.py[^\n`]*": "produire_livrables",
        r"uv run releve/render_pdf\.py[^\n`]*": "produire_livrables",
    }
    for motif, outil in remplacements.items():
        t = re.sub(motif, outil, t)
    entete = ("# Méthode de relevé (serveur MCP)\n\nOutils : preparer_dossier, voir_image (aperçus, tuiles), zoomer, "
              "nature_traits, ecrire_fichier (fichiers de travail/), extraire_occurrences, verifier_releve, "
              "produire_livrables, comparer_estimateur. Là où la méthode dit « lire » ou « Read », utiliser "
              "voir_image ou lire_fichier ; « écrire » = ecrire_fichier.\n\n"
              "## Colonnes du format EXEMPLE (rendu final, chaîne from_releve)\n\n"
              "- feuilles-classement.csv : ajouter `bordereau` = materiel (1 ligne par repère, défaut des plans de "
              "devis), agrege (1 ligne par famille) ou travaux ; mettre `cartouche=<NUMÉRO>` dans `note`.\n"
              "- nomenclature.csv : ajouter `code` (étiquette du symbole sur le plan : DP1, K, CE2…), `materiel` "
              "(nom de famille, ex. « Appareil de contrôle nLight DP1 »), `portee` (INSTALLER, FOURNIR ET "
              "INSTALLER…), `modele`, `prescription`, `discipline` (incendie | electricite | urgence) — valeurs "
              "lues sur le plan ou le devis seulement.\n"
              "- occurrences-*.csv : `prescription`, `reserve` (1 si doute), `parent`, et si le symbole est une "
              "boîte : `x0_pt,y0_pt,x1_pt,y1_pt`. La pastille est recentrée sur le symbole vectoriel le plus proche "
              "(ancrage automatique) ; un repère = un symbole.\n"
              "- reserves.md : R-001… une par ligne, en nommant la feuille ; renvoyer une ligne du bordereau par "
              "« voir R-00n » dans sa prescription.\n\n")
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


@mcp.resource("estimateur://pratiques-humaines", mime_type="text/markdown",
              description="Ce que les estimateurs font des documents reçus dans Plan Expert (libellés, voisins, pages).")
def ressource_pratiques() -> str:
    p = LIEN_HUMAIN / "PRATIQUES.md"
    return p.read_text(encoding="utf-8") if p.exists() else "Base humaine absente."


@mcp.prompt(name="releve_planexpert", description="Faire le relevé complet d'un dossier de plans.")
def prompt_releve(dossier: str) -> str:
    return (f"Fais le relevé de quantités électrique complet du dossier « {dossier} ».\n\n{INSTRUCTIONS}\n\n"
            f"Méthode à suivre à la lettre :\n\n{_methode()}")


# ---------------------------------------------------------------- transport HTTP protégé
class CleBearer:
    """Middleware ASGI : exige la clé ESTIMATEUR_MCP_CLE, en « Authorization: Bearer <clé> » ou dans l'URL
    (« /mcp?cle=<clé> » : le connecteur personnalisé de claude.ai n'envoie pas d'en-tête). /livrables/<dossier>/<fichier>
    sert un fichier de sortie/ sur présentation de son jeton (lien rendu par relever_automatique)."""

    def __init__(self, app, cle: str):
        self.app, self.cle = app, cle.encode()

    async def _refus(self, send, statut=401, corps=b'{"erreur":"cle absente ou invalide"}'):
        await send({"type": "http.response.start", "status": statut,
                    "headers": [(b"content-type", b"application/json"), (b"www-authenticate", b"Bearer")]})
        await send({"type": "http.response.body", "body": corps})

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            from urllib.parse import parse_qs, unquote

            qs = parse_qs((scope.get("query_string") or b"").decode())
            if scope["path"].startswith("/livrables/"):
                rel = unquote(scope["path"][len("/livrables/"):])
                if not hmac.compare_digest((qs.get("jeton") or [""])[0], _jeton(rel)) or "/" not in rel:
                    return await self._refus(send, 403, b'{"erreur":"jeton invalide"}')
                dossier, fichier = rel.split("/", 1)
                try:
                    p = sous_chemin(dossier_de(dossier) / "sortie", fichier)
                except ToolError:
                    p = None
                if p is None or not p.is_file():
                    return await self._refus(send, 404, b'{"erreur":"introuvable"}')
                await send({"type": "http.response.start", "status": 200, "headers": [
                    (b"content-type", b"application/zip" if p.suffix == ".zip" else b"application/pdf"),
                    (b"content-disposition", f'attachment; filename="{p.name}"'.encode())]})
                await send({"type": "http.response.body", "body": p.read_bytes()})
                return
            entetes = dict(scope.get("headers") or [])
            fourni = entetes.get(b"authorization", b"")
            fourni = fourni[7:].strip() if fourni.startswith(b"Bearer ") else (qs.get("cle") or [""])[0].encode()
            if self.cle and not hmac.compare_digest(fourni, self.cle):
                return await self._refus(send)
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
    return CleBearer(app, cle)   # sans clé (hôte local) : seulement la route /livrables


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

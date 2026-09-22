"""
Comparaison déterministe marque par marque, page par page, entre le relevé
humain (projet Plan Expert de l'estimateur) et le relevé IA (projet Plan
Expert produit par la chaîne). Tout est lu dans le XML des `.qpl` ; Plan
Expert n'est pas nécessaire.

CLI :
  python -m src.validation.compare_qpl --humain A.qpl --ia B.qpl \
      --dims png-dimensions.txt --feuilles feuilles.csv --sortie DIR \
      [--dossier S-1844] [--rasters-ia DIR]

Sorties dans DIR : ecart-dupuis.md, appariement.csv,
correspondance-libelles.csv, pages.csv.

Méthode (tout est calculé, rien n'est saisi à la main) :

1. Chargement. Par `<Plan>` : marques = `<Counter Name>/<Element X Y>`
   (coordonnées en pixels du raster du plan), lignes = `<Line>` (comptées à
   part, jamais appariées ; segments `<Element X1 Y1 X2 Y2>` ou `<Point>`).
   Taille du raster : humain → fichier de dimensions (`dossier|nom|L|H`,
   nom = `FileName` du plan) ; IA → taille réelle du PNG (Pillow), à défaut
   `raster_px` de feuilles.csv. Côté IA, la feuille est le nom du PNG
   (`FileName`) : le `Name` du plan peut différer (renommage au cartouche).
2. Appariement des pages.
   a. Par nom : plan humain `<PDF> - <page>` (ou `<PDF>[-unlocked]-page-000NN`)
      → (fichier, page) de feuilles.csv, noms comparés sans accents ni casse.
   b. Recalage : chaque paire est vérifiée géométriquement. Score = part des
      marques humaines ayant une marque IA à moins de 1,5 % de la diagonale
      du raster IA. La transformation « identité » (coordonnées normalisées
      [0,1]² des deux côtés) est essayée d'abord.
   c. Si l'identité donne un score < 0,4 (ou s'il n'y a pas de nom commun) et
      que la page humaine a ≥ 5 marques : recherche géométrique sur toutes
      les feuilles IA marquées ; translation par vote (histogramme des
      décalages), puis ajustement aux moindres carrés (échelles x/y +
      translation, ± 8 %) sur les couples retenus.
      - page à ≥ 20 marques : 8 orientations (0/90/180/270, avec et sans
        miroir) × échelle uniforme dans [0,7 ; 1,4] × l'échelle nominale ;
      - page à < 20 marques : voisinage de l'identité seulement (orientation
        0, échelle ± 5 %, translation ≤ 3 % de la diagonale) — une recherche
        libre sur quelques marques trouve toujours un recalage « parfait » ;
      - consensus par document source : l'échelle, les orientations et la
        translation des recalages sûrs (score ≥ 0,8 et ≥ 20 marques) sont
        imposées à toutes les pages du document (± 5 %, ± 3 %).
      On garde la meilleure feuille si score ≥ 0,4 — ≥ 0,8 s'il faut contredire
      la feuille désignée par le nom (départage à ± 0,05 par la
      F-mesure rappel / précision locale ; second candidat à < 0,1 signalé
      « AMBIGU »), sinon « page non appariée » (ou appariement par nom
      conservé et signalé).
   d. Raster humain de taille inconnue (JPG absents du fichier de dimensions) :
      l'échelle est estimée sur la page de même nom (orientation 0,
      translation ≤ 3 % de la diagonale), puis propagée au document (médiane).
   e. Plusieurs pages humaines sur la même feuille IA : affectation un-à-un,
      sans libellés, contre les marques déjà retenues (seuil des marques).
      Même document (copie de raster) : union sans doublons, page « EN
      DOUBLE » si tout est doublon. Documents différents (original + addenda)
      avec ≥ 50 % de doublons : « version remplacée », page exclue. Référence :
      la page désignée par le nom, puis un addenda, puis la plus marquée.
3. Appariement des marques par feuille IA : affectation optimale
   (`scipy.optimize.linear_sum_assignment`) sur la distance euclidienne en
   pixels IA, seuil 1,2 % de la diagonale ; sensibilité à 0,6 % et 2,5 %.
   Les libellés ne décident pas de l'appariement : une première passe sur les
   seules positions donne P(libellé IA | libellé humain) ; une seconde passe
   ajoute au coût 0,5 × seuil × (1 − P), ce qui ne change pas le nombre de
   couples mais départage des marques voisines (appareils superposés).
4. Correspondance des libellés déduite des couples appariés (libellé IA
   majoritaire par libellé humain, avec sa proportion).
"""
from __future__ import annotations

import argparse
import csv
import math
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import numpy as np
from scipy.optimize import linear_sum_assignment
from scipy.spatial import cKDTree

# --- Paramètres (en fraction de la diagonale du raster IA) -----------------
SEUIL_PAGE = 0.015            # recalage de page
SCORE_PAGE_MIN = 0.4          # score minimal pour accepter une page
SCORE_REMPLACE_NOM = 0.8      # score minimal pour contredire l'appariement par nom
MARQUES_MIN_GEOMETRIE = 5     # marques humaines minimales pour la géométrie
SEUIL_MARQUE = 0.012          # appariement des marques
SEUILS_SENSIBILITE = (0.006, 0.012, 0.025)
PLAGE_ECHELLE = (0.7, 1.4)    # recherche géométrique, relatif au nominal
PAS_ECHELLE = 0.03            # pas logarithmique de la recherche
CONSENSUS_SCORE, CONSENSUS_MARQUES, CONSENSUS_TOL = 0.8, 20, 0.05
TRANSLATION_MAX_INCONNU = 0.03
TRANSLATION_TOL = 0.03        # tolérance de translation autour du consensus
ECHANTILLON_VOTE = 150        # points au plus par côté pour le vote
EGALITE_SCORE = 0.05
PENALITE_LIBELLE = 0.5       # départage des voisins par cohérence de libellé
AJUSTEMENT_MAX = 0.08         # écart d'échelle max. accepté par les moindres carrés
AMBIGU_ECART = 0.1

# Les 8 isométries du carré (appliquées aux pixels humains avant échelle).
ROTATIONS: tuple[tuple[str, np.ndarray], ...] = (
    ("0°", np.array([[1, 0], [0, 1]])),
    ("90°", np.array([[0, -1], [1, 0]])),
    ("180°", np.array([[-1, 0], [0, -1]])),
    ("270°", np.array([[0, 1], [-1, 0]])),
    ("miroir 0°", np.array([[-1, 0], [0, 1]])),
    ("miroir 90°", np.array([[0, 1], [1, 0]])),
    ("miroir 180°", np.array([[1, 0], [0, -1]])),
    ("miroir 270°", np.array([[0, -1], [-1, 0]])),
)


class CompareErreur(ValueError):
    """Entrée illisible — refusée, jamais corrigée en silence."""


# --- Modèle -----------------------------------------------------------------

@dataclass
class Marque:
    ident: str
    cote: str               # "humain" | "ia"
    plan: str               # nom du plan (humain) ou feuille (IA)
    libelle: str
    x: float                # pixels du raster de ce plan
    y: float


@dataclass
class LigneQpl:
    libelle: str
    segments: int
    longueur_px: float


@dataclass
class Plan:
    nom: str
    fichier: str
    marques: list[Marque]
    lignes: list[LigneQpl]
    largeur: float | None = None
    hauteur: float | None = None
    source_dims: str = "inconnues"
    # Humain : document source et page ; IA : feuille, fichier PDF, page.
    base: str = ""
    page: int | None = None
    feuille: str = ""

    @property
    def xy(self) -> np.ndarray:
        if not self.marques:
            return np.zeros((0, 2))
        return np.array([(m.x, m.y) for m in self.marques], dtype=float)

    @property
    def diagonale(self) -> float:
        return math.hypot(self.largeur or 0.0, self.hauteur or 0.0)


@dataclass(frozen=True)
class Transfo:
    """p_ia = diag(sx, sy) · R_k · p_humain + t (pixels → pixels)."""
    k: int
    sx: float
    sy: float
    tx: float
    ty: float

    def appliquer(self, xy: np.ndarray) -> np.ndarray:
        if len(xy) == 0:
            return xy.reshape(0, 2)
        tourne = xy @ ROTATIONS[self.k][1].T
        return tourne * np.array([self.sx, self.sy]) + np.array([self.tx, self.ty])

    @property
    def echelle(self) -> float:
        return math.sqrt(abs(self.sx * self.sy))

    def decrire(self) -> str:
        return (f"{ROTATIONS[self.k][0]}, échelle x={self.sx:.4f} y={self.sy:.4f}, "
                f"translation ({self.tx:.0f}, {self.ty:.0f}) px IA")


@dataclass
class Recalage:
    feuille: str
    transfo: Transfo
    score: float            # part des marques humaines couvertes
    f_mesure: float
    couverts: int


@dataclass
class PairePage:
    humain: Plan
    feuille: str | None
    methode: str
    transfo: Transfo | None
    score: float | None
    note: str = ""
    second: Recalage | None = None
    nom_candidat: str | None = None


# --- Lecture ------------------------------------------------------------------

def normaliser_nom(texte: str) -> str:
    """Minuscules, sans accents, espaces compactées, sans extension .pdf."""
    texte = unicodedata.normalize("NFKD", texte)
    texte = "".join(c for c in texte if not unicodedata.combining(c))
    texte = re.sub(r"\.pdf$", "", texte.strip(), flags=re.IGNORECASE)
    texte = re.sub(r"-unlocked$", "", texte, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", texte).casefold().strip()


_RE_PAGE_TIRET = re.compile(r"^(?P<base>.+?) - (?P<page>\d+)(?P<copie>(?: \(\d+\)| \d+)*)$")
_RE_PAGE_EXPORT = re.compile(r"^(?P<base>.+?)(?:-unlocked)?-page-(?P<page>\d+)$", re.IGNORECASE)


def analyser_nom_humain(nom_plan: str, fichier: str) -> tuple[str, int | None]:
    """(document source, page) d'après le FileName, à défaut d'après le Name."""
    for candidat in (Path(fichier).stem if fichier else "", nom_plan):
        if not candidat:
            continue
        for motif in (_RE_PAGE_EXPORT, _RE_PAGE_TIRET):
            trouve = motif.match(candidat)
            if trouve:
                return trouve.group("base"), int(trouve.group("page"))
    return (Path(fichier).stem if fichier else nom_plan), None


def _lire_racine(path: Path) -> ET.Element:
    try:
        return ET.fromstring(path.read_bytes().decode("utf-8-sig"))
    except (OSError, UnicodeDecodeError, ET.ParseError) as exc:
        raise CompareErreur(f"QPL illisible : {path} ({exc})") from exc


def lire_qpl(path: Path, cote: str) -> list[Plan]:
    """Plans, marques et lignes d'un projet Plan Expert."""
    racine = _lire_racine(path)
    plans: list[Plan] = []
    for plan_el in racine.findall("./Plans/Plan"):
        nom = plan_el.get("Name", "")
        fichier = plan_el.get("FileName", "")
        marques: list[Marque] = []
        lignes: list[LigneQpl] = []
        cle = Path(fichier).stem if (cote == "ia" and fichier) else nom
        for layer in plan_el.iter("Layer"):
            for compteur in layer.findall("Counter"):
                libelle = (compteur.get("Name") or "").strip()
                for el in compteur.findall("Element"):
                    marques.append(Marque(
                        ident=f"{'H' if cote == 'humain' else 'IA'}:{cle}:{len(marques) + 1}",
                        cote=cote, plan=cle, libelle=libelle,
                        x=float(el.get("X", "0")), y=float(el.get("Y", "0"))))
            for ligne in layer.findall("Line"):
                segments, longueur = 0, 0.0
                for el in ligne.findall("Element"):
                    if el.get("X1") is not None:
                        segments += 1
                        longueur += math.hypot(float(el.get("X2", 0)) - float(el.get("X1", 0)),
                                               float(el.get("Y2", 0)) - float(el.get("Y1", 0)))
                points = [(float(p.get("X", 0)), float(p.get("Y", 0))) for p in ligne.findall("Point")]
                for a, b in zip(points, points[1:]):
                    segments += 1
                    longueur += math.hypot(b[0] - a[0], b[1] - a[1])
                lignes.append(LigneQpl((ligne.get("Name") or "").strip(), segments, longueur))
        plans.append(Plan(nom=nom, fichier=fichier, marques=marques, lignes=lignes))
    if not plans:
        raise CompareErreur(f"aucun <Plan> dans {path}")
    return plans


def lire_dimensions(path: Path, dossier: str | None) -> dict[str, tuple[float, float]]:
    """nom.png → (largeur, hauteur), restreint au dossier s'il est connu."""
    dims: dict[str, tuple[float, float]] = {}
    for brute in path.read_text(encoding="utf-8-sig").splitlines():
        champs = brute.rstrip("\r").split("|")
        if len(champs) != 4:
            continue
        nom_dossier, nom, largeur, hauteur = champs
        if dossier and not re.match(rf"^{re.escape(dossier)}(\s|$)", nom_dossier.strip()):
            continue
        try:
            dims[nom.strip()] = (float(largeur), float(hauteur))
        except ValueError:
            continue
    return dims


def lire_feuilles(path: Path) -> dict[str, dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as flux:
        lignes = list(csv.DictReader(flux))
    if not lignes or not {"feuille", "fichier", "page"} <= set(lignes[0]):
        raise CompareErreur(f"feuilles.csv sans colonnes feuille/fichier/page : {path}")
    return {ligne["feuille"].strip(): ligne for ligne in lignes}


def preparer_humain(plans: list[Plan], dims: dict[str, tuple[float, float]]) -> None:
    for plan in plans:
        plan.base, plan.page = analyser_nom_humain(plan.nom, plan.fichier)
        if plan.fichier in dims:
            plan.largeur, plan.hauteur = dims[plan.fichier]
            plan.source_dims = "fichier de dimensions"


def preparer_ia(plans: list[Plan], feuilles: dict[str, dict[str, str]],
                rasters: Path | None) -> list[str]:
    anomalies: list[str] = []
    for plan in plans:
        stem = Path(plan.fichier).stem if plan.fichier else plan.nom
        ligne = feuilles.get(stem) or feuilles.get(plan.nom)
        plan.feuille = stem
        if ligne is None:
            anomalies.append(f"Feuille IA « {stem} » (plan « {plan.nom} ») absente de feuilles.csv.")
        else:
            plan.base = ligne["fichier"]
            plan.page = int(ligne["page"]) if ligne["page"].strip().isdigit() else None
            brut = (ligne.get("raster_px") or "").lower().split("x")
            if len(brut) == 2 and all(v.strip().isdigit() for v in brut):
                plan.largeur, plan.hauteur = float(brut[0]), float(brut[1])
                plan.source_dims = "feuilles.csv"
        if rasters is not None and plan.fichier and (rasters / plan.fichier).is_file():
            from PIL import Image
            with Image.open(rasters / plan.fichier) as image:
                reel = (float(image.width), float(image.height))
            if plan.largeur is not None and (plan.largeur, plan.hauteur) != reel:
                anomalies.append(f"Feuille IA {stem} : raster {reel[0]:.0f}×{reel[1]:.0f} ≠ raster_px "
                                 f"{plan.largeur:.0f}×{plan.hauteur:.0f} de feuilles.csv (PNG retenu).")
            plan.largeur, plan.hauteur = reel
            plan.source_dims = "PNG"
        if plan.largeur is None:
            anomalies.append(f"Feuille IA {stem} : taille du raster inconnue.")
        if plan.nom != stem:
            anomalies.append(f"Plan IA « {plan.nom} » pointe sur le raster {plan.fichier} : "
                             f"la feuille retenue est {stem}.")
    return anomalies


# --- Recalage géométrique -----------------------------------------------------

def identite(humain: Plan, ia: Plan) -> Transfo:
    return Transfo(0, ia.largeur / humain.largeur, ia.hauteur / humain.hauteur, 0.0, 0.0)


def evaluer(h: np.ndarray, ia: np.ndarray, transfo: Transfo, seuil: float) -> tuple[float, float, int]:
    """(score = part des marques humaines couvertes, F-mesure, nb couvertes).
    La précision est mesurée sur les marques IA situées dans l'emprise des
    marques humaines transformées : elle pénalise un recalage qui « écrase »
    le relevé humain sur une zone dense du relevé IA."""
    if len(h) == 0 or len(ia) == 0:
        return 0.0, 0.0, 0
    q = transfo.appliquer(h)
    distances, _ = cKDTree(ia).query(q)
    couverts = int((distances <= seuil).sum())
    rappel = couverts / len(h)
    bas, haut = q.min(axis=0) - seuil, q.max(axis=0) + seuil
    dedans = ia[((ia >= bas) & (ia <= haut)).all(axis=1)]
    precision = 0.0
    if len(dedans):
        d2, _ = cKDTree(q).query(dedans)
        precision = float((d2 <= seuil).mean())
    f = 2 * rappel * precision / (rappel + precision) if rappel + precision else 0.0
    return rappel, f, couverts


def affiner(h: np.ndarray, ia: np.ndarray, transfo: Transfo, seuil: float) -> Transfo:
    """Moindres carrés (échelle + translation par axe) sur les plus proches voisins."""
    courant = transfo
    for _ in range(3):
        q = courant.appliquer(h)
        distances, indices = cKDTree(ia).query(q)
        garde = distances <= seuil
        if garde.sum() < 3:
            return courant
        p = (h[garde] @ ROTATIONS[courant.k][1].T)
        cible = ia[indices[garde]]
        params = []
        for axe, echelle_actuelle in ((0, courant.sx), (1, courant.sy)):
            if np.ptp(p[:, axe]) < 1e-6:
                params.append((echelle_actuelle, float(np.mean(cible[:, axe] - echelle_actuelle * p[:, axe]))))
            else:
                a, b = np.polyfit(p[:, axe], cible[:, axe], 1)
                params.append((float(a), float(b)))
        nouveau = Transfo(courant.k, params[0][0], params[1][0], params[0][1], params[1][1])
        # Garde-fou : l'ajustement ne corrige qu'un léger écart d'échelle ou
        # de cadrage ; il ne doit ni retourner ni « écraser » le relevé.
        rapports = (nouveau.sx / transfo.sx, nouveau.sy / transfo.sy)
        if not all(1 - AJUSTEMENT_MAX <= r <= 1 + AJUSTEMENT_MAX for r in rapports):
            return courant
        if nouveau == courant:
            break
        courant = nouveau
    return courant


def _echantillon(xy: np.ndarray) -> np.ndarray:
    pas = max(1, math.ceil(len(xy) / ECHANTILLON_VOTE))
    return xy[::pas]


def chercher(h: np.ndarray, ia: np.ndarray, seuil: float, echelles: np.ndarray,
             rotations: tuple[int, ...], t_max: float | None = None,
             t_centre: tuple[float, float] = (0.0, 0.0),
             candidats: int = 8) -> tuple[Transfo, float, float, int] | None:
    """Recherche (orientation, échelle uniforme) × translation par vote."""
    if len(h) == 0 or len(ia) == 0:
        return None
    hs, ias = _echantillon(h), _echantillon(ia)
    votes: list[tuple[int, int, float, float, float]] = []
    for k in rotations:
        tourne = hs @ ROTATIONS[k][1].T
        for s in echelles:
            decal = (ias[None, :, :] - (tourne * s)[:, None, :]).reshape(-1, 2)
            if t_max is not None:
                decal = decal[(np.abs(decal - np.array(t_centre)) <= t_max).all(axis=1)]
                if len(decal) == 0:
                    continue
            cases = np.floor(decal / seuil).astype(np.int64)
            cles = cases[:, 0] * 1_000_003 + cases[:, 1]
            uniques, comptes = np.unique(cles, return_counts=True)
            j = int(np.argmax(comptes))
            t = np.median(decal[cles == uniques[j]], axis=0)
            votes.append((int(comptes[j]), k, float(s), float(t[0]), float(t[1])))
    if not votes:
        return None
    votes.sort(key=lambda v: (-v[0], v[1], v[2]))
    meilleur: tuple[Transfo, float, float, int] | None = None
    for _, k, s, tx, ty in votes[:candidats]:
        brut = Transfo(k, s, s, tx, ty)
        fin = affiner(h, ia, brut, seuil)
        for transfo in (fin, brut):
            score, f, n = evaluer(h, ia, transfo, seuil)
            cle = (score, f)
            if meilleur is None or cle > (meilleur[1], meilleur[2]):
                meilleur = (transfo, score, f, n)
    return meilleur


def _grille(centre: float, bas: float, haut: float) -> np.ndarray:
    return np.exp(np.arange(math.log(centre * bas), math.log(centre * haut) + 1e-9, PAS_ECHELLE))


def echelle_nominale(humain: Plan, ia: Plan) -> float:
    return math.sqrt((ia.largeur * ia.hauteur) / (humain.largeur * humain.hauteur))


# --- Appariement des pages -----------------------------------------------------

@dataclass
class ResultatPages:
    paires: list[PairePage]
    non_appariees: list[tuple[Plan, str]]
    anomalies: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Contrainte:
    """Espace de recherche : échelle relative au nominal, orientations,
    translation (relative aux dimensions du raster IA) et sa tolérance
    (fraction de la diagonale IA ; None = libre)."""
    relatif: tuple[float, float] = PLAGE_ECHELLE
    centre_rel: float = 1.0
    rotations: tuple[int, ...] = tuple(range(8))
    t_rel: tuple[float, float] = (0.0, 0.0)
    t_tol: float | None = None


def contrainte_initiale(humain: Plan) -> Contrainte:
    """Page riche (≥ 20 marques) : recherche libre (8 orientations, échelle
    0,7–1,4 × nominal). Page pauvre : seulement au voisinage de l'identité
    (même cadrage sur une autre feuille, cas des addendas) — une recherche
    libre sur quelques marques trouve toujours un recalage « parfait »."""
    if len(humain.marques) >= CONSENSUS_MARQUES:
        return Contrainte()
    return Contrainte((1 - CONSENSUS_TOL, 1 + CONSENSUS_TOL), 1.0, (0,), (0.0, 0.0), TRANSLATION_TOL)


def _recherche_toutes(humain: Plan, ias: list[Plan], contrainte: Contrainte) -> list[Recalage]:
    resultats: list[Recalage] = []
    h = humain.xy
    for ia in ias:
        if len(ia.marques) < 3 or ia.largeur is None:
            continue
        seuil = SEUIL_PAGE * ia.diagonale
        nominal = echelle_nominale(humain, ia) * contrainte.centre_rel
        t_max = contrainte.t_tol * ia.diagonale if contrainte.t_tol is not None else None
        t_centre = (contrainte.t_rel[0] * ia.largeur, contrainte.t_rel[1] * ia.hauteur)
        trouve = chercher(h, ia.xy, seuil, _grille(nominal, *contrainte.relatif), contrainte.rotations,
                          t_max, t_centre)
        if trouve:
            transfo, score, f, n = trouve
            resultats.append(Recalage(ia.feuille, transfo, score, f, n))
    resultats.sort(key=lambda r: (-r.score, -r.f_mesure, r.feuille))
    # départage : à score quasi égal, la meilleure F-mesure l'emporte
    if len(resultats) > 1:
        tete = [r for r in resultats if resultats[0].score - r.score <= EGALITE_SCORE]
        gagnant = max(tete, key=lambda r: (r.f_mesure, r.score))
        resultats.remove(gagnant)
        resultats.insert(0, gagnant)
    return resultats


def estimer_dimensions_inconnues(humains: list[Plan], ia_par_page: dict, anomalies: list[str]) -> None:
    """Rasters humains sans dimensions : échelle ajustée sur la page de même nom
    (orientation 0, translation bornée), puis médiane propagée au document."""
    estimees: dict[str, list[tuple[float, float]]] = defaultdict(list)
    sans: list[Plan] = [p for p in humains if p.largeur is None and p.marques]
    for plan in sans:
        ia = ia_par_page.get((normaliser_nom(plan.base), plan.page))
        if ia is None or ia.largeur is None or len(ia.marques) < MARQUES_MIN_GEOMETRIE \
                or len(plan.marques) < MARQUES_MIN_GEOMETRIE:
            continue
        seuil = SEUIL_PAGE * ia.diagonale
        trouve = chercher(plan.xy, ia.xy, seuil, _grille(1.0, 0.1, 10.0), (0,),
                          t_max=TRANSLATION_MAX_INCONNU * ia.diagonale)
        if trouve and trouve[1] >= 0.6:
            transfo = trouve[0]
            plan.largeur, plan.hauteur = ia.largeur / transfo.sx, ia.hauteur / transfo.sy
            plan.source_dims = f"estimées par recalage sur {ia.feuille} (score {trouve[1]:.2f})"
            estimees[normaliser_nom(plan.base)].append((plan.largeur, plan.hauteur))
    for plan in sans:
        if plan.largeur is None and estimees.get(normaliser_nom(plan.base)):
            valeurs = np.array(estimees[normaliser_nom(plan.base)])
            plan.largeur, plan.hauteur = (float(v) for v in np.median(valeurs, axis=0))
            plan.source_dims = "estimées (médiane du document)"
        if plan.largeur is None:
            anomalies.append(f"Page humaine « {plan.nom} » : taille du raster inconnue et non estimable.")
        else:
            anomalies.append(f"Page humaine « {plan.nom} » : raster absent du fichier de dimensions, "
                             f"taille {plan.source_dims} ≈ {plan.largeur:.0f}×{plan.hauteur:.0f} px.")


def apparier_pages(humains: list[Plan], ias: list[Plan]) -> ResultatPages:
    anomalies: list[str] = []
    ia_par_feuille = {p.feuille: p for p in ias}
    ia_par_page = {(normaliser_nom(p.base), p.page): p for p in ias if p.base and p.page is not None}
    estimer_dimensions_inconnues(humains, ia_par_page, anomalies)

    paires: list[PairePage] = []
    non: list[tuple[Plan, str]] = []
    a_chercher: list[tuple[Plan, Plan | None, Recalage | None]] = []
    for humain in humains:
        candidat = ia_par_page.get((normaliser_nom(humain.base), humain.page))
        if not humain.marques:
            if candidat is not None:
                paires.append(PairePage(humain, candidat.feuille, "nom", None, None, "page sans marque",
                                        nom_candidat=candidat.feuille))
            continue
        if humain.largeur is None:
            if candidat is not None:
                paires.append(PairePage(humain, candidat.feuille, "nom", None, None,
                                        "taille du raster humain inconnue : marques non positionnables",
                                        nom_candidat=candidat.feuille))
            else:
                non.append((humain, "taille du raster humain inconnue, aucun nom commun"))
            continue
        ident: Recalage | None = None
        if candidat is not None and candidat.largeur is not None:
            transfo = identite(humain, candidat)
            seuil = SEUIL_PAGE * candidat.diagonale
            score, f, n = evaluer(humain.xy, candidat.xy, transfo, seuil)
            if len(candidat.marques) >= 3 and score >= SCORE_PAGE_MIN:
                affine = affiner(humain.xy, candidat.xy, transfo, seuil)
                s2, f2, n2 = evaluer(humain.xy, candidat.xy, affine, seuil)
                if s2 >= score:
                    transfo, score, f, n = affine, s2, f2, n2
            ident = Recalage(candidat.feuille, transfo, score, f, n)
            if score >= SCORE_PAGE_MIN or len(humain.marques) < MARQUES_MIN_GEOMETRIE:
                paires.append(PairePage(humain, candidat.feuille, "nom", transfo, score,
                                        nom_candidat=candidat.feuille))
                continue
        if len(humain.marques) < MARQUES_MIN_GEOMETRIE:
            non.append((humain, f"aucun nom commun et moins de {MARQUES_MIN_GEOMETRIE} marques"))
            continue
        a_chercher.append((humain, candidat, ident))

    # Recherche géométrique, puis consensus d'échelle/orientation par document.
    recherches: dict[str, list[Recalage]] = {}
    for humain, _, _ in a_chercher:
        recherches[humain.nom] = _recherche_toutes(humain, ias, contrainte_initiale(humain))
    # Consensus par document : échelle, orientation(s) et translation des
    # recalages sûrs, imposés ensuite à toutes les pages du même document.
    par_doc: dict[str, list[tuple[float, int, float, float]]] = defaultdict(list)
    for humain, _, _ in a_chercher:
        res = recherches[humain.nom]
        if res and res[0].score >= CONSENSUS_SCORE and len(humain.marques) >= CONSENSUS_MARQUES:
            ia = ia_par_feuille[res[0].feuille]
            t = res[0].transfo
            par_doc[normaliser_nom(humain.base)].append(
                (t.echelle / echelle_nominale(humain, ia), t.k, t.tx / ia.largeur, t.ty / ia.hauteur))
    consensus: dict[str, Contrainte] = {}
    for doc, surs in sorted(par_doc.items()):
        valeurs = np.array([(s, tx, ty) for s, _, tx, ty in surs])
        med = np.median(valeurs, axis=0)
        rotations = tuple(sorted({k for _, k, _, _ in surs}))
        consensus[doc] = Contrainte((1 - CONSENSUS_TOL, 1 + CONSENSUS_TOL), float(med[0]), rotations,
                                    (float(med[1]), float(med[2])), TRANSLATION_TOL)
        anomalies.append(
            f"Recalage géométrique, document « {doc} » : {len(surs)} page(s) sûre(s), échelle relative "
            f"médiane {med[0]:.3f} × nominal, orientation(s) {', '.join(ROTATIONS[k][0] for k in rotations)}, "
            f"translation médiane ({100 * med[1]:.1f} %, {100 * med[2]:.1f} %) du raster IA — imposées à "
            f"toutes les pages du document (± {100 * CONSENSUS_TOL:.0f} % d'échelle, "
            f"± {100 * TRANSLATION_TOL:.0f} % de diagonale).")
    for humain, _, _ in a_chercher:
        contrainte = consensus.get(normaliser_nom(humain.base))
        if contrainte is not None:
            recherches[humain.nom] = _recherche_toutes(humain, ias, contrainte)

    for humain, candidat, ident in a_chercher:
        res = recherches[humain.nom]
        meilleur = res[0] if res else None
        second = res[1] if len(res) > 1 else None
        # Un nom commun n'est contredit que par un recalage sûr (≥ 0,8).
        minimum = SCORE_PAGE_MIN
        if candidat is not None and meilleur is not None and meilleur.feuille != candidat.feuille:
            minimum = SCORE_REMPLACE_NOM
        if meilleur is not None and meilleur.score >= minimum and meilleur.couverts >= 3:
            note = ""
            if candidat is not None and candidat.feuille != meilleur.feuille:
                note = (f"le nom désignait {candidat.feuille} (score identité "
                        f"{ident.score:.2f}) ; la géométrie désigne {meilleur.feuille}")
            elif candidat is not None:
                note = f"même feuille que le nom, recalée (identité {ident.score:.2f})"
            if second is not None and meilleur.score - second.score < AMBIGU_ECART:
                note = (note + " ; " if note else "") + (
                    f"AMBIGU : {second.feuille} obtient {second.score:.2f}")
            paires.append(PairePage(humain, meilleur.feuille, "géométrie", meilleur.transfo,
                                    meilleur.score, note, second,
                                    candidat.feuille if candidat else None))
        elif candidat is not None:
            paires.append(PairePage(humain, candidat.feuille, "nom", ident.transfo if ident else None,
                                    ident.score if ident else None,
                                    f"recalage faible (identité {ident.score:.2f}) : aucune autre feuille IA "
                                    f"ne dépasse {SCORE_REMPLACE_NOM} ; appariement par nom conservé"
                                    if ident else "appariement par nom conservé sans recalage",
                                    meilleur, candidat.feuille))
        else:
            detail = (f"meilleure feuille {meilleur.feuille} à {meilleur.score:.2f}" if meilleur
                      else "aucune feuille IA marquée")
            non.append((humain, f"aucun nom commun ; géométrie insuffisante ({detail})"))
    ordre = {p.nom: i for i, p in enumerate(humains)}
    paires.sort(key=lambda p: ordre[p.humain.nom])
    return ResultatPages(paires, non, anomalies)


# --- Fusion des pages humaines en double ---------------------------------------

@dataclass
class MarqueRecalee:
    marque: Marque
    x_ia: float | None
    y_ia: float | None
    doublon_de: str | None = None


@dataclass
class Doublon:
    feuille: str
    page: str
    page_reference: str
    doublons: int
    total: int
    nature: str             # "copie" | "version remplacée" | "recouvrement partiel"


def _priorite(paire: PairePage) -> tuple:
    """Page de référence d'une feuille IA : celle que le nom désigne, puis un
    addenda (version la plus récente), puis la plus marquée."""
    return (paire.nom_candidat != paire.feuille or paire.methode != "nom",
            "addenda" not in normaliser_nom(paire.humain.base),
            -len(paire.humain.marques), paire.humain.nom)


def fusionner(paires: list[PairePage], ia_par_feuille: dict[str, Plan]
              ) -> tuple[dict[str, list[MarqueRecalee]], list[Doublon]]:
    """Marques humaines recalées dans le repère IA, groupées par feuille IA.

    Plusieurs pages humaines sur la même feuille IA : chaque page est
    confrontée aux marques déjà retenues par affectation optimale un-à-un,
    sans tenir compte des libellés (seuil = celui des marques). Les marques
    appariées sont des doublons, exclues du décompte.
    - Même document (copie du raster, ex. « 41 (2) (1) ») : on garde l'union.
    - Documents différents (original + addenda, libellés souvent préfixés
      « ADD ») et ≥ 50 % de doublons : la page est une version remplacée,
      exclue entièrement.
    """
    par_feuille: dict[str, list[PairePage]] = defaultdict(list)
    for paire in paires:
        if paire.feuille and paire.humain.marques:
            par_feuille[paire.feuille].append(paire)
    resultat: dict[str, list[MarqueRecalee]] = {}
    doublons: list[Doublon] = []
    for feuille, groupe in par_feuille.items():
        ia = ia_par_feuille[feuille]
        tolerance = SEUIL_MARQUE * ia.diagonale if ia.largeur else 0.0
        groupe = sorted(groupe, key=_priorite)
        gardees: list[MarqueRecalee] = []
        base_reference = normaliser_nom(groupe[0].humain.base)
        for paire in groupe:
            if paire.transfo is None:
                recalees = [MarqueRecalee(m, None, None) for m in paire.humain.marques]
            else:
                q = paire.transfo.appliquer(paire.humain.xy)
                recalees = [MarqueRecalee(m, float(x), float(y)) for m, (x, y) in zip(paire.humain.marques, q)]
            existantes = [g for g in gardees if g.x_ia is not None and g.doublon_de is None]
            positionnees = [r for r in recalees if r.x_ia is not None]
            if existantes and positionnees:
                res = apparier_marques(positionnees, [g.marque for g in existantes], tolerance,
                                       cibles_xy=np.array([(g.x_ia, g.y_ia) for g in existantes]))
                reference = Counter()
                for c in res.couples:
                    c.humain.doublon_de = c.ia.ident
                    reference[c.ia.plan] += 1
                n = len(res.couples)
                if n:
                    meme_doc = normaliser_nom(paire.humain.base) == base_reference
                    nature = "copie"
                    if not meme_doc:
                        if n >= 0.5 * len(recalees):
                            nature = "version remplacée"
                            ref = reference.most_common(1)[0][0]
                            for r in recalees:
                                r.doublon_de = r.doublon_de or f"version remplacée par {ref}"
                        else:
                            nature = "recouvrement partiel"
                    doublons.append(Doublon(feuille, paire.humain.nom, reference.most_common(1)[0][0],
                                            sum(1 for r in recalees if r.doublon_de), len(recalees), nature))
            gardees.extend(recalees)
        resultat[feuille] = gardees
    return resultat, doublons


# --- Appariement des marques ----------------------------------------------------

@dataclass
class Couple:
    humain: MarqueRecalee
    ia: Marque
    distance: float


@dataclass
class ResultatMarques:
    couples: list[Couple]
    manquantes: list[MarqueRecalee]     # humain seul
    en_trop: list[Marque]               # IA seul


def apparier_marques(humaines: list[MarqueRecalee], ia: list[Marque], seuil: float,
                     cibles_xy: np.ndarray | None = None,
                     probabilites: dict[str, dict[str, float]] | None = None) -> ResultatMarques:
    """Affectation optimale un-à-un (distance euclidienne), couples au-delà du
    seuil rejetés. `cibles_xy` remplace les coordonnées des cibles si fourni.

    `probabilites` (P(libellé IA | libellé humain), issue d'une première passe
    sans libellés) ajoute au coût d'un couple admissible une pénalité
    PENALITE_LIBELLE × seuil × (1 − P) : entre marques voisines (ex. deux
    appareils superposés), le couple de libellés cohérent l'emporte. Le
    nombre de couples n'en dépend pas (les couples hors seuil coûtent 1e9,
    l'affectation maximise donc d'abord le nombre de couples admissibles)."""
    positionnables = [h for h in humaines if h.x_ia is not None]
    non_position = [h for h in humaines if h.x_ia is None]
    if not positionnables or not ia:
        return ResultatMarques([], positionnables + non_position, list(ia))
    a = np.array([(h.x_ia, h.y_ia) for h in positionnables])
    b = cibles_xy if cibles_xy is not None else np.array([(m.x, m.y) for m in ia])
    distances = np.hypot(a[:, None, 0] - b[None, :, 0], a[:, None, 1] - b[None, :, 1])
    cout = distances.copy()
    if probabilites is not None:
        penalite = np.array([[1.0 - probabilites.get(h.marque.libelle, {}).get(m.libelle, 0.0) for m in ia]
                             for h in positionnables])
        cout = cout + PENALITE_LIBELLE * seuil * penalite
    cout = np.where(distances <= seuil, cout, 1e9)
    lignes, colonnes = linear_sum_assignment(cout)
    couples, pris_h, pris_ia = [], set(), set()
    for i, j in zip(lignes, colonnes):
        if distances[i, j] <= seuil:
            couples.append(Couple(positionnables[i], ia[j], float(distances[i, j])))
            pris_h.add(i)
            pris_ia.add(j)
    manquantes = [h for i, h in enumerate(positionnables) if i not in pris_h] + non_position
    en_trop = [m for j, m in enumerate(ia) if j not in pris_ia]
    return ResultatMarques(couples, manquantes, en_trop)


# --- Comparaison complète -------------------------------------------------------

@dataclass
class Comparaison:
    humains: list[Plan]
    ias: list[Plan]
    pages: ResultatPages
    doublons: list[Doublon]
    humaines_par_feuille: dict[str, list[MarqueRecalee]]
    resultats: dict[float, dict[str, ResultatMarques]]   # seuil → feuille → résultat
    manquantes_hors_page: list[Marque]                   # pages humaines non appariées
    en_trop_hors_page: dict[str, list[Marque]]           # feuilles IA sans page humaine
    anomalies: list[str]

    def ia_par_feuille(self) -> dict[str, Plan]:
        return {p.feuille: p for p in self.ias}


def comparer(humains: list[Plan], ias: list[Plan], anomalies_entree: list[str] | None = None) -> Comparaison:
    anomalies = list(anomalies_entree or [])
    pages = apparier_pages(humains, ias)
    anomalies.extend(pages.anomalies)
    ia_par_feuille = {p.feuille: p for p in ias}
    humaines_par_feuille, doublons = fusionner(pages.paires, ia_par_feuille)
    def passe(seuil_rel: float, probabilites: dict[str, dict[str, float]] | None) -> dict[str, ResultatMarques]:
        par_feuille = {}
        for feuille, humaines in humaines_par_feuille.items():
            ia = ia_par_feuille[feuille]
            uniques = [h for h in humaines if h.doublon_de is None]
            par_feuille[feuille] = apparier_marques(uniques, ia.marques, seuil_rel * ia.diagonale,
                                                    probabilites=probabilites)
        return par_feuille

    # Passe 1 : positions seules → P(libellé IA | libellé humain).
    compte: dict[str, Counter] = defaultdict(Counter)
    for res in passe(SEUIL_MARQUE, None).values():
        for couple in res.couples:
            compte[couple.humain.marque.libelle][couple.ia.libelle] += 1
    probabilites = {h: {i: n / sum(c.values()) for i, n in c.items()} for h, c in compte.items()}
    # Passe 2 : mêmes positions, voisins départagés par le libellé.
    resultats = {seuil_rel: passe(seuil_rel, probabilites) for seuil_rel in SEUILS_SENSIBILITE}
    hors_page = [m for plan, _ in pages.non_appariees for m in plan.marques]
    sans_humain = {p.feuille: list(p.marques) for p in ias
                   if p.marques and p.feuille not in humaines_par_feuille}
    return Comparaison(humains, ias, pages, doublons, humaines_par_feuille, resultats,
                       hors_page, sans_humain, anomalies)


# --- Libellés -------------------------------------------------------------------

@dataclass
class Correspondance:
    libelle_humain: str
    libelle_ia: str | None
    proportion: float
    appariees: int
    repartition: Counter


def table_libelles(comp: Comparaison) -> dict[str, Correspondance]:
    compte: dict[str, Counter] = defaultdict(Counter)
    for res in comp.resultats[SEUIL_MARQUE].values():
        for couple in res.couples:
            compte[couple.humain.marque.libelle][couple.ia.libelle] += 1
    table = {}
    for libelle in sorted({m.libelle for p in comp.humains for m in p.marques}):
        repartition = compte.get(libelle, Counter())
        n = sum(repartition.values())
        if n:
            cible, nb = sorted(repartition.items(), key=lambda kv: (-kv[1], kv[0]))[0]
            table[libelle] = Correspondance(libelle, cible, nb / n, n, repartition)
        else:
            table[libelle] = Correspondance(libelle, None, 0.0, 0, repartition)
    return table


# --- Écriture -------------------------------------------------------------------

def _f(v: float | None, n: int = 4) -> str:
    return "" if v is None else f"{v:.{n}f}"


def _pct(a: float, b: float) -> str:
    return f"{100 * a / b:.1f} %" if b else "—"


def _md(texte: str) -> str:
    return str(texte).replace("|", "\\|")


def totaux(comp: Comparaison, seuil: float = SEUIL_MARQUE) -> dict[str, int]:
    res = comp.resultats[seuil]
    humaines_uniques = sum(1 for lst in comp.humaines_par_feuille.values() for h in lst if h.doublon_de is None)
    humaines_uniques += len(comp.manquantes_hors_page)
    appariees = sum(len(r.couples) for r in res.values())
    ia_total = sum(len(p.marques) for p in comp.ias)
    return {
        "humaines_brutes": sum(len(p.marques) for p in comp.humains),
        "doublons": sum(1 for lst in comp.humaines_par_feuille.values() for h in lst if h.doublon_de),
        "humaines": humaines_uniques,
        "ia": ia_total,
        "appariees": appariees,
        "manquantes": humaines_uniques - appariees,
        "en_trop": ia_total - appariees,
    }


def ecrire_sorties(comp: Comparaison, sortie: Path, entrees: dict[str, str]) -> dict[str, int]:
    sortie.mkdir(parents=True, exist_ok=True)
    ia_par_feuille = comp.ia_par_feuille()
    table = table_libelles(comp)
    res = comp.resultats[SEUIL_MARQUE]
    tot = totaux(comp)
    humains_de_feuille: dict[str, list[str]] = defaultdict(list)
    for paire in comp.pages.paires:
        if paire.feuille and paire.humain.marques:
            humains_de_feuille[paire.feuille].append(paire.humain.nom)
    plan_humain = {p.nom: p for p in comp.humains}

    # appariement.csv -----------------------------------------------------------
    statut_h: dict[str, tuple[str, str, float | None, str]] = {}
    statut_ia: dict[str, tuple[str, str, float | None, str]] = {}
    for feuille, r in res.items():
        for c in r.couples:
            statut_h[c.humain.marque.ident] = ("appariée", c.ia.ident, c.distance, c.ia.libelle)
            statut_ia[c.ia.ident] = ("appariée", c.humain.marque.ident, c.distance, c.humain.marque.libelle)
    with (sortie / "appariement.csv").open("w", encoding="utf-8", newline="") as flux:
        w = csv.writer(flux)
        w.writerow(["cote", "page_humaine", "feuille_ia", "libelle", "x_px", "y_px", "x_norm", "y_norm",
                    "x_px_ia", "y_px_ia", "statut", "id", "id_apparie", "libelle_apparie", "distance_px_ia"])
        for feuille, humaines in comp.humaines_par_feuille.items():
            for h in humaines:
                plan = plan_humain[h.marque.plan]
                if h.doublon_de:
                    nature = "version remplacée" if h.doublon_de.startswith("version") else "doublon"
                    statut = (f"exclue ({nature})", h.doublon_de, None, "")
                else:
                    statut = statut_h.get(h.marque.ident, ("manquante IA", "", None, ""))
                w.writerow(["humain", plan.nom, feuille, h.marque.libelle, _f(h.marque.x, 0), _f(h.marque.y, 0),
                            _f(h.marque.x / plan.largeur if plan.largeur else None),
                            _f(h.marque.y / plan.hauteur if plan.hauteur else None),
                            _f(h.x_ia, 0), _f(h.y_ia, 0), statut[0], h.marque.ident, statut[1], statut[3],
                            _f(statut[2], 1)])
        for m in comp.manquantes_hors_page:
            plan = plan_humain[m.plan]
            w.writerow(["humain", plan.nom, "", m.libelle, _f(m.x, 0), _f(m.y, 0),
                        _f(m.x / plan.largeur if plan.largeur else None),
                        _f(m.y / plan.hauteur if plan.hauteur else None), "", "",
                        "manquante IA (page non appariée)", m.ident, "", "", ""])
        for ia in comp.ias:
            for m in ia.marques:
                if ia.feuille in comp.humaines_par_feuille:
                    statut = statut_ia.get(m.ident, ("en trop IA", "", None, ""))
                else:
                    statut = ("en trop IA (feuille sans page humaine)", "", None, "")
                w.writerow(["ia", " + ".join(humains_de_feuille.get(ia.feuille, [])), ia.feuille, m.libelle,
                            _f(m.x, 0), _f(m.y, 0), _f(m.x / ia.largeur if ia.largeur else None),
                            _f(m.y / ia.hauteur if ia.hauteur else None), _f(m.x, 0), _f(m.y, 0),
                            statut[0], m.ident, statut[1], statut[3], _f(statut[2], 1)])

    # correspondance-libelles.csv -------------------------------------------------
    ia_compte = Counter(m.libelle for p in comp.ias for m in p.marques)
    h_compte = Counter(h.marque.libelle for lst in comp.humaines_par_feuille.values() for h in lst
                       if h.doublon_de is None)
    h_compte.update(m.libelle for m in comp.manquantes_hors_page)
    manq_lib = Counter(h.marque.libelle for r in res.values() for h in r.manquantes)
    manq_lib.update(m.libelle for m in comp.manquantes_hors_page)
    groupe: dict[str, list[str]] = defaultdict(list)
    for lib, c in table.items():
        if c.libelle_ia:
            groupe[c.libelle_ia].append(lib)
    mauvais_type: list[Couple] = []
    mauvais_par_lib: Counter = Counter()
    for r in res.values():
        for c in r.couples:
            cible = table[c.humain.marque.libelle].libelle_ia
            if cible is not None and c.ia.libelle != cible:
                mauvais_type.append(c)
                mauvais_par_lib[c.humain.marque.libelle] += 1
    lignes_lib = []
    for lib in sorted(h_compte, key=lambda l: (-h_compte[l], l)):
        c = table[lib]
        ia_n = ia_compte.get(c.libelle_ia, 0) if c.libelle_ia else 0
        partage = groupe.get(c.libelle_ia, [lib]) if c.libelle_ia else [lib]
        h_groupe = sum(h_compte[l] for l in partage)
        lignes_lib.append({
            "libelle_humain": lib, "libelle_ia": c.libelle_ia or "", "proportion": f"{c.proportion:.2f}",
            "appariees": c.appariees, "humain": h_compte[lib], "ia_libelle_total": ia_n,
            "humain_groupe": h_groupe, "ecart_groupe": ia_n - h_groupe if c.libelle_ia else "",
            "libelles_humains_partages": " ; ".join(partage) if len(partage) > 1 else "",
            "manquantes_ia": manq_lib.get(lib, 0),
            "meme_position_libelle_different": mauvais_par_lib.get(lib, 0),
            "repartition": " ; ".join(f"{k}={v}" for k, v in c.repartition.most_common()),
        })
    with (sortie / "correspondance-libelles.csv").open("w", encoding="utf-8", newline="") as flux:
        champs = list(lignes_lib[0].keys()) if lignes_lib else ["libelle_humain"]
        w = csv.DictWriter(flux, fieldnames=champs)
        w.writeheader()
        w.writerows(lignes_lib)
    cibles = {c.libelle_ia for c in table.values() if c.libelle_ia}
    ia_sans = sorted((lib for lib in ia_compte if lib not in cibles), key=lambda l: (-ia_compte[l], l))
    h_sans = sorted((lib for lib in h_compte if table[lib].libelle_ia is None), key=lambda l: (-h_compte[l], l))

    # pages.csv --------------------------------------------------------------------
    lignes_pages = []
    doublons_par_page = {d.page: d for d in comp.doublons}
    for paire in comp.pages.paires:
        h = paire.humain
        if not h.marques and not h.lignes:
            continue
        r = res.get(paire.feuille) if paire.feuille else None
        mes = [x for x in comp.humaines_par_feuille.get(paire.feuille, []) if x.marque.plan == h.nom]
        uniques = {x.marque.ident for x in mes if x.doublon_de is None}
        app = sum(1 for c in r.couples if c.humain.marque.ident in uniques) if r else 0
        d = doublons_par_page.get(h.nom)
        lignes_pages.append({
            "page_humaine": h.nom, "document": h.base, "page": h.page or "",
            "feuille_ia": paire.feuille or "", "plan_ia": _nom_plan_ia(ia_par_feuille, paire.feuille),
            "methode": paire.methode, "score": _f(paire.score, 3),
            "transformation": paire.transfo.decrire() if paire.transfo else "",
            "dims_humain": f"{h.largeur:.0f}x{h.hauteur:.0f} ({h.source_dims})" if h.largeur else "inconnues",
            "marques_humain": len(h.marques), "doublons": d.doublons if d else 0,
            "marques_ia_feuille": len(ia_par_feuille[paire.feuille].marques) if paire.feuille else "",
            "appariees": app, "manquantes_ia": len(uniques) - app,
            "en_trop_ia_feuille": len(r.en_trop) if r else "",
            "lignes_humain": len(h.lignes),
            "lignes_ia_feuille": len(ia_par_feuille[paire.feuille].lignes) if paire.feuille else "",
            "second_candidat": f"{paire.second.feuille} ({paire.second.score:.2f})" if paire.second else "",
            "note": paire.note,
        })
    for plan, raison in comp.pages.non_appariees:
        lignes_pages.append({
            "page_humaine": plan.nom, "document": plan.base, "page": plan.page or "", "feuille_ia": "",
            "plan_ia": "", "methode": "non appariée", "score": "", "transformation": "",
            "dims_humain": f"{plan.largeur:.0f}x{plan.hauteur:.0f} ({plan.source_dims})" if plan.largeur else "inconnues",
            "marques_humain": len(plan.marques), "doublons": 0, "marques_ia_feuille": "", "appariees": 0,
            "manquantes_ia": len(plan.marques), "en_trop_ia_feuille": "", "lignes_humain": len(plan.lignes),
            "lignes_ia_feuille": "", "second_candidat": "", "note": raison,
        })
    for feuille, marques in comp.en_trop_hors_page.items():
        ia = ia_par_feuille[feuille]
        lignes_pages.append({
            "page_humaine": "", "document": ia.base, "page": ia.page or "", "feuille_ia": feuille,
            "plan_ia": ia.nom, "methode": "feuille IA sans page humaine", "score": "", "transformation": "",
            "dims_humain": "", "marques_humain": 0, "doublons": 0, "marques_ia_feuille": len(marques),
            "appariees": 0, "manquantes_ia": 0, "en_trop_ia_feuille": len(marques), "lignes_humain": 0,
            "lignes_ia_feuille": len(ia.lignes), "second_candidat": "", "note": "",
        })
    with (sortie / "pages.csv").open("w", encoding="utf-8", newline="") as flux:
        w = csv.DictWriter(flux, fieldnames=list(lignes_pages[0].keys()) if lignes_pages else ["page_humaine"])
        w.writeheader()
        w.writerows(lignes_pages)

    # ecart-dupuis.md ----------------------------------------------------------------
    pages_h_marquees = [p for p in comp.humains if p.marques]
    appariees_h = [p for p in comp.pages.paires if p.humain.marques and p.feuille]
    ia_marquees = [p for p in comp.ias if p.marques]
    ia_avec_h = [p for p in ia_marquees if p.feuille in comp.humaines_par_feuille]
    L: list[str] = []
    L.append(f"# Écart relevé humain (Dupuis) / relevé IA — {entrees.get('dossier', '')}".rstrip(" —"))
    L.append("")
    L.append(f"_Généré le {date.today().isoformat()} par `src.validation.compare_qpl` — comparaison "
             "déterministe marque par marque ; aucun chiffre saisi à la main._")
    L.append("")
    L.append(f"- Humain : `{entrees['humain']}`")
    L.append(f"- IA : `{entrees['ia']}`")
    L.append(f"- Dimensions : `{entrees['dims']}` ; feuilles : `{entrees['feuilles']}`")
    L.append("")
    L.append("## Résumé")
    L.append("")
    L.append("| Indicateur | Valeur |")
    L.append("|---|---:|")
    L.append(f"| Pages humaines (toutes / avec marques) | {len(comp.humains)} / {len(pages_h_marquees)} |")
    L.append(f"| Feuilles IA (toutes / avec marques) | {len(comp.ias)} / {len(ia_marquees)} |")
    L.append(f"| Pages humaines marquées appariées / non appariées | {len(appariees_h)} / "
             f"{len(comp.pages.non_appariees)} |")
    L.append(f"| Feuilles IA marquées avec / sans page humaine | {len(ia_avec_h)} / {len(comp.en_trop_hors_page)} |")
    L.append(f"| Marques humaines brutes | {tot['humaines_brutes']} |")
    L.append(f"| … dont exclues (pages en double, versions remplacées) | {tot['doublons']} |")
    L.append(f"| **Marques humaines retenues** | **{tot['humaines']}** |")
    L.append(f"| **Marques IA** | **{tot['ia']}** |")
    L.append(f"| **Appariées** (seuil {100 * SEUIL_MARQUE:.1f} % diag.) | **{tot['appariees']}** |")
    L.append(f"| Manquantes côté IA (humain seul) | {tot['manquantes']} |")
    L.append(f"| En trop côté IA (IA seul) | {tot['en_trop']} |")
    L.append(f"| Rappel (appariées / humaines) | {_pct(tot['appariees'], tot['humaines'])} |")
    L.append(f"| Précision (appariées / IA) | {_pct(tot['appariees'], tot['ia'])} |")
    n_hors = len(comp.manquantes_hors_page)
    n_trop_hors = sum(len(v) for v in comp.en_trop_hors_page.values())
    L.append(f"| … manquantes sur pages humaines non appariées | {n_hors} |")
    L.append(f"| … en trop sur feuilles IA sans page humaine | {n_trop_hors} |")
    L.append(f"| Couples « même position, libellé différent » | {len(mauvais_type)} |")
    n_lignes_h = sum(len(p.lignes) for p in comp.humains)
    n_lignes_ia = sum(len(p.lignes) for p in comp.ias)
    L.append(f"| Lignes (longueurs) humain / IA — non appariées | {n_lignes_h} / {n_lignes_ia} |")
    L.append("")
    L.append("## Sensibilité au seuil d'appariement des marques")
    L.append("")
    L.append("| Seuil (% diagonale IA) | Appariées | Manquantes IA | En trop IA | Rappel | Précision |")
    L.append("|---:|---:|---:|---:|---:|---:|")
    for s in SEUILS_SENSIBILITE:
        t = totaux(comp, s)
        L.append(f"| {100 * s:.1f} % | {t['appariees']} | {t['manquantes']} | {t['en_trop']} | "
                 f"{_pct(t['appariees'], t['humaines'])} | {_pct(t['appariees'], t['ia'])} |")
    L.append("")
    if comp.anomalies or comp.doublons:
        L.append("## Anomalies et signalements")
        L.append("")
        for a in comp.anomalies:
            L.append(f"- {_md(a)}")
        for d in comp.doublons:
            if d.nature == "copie":
                etat = "page EN DOUBLE" if d.doublons == d.total else "copie partielle"
                detail = "doublons exclus du décompte, le reste est ajouté"
            elif d.nature == "version remplacée":
                etat = "VERSION REMPLACÉE"
                detail = "page entière exclue du décompte (autre document, même feuille IA)"
            else:
                etat = "recouvrement partiel"
                detail = "doublons exclus, le reste est ajouté"
            L.append(f"- {etat} : « {_md(d.page)} » → feuille {d.feuille} : {d.doublons}/{d.total} marques "
                     f"exclues, référence « {_md(d.page_reference)} » ({detail}).")
        for paire in comp.pages.paires:
            if paire.note and paire.humain.marques:
                L.append(f"- Page « {_md(paire.humain.nom)} » → {paire.feuille} ({paire.methode}) : {_md(paire.note)}.")
        L.append("")
    L.append("## Correspondance des libellés et décompte par libellé humain")
    L.append("")
    L.append("Libellé IA = libellé majoritaire parmi les marques IA appariées aux marques de ce libellé humain "
             "(proportion entre parenthèses). « IA total » = toutes les marques IA de ce libellé ; si plusieurs "
             "libellés humains pointent vers le même libellé IA, l'écart est calculé sur le groupe.")
    L.append("")
    L.append("| Libellé humain | Libellé IA (part) | Humain | Appariées | Manquantes IA | IA total | Écart groupe | "
             "Même pos., autre libellé |")
    L.append("|---|---|---:|---:|---:|---:|---:|---:|")
    for ligne in lignes_lib:
        cible = f"{_md(ligne['libelle_ia'])} ({float(ligne['proportion']) * 100:.0f} %)" if ligne["libelle_ia"] else "—"
        ecart = ligne["ecart_groupe"]
        ecart_txt = f"{ecart:+d}" if isinstance(ecart, int) else "—"
        if ligne["libelles_humains_partages"]:
            ecart_txt += " (groupe)"
        L.append(f"| {_md(ligne['libelle_humain'])} | {cible} | {ligne['humain']} | {ligne['appariees']} | "
                 f"{ligne['manquantes_ia']} | {ligne['ia_libelle_total']} | {ecart_txt} | "
                 f"{ligne['meme_position_libelle_different']} |")
    L.append("")
    L.append(f"**Libellés humains sans correspondance** ({len(h_sans)}) : "
             + (", ".join(f"{_md(l)} ({h_compte[l]})" for l in h_sans) or "aucun") + ".")
    L.append("")
    L.append(f"**Libellés IA sans correspondance** ({len(ia_sans)}) : "
             + (", ".join(f"{_md(l)} ({ia_compte[l]})" for l in ia_sans) or "aucun") + ".")
    L.append("")
    L.append("## Par page")
    L.append("")
    L.append("| Page humaine | Feuille IA | Méthode | Score | Humain | Doublons | IA feuille | Appariées | "
             "Manquantes IA | En trop IA |")
    L.append("|---|---|---|---:|---:|---:|---:|---:|---:|---:|")
    for lp in lignes_pages:
        if not lp["marques_humain"] and not lp["marques_ia_feuille"]:
            continue
        L.append(f"| {_md(lp['page_humaine']) or '—'} | {lp['feuille_ia'] or '—'} | {lp['methode']} | {lp['score']} | "
                 f"{lp['marques_humain']} | {lp['doublons']} | {lp['marques_ia_feuille']} | {lp['appariees']} | "
                 f"{lp['manquantes_ia']} | {lp['en_trop_ia_feuille']} |")
    L.append("")
    L.append("Les transformations de recalage (orientation, échelles, translation) sont dans `pages.csv`.")
    L.append("")
    L.append("## Marques manquantes côté IA (humain seul)")
    L.append("")
    L.append("| Page humaine | Feuille IA | Libellé humain | x_norm | y_norm | x px IA | y px IA |")
    L.append("|---|---|---|---:|---:|---:|---:|")
    for feuille, r in res.items():
        for h in sorted(r.manquantes, key=lambda h: (h.marque.plan, h.marque.libelle, h.y_ia or 0, h.x_ia or 0)):
            plan = plan_humain[h.marque.plan]
            L.append(f"| {_md(plan.nom)} | {feuille} | {_md(h.marque.libelle)} | "
                     f"{_f(h.marque.x / plan.largeur if plan.largeur else None, 3)} | "
                     f"{_f(h.marque.y / plan.hauteur if plan.hauteur else None, 3)} | "
                     f"{_f(h.x_ia, 0)} | {_f(h.y_ia, 0)} |")
    for m in comp.manquantes_hors_page:
        plan = plan_humain[m.plan]
        L.append(f"| {_md(plan.nom)} | — (page non appariée) | {_md(m.libelle)} | "
                 f"{_f(m.x / plan.largeur if plan.largeur else None, 3)} | "
                 f"{_f(m.y / plan.hauteur if plan.hauteur else None, 3)} | | |")
    L.append("")
    L.append("## Marques en trop côté IA (IA seul)")
    L.append("")
    L.append("| Feuille IA | Page(s) humaine(s) | Libellé IA | x_norm | y_norm | x px IA | y px IA |")
    L.append("|---|---|---|---:|---:|---:|---:|")
    for feuille, r in res.items():
        ia = ia_par_feuille[feuille]
        for m in sorted(r.en_trop, key=lambda m: (m.libelle, m.y, m.x)):
            L.append(f"| {feuille} | {_md(' + '.join(humains_de_feuille.get(feuille, [])))} | {_md(m.libelle)} | "
                     f"{m.x / ia.largeur:.3f} | {m.y / ia.hauteur:.3f} | {m.x:.0f} | {m.y:.0f} |")
    for feuille, marques in comp.en_trop_hors_page.items():
        ia = ia_par_feuille[feuille]
        for m in sorted(marques, key=lambda m: (m.libelle, m.y, m.x)):
            L.append(f"| {feuille} | — (aucune page humaine) | {_md(m.libelle)} | "
                     f"{_f(m.x / ia.largeur if ia.largeur else None, 3)} | "
                     f"{_f(m.y / ia.hauteur if ia.hauteur else None, 3)} | {m.x:.0f} | {m.y:.0f} |")
    L.append("")
    if mauvais_type:
        L.append("## Même position, libellé différent (probable mauvais type)")
        L.append("")
        L.append("| Feuille IA | Libellé humain | Libellé IA attendu | Libellé IA posé | x px IA | y px IA |")
        L.append("|---|---|---|---|---:|---:|")
        for c in sorted(mauvais_type, key=lambda c: (c.ia.plan, c.humain.marque.libelle, c.ia.y, c.ia.x)):
            L.append(f"| {c.ia.plan} | {_md(c.humain.marque.libelle)} | "
                     f"{_md(table[c.humain.marque.libelle].libelle_ia)} | {_md(c.ia.libelle)} | "
                     f"{c.ia.x:.0f} | {c.ia.y:.0f} |")
        L.append("")
    L.append("## Méthode et limites")
    L.append("")
    L.append(f"- Pages : nom (PDF, page) puis recalage géométrique (seuil {100 * SEUIL_PAGE:.1f} % diag., score ≥ "
             f"{SCORE_PAGE_MIN}, 8 orientations, échelle uniforme ± ajustement par axe). Marques : affectation "
             f"optimale sur la distance, seuil {100 * SEUIL_MARQUE:.1f} % de la diagonale du raster IA, sans "
             "tenir compte des libellés.")
    L.append("- Les coordonnées `X`/`Y` des éléments sont prises telles quelles (pas de correction de centre "
             "de symbole : l'écart est inférieur à 0,3 % de la diagonale).")
    L.append("- Les lignes (longueurs) sont seulement comptées ; elles ne sont pas comparées.")
    L.append("")
    (sortie / "ecart-dupuis.md").write_text("\n".join(L), encoding="utf-8")
    return tot


def _nom_plan_ia(ia_par_feuille: dict[str, Plan], feuille: str | None) -> str:
    if not feuille or feuille not in ia_par_feuille:
        return ""
    return ia_par_feuille[feuille].nom


# --- CLI ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python -m src.validation.compare_qpl",
                                description="Compare un relevé humain et un relevé IA (.qpl) marque par marque.")
    p.add_argument("--humain", required=True, type=Path, help="projet Plan Expert de l'estimateur")
    p.add_argument("--ia", required=True, type=Path, help="projet Plan Expert produit par la chaîne")
    p.add_argument("--dims", required=True, type=Path, help="dimensions des rasters humains (dossier|nom|L|H)")
    p.add_argument("--feuilles", required=True, type=Path, help="feuilles.csv du dossier IA")
    p.add_argument("--sortie", required=True, type=Path, help="répertoire de sortie")
    p.add_argument("--dossier", default=None,
                   help="préfixe du dossier dans le fichier de dimensions (défaut : S-<n> tiré de --humain)")
    p.add_argument("--rasters-ia", type=Path, default=None,
                   help="répertoire des PNG IA (défaut : celui du .qpl IA)")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        dossier = args.dossier
        if dossier is None:
            trouve = re.search(r"S-\d+", args.humain.name)
            dossier = trouve.group(0) if trouve else None
        dims = lire_dimensions(args.dims, dossier)
        feuilles = lire_feuilles(args.feuilles)
        humains = lire_qpl(args.humain, "humain")
        ias = lire_qpl(args.ia, "ia")
        preparer_humain(humains, dims)
        anomalies = preparer_ia(ias, feuilles, args.rasters_ia or args.ia.parent)
        comp = comparer(humains, ias, anomalies)
        tot = ecrire_sorties(comp, args.sortie, {
            "dossier": dossier or "", "humain": str(args.humain), "ia": str(args.ia),
            "dims": str(args.dims), "feuilles": str(args.feuilles)})
    except (CompareErreur, OSError) as exc:
        print(f"erreur : {exc}", file=sys.stderr)
        return 2
    print(f"{dossier or ''} : humaines {tot['humaines']} (doublons exclus {tot['doublons']}), IA {tot['ia']}, "
          f"appariées {tot['appariees']}, manquantes IA {tot['manquantes']}, en trop IA {tot['en_trop']} "
          f"→ {args.sortie / 'ecart-dupuis.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

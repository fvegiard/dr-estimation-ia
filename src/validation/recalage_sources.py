"""Rattachement des pages pour l'acceptation plans seuls, après vérification du gel.

Un nom de raster donne une piste, jamais une transformation. Une page ne peut
participer au score que si son fond et sa révision ont été contrôlés indépendamment
des marques. Le jeu de référence historique n'utilise pas ce module.
"""
from __future__ import annotations

import csv
import json
import re
from collections import Counter
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.ndimage import maximum_filter

from src.validation import compare_qpl as cq
from src.validation.gel import _sha256

NOM_ATTESTATION = "recalage-pages.json"
TOL_ANCRE = .002  # repères normalisés ; ne pas reprendre le seuil des appareils
DATE_ISO = r"\d{4}-\d{2}-\d{2}"
# L'ordre date/mention varie selon le cartouche. Seules les lignes numérotées
# du cartouche sont admissibles, pas les dates des plans ou de leur fichier.
REVISION = re.compile(rf"\b\d{{1,2}}\s+(?:({DATE_ISO})\s+pour\b|pour [a-z0-9 '-]{{1,90}}?\s+({DATE_ISO}))\b")
ATTESTEE = "attestée"
REMPLACEE = "version remplacée attestée"
REMPLACEMENT_PRESUME = "version remplacée présumée"
A_VERIFIER = "à vérifier"


@dataclass
class PageControlee:
    plan: cq.Plan
    etat: str
    note: str
    source: str = ""
    page: int | None = None
    feuille: str = ""
    transfo: cq.Transfo | None = None


@dataclass
class Controle:
    humaines: list[PageControlee] = field(default_factory=list)
    sans_reference: list[cq.Plan] = field(default_factory=list)
    sans_qpl: list[str] = field(default_factory=list)

    @property
    def reserves_humaines(self) -> list[PageControlee]:
        return [p for p in self.humaines if p.etat in (A_VERIFIER, REMPLACEMENT_PRESUME)
                and (p.plan.marques or p.plan.lignes)]

    @property
    def complet(self) -> bool:
        return not (self.reserves_humaines or self.sans_reference or self.sans_qpl)

    def detail(self) -> str:
        remplacees = [p for p in self.humaines if p.etat == REMPLACEE]
        indices = [p for p in self.humaines if p.etat == REMPLACEMENT_PRESUME]
        return (f"{sum(p.etat == ATTESTEE for p in self.humaines)} page(s) active(s) attestée(s) ; "
                f"{len(self.sans_reference)} feuille(s) IA sans référence attestée ; "
                f"{len(self.sans_qpl)} feuille(s) prévue(s) sans plan QPL ; "
                f"{len(self.reserves_humaines)} page(s) humaine(s) avec relevé à vérifier "
                f"({sum(len(p.plan.marques) for p in self.reserves_humaines)} marque(s), dont "
                f"{sum(len(p.plan.marques) for p in indices)} sur des versions présumées remplacées) ; "
                f"{sum(len(p.plan.marques) for p in remplacees)} marque(s) sur des versions remplacées attestées")

    def comparer(self, ias: list[cq.Plan], anomalies: list[str]) -> cq.Comparaison:
        paires = [cq.PairePage(p.plan, p.feuille, "fond attesté", p.transfo, None, p.note)
                  for p in self.humaines if p.etat == ATTESTEE]
        retenues = {p.feuille for p in paires}
        return cq.comparer([p.humain for p in paires], [p for p in ias if p.feuille in retenues],
                           anomalies, pages_attestees=cq.ResultatPages(paires, []))


def _lire_attestation(ref: Path, qpl: Path, connus: set[str], empreintes: set[str]):
    chemin = ref / NOM_ATTESTATION
    if not chemin.is_file():
        return {}, {}
    j = json.loads(chemin.read_text(encoding="utf-8"))
    if not isinstance(j, dict) or j.get("version") != 1 or j.get("qpl_sha256") != _sha256(qpl):
        raise cq.CompareErreur(f"{NOM_ATTESTATION} : version ou SHA-256 du QPL humain incohérent")
    alias, calages = j.get("documents", {}), j.get("calages", {})
    if not isinstance(alias, dict) or not isinstance(calages, dict) or set(calages) - connus:
        raise cq.CompareErreur(f"{NOM_ATTESTATION} : documents ou noms de rasters humains invalides")
    documents = {}
    for nom, sha in alias.items():
        cle = cq.normaliser_nom(nom)
        if not cle or cle in documents or not isinstance(sha, str) or sha not in empreintes:
            raise cq.CompareErreur(f"{NOM_ATTESTATION} : document ambigu ou absent des PDF gelés ({nom})")
        documents[cle] = sha
    return documents, calages


def _texte_atteste(a, cle):
    v = a.get(cle)
    if not isinstance(v, str) or not v.strip():
        raise cq.CompareErreur(f"attestation sans {cle}")
    return v.strip()


def _source_du_calage(a):
    if not isinstance(a, dict):
        raise cq.CompareErreur("attestation de page invalide")
    n = a.get("page")
    if type(n) is not int or n < 1:
        raise cq.CompareErreur("numéro de page attesté invalide")
    return _texte_atteste(a, "pdf_sha256"), n


def _ancres(a, largeur, hauteur, ia):
    """Échelle par axe + translation, sans rotation. Ancres dispersées dans les deux fonds."""
    xy = np.asarray(a.get("ancres"), dtype=float)
    if (xy.ndim != 3 or xy.shape[1:] != (2, 2) or len(xy) < 3 or
            not np.isfinite(xy).all() or np.any((xy < 0) | (xy > 1))):
        raise cq.CompareErreur("trois paires de repères de fond normalisés au minimum")
    h, p = xy[:, 0, :], xy[:, 1, :]
    if any(np.any(np.ptp(z, axis=0) < .25) or np.linalg.svd(z - z.mean(axis=0), compute_uv=False)[-1] < .06
           for z in (h, p)):
        raise cq.CompareErreur("repères de fond trop groupés ou alignés")
    (sx, tx), (sy, ty) = (np.linalg.lstsq(np.c_[h[:, k], np.ones(len(h))], p[:, k], rcond=None)[0]
                          for k in (0, 1))
    residu = np.max(np.abs(h * [sx, sy] + [tx, ty] - p))
    if residu > TOL_ANCRE or min(sx, sy) <= 0:
        raise cq.CompareErreur("repères de fond incompatibles avec un recalage sans rotation")
    sx, sy = float(sx * ia.largeur / largeur), float(sy * ia.hauteur / hauteur)
    if not .98 <= sx / sy <= 1.02:
        raise cq.CompareErreur("échelles physiques x/y incohérentes")
    return cq.Transfo(0, sx, sy, float(tx * ia.largeur), float(ty * ia.hauteur))


def _comparer_fond(page, image, cadre, transfo, revision):
    """Vérifier l'encre des deux fonds à la transformation fixée par les ancres.

    Le cartouche est contrôlé séparément pour ne pas noyer sa différence dans
    un plan de base commun. Pas de recherche de la transformation sur les marques.
    """
    import pymupdf

    rect = page.rect
    gris = image.convert("L")

    def rendre(z, clip=None, reduction=1):
        pix = page.get_pixmap(matrix=pymupdf.Matrix(z, z), clip=clip, colorspace=pymupdf.csGRAY,
                              alpha=False, annots=False)
        w, h = pix.width, pix.height
        kx, ky = 1 / transfo.sx, 1 / transfo.sy
        dx, dy = cadre.largeur / (z * rect.width), cadre.hauteur / (z * rect.height)
        fond = gris.transform((w, h), Image.Transform.AFFINE,
            (kx * dx, 0, kx * (dx * pix.x - transfo.tx), 0, ky * dy, ky * (dy * pix.y - transfo.ty)),
            Image.Resampling.BILINEAR, fillcolor=255)
        source = Image.frombytes("L", (w, h), pix.samples)
        if reduction != 1:
            # Réduire les deux images avec le même filtre. Un PDF rendu
            # directement à 1200 px épaissit les traits fins (règles CAO).
            taille = round(w / reduction), round(h / reduction)
            fond = fond.resize(taille, Image.Resampling.LANCZOS)
            source = source.resize(taille, Image.Resampling.LANCZOS)
        return np.asarray(fond) < 224, np.asarray(source) < 224

    def concordance(x, y):
        if not x.any() or not y.any():
            return 0.0
        return min(float(maximum_filter(y, size=3)[x].mean()), float(maximum_filter(x, size=3)[y].mean()))

    a, b = rendre(3600 / max(rect.width, rect.height), reduction=3)
    h, w = a.shape
    cartouche = np.s_[round(.62 * h):, round(.72 * w):]
    global_, titre = concordance(a, b), concordance(a[cartouche], b[cartouche])
    if global_ < .85 or titre < .85:
        raise cq.CompareErreur(f"fond ou cartouche différents (encre commune {global_:.0%} / {titre:.0%})")
    # Une ligne de révision absente peut peser très peu dans l'image entière.
    # Vérifier aussi l'encre de la date courante, à plus grande résolution.
    zone = pymupdf.Rect(.72 * rect.width, .62 * rect.height, rect.width, rect.height)
    dates = page.search_for(revision.isoformat(), clip=zone * page.derotation_matrix)
    if not dates or any(concordance(*rendre(3, d * page.rotation_matrix)) < .85 for d in dates):
        raise cq.CompareErreur("date du cartouche non confirmée dans le fond humain")
    return f"encre commune {global_:.0%} / cartouche {titre:.0%} ; zone date contrôlée"


def _transformer(a, ref, plan, ia, pdf, page, feuille_attendue):
    # Examiner le cartouche source, et lier la lecture manuelle du cartouche
    # humain et les ancres au raster exact (pas à un PNG exporté depuis l'IA).
    from src.estimer.plan_index import displayed_words, find_sheet, reading_order, title_block_words
    import pymupdf

    feuille = _texte_atteste(a, "feuille")
    revision = date.fromisoformat(_texte_atteste(a, "revision"))
    preuve = _texte_atteste(a, "preuve")
    if feuille_attendue and feuille != feuille_attendue or ia is not None and (
            feuille != ia.feuille or not ia.largeur or not ia.hauteur):
        raise cq.CompareErreur("feuille ou dimensions incohérentes avec la sélection gelée")
    if ia is not None and not plan.marques:
        _texte_atteste(a, "preuve_zero")  # un plan importé sans compteurs n'est pas un zéro contrôlé
    nom = plan.fichier
    racine = (ref / "rasters").resolve()
    raster = (racine / nom).resolve()
    if (not nom or Path(nom).name != nom or "\\" in nom or not racine.is_relative_to(ref.resolve()) or
            not raster.is_relative_to(racine) or not raster.is_file()):
        raise cq.CompareErreur("raster humain exact absent de reference/rasters/")
    sha = _texte_atteste(a, "raster_sha256")
    if not re.fullmatch(r"[0-9a-f]{64}", sha) or _sha256(raster) != sha:
        raise cq.CompareErreur("SHA-256 du raster humain différent de l'attestation")
    with pymupdf.open(pdf) as doc, Image.open(raster) as image:
        p = doc[page - 1]
        tb = reading_order(title_block_words(displayed_words(p), p.rect.width, p.rect.height))
        numero, _ = find_sheet(tb)
        dates = {date.fromisoformat(x or y) for x, y in REVISION.findall(cq.normaliser_nom(" ".join(w[4] for w in tb)))}
        if not numero or numero.replace("-", "") != feuille.replace("-", ""):
            raise cq.CompareErreur("numéro de feuille différent du cartouche source")
        if not dates or revision != max(dates):
            raise cq.CompareErreur("date de révision courante non confirmée dans le cartouche source")
        largeur, hauteur = image.size
        if plan.largeur is not None and (plan.largeur, plan.hauteur) != (largeur, hauteur):
            raise cq.CompareErreur("dimensions du raster différentes de l'inventaire humain")
        if any(not (0 <= m.x < largeur and 0 <= m.y < hauteur) for m in plan.marques):
            raise cq.CompareErreur("coordonnée humaine hors du raster attesté")
        cadre = ia or cq.Plan("", "", [], [], p.rect.width, p.rect.height)
        transfo = _ancres(a, largeur, hauteur, cadre)
        similarite = _comparer_fond(p, image, cadre, transfo, revision)
    plan.largeur, plan.hauteur, plan.source_dims = largeur, hauteur, "raster humain vérifié"
    return transfo, f"cartouche {feuille}, {revision} ; {similarite} ; {preuve}"


def controler(humains: list[cq.Plan], ias: list[cq.Plan], inventaire: dict,
              feuilles: dict, ref: Path, qpl: Path) -> Controle:
    """Ne jamais chercher de feuille à partir de la densité des marques IA."""
    documents = {e["sha256"]: e for e in inventaire["fichiers"]}
    revisions = inventaire.get("revisions")
    if len(documents) != len(inventaire["fichiers"]):
        raise cq.CompareErreur("des PDF gelés ont la même empreinte : identifier la copie active")
    alias, calages = _lire_attestation(ref, qpl, {p.fichier for p in humains}, set(documents))
    natifs = {cq.normaliser_nom(e["fichier"]): sha for sha, e in documents.items()}
    if len(natifs) != len(documents) or any(nom in natifs and natifs[nom] != sha for nom, sha in alias.items()):
        raise cq.CompareErreur("noms de PDF sources ambigus")
    if len({p.nom for p in humains}) != len(humains) or len({p.feuille for p in ias}) != len(ias):
        raise cq.CompareErreur("noms de pages QPL non uniques")
    ia_par_source = {}
    for ia in ias:
        cle = ia.base, ia.page
        if cle in ia_par_source:
            raise cq.CompareErreur(f"plusieurs feuilles IA pour le même PDF/page ({cle})")
        ia_par_source[cle] = ia
    attendues = set(feuilles)
    if revisions is not None:
        attendues.update(f for pages in revisions["actives"].values() for f in pages.values())
    resultat = Controle(sans_qpl=sorted(attendues - {p.feuille for p in ias}))
    selection_manquante = revisions is None and any(e["classement"] == "addenda" for e in documents.values())
    for plan in humains:
        a = calages.get(plan.fichier)
        indice = cq.normaliser_nom(plan.base)
        sha, page = alias.get(indice, natifs.get(indice)), plan.page
        ligne = PageControlee(plan, A_VERIFIER, "aucun PDF gelé ne permet d'identifier ce fond")
        resultat.humaines.append(ligne)
        try:
            if a is not None:
                ca = _source_du_calage(a)
                if sha and page and ca != (sha, page):
                    raise cq.CompareErreur("attestation contraire à l'identité PDF/page du raster")
                sha, page = ca
            if not sha or sha not in documents:
                continue
            if not page or not 1 <= page <= documents[sha].get("pages", 0):
                ligne.note = "document candidat, mais pagination absente ou hors du PDF gelé"
                continue
            ligne.source, ligne.page = documents[sha]["fichier"], page
            remplacee = (revisions or {}).get("remplacees", {}).get(ligne.source, {}).get(str(page))
            candidate = ia_par_source.get((ligne.source, page))
            source = Path(inventaire["inbox"]) / ligne.source
            if selection_manquante:
                ligne.note = "addendas gelés sans sélection des révisions attestée"
            elif remplacee:
                ligne.etat = REMPLACEMENT_PRESUME
                ligne.note = f"PDF/page candidats → {remplacee} selon le profil gelé ; aucun report"
                if a is not None:
                    _, preuve = _transformer(a, ref, plan, None, source, page, remplacee.split(" → ")[0])
                    ligne.etat, ligne.note = REMPLACEE, f"{ligne.note} ; {preuve}"
            elif candidate is None:
                ligne.note = "PDF/page désignés, mais pas de feuille IA correspondante dans la passe gelée"
            else:
                ligne.feuille = candidate.feuille
                ligne.note = "PDF/page candidats ; cartouche et fond du raster humain non attestés"
                if a is not None:
                    active = revisions["actives"].get(ligne.source, {}).get(str(page)) if revisions is not None else None
                    if revisions is not None and active is None:
                        raise cq.CompareErreur("page absente de la sélection des révisions actives")
                    ligne.transfo, ligne.note = _transformer(a, ref, plan, candidate, source, page, active)
                    ligne.etat = ATTESTEE
        except (OSError, TypeError, ValueError, IndexError, RuntimeError, Image.DecompressionBombError) as exc:
            ligne.note = str(exc)

    # Plusieurs rasters pour la même feuille ne sont pas fusionnés en fonction
    # du taux de recouvrement des compteurs : leur identité doit être clarifiée.
    par_feuille = Counter(p.feuille for p in resultat.humaines if p.transfo is not None)
    for p in resultat.humaines:
        if p.transfo is not None and par_feuille[p.feuille] > 1:
            p.transfo = None
            p.etat, p.note = A_VERIFIER, "plusieurs rasters attestés pour la feuille ; périmètres à départager"
    resultat.sans_reference = [p for p in ias if par_feuille[p.feuille] != 1]
    return resultat


def ecrire(resultat: Controle, sortie: Path) -> None:
    """Conserver les pages et chaque marque hors score avec les coordonnées natives."""
    with ((sortie / "recalage-pages.csv").open("w", encoding="utf-8", newline="") as f,
          (sortie / "marques-hors-comparaison.csv").open("w", encoding="utf-8", newline="") as m):
        pages, marques = csv.writer(f), csv.writer(m)
        pages.writerow(["cote", "raster", "pdf_source", "page_source", "feuille_ia_ou_candidate",
                        "etat", "marques", "lignes", "note"])
        marques.writerow(["cote", "raster", "feuille_ia_ou_candidate", "etat", "id", "libelle", "x_px", "y_px"])
        for h in resultat.humaines:
            pages.writerow(["humain", h.plan.fichier, h.source, h.page, h.feuille, h.etat,
                            len(h.plan.marques), len(h.plan.lignes), h.note])
            if h.transfo is None:
                for p in h.plan.marques:
                    marques.writerow(["humain", h.plan.fichier, h.feuille, h.etat, p.ident, p.libelle, p.x, p.y])
        for ia in resultat.sans_reference:
            etat = "sans référence attestée"
            pages.writerow(["ia", ia.fichier, ia.base, ia.page, ia.feuille, etat,
                            len(ia.marques), len(ia.lignes), "aucune comparaison sur cette feuille"])
            for p in ia.marques:
                marques.writerow(["ia", ia.fichier, ia.feuille, etat, p.ident, p.libelle, p.x, p.y])
        for feuille in resultat.sans_qpl:
            pages.writerow(["ia", "", "", "", feuille, "absente du QPL", "", "", "relevé de la feuille non vérifiable"])
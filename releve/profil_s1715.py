"""Premiers témoins de reconnaissance S-1715, limités au jeu de plans attesté."""
from __future__ import annotations

import csv
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pymupdf as pdf

from commun import sha256
from revisions import selection

BLEU, VERT = (0., 0., .808), (0., .68, 0.)
RSP = "RSP-C-347-Z1"
MODELE_A1 = "24CZSCT3-UNV-LOW-3500K"
TITRE_TYPIQUE = f"RACCORDEMENT TYPIQUE CONTRÔLEUR {RSP}"
NOTE_PCA = "PANNEAU DE CONTRÔLE D'ACCÈS FOURNI ET INSTALLÉ PAR L'ENTREPRENEUR."


@dataclass(frozen=True)
class Famille:
    feuille: str
    label: str
    famille: str
    code: str
    forme: str
    legende: str
    preuve: str
    modele: str = ""
    portee: str = "À PRÉCISER"


FAMILLES = {
    "A1": Famille("E201", "LUMINAIRE TYPE A1", "eclairage", "LA1", "carre", "E002-A1",
                  "ELE-002 E002 p.2 légende; E101 p.4 tableau A1; E201 p.5 rectangle et type", MODELE_A1),
    "USB": Famille("E301", "PRISE DOUBLE 15A 120V AVEC PORT USB", "prise", "PC", "cercle", "E002-USB",
                   "ELE-002 E002 p.2 légende USB; E301 p.6 cercle à deux tiges et étiquette"),
    "PCA": Famille("T201", "PANNEAU DE CONTRÔLE D'ACCÈS", "telecom", "PCA", "carre", "T001-PCA",
                   "Soumission T001 p.8 légende; T201 p.11 glyphe et renvoi note 2", portee="INSTALLER"),
    RSP: Famille("E003", f"CONTRÔLEUR WAVELINX {RSP}", "commande", "RSP", "carre", "HORS LEGENDE",
                 "ELE-002 E003 p.3 modèle et glyphe dans une zone raccordée, hors raccordement typique", RSP),
}


def _mots(page, code):
    return sorted((w for w in page.get_text("words") if w[4] == code), key=lambda w: (w[1], w[0]))


def _traces(page, rgb, poids):
    return [d for d in page.get_drawings() if d.get("type") == "s" and d.get("color") and
            all(abs(a - b) < .01 for a, b in zip(d["color"], rgb, strict=True)) and
            abs((d["width"] or 0) - poids) < .04 and d.get("dashes") in (None, "", "[] 0")]


def _segments(traces):
    return [(it[1], it[2]) for d in traces for it in d["items"] if it[0] == "l"]


def _centre(r):
    return (r.tl + r.br) / 2


def _couvert(segments, y, x0, x1):
    """Bord horizontal, parfois interrompu par un glyphe dessiné par-dessus."""
    intervalles = sorted((max(x0, min(a.x, b.x)), min(x1, max(a.x, b.x)))
                         for a, b in segments if abs(a.y - y) <= .16 and abs(b.y - y) <= .16 and
                         min(a.x, b.x) >= x0 - .2 and max(a.x, b.x) <= x1 + .2)
    fin, manque = x0, 0.
    for a, b in intervalles:
        manque += max(0., a - fin)
        fin = max(fin, b)
    return manque + x1 - fin <= 3.0  # ouverture de 2,64 pt observée sous le détecteur d'E201


def rectangles_a1(traces):
    lignes = _segments(traces)
    verticaux = set()
    for a, b in lignes:
        if abs(a.x - b.x) <= .16 and 17.0 <= abs(b.y - a.y) <= 17.6:
            verticaux.add((round((a.x + b.x) / 2, 2), round(min(a.y, b.y), 2), round(max(a.y, b.y), 2)))
    verticaux = sorted(verticaux)
    return [pdf.Rect(x, y, u, v) for i, (x, y, v) in enumerate(verticaux)
            for u, t, w in verticaux[i+1:] if 34.2 <= u-x <= 34.9 and abs(t-y) <= .16 and abs(w-v) <= .16
            and _couvert(lignes, y, x, u) and _couvert(lignes, v, x, u)]


def _contours(traces):
    """Les objets du PDF CAO sont parfois empaquetés dans un seul tracé."""
    for trace in traces:
        points = []
        for op, *p in trace["items"]:
            if op != "l":
                points = []
                continue
            a, b = p
            if not points or abs(a - points[-1]) > .04:
                points = [a]
            points.append(b)
            if abs(b - points[0]) <= .04:
                if len(points) >= 4:
                    yield points[:-1]
                points = []


def _boite(points):
    return pdf.Rect(min(p.x for p in points), min(p.y for p in points), max(p.x for p in points), max(p.y for p in points))


def prises_usb(traces):
    lignes = _segments(traces)
    retour = {}
    for pts in _contours(traces):
        r = _boite(pts)
        c = _centre(r)
        if not (12 <= len(pts) <= 20 and 9.5 <= r.width <= 10.2 and 9.5 <= r.height <= 10.2 and
                all(abs(abs(p - c) - (r.width + r.height) / 4) <= .45 for p in pts)):
            continue
        # Variantes horizontale/verticale : deux tiges parallèles, traversent
        # le cercle et ne dépassent que d'un même côté (pas la prise plafond).
        for axe in (0, 1):
            travers = 1 - axe
            tiges = set()
            for a, b in lignes:
                u, v = sorted((a[axe] - c[axe], b[axe] - c[axe]))
                delta = (a[travers] + b[travers]) / 2 - c[travers]
                if (abs(a[travers] - b[travers]) <= .16 and 13.3 <= v-u <= 14.1 and
                        1.15 <= abs(delta) <= 1.74 and min(u, -v) < -8.6 and -5.2 <= max(u, -v) <= -4.1):
                    tiges.add((delta > 0, u < -v))
            if any((False, sens) in tiges and (True, sens) in tiges for sens in (True, False)):
                retour[tuple(r)] = r
    return list(retour.values())


def _rectangles_pca(traces):
    retour = {}
    for pts in _contours(traces):
        r = _boite(pts)
        coins = {(p.x > _centre(r).x, p.y > _centre(r).y) for p in pts}
        if (len(pts) == len(coins) == 4 and 8.2 <= r.width <= 8.9 and 17.7 <= r.height <= 18.5 and
                all(min(abs(p.x-r.x0), abs(p.x-r.x1)) <= .16 and min(abs(p.y-r.y0), abs(p.y-r.y1)) <= .16 for p in pts)):
            retour[tuple(r)] = r
    return list(retour.values())


def _univoques(mots, rectangles, lie):
    choix = [[i for i, r in enumerate(rectangles) if lie(pdf.Rect(w[:4]), r)] for w in mots]
    comptes = Counter(i for li in choix for i in li)
    for w, li in zip(mots, choix, strict=True):
        yield w, rectangles[li[0]] if len(li) == 1 and comptes[li[0]] == 1 else None


def _image_rsp(page, mot):
    x, y = round((mot[0] + mot[2]) / 2), round(mot[3])
    zone = pdf.Rect(x-43, y+8, x+43, y+95)
    pix = page.get_pixmap(matrix=pdf.Matrix(2, 2), clip=zone, colorspace=pdf.csGRAY, alpha=False, annots=False)
    return np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width) < 185, zone


def score_glyphe(candidat, patron):
    """Dice sur l'encre, à ±2 pt pour l'arrondi du placement de l'étiquette."""
    if candidat.shape != patron.shape or not candidat.any() or not patron.any():
        return 0.
    h, w = patron.shape
    a = np.pad(candidat, 4)
    return max(2 * (a[y:y+h, x:x+w] & patron).sum() / (candidat.sum() + patron.sum())
               for y in range(9) for x in range(9))


def controleurs(page):
    mots = _mots(page, RSP)
    zone_typique = pdf.Rect(2505, 1290, 2990, 1558)
    temoins = [w for w in mots if abs(_centre(pdf.Rect(w[:4])).x - 836) < 1 and abs(w[3] - 688) < 1]
    if len(temoins) != 1 or not page.search_for(TITRE_TYPIQUE, clip=zone_typique):
        raise ValueError("E003 : témoin de glyphe ou raccordement typique non retrouvé")
    patron, _ = _image_rsp(page, temoins[0])
    for mot in mots:
        if zone_typique.contains(pdf.Rect(mot[:4])):
            yield mot, None, "hors compte : raccordement typique, pas un appareil de zone"
            continue
        image, zone = _image_rsp(page, mot)
        score = score_glyphe(image, patron)
        if score < .86:
            yield mot, None, f"modèle sans glyphe concordant (score {score:.3f})"
        else:
            yy, xx = np.nonzero(image)
            boite = pdf.Rect(zone.x0 + xx.min()/2, zone.y0 + yy.min()/2,
                            zone.x0 + (xx.max()+1)/2, zone.y0 + (yy.max()+1)/2)
            yield mot, boite, f"glyphe du contrôleur (score {score:.3f})"


def _verifier_jeu(w, feuilles):
    if (w / "gel.json").exists():
        raise ValueError("Profil S-1715 : sortie déjà gelée; utiliser un dossier neuf")
    inv = json.loads((w / "inventaire.json").read_text(encoding="utf-8"))
    fichiers = {e["fichier"]: e for e in inv["fichiers"]}
    revisions = selection(fichiers)
    if (len(fichiers) != len(inv["fichiers"]) or inv.get("plans_seuls") is not True or
            not revisions or revisions["dossier"] != "S-1715" or revisions != inv.get("revisions")):
        raise ValueError("Profil S-1715 : sélectionner les trois PDF attestés en mode plans seuls")
    actives = {f: (nom, n) for nom, pages in revisions["actives"].items() for n, f in pages.items()}
    if actives != {f: (r["fichier"], r["page"]) for f, r in feuilles.items()}:
        raise ValueError("Profil S-1715 : feuilles actives différentes de l'inventaire gelable")
    inbox = Path(inv["inbox"]).resolve()
    for nom, d in fichiers.items():
        p = inbox / nom
        if p.is_symlink() or not p.resolve().is_relative_to(inbox) or sha256(p) != d["sha256"]:
            raise ValueError(f"Profil S-1715 : PDF de source modifié : {nom}")
    return inbox, actives


def _csv(path, champs, lignes):
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=champs.split(","))
        w.writeheader()
        w.writerows(lignes)


def appliquer(work, feuilles):
    w = Path(work)
    inbox, actives = _verifier_jeu(w, feuilles)
    ele, ao = (inbox / actives[f][0] for f in ("E003", "T201"))
    with pdf.open(ele) as e, pdf.open(ao) as t:
        docs = {actives["E003"][0]: e, actives["T201"][0]: t}
        p = {f: docs[nom][int(n)-1] for f, (nom, n) in actives.items()}
        if any(p[f].rotation for f in ("E002", "E003", "E101", "E201", "E301", "T001", "T201")):
            raise ValueError("Profil S-1715 : rotation inattendue")
        for f, texte in (("E002", "LUMINAIRE DE TYPE"), ("E101", MODELE_A1), ("E002", "AVEC PORT USB"),
                         ("T001", "PANNEAU DE CONTRÔLE D'ACCÈS"), ("T201", NOTE_PCA)):
            if not p[f].search_for(texte):
                raise ValueError(f"Profil S-1715 : preuve de légende ou de portée absente sur {f} ({texte})")
        e201, e301, t201 = p["E201"], p["E301"], p["T201"]

        def usb_proche(m, r):
            c = _centre(r)
            d = np.hypot(max(m.x0-c.x, c.x-m.x1, 0), max(m.y0-c.y, c.y-m.y1, 0))
            return 4.8 <= d <= 8.5 and not m.intersects(r)

        plan = {
            "A1": _univoques(_mots(e201, "A1"), rectangles_a1(_traces(e201, BLEU, .6)),
                              lambda m, r: .35 <= r.y0 - m.y1 <= 9 and 2 <= _centre(m).x-r.x0 <= 8),
            "USB": _univoques(_mots(e301, "USB"), prises_usb(_traces(e301, BLEU, .84)), usb_proche),
            "PCA": _univoques(_mots(t201, "PCA"), _rectangles_pca(_traces(t201, VERT, .84)),
                              lambda m, r: r.contains(m) and pdf.Point(2017.6, 643.5) in r),
        }
        candidats = {k: [(m, r, "glyphe et libellé univoques" if r else "sans glyphe univoque dans la portée lue")
                         for m, r in li] for k, li in plan.items()}
        candidats[RSP] = list(controleurs(p["E003"]))

    occ, audit, comptes = [], [], Counter()
    for code, li in candidats.items():
        fam = FAMILLES[code]
        for mot, r, motif in li:
            centre = _centre(r or pdf.Rect(mot[:4]))
            xy = dict(x_pt=f"{centre.x:.2f}", y_pt=f"{centre.y:.2f}")
            audit.append(dict(feuille=fam.feuille, jeton=code, **xy, retenu="oui" if r else "non", raison=motif))
            if r is None:
                continue
            comptes[code] += 1
            reserve = "Portée à confirmer avec les avis écrits et le devis" if fam.portee == "À PRÉCISER" else ""
            cadre = dict(zip(("x0_pt", "y0_pt", "x1_pt", "y1_pt"), (f"{v:.2f}" for v in r + (-.7, -.7, .7, .7))))
            occ.append(dict(feuille=fam.feuille, label=fam.label, **xy, source="visuel", note=f"{fam.preuve}; {motif}",
                            designation=code, portee=fam.portee, modele=fam.modele, reserve=reserve,
                            **(cadre if fam.forme == "carre" else {"rayon_pt": f"{r.width/2+.6:.2f}"})))

    _csv(w / "contexte-candidats.csv", "feuille,jeton,x_pt,y_pt,retenu,raison", audit)
    _csv(w / "occurrences-texte.csv", "feuille,label,x_pt,y_pt,source,note", [])
    _csv(w / "occurrences-visuel.csv", "feuille,label,x_pt,y_pt,source,note,designation,portee,modele,reserve,x0_pt,y0_pt,x1_pt,y1_pt,rayon_pt", occ)
    _csv(w / "nomenclature.csv", "label,famille,forme,code,description,source,materiel,modele,discipline,legende", (
        dict(label=f.label, famille=f.famille, forme=f.forme, code=f.code, description=f.label,
             source=f.preuve, materiel=f.label, modele=f.modele, discipline="electricite", legende=f.legende)
        for k, f in FAMILLES.items() if comptes[k]))
    _csv(w / "legende.csv", "feuille,no,description,code,statut,qte,preuve", (
        dict(feuille=f.legende.split("-")[0], no=f.legende, description=f.label,
             code=f.code, statut="compte", qte=comptes[k], preuve=f.preuve)
        for k, f in FAMILLES.items() if k != RSP and comptes[k]))
    roles = {"E001": "detail", "E002": "legende", "E003": "schema", "E101": "tableau",
             "T000": "detail", "T001": "legende", "T100": "detail", "T101": "detail"}
    _csv(w / "feuilles-classement.csv", "feuille,type,echelle,note", (
        dict(feuille=f, type=roles.get(f, "plan"), echelle="1:100" if f in ("E201", "E301", "T201") else "",
             note=f"Source {nom} p.{n}; feuille {f}") for f, (nom, n) in actives.items()))
    (w / "reserves.md").write_text(
        "# Réserves — S-1715, reconnaissance limitée\n\n"
        "- R-001 — E201 / E301 : seuls les A1 et les duplex USB sont qualifiés; leur portée reste à confirmer. "
        "Autres luminaires, variantes de prises, détection et services : non évalués, pas de quantités d'absence.\n"
        f"- R-002 — E003 p.3 : {FAMILLES[RSP].label} relevé sur le schéma seulement; "
        "raccordement typique exclu. Le rapprochement aux symboles du plan, la portée, "
        "les autres appareils, accessoires et parcours restent à vérifier.\n"
        "- R-003 — T201 : ne retenir que le PCA renvoyant à la note 2. Les équipements client, portes, "
        "autres variantes et réseaux ne se déduisent pas du seul PCA.\n"
        "- R-004 — Avis écrits ELE-001/ELE-002, devis et autres disciplines non vérifiés; légende partielle. "
        "Aucun métré de câble/conduit ni chiffrage final. Voir `contexte-candidats.csv` pour les refus.\n"
        "- R-005 — E102 : plan d'implantation non relevé par ce profil. Aucun zéro d'absence établi.\n",
        encoding="utf-8")
    (w / "rapport-releve.md").write_text(
        "# S-1715 — témoins sur plans seuls\n\n"
        "Reconnaissance partielle, sans quantité déduite d'un exemple de raccordement.\n\n" +
        "\n".join(f"- {f.feuille} — {f.label} : {comptes[k]} repère(s). {f.preuve}." for k, f in FAMILLES.items()) + "\n",
        encoding="utf-8")
    print(f"Profil local S-1715 : {len(occ)} repères, dont {comptes[RSP]} sur le schéma E003 ; relevé partiel")
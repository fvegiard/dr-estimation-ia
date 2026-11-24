"""Deux règles locales SAQ Varennes, liées à l'empreinte du PDF de soumission.

Ne remplace ni la lecture complète du plan, ni la bibliothèque partagée. Les
candidats non résolus sont écrits avec leurs coordonnées, jamais comptés par défaut.
"""
from __future__ import annotations

import csv
import json
import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

import pymupdf as pdf

from commun import sha256

EMPREINTE = "456eecd92a05beef45ae214d65cff804ac410d916c9891caeb9fddf94716b334"
PAGES = {"E100": 3, "E101": 4, "E200D": 7, "E200": 8, "E300D": 10, "E300": 11}
PRISE = "PRISE DUPLEX 15A 120V"
TYPE = re.compile(r"D[34]-[BN](?:T[12])?")
PORTEES = {"N.": "INSTALLER", "E.C.": "CONSERVER", "E.D.": "ENLEVER",
           "E.M.": "MODIFIER", "E.R.": "RELOCALISER", "R.": "RELOCALISER"}
COULEURS = {"cyan": (0, .647, .867), "gris": (.302,) * 3, "pâle": (.8,) * 3,
            "vert": (.216, .867, 0), "rouge": (.867, 0, 0)}


@dataclass
class Candidat:
    x: float
    y: float
    rayon: float
    famille: str
    style: str
    preuve: str
    options: list[tuple[float, tuple]]
    label: str = ""
    portee: str = ""
    motif: str = ""


def couleur(d):
    rgb = d.get("color")
    return next((nom for nom, ref in COULEURS.items() if rgb and
                 all(abs(c - v) <= .009 for c, v in zip(rgb, ref, strict=True))), "autre")


def continu(d):
    # Le PDF peut vectoriser les pointillés en plusieurs tracés solides. Une
    # couleur rouge même avec dashes=[] n'autorise donc jamais INSTALLER.
    return d.get("dashes") in (None, "", "[] 0")


def centre(r):
    return (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2


def ecart_mot(x, y, mot):
    return math.hypot(max(mot[0] - x, x - mot[2], 0), max(mot[1] - y, y - mot[3], 0))


def cercle(d):
    r, it = d["rect"], d["items"]
    if d.get("fill") is not None or not continu(d) or not (11.9 <= r.width <= 13 and
            abs(r.width - r.height) <= .25 and len(it) == 4 and all(p[0] == "c" for p in it)):
        return False
    x, y = centre(r)
    rho = (r.width + r.height) / 4
    return all(abs(math.hypot(p[1].x - x, p[1].y - y) - rho) < .3 and
               abs(p[-1] - it[(i + 1) % 4][1]) < .2 for i, p in enumerate(it))


def traverses(d, lignes):
    """Deux traverses de même longueur et centrées, à travers le cercle entier."""
    x, y = centre(d["rect"])
    diam = d["rect"].width
    traits = []
    for e in lignes:
        _, a, b = e["items"][0]
        longueur = abs(b - a)
        if not 1.48 * diam <= longueur <= 1.62 * diam:
            continue
        if abs((e["width"] or 0) - (d["width"] or 0)) > .04:
            continue
        u = (b - a) / longueur
        if u.x < -.001 or (abs(u.x) <= .001 and u.y < 0):
            u = -u
        m = (a + b) / 2 - pdf.Point(x, y)
        h, v = m.x * u.x + m.y * u.y, m.x * u.y - m.y * u.x
        if abs(h) <= .30 * diam and abs(v) <= .18 * diam:
            traits.append((u, h, v, e))
    paires = [(e, f) for i, (u, h, v, e) in enumerate(traits)
              for w, j, k, f in traits[i + 1:] if abs(w - u) < .035 and abs(h - j) < .7
              and .24 * diam <= abs(v - k) <= .30 * diam]
    return paires[0] if len(paires) == 1 else None


def encre_variante(cercle_, traits, encre):
    r = cercle_["rect"]
    for d in encre:
        b = d["rect"]
        if d in traits or d is cercle_ or not r.intersects(b) or max(b.width, b.height) > 2.6 * r.width:
            continue
        # Remplissage, cadre, ou troisième trait (notamment flèche des toiles).
        if d.get("fill") is not None or any(it[0] in {"l", "re", "qu"} for it in d["items"]):
            return True
    return False


def associer(candidats, marge=1.8):
    """Le mot et le symbole doivent être mutuellement les plus proches, sans égalité."""
    inverse = defaultdict(list)
    for i, c in enumerate(candidats):
        c.options.sort()
        for distance, mot in c.options:
            inverse[mot].append((distance, i))
    for mot in inverse:
        inverse[mot].sort()
    for i, c in enumerate(candidats):
        if not c.options:
            yield c, None, "aucune étiquette associée"
            continue
        d, mot = c.options[0]
        rev = inverse[mot]
        if (rev[0][1] != i or len(rev) > 1 and rev[1][0] - d < marge or
                len(c.options) > 1 and c.options[1][0] - d < marge):
            yield c, None, "étiquette disputée ou association non univoque"
        else:
            yield c, mot[4], ""


def prises(traces, mots, feuille):
    palette = defaultdict(list)
    for d in traces:
        style = couleur(d)
        if style in {"cyan", "gris", "pâle", "rouge"} and max(d["rect"].width, d["rect"].height) <= 35:
            palette[style].append(d)
    candidats = []
    for style in ("cyan", "gris", "pâle", "rouge"):
        encre = palette[style]
        lignes = [d for d in encre if continu(d) and d.get("fill") is None and
                  len(d["items"]) == 1 and d["items"][0][0] == "l"]
        for d in encre:
            if not cercle(d):
                continue
            x, y = centre(d["rect"])
            if any(math.hypot(c.x - x, c.y - y) < .3 for c in candidats):
                continue  # la surimpression cyan/gris E200 est un seul glyphe
            traits = traverses(d, lignes)
            # Ne pas faire de marque pour un cercle nu, mais le garder à vérifier.
            motif = ("traverses complètes non prouvées" if not traits else
                     "variante ou superposition de traits à vérifier" if encre_variante(d, traits, encre) else "")
            candidats.append(Candidat(x, y, d["rect"].width / 2, "prise", style,
                f"E100 p.3 (192, 503), cercle et deux traverses; tracé {d['seqno']}",
                [(ecart_mot(x, y, w), w) for w in mots if w[4] in PORTEES and ecart_mot(x, y, w) <= 24],
                motif=motif))
    for c, tag, motif in associer([c for c in candidats if not c.motif]):
        if motif:
            c.motif = motif
        elif tag == "E.C." and c.style in {"cyan", "gris", "pâle"}:
            c.portee = "CONSERVER"
        elif tag == "N." and feuille == "E200" and c.style == "cyan":
            c.portee = "INSTALLER"
        else:
            c.motif = f"portée {tag} et tracé {c.style} non confirmés par la règle locale"
        if c.portee:
            c.label = PRISE
            c.preuve += f"; {tag} (E100, portée)"
    return candidats


def triangle(d):
    it, r = d["items"], d["rect"]
    if len(it) != 3 or any(p[0] != "l" for p in it) or not (4.3 <= max(r.width, r.height) <= 5.7):
        return False
    longueurs = [abs(p[2] - p[1]) for p in it]
    return min(longueurs) > 0 and max(longueurs) / min(longueurs) < 1.17 and all(
        abs(p[2] - it[(i + 1) % 3][1]) <= .18 for i, p in enumerate(it))


def rail_touche(d, rails):
    pts = [p[1] for p in d["items"]]
    r = d["rect"]
    for n, q in rails:
        b = q.rect
        if b.x0 > r.x1 + .24 or b.x1 < r.x0 - .24 or b.y0 > r.y1 + .24 or b.y1 < r.y0 - .24:
            continue
        for a, z in ((q.ul, q.ur), (q.ul, q.ll), (q.ll, q.lr), (q.ur, q.lr)):
            u = z - a
            longueur = abs(u)
            if longueur < 16:
                continue
            u /= longueur
            for point in pts:
                p = point - a
                if -.21 <= p.x * u.x + p.y * u.y <= longueur + .21 and abs(p.x * u.y - p.y * u.x) <= .21:
                    return n, a, u, q.rect.tl + (q.rect.br - q.rect.tl) / 2
    return None


def mots_du_rail(x, y, mots, rail):
    """Lire le libellé dans le même couloir et du même côté du rail que le glyphe."""
    _, _, u, origine = rail
    horizontal = abs(u.x) >= .98
    if not horizontal and abs(u.y) < .98:
        return []  # aucune portée déduite pour les orientations non étalonnées
    axe, travers = (0, 1) if horizontal else (1, 0)
    xy = (x, y)
    retour = []
    for w in mots:
        milieu = ((w[0] + w[2]) / 2, (w[1] + w[3]) / 2)
        if not TYPE.fullmatch(w[4]) or not (w[axe + 2] - w[axe] >= 1.5 * (w[travers + 2] - w[travers])):
            continue
        meme_cote = (milieu[travers] - origine[travers]) * (xy[travers] - origine[travers]) > 0
        lateral = abs(milieu[travers] - xy[travers])
        longitudinal = max(w[axe] - xy[axe], xy[axe] - w[axe + 2], 0)
        if meme_cote and lateral <= 4.5 and 1 <= longitudinal <= 9:
            retour.append((math.hypot(longitudinal, lateral), w))
    return retour


def projecteurs(traces, mots, feuille):
    rails = [(d["seqno"], it[1]) for d in traces if couleur(d) == "vert" and continu(d)
             and .9 <= (d["width"] or 0) <= 1.2 for it in d["items"] if it[0] == "qu"
             and max(it[1].rect.width, it[1].rect.height) >= 16]
    candidats = []
    for d in traces:
        style = couleur(d)
        if style not in {"vert", "pâle", "rouge", "gris"} or not triangle(d):
            continue
        x, y = centre(d["rect"])
        if any(math.hypot(c.x - x, c.y - y) < .3 for c in candidats):
            continue
        proches = [(ecart_mot(x, y, w), w) for w in mots if TYPE.fullmatch(w[4]) and ecart_mot(x, y, w) <= 13]
        if feuille == "E300D" and not proches and style not in {"rouge", "pâle"}:
            continue
        rail = rail_touche(d, rails) if style == "vert" and continu(d) else None
        motif = ("feuille démolition, aucune pose déduite" if feuille == "E300D" else
                 "triangle sans rail vert continu jointif" if rail is None else "")
        candidats.append(Candidat(x, y, max(d["rect"].width, d["rect"].height) / 2, "projecteur", style,
            f"E101 p.4 (D3 y=583, D4 y=762); triangle {d['seqno']}; rail {rail[0] if rail else 'non identifié'}",
            mots_du_rail(x, y, mots, rail) if rail and feuille == "E300" else proches, motif=motif))
    for c, tag, motif in associer([c for c in candidats if not c.motif]):
        c.motif = motif
        if tag:
            c.portee, c.label = "INSTALLER", f"PROJECTEUR {tag}"
            c.preuve += f"; étiquette {tag}"
    return candidats


def recouper_prises(construction, demolition):
    """Les deux fonds de RDC ont le même repère PDF (à cette empreinte seulement)."""
    for c in construction:
        voisins = [d for d in demolition if math.hypot(d.x - c.x, d.y - c.y) <= 1.5]
        if not voisins:
            continue
        if c.portee == "CONSERVER" and len(voisins) == 1 and voisins[0].portee == "CONSERVER":
            d = voisins[0]
            c.motif = f"même existant conservé reporté sur E200D ({d.x:.2f}, {d.y:.2f}); compté une fois sur E200D"
            c.label = c.portee = ""
        elif c.portee:
            c.motif = "recouvrement E200/E200D non résolu; vérifier la portée et l'identité"
            c.label = c.portee = ""


def ecrire_csv(p, champs, lignes):
    with p.open("w", newline="", encoding="utf-8") as f:
        e = csv.DictWriter(f, fieldnames=champs.split(","))
        e.writeheader()
        e.writerows(lignes)


def appliquer(work: str, feuilles: dict, classer) -> bool:
    """Écrit les sorties du pilote seulement si le PDF et ses feuilles sont attestés."""
    w = Path(work)
    p = w / "inventaire.json"
    if not p.is_file():
        return False
    inv = json.loads(p.read_text(encoding="utf-8"))
    fichiers = inv.get("fichiers", [])
    if len(fichiers) != 1 or fichiers[0].get("sha256") != EMPREINTE or fichiers[0].get("classement") != "plans":
        return False
    if len(feuilles) != 12:  # pas d'extrapolation à une demande de feuille unique
        return False
    source = Path(inv["inbox"]) / fichiers[0]["fichier"]
    if sha256(source) != EMPREINTE or any(int(feuilles.get(f, {}).get("page", 0)) != n or
                                         feuilles[f]["fichier"] != source.name for f, n in PAGES.items()):
        raise ValueError("S-1844 : source ou repérage des feuilles non conforme au profil local")
    with pdf.open(source) as doc:
        if len(doc) != 12 or any(doc[n - 1].rotation for n in PAGES.values()):
            raise ValueError("S-1844 : pagination ou rotation inattendue")
        par_f = {}
        for f, n in PAGES.items():
            if f in {"E100", "E101"}:
                continue
            page = doc[n - 1]
            regle = prises if f.startswith("E200") else projecteurs
            par_f[f] = regle(page.get_drawings(), page.get_text("words"), f)
    recouper_prises(par_f["E200"], par_f["E200D"])

    occ, nom, leg, bilan = [], {}, {}, []
    for f, cs in par_f.items():
        for c in sorted(cs, key=lambda c: (c.y, c.x)):
            x, y = f"{c.x:.2f}", f"{c.y:.2f}"
            bilan.append(dict(feuille=f, page=PAGES[f], x_pt=x, y_pt=y, famille=c.famille, style=c.style,
                              label=c.label, portee=c.portee, preuve=c.preuve, reserve=c.motif,
                              etiquettes=" / ".join(f"{m[4]} ({d:.1f} pt)" for d, m in sorted(c.options))))
            if not c.label:
                continue
            prise = c.famille == "prise"
            tag = "" if prise else c.label.split()[-1]
            code, no, fl = ("PC", "S01", "E100") if prise else (tag, f"TYPE-{tag}", "E101")
            occ.append(dict(feuille=f, label=c.label, x_pt=x, y_pt=y, source="visuel", note=c.preuve,
                            designation=tag, portee=c.portee, modele=tag, reserve="", rayon_pt=f"{c.rayon:.2f}"))
            nom.setdefault(c.label, dict(label=c.label, famille="prise" if prise else "eclairage", forme="cercle",
                description=c.label, source=f"{source.name}, {fl}, p.{PAGES[fl]}; occurrences avec tracé et étiquette",
                code=code, materiel=c.label, modele=tag, discipline="electricite", legende=no))
            leg.setdefault(no, dict(feuille=fl, no=no, section="Services" if prise else "Éclairage",
                symbole="cercle et deux traverses" if prise else "triangle jointif au rail et étiquette",
                description=c.label, code=code, statut="compte", qte=0, preuve=f"{source.name}, {fl}, p.{PAGES[fl]}"))
            leg[no]["qte"] += 1
    ecrire_csv(w / "contexte-candidats.csv", "feuille,page,x_pt,y_pt,famille,style,label,portee,preuve,reserve,etiquettes", bilan)
    ecrire_csv(w / "occurrences-visuel.csv", "feuille,label,x_pt,y_pt,source,note,designation,portee,modele,reserve,x0_pt,y0_pt,x1_pt,y1_pt,angle_deg,rayon_pt", occ)
    ecrire_csv(w / "occurrences-texte.csv", "feuille,label,x_pt,y_pt,source,note", [])
    ecrire_csv(w / "nomenclature.csv", "label,famille,forme,rgb,jeton_regex,description,source,code,materiel,portee,modele,prescription,discipline,legende", nom.values())
    ecrire_csv(w / "legende.csv", "feuille,section,no,symbole,description,code,statut,qte,preuve", leg.values())
    ecrire_csv(w / "feuilles-classement.csv", "feuille,type,echelle,note,bordereau", (
        dict(feuille=f, type={"E002": "devis", "E102": "schema", "E103": "schema"}.get(f, classer(r)),
             note=f"feuille={f} · {r.get('titre', '')}") for f, r in feuilles.items()))
    (w / "reserves.md").write_text(
        "# Réserves — pilote S-1844\n\n"
        "- R-001 — Seuls les duplex ordinaires E200/E200D et projecteurs D3/D4 E300 sont testés. "
        "Les autres variantes, objets, familles, feuilles et notes restent à relever; aucun zéro d'absence n'est établi.\n"
        "- R-002 — E300D : dépose/rails et types non confirmés, jamais convertis en pose. E200/E200D : "
        "glyphes superposés dédupliqués seulement si leur identité et leur portée concordent.\n"
        "- R-003 — E300 (2000.2, 622.9), carré bleu barré : boîte de jonction probable (E100), "
        "dimension et portée non établies; pas intégrée aux quantités.\n"
        "- R-004 — Aucun parcours de filage, addenda ou devis externe déduit. Voir `contexte-candidats.csv` "
        "pour les candidats écartés ou réservés avec position. Les signatures du moteur générique ne sont pas reclassées.\n",
        encoding="utf-8")
    comptes = Counter((o["feuille"], o["label"], o["portee"]) for o in occ)
    (w / "rapport-releve.md").write_text(
        f"# S-1844 — essai contextuel local sur plans seuls\n\n{len(occ)} repères; {len(bilan) - len(occ)} "
        "candidats écartés ou réservés. Le relevé n'est pas exhaustif.\n\n"
        + "\n".join(f"- {f} — {label} ({portee}) : {n}" for (f, label, portee), n in sorted(comptes.items())) + "\n",
        encoding="utf-8")
    print(f"Profil local S-1844 : {len(occ)} occurrences, {len(nom)} libellés, {len(bilan) - len(occ)} candidats non comptés")
    return True
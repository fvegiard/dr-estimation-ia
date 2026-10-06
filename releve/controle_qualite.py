# /// script
# requires-python = ">=3.12"
# dependencies = ["pymupdf>=1.24"]
# ///
"""Contrôle qualité BLOQUANT d'un relevé (sorties de l'agent) avant de le déclarer conforme.

Usage : python releve/controle_qualite.py WORKDIR [--reference familles-par-feuille.csv --feuille-ref DSI01 --feuille F]
Écrit WORKDIR/qualite.json ; code 0 si aucune erreur bloquante, 2 sinon.

Un succès technique de l'agent (fichiers écrits) ne prouve pas un relevé exact (run1 Gemma DSI01 du 2026-09-29 :
« success » avec 31 marques contre 122 chez l'estimateur). Contrôles :
  Q1 sorties obligatoires présentes et non vides ; chaque feuille « plan » a au moins une occurrence ;
  Q2 chaque libellé d'occurrence existe dans nomenclature.csv ;
  Q3 un libellé = un appareil : même libellé pour deux jetons/descriptions différents = fusion interdite (R1/R3) ;
  Q4 classement : le préfixe du repère lu (note « [DT1.2] ») doit correspondre au jeton_regex du libellé choisi ;
  Q5 repère en double sur une même feuille ;
  Q6 trous dans une suite de repères (K1.1, K1.2, K1.6 → K1.3-K1.5 manquent) non expliqués dans reserves.md ;
  Q7 coordonnées hors de la feuille ;
  Q8 appareil de la nomenclature jamais relevé sur les plans et absent de reserves.md ;
  Q9 (si une référence est fournie) écart par famille > 5 % de la référence ;
  Q10 coordonnées fabriquées sur une grille mentale au lieu d'être lues sur le plan ;
  Q11 légende complète : chaque ligne de `legende.csv` est soit comptée (une famille de la nomenclature la cite et a
      des occurrences), soit marquée absente / hors portée avec une preuve ; chaque famille cite sa ligne de légende
      (ou `HORS LEGENDE`) ; une feuille de légende fournie sans `legende.csv` est une erreur ;
  Q12 une famille par symbole de légende : deux familles sur la même ligne de légende seulement si leurs codes du
      vocabulaire diffèrent (comptoir / comptoir DDFT, luminaire type A / type F) ; jamais deux familles qui ne
      diffèrent que par la puissance (la puissance va dans `designation` de l'occurrence) ;
  Q13 devis fourni (`devis/*-articles.csv`) : chaque famille a un `modele` (référence du devis, `EXISTANT`, ou
      `MODELE NON INDIQUE DANS LA SOURCE ELECTRIQUE` quand le devis a été lu sans y trouver l'appareil) ;
  Q14 code de famille conforme au vocabulaire de la légende (`releve/legende.py::code_attendu`) quand il s'applique ;
      un existant (portée REMPLACER / CONSERVER) peut aussi porter le code existant CH / I / PC / T / M01… (règle R11) ;
  Q15 omission probable : un cercle vectoriel du plan qui a exactement la signature (diamètre, épaisseur de trait)
      d'un symbole déjà relevé, sans occurrence à moins de 8 pt et sans justification « Q15 (x, y) » dans reserves.md.
      Contrôle à l'aveugle (ni gold ni référence) : il compare le plan à lui-même. Constaté sur E08 (2026-10-05) :
      une prise bien visible et une prise cachée sous une hachure d'armoire oubliées dans chaque logement.

Q11-Q14 : correctif E08 du 2026-10-05 (codes inventés PU/VE/PA…, plinthes éclatées par puissance, prises de comptoir
fondues dans les prises DDFT, luminaire type C oublié, bordereau « MODELE NON PRECISE » malgré le devis E15).

Q10 : un symbole réel tombe sur une coordonnée quelconque. Si presque toutes les marques sont des
multiples ronds (10 pt, 25 pt…), le modèle a inventé des positions au lieu de les lire — run2 Gemma
DSI01 du 2026-09-29 : 53/53 marques multiples de 10 en x ET en y, soit une chance sur 100^53, et
aucune ne tombait sur un symbole. Contrôle aveugle : il ne demande ni référence ni ancrage.
"""
from __future__ import annotations

import argparse
import collections
import csv
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import legende as LG  # noqa: E402

REPERE = re.compile(r"\[?\b([A-Z]{1,4}\d?)(\d+)\.(\d+)\]?")
TOLERANCE_REF = 0.05
PAS_GRILLE = (5, 10, 25, 50)  # pas ronds typiques d'une position inventée
MIN_GRILLE = 8                # en dessous, la coïncidence reste plausible
SEUIL_GRILLE = 0.80           # part de marques alignées à partir de laquelle on bloque
SEUIL_GRILLE_AVERT = 0.15     # au-dessus, le modèle arrondit trop (humains mesurés : 0,9 %)


def coordonnees(o):
    """(x, y) d'une occurrence, ou None si illisible."""
    try:
        return float(o.get("x_pt") or o.get("x")), float(o.get("y_pt") or o.get("y"))
    except (TypeError, ValueError):
        return None


def grille_suspecte(points, pas=PAS_GRILLE, minimum=MIN_GRILLE, seuil=SEUIL_GRILLE):
    """Plus grand pas sur lequel au moins `seuil` des points sont alignés en x ET en y.

    Renvoie (pas, nombre_aligné, total) ou None. Des positions lues sur un plan ne
    s'alignent pas : la probabilité que n marques tombent toutes sur un multiple de 10
    dans les deux axes est de 100^-n.

    Le pas 5 compte aussi : mesuré sur le dépôt, les relevés humains n'y tombent que
    dans 3,1 % des cas (319 marques) alors que kimi-k3 y tombe à 100 % sur 104 marques.
    Un modèle peut arrondir finement et paraître précis ; c'est la même invention.
    On renvoie le pas le plus grand qui tient, car c'est celui qui décrit vraiment la
    maille employée : gemma-4-31b est à 100 % sur 10 pt, kimi-k3 seulement sur 5 pt."""
    if len(points) < minimum:
        return None
    for p in sorted(pas, reverse=True):
        n = sum(1 for x, y in points if x % p == 0 and y % p == 0)
        if n >= seuil * len(points):
            return p, n, len(points)
    return None


def part_arrondie(points, pas=10):
    """Part des marques tombant sur un multiple de `pas` dans les deux axes.

    Repère mesuré sur les relevés humains du dépôt : 3 coordonnées rondes sur 319
    marques, soit 0,9 %. Un taux nettement supérieur sans atteindre SEUIL_GRILLE
    signale un modèle qui arrondit ses lectures — imprécis sans être inventé."""
    if not points:
        return 0.0
    return sum(1 for x, y in points if x % pas == 0 and y % pas == 0) / len(points)


def lire_csv(p, mal_formees=None):
    """Lit un CSV en normalisant les clés. Une ligne ayant plus de champs que d'en-têtes
    est signalée (csv.DictReader range le surplus dans une liste sous la clé None) : le
    contrôle doit la rapporter comme erreur, jamais planter dessus."""
    if not os.path.isfile(p):
        return []
    out = []
    with open(p, encoding="utf-8", newline="") as fh:
        for i, r in enumerate(csv.DictReader(fh), start=2):
            surplus = r.pop(None, None)
            if surplus is not None and mal_formees is not None:
                mal_formees.append(f"{os.path.basename(p)} ligne {i} : {len(surplus)} champ(s) en trop "
                                   f"({', '.join(str(s) for s in surplus)[:80]}) — virgule non échappée ?")
            out.append({(k or "").strip(): (v if isinstance(v, str) else " ".join(map(str, v or []))).strip()
                        for k, v in r.items()})
    return out


def famille_de_repere(prefixe, nomenclature):
    """Libellés dont le jeton_regex reconnaît le préfixe du repère (ex. DT → DETECTEUR THERMIQUE)."""
    out = set()
    for n in nomenclature:
        rx = n.get("jeton_regex")
        if rx:
            try:
                if re.fullmatch(rx, prefixe):
                    out.add(n["label"])
            except re.error:
                pass
    return out


MOTS_VIDES = {"DE", "DU", "LA", "LE", "ET", "A", "D", "L", "UNITE", "TYPE"}


def piste_confusion(lab, comptes, fiche):
    """Nomme le libellé qui a probablement absorbé `lab`, ou '' si aucun candidat.

    Un libellé jamais employé est rarement un appareil absent : il est compté sous un voisin.
    On classe les libellés employés par mots significatifs partagés (DETECTEUR THERMIQUE 135F →
    DETECTEUR THERMIQUE), puis par nombre de marques. Sans mot commun, on accepte un voisin de
    même famille et même forme ; sinon on n'invente pas de piste."""
    mots = {m for m in re.split(r"[^A-Z0-9]+", (lab or "").upper()) if m and m not in MOTS_VIDES}
    meilleurs = []
    for autre, n in comptes.items():
        if not autre or autre == lab or not n:
            continue
        communs = len(mots & {m for m in re.split(r"[^A-Z0-9]+", autre.upper()) if m and m not in MOTS_VIDES})
        meme_type = fiche.get(autre) is not None and fiche.get(autre) == fiche.get(lab)
        if communs or meme_type:
            meilleurs.append((communs, n, autre, meme_type))
    if not meilleurs:
        return ""
    communs, n, autre, meme_type = max(meilleurs)
    motif = (f"{communs} mot(s) en commun" if communs else "même famille et même forme")
    return f" — confusion probable avec {autre!r} ({n} marques, {motif})"


STATUTS_LEGENDE = {"compte", "absent", "hors_portee"}
HORS_LEGENDE = re.compile(r"^HORS[ _-]?LEGENDE", re.I)


def controler_legende(work, nomen, comptes, classement, mal):
    """Q11-Q14 (voir docstring du module). `comptes` = occurrences par libellé sur les feuilles plan."""
    err = []
    leg_path = os.path.join(work, "legende.csv")
    legende_rows = lire_csv(leg_path, mal)
    roles = {r.get("feuille"): (r.get("role") or "") for r in lire_csv(os.path.join(work, "feuilles.csv"))}
    feuilles_legende = sorted({f for f, r in roles.items() if r == "legende"}
                              | {r.get("feuille") for r in classement if r.get("type") == "legende"})
    if feuilles_legende and not legende_rows:
        err.append(f"Q11 feuille(s) de légende {', '.join(feuilles_legende)} fournie(s) mais legende.csv absent ou vide : "
                   "transcrire chaque ligne de légende (§1b) avant de nommer les familles")
    if legende_rows:
        nos = {}
        for r in legende_rows:
            no = (r.get("no") or "").strip()
            if not no:
                err.append(f"Q11 ligne de legende.csv sans numéro : {r.get('description', '')[:60]!r}")
                continue
            nos[no] = r
        par_ligne = collections.defaultdict(list)
        for n in nomen:
            ref = (n.get("legende") or "").strip()
            if not ref:
                err.append(f"Q11 famille {n.get('label')!r} sans colonne `legende` : citer le numéro de ligne de "
                           "legende.csv, ou HORS LEGENDE avec une réserve")
            elif HORS_LEGENDE.match(ref):
                continue
            elif ref not in nos:
                err.append(f"Q11 famille {n.get('label')!r} cite la ligne de légende {ref!r} absente de legende.csv")
            else:
                par_ligne[ref].append(n)
        for no, r in nos.items():
            statut = (r.get("statut") or "").strip().lower()
            desc = (r.get("description") or "")[:70]
            if statut not in STATUTS_LEGENDE:
                err.append(f"Q11 ligne de légende {no} ({desc!r}) : statut {statut!r} — attendu compte, absent ou hors_portee")
            elif statut == "compte":
                fams = par_ligne.get(no, [])
                if not fams:
                    err.append(f"Q11 ligne de légende {no} ({desc!r}) marquée comptée mais aucune famille ne la cite")
                elif not any(comptes.get(n.get("label")) for n in fams):
                    err.append(f"Q11 ligne de légende {no} ({desc!r}) marquée comptée mais aucune occurrence relevée")
            elif not (r.get("preuve") or "").strip():
                err.append(f"Q11 ligne de légende {no} ({desc!r}) marquée {statut} sans preuve (zone du plan vérifiée)")
            if statut in ("absent", "hors_portee") and par_ligne.get(no) and any(comptes.get(n.get("label")) for n in par_ligne[no]):
                err.append(f"Q11 ligne de légende {no} ({desc!r}) marquée {statut} alors que des occurrences la citent")
        # Q12 : une famille par symbole de légende
        for no, fams in par_ligne.items():
            if len(fams) < 2:
                continue
            codes = [LG.code_attendu(n.get("materiel") or n.get("description") or n.get("label") or "") for n in fams]
            if "" in codes or len(set(codes)) < len(codes):
                err.append(f"Q12 ligne de légende {no} éclatée en {len(fams)} familles "
                           f"({', '.join(repr(n.get('label')) for n in fams)}) : une seule famille par symbole ; la "
                           "variante (puissance, circuit) va dans la colonne `designation` de chaque occurrence")
    labels = [n for n in nomen if n.get("label")]
    for i, a in enumerate(labels):
        for b in labels[i + 1:]:
            for champ in ("label", "materiel"):
                if LG.variante_puissance(a.get(champ) or "", b.get(champ) or ""):
                    err.append(f"Q12 {a.get('label')!r} et {b.get('label')!r} ne diffèrent que par la puissance : une "
                               "seule famille, la puissance va dans `designation` de chaque occurrence")
                    break
    # Q13 : modèle tiré du devis quand un devis est fourni
    articles = [r for p in sorted(glob.glob(os.path.join(work, "devis", "*-articles.csv"))) for r in lire_csv(p)]
    if any((r.get("modele") or "").strip() for r in articles):
        for n in nomen:
            if n.get("label") and not (n.get("modele") or "").strip():
                err.append(f"Q13 famille {n.get('label')!r} sans `modele` alors qu'un devis est fourni : référence du devis "
                           "(section dans `source`), EXISTANT, ou MODELE NON INDIQUE DANS LA SOURCE ELECTRIQUE")
    # Q14 : code conforme au vocabulaire de la légende
    for n in nomen:
        if (n.get("discipline") or "").lower() == "incendie" or not n.get("label"):
            continue
        attendu = LG.code_attendu(n.get("materiel") or n.get("description") or "")
        code = re.sub(r"[^A-Z0-9]", "", (n.get("code") or "").upper())
        existant = (n.get("portee") or "").upper() in ("REMPLACER", "CONSERVER")
        if attendu and code and code != attendu and not (existant and LG.code_existant_admis(code, n.get("materiel") or n.get("description") or "")):
            err.append(f"Q14 famille {n.get('label')!r} : code {code!r} alors que la description "
                       f"{(n.get('materiel') or n.get('description'))[:60]!r} donne {attendu!r} (vocabulaire de la légende)")
    return err


RAYON_APPARIEMENT = 3.0   # pt : une occurrence posée au centre vectoriel d'un cercle « porte » sa signature
RAYON_OMISSION = 8.0      # pt : au-delà, le cercle n'est couvert par aucune occurrence


def cercles_vectoriels(pdf_path):
    """Cercles du dessin vectoriel (chemins faits seulement de courbes, boîte carrée de 6 à 40 pt) :
    [(cx, cy, diamètre arrondi 0,1, épaisseur arrondie 0,01)], dans le repère affiché (page tournée)."""
    try:
        import pymupdf
    except ImportError:            # environnement sans pymupdf : contrôle non disponible, jamais bloquant
        return None
    doc = pymupdf.open(pdf_path)
    try:
        page = doc[0]
        M = page.rotation_matrix
        out = []
        for d in page.get_drawings():
            it = d.get("items") or []
            if len(it) < 4 or any(i[0] != "c" for i in it):
                continue
            r = d["rect"] * M
            w, h = r.width, r.height
            if not (6 <= w <= 40) or abs(w - h) > 0.08 * max(w, h):
                continue
            out.append(((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2, round(w, 1), round(d.get("width") or 0, 2)))
        return out
    finally:
        doc.close()


def justifie_q15(reserves, x, y, tol=3.0):
    """Vrai si une ligne de reserves.md mentionne « Q15 » et un couple de coordonnées à moins de `tol` pt."""
    for ligne in reserves.splitlines():
        if "Q15" not in ligne:
            continue
        # « (643, 431) », « 643.5 ; 430.9 » ou, à la française, « 643,5 / 430,9 »
        couples = re.findall(r"(\d+(?:[.,]\d+)?)\s*/\s*(\d+(?:[.,]\d+)?)", ligne) + \
            re.findall(r"(\d+(?:\.\d+)?)\s*[,;]\s*(\d+(?:\.\d+)?)", ligne)
        for a, b in couples:
            if abs(float(a.replace(",", ".")) - x) <= tol and abs(float(b.replace(",", ".")) - y) <= tol:
                return True
    return False


def controler_omissions(work, plans, occ, reserves):
    """Q15 (voir docstring du module)."""
    err = []
    for f in plans:
        pdf = os.path.join(work, "feuilles", f"{f}.pdf")
        if not os.path.isfile(pdf):
            continue
        cercles = cercles_vectoriels(pdf)
        if not cercles:
            continue
        pts = [(c[0], c[1], o.get("label")) for o in occ if o.get("feuille") == f for c in [coordonnees(o)] if c]
        signatures = collections.defaultdict(collections.Counter)
        for x, y, d, lw in cercles:
            for ox, oy, lab in pts:
                if abs(ox - x) <= RAYON_APPARIEMENT and abs(oy - y) <= RAYON_APPARIEMENT:
                    signatures[(d, lw)][lab] += 1
        vus = set()
        for x, y, d, lw in cercles:
            if (d, lw) not in signatures or (round(x), round(y)) in vus:
                continue
            vus.add((round(x), round(y)))
            if any((ox - x) ** 2 + (oy - y) ** 2 <= RAYON_OMISSION ** 2 for ox, oy, _ in pts):
                continue
            if justifie_q15(reserves, x, y):
                continue
            lab = signatures[(d, lw)].most_common(1)[0][0]
            err.append(f"Q15 {f} ({x:.1f}, {y:.1f}) : cercle vectoriel Ø{d} pt, trait {lw} pt — même signature que "
                       f"{lab!r} déjà relevé, mais aucune occurrence : relève-le, ou justifie dans reserves.md une ligne "
                       f"« Q15 ({x:.0f}, {y:.0f}) : <pourquoi ce n'est pas un appareil> » (zoom à l'appui)")
    return err


def controler(work, reference=None, feuille_ref=None, feuille=None):
    err, avert, mal = [], [], []
    classement = lire_csv(os.path.join(work, "feuilles-classement.csv"), mal)
    nomen = lire_csv(os.path.join(work, "nomenclature.csv"), mal)
    occ = lire_csv(os.path.join(work, "occurrences-visuel.csv"), mal) + lire_csv(os.path.join(work, "occurrences-texte.csv"), mal)
    occ = [o for o in occ if o.get("exclure") not in ("1", "oui")]
    tailles = {r["feuille"]: (float(r["largeur_pt"] or 0), float(r["hauteur_pt"] or 0)) for r in lire_csv(os.path.join(work, "feuilles.csv"))}
    reserves = open(os.path.join(work, "reserves.md"), encoding="utf-8").read() if os.path.isfile(os.path.join(work, "reserves.md")) else ""

    # Q0 : lignes mal formées (champ en trop = virgule non échappée dans un libellé ou une note)
    for m in mal:
        err.append(f"Q0 ligne mal formée : {m}")
    # Q1
    for f in ("feuilles-classement.csv", "nomenclature.csv", "reserves.md", "rapport-releve.md"):
        p = os.path.join(work, f)
        if not os.path.isfile(p) or os.path.getsize(p) == 0:
            err.append(f"Q1 sortie manquante ou vide : {f}")
    plans = [r["feuille"] for r in classement if r.get("type") == "plan"]
    par_feuille = collections.Counter(o.get("feuille") for o in occ)
    for f in plans:
        if not par_feuille.get(f):
            err.append(f"Q1 feuille plan sans aucune occurrence : {f}")
    # Q2
    labels = {n.get("label") for n in nomen}
    for lab in sorted({o.get("label") for o in occ} - labels):
        err.append(f"Q2 libellé absent de nomenclature.csv : {lab!r}")
    # Q3
    defs = collections.defaultdict(set)
    for n in nomen:
        defs[n.get("label")].add((n.get("jeton_regex") or "", (n.get("description") or "").upper()))
    for lab, d in defs.items():
        jetons = {j for j, _ in d if j}
        if len(jetons) > 1:
            err.append(f"Q3 libellé {lab!r} fusionne des appareils distincts (jetons {sorted(jetons)}) : un libellé par appareil")
    # Q4 / Q5 / Q6
    vus = collections.defaultdict(list)
    for o in occ:
        m = REPERE.search((o.get("note") or "").upper())
        if not m:
            continue
        pref, niv, num = m.group(1), m.group(2), int(m.group(3))
        rep = f"{pref}{niv}.{num}"
        vus[(o.get("feuille"), rep)].append(o)
        attendus = famille_de_repere(pref, nomen)
        if attendus and o.get("label") not in attendus:
            err.append(f"Q4 classement : {rep} ({o.get('feuille')}) relevé comme {o.get('label')!r}, attendu {sorted(attendus)}")
    for (f, rep), l in vus.items():
        if len(l) > 1:
            err.append(f"Q5 repère {rep} relevé {len(l)} fois sur {f}")
    suites = collections.defaultdict(set)
    for (f, rep) in vus:
        m = REPERE.search(rep)
        suites[(f, m.group(1), m.group(2))].add(int(m.group(3)))
    for (f, pref, niv), nums in suites.items():
        trous = [f"{pref}{niv}.{i}" for i in range(1, max(nums)) if i not in nums]
        trous = [t for t in trous if t not in reserves]
        if trous:
            err.append(f"Q6 {f} : repères manquants dans la suite {pref}{niv}.x : {', '.join(trous[:15])}{' …' if len(trous) > 15 else ''}")
    n_reperes = len(vus)
    if occ and n_reperes == 0:
        avert.append("aucun repère lu dans les notes : Q4-Q6 non vérifiables (classement non contrôlé)")
    # Q7
    for o in occ:
        W, H = tailles.get(o.get("feuille"), (0, 0))
        try:
            x, y = float(o.get("x_pt") or o.get("x") or -1), float(o.get("y_pt") or o.get("y") or -1)
        except ValueError:
            x = y = -1
        if W and not (0 <= x <= W and 0 <= y <= H):
            err.append(f"Q7 coordonnées hors feuille : {o.get('feuille')} {o.get('label')} ({x}, {y})")
    # Q8
    comptes = collections.Counter(o.get("label") for o in occ if o.get("feuille") in plans)
    fiche = {n.get("label"): (n.get("famille", ""), n.get("forme", "")) for n in nomen}
    for lab in sorted(labels):
        if lab and not comptes.get(lab) and lab not in reserves:
            err.append(f"Q8 {lab!r} est dans la nomenclature mais n'est relevé sur aucun plan "
                       f"(ni justifié en réserve){piste_confusion(lab, comptes, fiche)}")
    # Q9
    comparaison = None
    if reference and feuille_ref:
        ref = {r["designation"]: int(r["qte"]) for r in lire_csv(reference) if r.get("feuille") == feuille_ref}
        ia = collections.Counter()
        for o in occ:
            if feuille and o.get("feuille") != feuille:
                continue
            m = REPERE.search((o.get("note") or "").upper())
            fam = m.group(1) if m and m.group(1) in ref else None
            if fam is None:
                cand = [j for n in nomen if n.get("label") == o.get("label") for j in [n.get("jeton_regex") or ""] if j in ref]
                fam = cand[0] if len(set(cand)) == 1 else "?"
            ia[fam] += 1
        comparaison = {f: {"reference": ref.get(f, 0), "ia": ia.get(f, 0)} for f in sorted(set(ref) | set(ia))}
        for f, c in comparaison.items():
            if abs(c["ia"] - c["reference"]) > TOLERANCE_REF * max(c["reference"], 1):
                err.append(f"Q9 {feuille_ref} famille {f} : IA {c['ia']} / référence {c['reference']}")
    # Q10 : positions inventées sur une grille au lieu d'être lues sur le plan
    par_feuille = collections.defaultdict(list)
    for o in occ:
        c = coordonnees(o)
        if c:
            par_feuille[o.get("feuille")].append(c)
    grilles = {}
    for f, pts in sorted(par_feuille.items()):
        g = grille_suspecte(pts)
        if g:
            pas, n, tot = g
            grilles[f] = {"pas": pas, "alignees": n, "total": tot}
            err.append(f"Q10 {f} : {n}/{tot} marques sur une grille de {pas} pt (x et y) — positions "
                       f"inventées, pas lues sur le plan")
        elif len(pts) >= MIN_GRILLE and (part := part_arrondie(pts)) >= SEUIL_GRILLE_AVERT:
            avert.append(f"Q10 {f} : {part:.0%} des marques sur un multiple de 10 pt (relevés humains "
                         f"mesurés : 0,9 %) — lectures arrondies, positions à revalider")
    # Q11-Q14 : familles tirées de la légende, une famille par symbole, modèle tiré du devis, code du vocabulaire
    err += controler_legende(work, nomen, comptes, classement, mal)
    # Q15 : symboles identiques à un symbole relevé mais sans occurrence (omissions probables)
    err += controler_omissions(work, plans, occ, reserves)
    res = {"conforme": not err, "erreurs": err, "avertissements": avert, "occurrences": len(occ), "reperes_lus": n_reperes,
           "comparaison_reference": comparaison, "grilles_suspectes": grilles}
    json.dump(res, open(os.path.join(work, "qualite.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    return res


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("work"); ap.add_argument("--reference"); ap.add_argument("--feuille-ref"); ap.add_argument("--feuille")
    a = ap.parse_args()
    r = controler(a.work, a.reference, a.feuille_ref, a.feuille)
    print(f"conforme={r['conforme']} erreurs={len(r['erreurs'])} occurrences={r['occurrences']} repères={r['reperes_lus']}")
    for e in r["erreurs"][:40]:
        print(" -", e)
    sys.exit(0 if r["conforme"] else 2)


if __name__ == "__main__":
    main()

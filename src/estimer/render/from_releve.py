"""Bridge: releve/ chain output -> EXEMPLE renderer input (estimate.json + bordereau.csv + reserves.md + plans.pdf).

    python -m src.estimer.render.from_releve WORKDIR OUT_DIR [--render OUT.pdf]

WORKDIR is a relevé working directory prepared by `releve/prepare.py` and filled by the `releveur` agent
(`feuilles.csv`, `feuilles-classement.csv`, `nomenclature.csv`, `occurrences-texte.csv`, `occurrences-visuel.csv`,
`reserves.md`, `feuilles/<F>.pdf`). OUT_DIR receives:

  plans.pdf        the original vector page of every sheet that has occurrences, in sheet-name order
  estimate.json    one counter per nomenclature label; one element per occurrence (x/y in PDF points,
                   width_px/height_px = page size in points, so the renderer maps 1:1)
  bordereau.csv    one row per repère (gold `bordereau-materiel.csv` schema + `reserve`)
  reserves.md      `## <sheet>` sections for the "RESERVES ET COMPLEMENTS" block
  feuilles.json    per sheet: display name, source sheet id, page, bordereau format

Nothing is invented: every row is one occurrence written by the relevé; descriptive fields come from the
nomenclature/occurrence columns the relevé wrote, otherwise the neutral wording MODELE NON PRECISE / A PRECISER.

Optional columns read when present (written by the `releve-planexpert` skill since 2026-09-29):
  nomenclature.csv : code (symbol tag on the plan, e.g. DF, K, CE2), materiel (family name), portee, modele,
                     prescription, discipline (incendie | electricite | urgence)
  occurrences-*.csv: designation, portee, modele, prescription, parent, qte, reserve, x0_pt, y0_pt, x1_pt, y1_pt
  feuilles-classement.csv : bordereau (materiel | agrege | travaux)
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "releve"))
from commun import load_feuilles, load_nomenclature, read_csv  # noqa: E402  (releve/ helpers are the single source of truth)
from .ancrage import LINEAR_MAX, LINEAR_W, SYM_MAX, SymbolIndex, _rect_dist, anchor, word_boxes  # noqa: E402
from . import style as S  # noqa: E402

DEFAULT_MODEL = "MODELE NON PRECISE"
DEFAULT_PORTEE = "A PRECISER"
FORMATS = ("materiel", "agrege", "travaux")
# releve family -> EXEMPLE discipline (repère prefix): I = incendie, M = materiel electrique
INCENDIE = {"alarme", "securite_incendie", "incendie"}
URGENCE = {"secours", "urgence"}
# releve shape (Plan Expert enum or name) -> renderer marker; boxes with a bbox are drawn as rectangles
SHAPES = {"2": "diamond", "losange": "diamond"}
READING_BAND_PT = 40.0     # reading order of sources: top-to-bottom bands of 40 pt, then left-to-right
ANCHOR_TEXT_R = 14.0       # a text tag is attached to the closest vector symbol within 14 pt of the tag box
REVALIDER = "revalider"


def _glyphe_symbole(token: str) -> bool:
    """Jeton fait seulement de signes (« $ », « # ») : glyphe de symbole dessiné par une police CAO."""
    t = (token or "").strip()
    return bool(t) and not any(ch.isalnum() for ch in t)


def _touch(a: pymupdf.Rect, b: pymupdf.Rect, gap: float = 1.0) -> bool:
    dx = max(b.x0 - a.x1, a.x0 - b.x1, 0.0)
    dy = max(b.y0 - a.y1, a.y0 - b.y1, 0.0)
    return dx <= gap and dy <= gap


def _add_note(o: dict, text: str) -> None:
    """Motif de réserve posé par le rendu (ancrage) ; la note du relevé (lieu, jeton) reste intacte."""
    o.setdefault("motifs", []).append(text)


def reserve_motif(o: dict) -> str:
    """Motif affiché au bordereau : motifs d'ancrage, plus la note du relevé quand la marque est en réserve.
    Les notes de lieu des marques sans réserve (« log. A chambre, note 4 ») ne sont pas des motifs."""
    parts = list(o.get("motifs", []))
    if _cell(o, "reserve") and _cell(o, "note") and not _jeton(o):
        parts.insert(0, _cell(o, "note"))
    return "; ".join(parts)


def _to_text(o: dict, why: str, stats: dict, key: str) -> None:
    """Keep the text position, reserve with '*' (identification a revalider)."""
    o["flags"] = [REVALIDER]
    o["reserve"] = o.get("reserve") or "1"
    _add_note(o, why)
    stats[key] += 1


def anchor_sheet(page: pymupdf.Page, items: list[dict], idx: SymbolIndex | None = None) -> dict:
    """Move every text mark onto the symbol its tag designates (EXEMPLE: marker around the SYMBOL).

    Pass 1 finds a symbol per text mark. Pass 2 settles claims: a symbol wanted by marks of different
    families goes to the mark whose tag is closest; the others keep their text position with '*'.
    Text marks with no symbol within ANCHOR_TEXT_R, or ambiguous between glued symbols, get '*' and a
    reserve. Visual marks (placed on the symbol by the relevé) are not moved, nor are glyph marks (a token
    with no letter or digit, e.g. `$` = switch S: the glyph IS the symbol, it is centred on its own box).
    Returns counts."""
    idx = idx or SymbolIndex(page)
    words = word_boxes(page)
    stats = defaultdict(int)
    found = []
    for o in items:
        x, y = o["x"], o["y"]
        o["x_texte"], o["y_texte"] = x, y
        tok = _jeton(o)
        if not (_cell(o, "source").lower() == "texte" or tok):
            stats["visuel_inchange"] += 1
            continue
        near = [w for w in words if w[0].contains(pymupdf.Point(x, y)) or
                abs((w[0].x0 + w[0].x1) / 2 - x) < 4 and abs((w[0].y0 + w[0].y1) / 2 - y) < 4]
        if tok:
            near = [w for w in near if w[1].strip() == tok] or near
        tag, color = (near[0][0], near[0][2]) if near else (pymupdf.Rect(x - 1.5, y - 1.5, x + 1.5, y + 1.5), None)
        if near and _glyphe_symbole(tok or near[0][1]):
            # le jeton est un glyphe de police sans lettre ni chiffre (« $ » = interrupteur S du plan) : c'est le
            # symbole lui-même, pas une étiquette posée à côté. Le recaler sur le cercle voisin le plus proche
            # envoyait 10 CU sur 20 sur les bulles de note 6/8 (essai E08 du 2026-10-05) : on garde le glyphe.
            o["x"], o["y"] = (tag.x0 + tag.x1) / 2, (tag.y0 + tag.y1) / 2
            stats["glyphe_symbole"] += 1
            continue
        a = anchor(idx, tag, ANCHOR_TEXT_R, color, words)
        if a is None:
            _to_text(o, "ancrage symbole non trouve: marque au texte (*)", stats, "texte_sans_symbole")
            continue
        found.append((o, a))
    visuals = [o for o in items if not (_cell(o, "source").lower() == "texte" or _jeton(o))]
    claims: dict[tuple, list] = defaultdict(list)
    keys: list[pymupdf.Rect] = []         # one claim per physical symbol: boxes overlapping >= 50 % merge
    for o, a in found:
        r = pymupdf.Rect(a.bbox)
        # one symbol = one repère: boxes overlapping >= 50 %, or touching parts of one symbol (S box + horn
        # triangle of a klaxon), are the same physical symbol
        key = next((k for k in keys if (k & r).get_area() >= 0.5 * min(k.get_area(), r.get_area())
                    or _touch(k, r)), None)
        if key is None:
            keys.append(r)
            key = r
        claims[tuple(key)].append((a.dist, o, a))
    for key, lst in claims.items():
        lst.sort(key=lambda t: t[0])
        owner_label = lst[0][1]["label"]
        box = pymupdf.Rect(key)
        taken_by = next((v["label"] for v in visuals if v["label"] != owner_label and
                         (box + (-1.5, -1.5, 1.5, 1.5)).contains(pymupdf.Point(v["x"], v["y"]))), None)
        for rank, (d, o, a) in enumerate(lst):
            if taken_by and o["label"] != taken_by:   # a visual mark of another family already sits there
                _to_text(o, f"symbole le plus proche deja releve comme {taken_by} (*)", stats, "symbole_pris")
                continue
            if o["label"] != owner_label:     # symbol belongs to another family's tag (closer)
                _to_text(o, f"symbole le plus proche deja attribue a {owner_label} (*)", stats, "symbole_pris")
                continue
            if rank and o["label"] == owner_label:
                o["flags"] = [REVALIDER]      # same family twice on one symbol: keep both, revalidate
                _add_note(o, "meme symbole qu'une autre marque (*)")
                stats["meme_symbole"] += 1
            if a.ambiguous:
                o["flags"] = [REVALIDER]
                _add_note(o, "ancrage ambigu entre plusieurs symboles (*)")
                stats["ambigu"] += 1
            o["x"], o["y"] = a.x, a.y
            w, h = a.bbox[2] - a.bbox[0], a.bbox[3] - a.bbox[1]
            if max(w, h) > 30:                      # linear symbol (strip light, PL): rectangle on its length
                o["x0_pt"], o["y0_pt"], o["x1_pt"], o["y1_pt"] = (a.bbox[0] - 1, a.bbox[1] - 1,
                                                                  a.bbox[2] + 1, a.bbox[3] + 1)
            else:
                o["rayon"] = max(w, h) / 2 + 1.0   # marker circle drawn AROUND the symbol
            stats["texte_ancre"] += 1
    return dict(stats)


PLAN_RECT_REACH = 8.0      # search area around a "plan" family mark
PLAN_RECT_TOUCH = 1.0      # a closed linear shape is taken only if the mark is in it or touches it


def _famille_b(nom_row: dict, label: str):
    return S.palette_b(letter_code(nom_row, label))


def _linear(r: pymupdf.Rect) -> bool:
    big, small = max(r.width, r.height), min(r.width, r.height)
    return SYM_MAX < big <= LINEAR_MAX and 1.5 <= small <= LINEAR_W and big >= 3 * small


def plan_rects(idx: SymbolIndex, items: list[dict], nom: dict) -> int:
    """Gold palette B (spec §2.2) : plinthes PL et linéaires LC = rectangle aux dimensions graphiques du plan.

    Pour chaque marque d'une famille de forme "plan" sans boîte, la boîte est le rectangle linéaire
    (long >= 3 x large, de SYM_MAX à LINEAR_MAX pt) qui contient la marque ; sans rectangle trouvé, la
    marque garde sa forme par défaut (carré). Renvoie le nombre de boîtes posées."""
    n = 0
    for o in items:
        pb = _famille_b(nom[o["label"]], o["label"])
        if not pb or pb[1] != "plan" or all(_float(o.get(k)) is not None for k in ("x0_pt", "y0_pt", "x1_pt", "y1_pt")):
            continue
        p = pymupdf.Rect(o["x"], o["y"], o["x"], o["y"])
        # 1) symbole linéaire fermé qui contient (ou touche) la marque : sa boîte exacte (gold : 7,08 pt)
        area = p + (-PLAN_RECT_REACH, -PLAN_RECT_REACH, PLAN_RECT_REACH, PLAN_RECT_REACH)
        best = None
        for r, _ in idx.shapes_near(area):
            big, small = max(r.width, r.height), min(r.width, r.height)
            if big <= SYM_MAX or big < 3 * small:
                continue
            d = _rect_dist(r, p)
            if d <= PLAN_RECT_TOUCH and (best is None or (d, -small) < best[0]):
                best = ((d, -small), r)
        r = best[1] if best else None
        # 2) sinon, les 4 bords les plus proches autour de la marque, sur un même contour puis sur des contours
        #    distincts (plinthe collée au mur : son bord est le trait du mur). Jamais la forme fermée voisine :
        #    la fenêtre à 6 pt prenait la place de la plinthe.
        if r is None:
            pt = pymupdf.Point(o["x"], o["y"])
            enc = idx.enclosure(pt, reach=LINEAR_MAX / 2)
            if enc is None or not _linear(enc):
                enc = idx.enclosure(pt, reach=LINEAR_MAX / 2, same_shape=False)
            r = enc if enc is not None and _linear(enc) else None
        if r is not None:
            o["x0_pt"], o["y0_pt"], o["x1_pt"], o["y1_pt"] = r.x0, r.y0, r.x1, r.y1
            n += 1
    return n


TYPE_RE = re.compile(r"\btype\s+([A-Z])\b", re.I)
WATT_RE = re.compile(r"\b(\d+)\s*W\b")
CIRCUIT_RE = re.compile(r"\bC(\d+(?:,\d+)*)\b")


def detail_lines(designation: str) -> list[str]:
    """2e (et 3e) ligne d'étiquette des feuilles agrégées (gold p.62 : `LA-01` / `TYPE A` / `C7`,
    `PL-01` / `1250 W C13,15`, `AF-01` / `C2`) lues dans la désignation du relevé. Rien sans circuit lu."""
    c = CIRCUIT_RE.search(designation or "")
    if not c:
        return []
    t, w = TYPE_RE.search(designation), WATT_RE.search(designation)
    out = [f"TYPE {t.group(1).upper()}"] if t else []
    out.append(" ".join(([f"{w.group(1)} W"] if w else []) + [f"C{c.group(1)}"]))
    return out


# symbols with no ASCII decomposition: spelled out instead of silently dropped by the ASCII fold
ASCII_SYMBOLS = {"\u2192": "->", "\u2190": "<-", "\u00ab": '"', "\u00bb": '"', "\u2018": "'", "\u2019": "'",
                 "\u201c": '"', "\u201d": '"', "\u00a7": "par. ", "\u2248": "~", "\u00d7": "x", "\u2260": "<>",
                 "\u2264": "<=", "\u2265": ">=", "\u2013": "-", "\u2014": "-", "\u2026": "...", "\u00b0": " deg",
                 # ligatures : NFKD ne les décompose pas, elles disparaissaient sans trace (« œuvre » -> « uvre »)
                 "\u0153": "oe", "\u0152": "OE", "\u00e6": "ae", "\u00c6": "AE"}


def _fold(s: str) -> str:
    s = _normaliser(s)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", s).strip()


def _normaliser(s: str) -> str:
    """Nettoyage commun : guillemets français resserrés et symboles hors Latin-1 remplacés."""
    s = re.sub("\u00ab[\\s\u00a0\u202f]*", "\u00ab", s or "")      # French guillemets: drop the inner spaces
    s = re.sub("[\\s\u00a0\u202f]*\u00bb", "\u00bb", s)
    return "".join(ASCII_SYMBOLS.get(ch, ch) for ch in s)


def ascii_upper(s: str) -> str:
    """EXEMPLE text is unaccented upper-case ASCII (REPERES, QUANTITES).

    Écart conservé volontairement : ces colonnes (code, designation, portee, parent,
    materiel) servent de clés de jointure avec `nomenclature.csv` et avec le bordereau
    de l'estimateur, lui-même sans accents. Plier ici garde le rapprochement stable ;
    l'accent reviendrait des deux côtés ou d'aucun, jamais d'un seul."""
    return _fold(s).upper()


def texte_lisible(s: str) -> str:
    """Texte libre (modèle, prescription, note, réserve) : les accents sont conservés.

    L'EXEMPLE les a perdus (« Calibre et caracteristiques a verifier ») ; c'est un défaut
    de son export, pas une règle de présentation — vérifié : la police `helv` du rendu est
    en Latin-1 et restitue é è à ç î ô û sans perte après aller-retour PDF. On ne reproduit
    donc pas ce défaut. Tout caractère hors Latin-1 reste plié, sinon le PDF afficherait
    un signe faux à la place."""
    s = _normaliser(s)
    s = "".join(ch if _latin1(ch) else unicodedata.normalize("NFKD", ch).encode("ascii", "ignore").decode("ascii")
                for ch in s)
    return re.sub(r"\s+", " ", s).strip()


def _latin1(ch: str) -> bool:
    try:
        ch.encode("latin-1")
    except UnicodeEncodeError:
        return False
    return True


def ascii_text(s: str) -> str:
    """Conservé pour compatibilité : redirige vers `texte_lisible`."""
    return texte_lisible(s)


def natural_key(name: str):
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", name)]


def _cell(r: dict, key: str) -> str:
    return (r.get(key) or "").strip()


def _float(v, default=None):
    try:
        return float(str(v).replace(",", "."))
    except (TypeError, ValueError):
        return default


def read_nomenclature(work: Path) -> dict[str, dict]:
    out = {}
    for r in read_csv(str(work / "nomenclature.csv")):
        label = _cell(r, "label")
        if label:
            out[label] = r
    return out


def read_occurrences(work: Path) -> list[dict]:
    rows = []
    for name in ("occurrences-texte.csv", "occurrences-visuel.csv"):
        for r in read_csv(str(work / name)):
            if _cell(r, "exclure").lower() in ("1", "oui", "x", "true"):
                continue
            x, y = _float(r.get("x_pt")), _float(r.get("y_pt"))
            if x is None or y is None or not _cell(r, "feuille") or not _cell(r, "label"):
                continue
            rows.append(dict(r, x=x, y=y, feuille=_cell(r, "feuille"), label=_cell(r, "label")))
    return rows


def discipline(nom_row: dict) -> str:
    d = _cell(nom_row, "discipline").lower()
    if d in ("incendie", "electricite", "urgence"):
        return d
    fam = _cell(nom_row, "famille").lower()
    if fam in INCENDIE:
        return "incendie"
    if fam in URGENCE:
        return "urgence"
    return "electricite"


def sheet_format(classement: dict, items: list[dict]) -> str:
    """Bordereau format of a sheet: explicit `bordereau` column of feuilles-classement.csv, else
    incendie or schema -> materiel (one row per repère), all urgence -> travaux, other plans -> agrege."""
    f = _cell(classement, "bordereau").lower()
    if f in FORMATS:
        return f
    disc = {it["discipline"] for it in items}
    if (classement.get("type") or "").strip() == "schema" or "incendie" in disc:
        return "materiel"
    if disc == {"urgence"}:
        return "travaux"
    return "agrege"


def letter_code(nom_row: dict, label: str) -> str:
    """Aggregated/travaux family ID (CH, PC, IS): the `code` column, else the letters of the text token."""
    c = ascii_upper(_cell(nom_row, "code"))
    if c:
        return re.sub(r"[^A-Z0-9]", "", c) or "X"
    tok = _cell(nom_row, "jeton_regex")
    if re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", tok):
        return tok.upper()
    return re.sub(r"[^A-Z]", "", ascii_upper(label))[:3] or "X"


def build(work: Path, out: Path, ancrage: bool = True) -> dict:
    work, out = Path(work), Path(out)
    out.mkdir(parents=True, exist_ok=True)
    feuilles = load_feuilles(str(work))
    for r in read_csv(str(work / "feuilles-classement.csv")):   # optional `bordereau` column (not kept by commun)
        if r.get("feuille") in feuilles and _cell(r, "bordereau"):
            feuilles[r["feuille"]]["bordereau"] = _cell(r, "bordereau")
    nom = read_nomenclature(work)
    palette = load_nomenclature(str(work))          # releve/ palette: rgb + Plan Expert shape per label
    occ = read_occurrences(work)
    unknown = sorted({o["label"] for o in occ if o["label"] not in nom})
    if unknown:
        raise SystemExit("labels absents de nomenclature.csv : " + ", ".join(unknown))
    missing = sorted({o["feuille"] for o in occ if o["feuille"] not in feuilles})
    if missing:
        raise SystemExit("feuilles absentes de feuilles.csv : " + ", ".join(missing))

    by_sheet: dict[str, list[dict]] = defaultdict(list)
    for o in occ:
        n = nom[o["label"]]
        it = dict(o, discipline=discipline(n))
        by_sheet[o["feuille"]].append(it)

    # Every classified `plan` sheet is included even with zero occurrences (matches the old renderer:
    # render_pdf.py's `sheets = ... feuilles[f].get("type") == "plan" or by_sheet.get(f)`), so a floor that
    # genuinely has no devices yet still ships in Plans-annotes.pdf instead of silently vanishing.
    fids = sorted({f for f in feuilles if feuilles[f].get("type") == "plan"} | set(by_sheet),
                  key=lambda f: natural_key(feuilles[f]["nom"]))
    plans = pymupdf.open()
    sheets_json, counters, bord_rows, meta = [], defaultdict(list), [], []
    for page_no, fid in enumerate(fids, start=1):
        info = feuilles[fid]
        name = info["nom"]
        src = pymupdf.open(str(work / "feuilles" / f"{fid}.pdf"))
        W, H = src[0].rect.width, src[0].rect.height
        plans.insert_pdf(src)
        if src[0].rotation:                   # marks live in displayed coordinates: bake the rotation into the content stream
            pg = plans[-1]
            M = pymupdf.Matrix(1, 0, 0, -1, 0, src[0].mediabox.height) * src[0].rotation_matrix * pymupdf.Matrix(1, 0, 0, -1, 0, H)
            data = pg.read_contents()
            xr = plans.get_new_xref()
            plans.update_object(xr, "<<>>")
            plans.update_stream(xr, ("q %g %g %g %g %g %g cm\n" % (M.a, M.b, M.c, M.d, M.e, M.f)).encode() + data + b"\nQ")
            pg.set_contents(xr)
            pg.set_rotation(0)
            pg.set_mediabox(pymupdf.Rect(0, 0, W, H))
            pg.set_cropbox(pymupdf.Rect(0, 0, W, H))
        items = by_sheet[fid]
        fmt = sheet_format(info, items)
        idx = SymbolIndex(src[0]) if (ancrage or fmt == "agrege") and items else None
        anc = anchor_sheet(src[0], items, idx) if ancrage else {}
        if fmt == "agrege" and idx is not None:
            anc["rectangle_plan"] = plan_rects(idx, items, nom)
        src.close()
        sheets_json.append({"sheet": name, "page": page_no, "width_px": W, "height_px": H})
        meta.append({"sheet": name, "feuille": fid, "page": page_no, "format": fmt,
                     "type": info.get("type", ""), "note": info.get("note_classement", ""), "ancrage": anc})

        # source ids: reading order over the whole sheet
        order = sorted(items, key=lambda o: (int(o.get("y_texte", o["y"]) // READING_BAND_PT),
                                             o.get("x_texte", o["x"])))
        for k, o in enumerate(order, start=1):
            o["source_id"] = f"{name}-{k:03d}"

        # family codes: materiel sheets number families per discipline in alphabetical order of the
        # family name (EXEMPLE DSI01: I01 AVERTISSEUR DE FUMEE ... I08 RELAIS); other formats use the letter code
        def materiel_of(o):
            n = nom[o["label"]]
            return ascii_upper(_cell(n, "materiel") or _cell(n, "description") or o["label"])
        fam_code: dict[str, str] = {}
        if fmt == "materiel":
            for prefix, disc_set in (("I", {"incendie"}), ("M", {"electricite", "urgence"})):
                names = sorted({materiel_of(o) for o in items if o["discipline"] in disc_set})
                for i, m in enumerate(names, start=1):
                    fam_code[(prefix, m)] = f"{prefix}{i:02d}"
        seq: dict[str, int] = defaultdict(int)
        for o in sorted(items, key=lambda o: (materiel_of(o), int(o.get("y_texte", o["y"]) // READING_BAND_PT),
                                              o.get("x_texte", o["x"]))):
            n = nom[o["label"]]
            mat = materiel_of(o)
            if fmt == "materiel":
                code = fam_code[("I" if o["discipline"] == "incendie" else "M", mat)]
            else:
                code = letter_code(n, o["label"])
            seq[code] += 1
            repere = f"{code}-{seq[code]:02d}"
            designation = ascii_upper(_cell(o, "designation") or _cell(n, "code") or _jeton(o) or o["label"])
            portee = ascii_upper(_cell(o, "portee") or _cell(n, "portee")) or DEFAULT_PORTEE
            modele = ascii_text(_cell(o, "modele") or _cell(n, "modele")) or DEFAULT_MODEL
            prescription = ascii_text(_cell(o, "prescription") or _cell(n, "prescription") or _cell(n, "description"))
            parent = ascii_upper(_cell(o, "parent"))
            qte = _float(o.get("qte"), 1.0)
            reserve = _cell(o, "reserve")
            el = {"sheet": name, "page": page_no, "x": o["x"], "y": o["y"], "repere": repere, "code": code,
                  "source": o["source_id"], "shape": SHAPES.get(_cell(n, "forme").lower(), "circle"),
                  "flags": o.get("flags", [])}
            if o.get("rayon"):
                el["radius"] = round(o["rayon"], 2)
            if fmt == "agrege":
                # gold palette B (spec §2.2-2.3) : couleur, forme et taille fixes par code de famille, quelle que
                # soit la taille du symbole ; code absent de la table -> couleur du relevé, cercle de 10,88 pt
                pb = S.palette_b(code)
                pal = palette.get(o["label"], {})
                if pb:
                    el["color"] = list(pb[0])
                    el["shape"] = "square" if pb[1] == "plan" else pb[1]
                    el["radius"] = pb[2] / 2
                else:
                    if pal.get("rgb"):
                        el["color"] = list(pal["rgb"])
                    el["shape"] = {0: "circle", 1: "square", 2: "diamond"}.get(pal.get("forme"), "circle")
                    el["radius"] = S.PALETTE_B_SIZE / 2
                size = S.LABEL_SIZE_B.get(re.match(r"[A-Z]*", code).group(0))
                if size:
                    el["label_size"] = size
                if not reserve:            # W et circuits affichés seulement s'ils sont vérifiés (pas en réserve)
                    el["label_lines"] = detail_lines(_cell(o, "designation"))
            bb =[_float(o.get(k)) for k in ("x0_pt", "y0_pt", "x1_pt", "y1_pt")]
            if all(v is not None for v in bb):
                el["bbox"] = bb
                el["shape"] = "rect"
            counters[o["label"]].append(el)
            bord_rows.append({"feuille": name, "repere": repere, "source": o["source_id"], "materiel": mat,
                              "designation": designation, "qte": f"{qte:g}", "portee": portee, "modele": modele,
                              "prescription": prescription, "parent": parent, "reserve": reserve,
                              "ref": ascii_text(_cell(n, "source")), "code": code, "format": fmt, "note": ascii_text(reserve_motif(o))})

    plans.save(str(out / "plans.pdf"), garbage=3, deflate=True)
    est = {"source": "releve", "workdir": str(work), "sheets": sheets_json,
           "counters": [{"family": label, "name": label, "elements": els} for label, els in sorted(counters.items())]}
    (out / "estimate.json").write_text(json.dumps(est, ensure_ascii=False, indent=1), encoding="utf-8")
    cols = ["feuille", "repere", "source", "materiel", "designation", "qte", "portee", "modele", "prescription",
            "parent", "reserve", "ref", "code", "format", "note"]
    bord_rows.sort(key=lambda r: (natural_key(r["feuille"]), natural_key(r["repere"])))
    with open(out / "bordereau.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(bord_rows)
    (out / "reserves.md").write_text(reserves_by_sheet(work, [m["sheet"] for m in meta], feuilles),
                                     encoding="utf-8")
    (out / "feuilles.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    return {"sheets": len(meta), "reperes": len(bord_rows), "plans_pages": len(fids)}


def _jeton(o: dict) -> str:
    m = re.match(r"mot '(.+)'$", _cell(o, "note"))
    return m.group(1) if m else ""


def _sheet_tokens(line: str) -> set[str]:
    return {t.replace("-", "").upper() for t in re.findall(r"\b[A-Za-z]{1,4}-?\d{2,4}[A-Za-z]?\b", line)}


def reserves_by_sheet(work: Path, names: list[str], feuilles: dict) -> str:
    """Split the relevé `reserves.md` into `## <sheet>` sections: a reserve line goes to every sheet it names
    (E-201 matches E201); lines naming no relevé sheet are general and go to every sheet."""
    path = work / "reserves.md"
    lines = []
    if path.is_file():
        for raw in path.read_text(encoding="utf-8").splitlines():
            s = raw.strip()
            if not s or s.startswith("#"):
                continue
            s = re.sub(r"^[-*]\s+", "", s).replace("**", "")
            lines.append(ascii_text(s))
    aliases = {n: {n.replace("-", "").upper()} for n in names}
    for fid, info in feuilles.items():
        if info.get("nom") in aliases:
            aliases[info["nom"]].add(fid.replace("-", "").upper())
    general = [l for l in lines if not (_sheet_tokens(l) & set().union(*aliases.values()))]
    out = []
    for n in names:
        own = [l for l in lines if _sheet_tokens(l) & aliases[n]]
        out.append(f"## {n}")
        out += own + general
        out.append("")
    return "\n".join(out) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m src.estimer.render.from_releve", description=__doc__.splitlines()[0])
    ap.add_argument("workdir", type=Path)
    ap.add_argument("out_dir", type=Path)
    ap.add_argument("--render", type=Path, default=None, help="also render the EXEMPLE-format PDF here")
    ap.add_argument("--report", type=Path, default=None)
    ap.add_argument("--sans-ancrage", action="store_true", help="keep relevé positions (no symbol anchoring)")
    a = ap.parse_args(argv)
    res = build(a.workdir, a.out_dir, ancrage=not a.sans_ancrage)
    print(f"{a.out_dir}: {res['sheets']} feuilles, {res['reperes']} reperes")
    if a.render:
        from . import load_input, render
        rep = render(load_input(a.out_dir), a.out_dir / "plans.pdf", a.render)
        print(f"{a.render}: {rep['pages']} pages")
        if a.report:
            a.report.write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

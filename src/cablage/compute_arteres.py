"""
Métré des artères — calcul sur coordonnées PDF exactes.

Porté depuis planexpert-s1857-saint-michel/arteres/compute_arteres.py et
**généralisé** (docs/pipeline-qpl.md §4.2 : « sortir PARAMS, FRAME, LEVEL,
EQ et FEEDERS dans un JSON/CSV par soumission ; garder dans le code
seulement la géométrie »). Le code ci-dessous ne contient donc QUE la
géométrie, commune à toute soumission :

  - trajets horizontaux orthogonaux (distance de Manhattan, A → coude → B) ;
  - départ inter-niveaux via le puits technique
    (manhattan(S,R) + manhattan(R,D)) ;
  - montée verticale = |Δ niveau| + end_rise(source) + end_rise(destination) ;
  - départ « local » = raccord paramétré (ex. CC → unité) ;
  - départ « reserve » = destination non localisée : longueur NULLE et
    statut explicite, jamais une valeur inventée.

CLI :
  python -m src.cablage.compute_arteres --config config.json --out DOSSIER

Schéma du JSON de configuration (toutes les données de la soumission) :
{
  "mm_par_pt_h": 35.27336945,       // calibration (axes horizontaux)
  "mm_par_pt_v": 35.28380074,       // calibration (axes verticaux)
  "px_par_pt": 2.388502970,         // largeur_raster_px / largeur_page_pt
  "frames":    {"E405": [381.0, 1281.12]},          // origine axes (pt)
  "levels":    {"SS": 36155, "RDC": 39200},         // niveaux (mm)
  "storey":    {"SS": 3045, "RDC": 3300},           // hauteur d'étage (mm)
  "sheet_level": {"E405": "SS"},
  "params": {
    "hauteur_appareil_mm": 1500, "extremite_toiture_mm": 1000,
    "raccord_local_cc_m": 3.0, "flexible_mm": 450,
    "support_pas_m": 1.5, "reserve_tirage_pct": 5.0,
    "point_puits_technique": "description de la réserve"
  },
  "equipment": {"P-P1": ["E405", 647.3, 1390.3, "texte PDF"]},
  "riser":     ["E405", 918.2, 723.6],
  "feeders":   [{"id": "F01", "src": "A", "dst": "B", "protection": "...",
                 "spec": "...", "note": "", "route": "direct", "local_m": 0.0}]
}

Sorties (dans --out) : arteres-metres.csv et arteres-summary.json
(ce dernier est l'entrée de `src.cablage.inject_lines`).
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Feeder:
    id: str
    src: str
    dst: str
    protection: str
    spec: str
    note: str = ''
    route: str = 'direct'   # direct | puits | local | reserve
    local_m: float = 0.0


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def end_rise(level, storey, params):
    """Montée d'extrémité (m) : toiture = sortie paramétrée ; sinon hauteur
    d'étage moins hauteur d'appareil, planchée à 0."""
    if level == 'TOIT':
        return params['extremite_toiture_mm'] / 1000.0
    return max(storey[level] - params['hauteur_appareil_mm'], 0) / 1000.0


def segments_same_sheet(a, b):
    """Tracé orthogonal A -> coude -> B en coordonnées feuille (pt)."""
    return [((a[0], a[1]), (b[0], a[1])), ((b[0], a[1]), (b[0], b[1]))]


def calculer(donnees: dict) -> tuple[list[dict], list[dict]]:
    """Calcule le métré de chaque départ. Retourne (rows, qpl_lines) —
    respectivement les lignes du CSV de métré et les tracés raster pour
    l'injection QPL."""
    mm_h = float(donnees['mm_par_pt_h'])
    mm_v = float(donnees['mm_par_pt_v'])
    px_par_pt = float(donnees['px_par_pt'])
    frames = {k: tuple(v) for k, v in donnees['frames'].items()}
    levels = donnees['levels']
    storey = donnees['storey']
    sheet_level = donnees['sheet_level']
    params = donnees['params']
    equipment = {k: tuple(v) for k, v in donnees['equipment'].items()}
    riser = tuple(donnees['riser'])
    feeders = [Feeder(**f) for f in donnees['feeders']]

    def to_building(sheet, x, y):
        ax, by = frames[sheet]
        return ((x - ax) * mm_h / 1000.0, (y - by) * mm_v / 1000.0)

    def to_sheet(sheet, X, Y):
        ax, by = frames[sheet]
        return (ax + X * 1000.0 / mm_h, by + Y * 1000.0 / mm_v)

    rows, lines = [], []
    for f in feeders:
        r = {'id': f.id, 'de': f.src, 'vers': f.dst, 'protection': f.protection,
             'conducteurs_conduit': f.spec, 'parcours': f.route,
             'L_h_m': 0.0, 'L_v_m': 0.0, 'L_direct_h_m': '', 'note': f.note, 'statut': ''}
        if f.route == 'reserve':
            r['statut'] = 'RESERVE: longueur non mesurable, destination non localisee'
            rows.append(r)
            continue
        if f.route == 'local':
            r['L_h_m'] = f.local_m
            r['statut'] = 'parametre raccord local'
            rows.append(r)
            continue
        s_sheet, sx, sy, _ = equipment[f.src]
        d_sheet, dx, dy, _ = equipment[f.dst]
        S = to_building(s_sheet, sx, sy)
        D = to_building(d_sheet, dx, dy)
        ls, ld = sheet_level[s_sheet], sheet_level[d_sheet]
        if s_sheet == d_sheet:
            lh = manhattan(S, D)
            lines.append((f, s_sheet, segments_same_sheet((sx, sy), (dx, dy)), 'H'))
            lv = end_rise(ls, storey, params) + end_rise(ld, storey, params)
            r['parcours'] = 'meme niveau, orthogonal'
        else:
            R = to_building(*riser)
            lh = manhattan(S, R) + manhattan(R, D)
            r['L_direct_h_m'] = round(manhattan(S, D), 2)
            rs = to_sheet(s_sheet, *R)
            rd = to_sheet(d_sheet, *R)
            lines.append((f, s_sheet, segments_same_sheet((sx, sy), rs), 'H-source'))
            lines.append((f, d_sheet, segments_same_sheet(rd, (dx, dy)), 'H-dest'))
            lv = (abs(levels[ld] - levels[ls]) / 1000.0
                  + end_rise(ls, storey, params) + end_rise(ld, storey, params))
            r['parcours'] = 'via puits technique, orthogonal'
        r['L_h_m'] = round(lh, 2)
        r['L_v_m'] = round(lv, 2)
        r['statut'] = 'mesure' if 'NON INDIQUE' not in f.spec else 'mesure - calibre a confirmer'
        rows.append(r)

    for r in rows:
        tot = float(r['L_h_m'] or 0) + float(r['L_v_m'] or 0)
        r['L_total_m'] = round(tot, 2)
        r['L_avec_reserve_m'] = round(tot * (1 + params['reserve_tirage_pct'] / 100.0), 2)
        r['supports_1p5m'] = math.ceil(tot / params['support_pas_m']) if tot else 0

    # Tracés Plan Expert (pixels raster) pour injection QPL
    qpl_lines = []
    for f, sheet, segs, kind in lines:
        els = []
        for (x1, y1), (x2, y2) in segs:
            if abs(x1 - x2) < 0.01 and abs(y1 - y2) < 0.01:
                continue
            els.append({'X1': round(x1 * px_par_pt), 'Y1': round(y1 * px_par_pt),
                        'X2': round(x2 * px_par_pt), 'Y2': round(y2 * px_par_pt)})
        suffixe = '' if kind == 'H' else (
            '[SS->puits]' if kind == 'H-source' else '[puits->' + sheet_level[sheet] + ']')
        name = ('ART %s %s>%s %s' % (f.id, f.src, f.dst, suffixe)).strip()
        qpl_lines.append({'plan': sheet + '_Rev0', 'name': name, 'elements': els, 'feeder': f.id})
    return rows, qpl_lines


def ecrire_sorties(donnees: dict, rows: list[dict], qpl_lines: list[dict], out_dir: Path) -> tuple[Path, Path]:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / 'arteres-metres.csv'
    with open(csv_path, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    summary_path = out_dir / 'arteres-summary.json'
    summary = {
        'params': donnees['params'], 'frames': donnees['frames'], 'levels': donnees['levels'],
        'equipment': donnees['equipment'], 'riser': donnees['riser'],
        'lines': qpl_lines, 'rows': rows,
    }
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding='utf-8')
    return csv_path, summary_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m src.cablage.compute_arteres",
        description="Métré des artères depuis un JSON de configuration de soumission.",
    )
    parser.add_argument("--config", type=Path, required=True,
                        help="JSON des données de la soumission (niveaux, équipements, départs)")
    parser.add_argument("--out", type=Path, required=True,
                        help="Dossier de sortie (arteres-metres.csv + arteres-summary.json)")
    args = parser.parse_args(argv)
    donnees = json.loads(args.config.read_text(encoding='utf-8'))
    rows, qpl_lines = calculer(donnees)
    csv_path, summary_path = ecrire_sorties(donnees, rows, qpl_lines, args.out)
    print('rows', len(rows), 'lines', len(qpl_lines))
    for r in rows:
        print('%s %-9s -> %-8s h=%6.2f v=%5.2f tot=%6.2f  %s'
              % (r['id'], r['de'], r['vers'], r['L_h_m'], r['L_v_m'], r['L_total_m'], r['statut'][:40]))
    print(f"OK : {csv_path} + {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

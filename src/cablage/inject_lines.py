"""
Injecte les parcours horizontaux des artères comme objets <Line> dans un
.qpl existant. Le XML original est préservé octet pour octet hors
insertions (même approche que `src.qpl.import_counters`).

Porté depuis planexpert-s1857-saint-michel/arteres/inject_lines.py avec
les corrections obligatoires du SPEC :

1. BOGUE CORRIGÉ — l'assertion d'unicité des GroupID était toujours vraie :
       assert len(gids2) == len(set(gids2)) - 0 or True
   remplacée par :
       assert len(gids2) == len(set(gids2))
2. Chemins paramétrés : source / résumé / destination sont des arguments
   (le script d'origine lisait `../v3-roundtrip/incoming-project.zip` en
   dur). Couleur, épaisseur de plume, liste des feuilles à passer en
   Precision=2 et rapport mm/px sont des options.

CLI :
  python -m src.cablage.inject_lines SOURCE.qpl SUMMARY.json SORTIE.qpl \
      [--couleur -29696] [--pen-width 6] [--mm-par-px 14.768] \
      [--feuilles-precision E400,E401] [--force]

L'audit JSON (`SORTIE.qpl.audit.json`) contient les sha256 avant/après,
les compteurs et, si --mm-par-px est fourni, la longueur attendue de
chaque artère en mètres — à comparer à ce que Plan Expert affiche.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.sax.saxutils import escape

COULEUR_DEFAUT = '-29696'       # orange ARGB 0xFFFF8800 (PIPELINE §2.6-2.7)
PEN_WIDTH_DEFAUT = 6


def injecter(source: Path, summary_path: Path, destination: Path, *,
             couleur: str = COULEUR_DEFAUT, pen_width: int = PEN_WIDTH_DEFAUT,
             mm_par_px: float | None = None,
             feuilles_precision: list[str] | None = None,
             force: bool = False) -> dict:
    source, destination = Path(source), Path(destination)
    if destination.exists() and not force:
        raise FileExistsError(f"{destination} existe déjà (utiliser --force)")
    summary = json.loads(Path(summary_path).read_text(encoding='utf-8'))
    data = source.read_bytes()
    text = data.decode('utf-8')
    root = ET.fromstring(text.lstrip('﻿'))
    assert root.tag == 'QuoterPlanSession'
    gids = [int(n.get('GroupID')) for n in root.iter() if n.get('GroupID')]
    gid = max(gids)

    fragments_by_plan: dict[str, list[str]] = {}
    expected = []
    for ln in summary['lines']:
        if not ln['elements']:
            continue
        gid += 1
        els = ''.join(
            '\r\n\t\t\t\t\t\t<Element X1="%d" Y1="%d" X2="%d" Y2="%d" />'
            % (e['X1'], e['Y1'], e['X2'], e['Y2']) for e in ln['elements'])
        frag = ('\r\n\t\t\t\t\t<Line Name="%s" GroupID="%d" Color="%s" PenWidth="%d" '
                'PenType="Generic" ShowMeasure="True" Visible="True">%s\r\n\t\t\t\t\t</Line>'
                % (escape(ln['name'], {'"': '&quot;'}), gid, couleur, pen_width, els))
        fragments_by_plan.setdefault(ln['plan'], []).append(frag)
        px = sum(abs(e['X2'] - e['X1']) + abs(e['Y2'] - e['Y1']) for e in ln['elements'])
        entree = {'plan': ln['plan'], 'name': ln['name'], 'group_id': gid,
                  'pixels': px, 'feeder': ln['feeder']}
        if mm_par_px is not None:
            entree['expected_m'] = round(px * mm_par_px / 1000, 2)
        expected.append(entree)

    out = text
    for plan, frags in fragments_by_plan.items():
        m = re.search(r'<Plan Name="%s" FileName="[^"]+">' % re.escape(plan), out)
        assert m, plan
        # fin du premier Layer Index="0" de ce plan
        layer_end = out.find('</Layer>', m.end())
        assert layer_end > 0
        out = out[:layer_end] + ''.join(frags) + '\r\n\t\t\t\t' + out[layer_end:]

    # Précision d'affichage 0.01 m sur les feuilles calibrées demandées
    for sh in feuilles_precision or []:
        m = re.search(
            r'(<Plan Name="%s_Rev0" FileName="[^"]+">.*?<Scale Value="100" Type="0" Precision=")0(")'
            % re.escape(sh), out, re.S)
        if m:
            out = out[:m.start(1)] + m.group(1) + '2' + m.group(2) + out[m.end(2):]

    root2 = ET.fromstring(out.lstrip('﻿'))
    lines_after = [n for n in root2.iter('Line')]
    gids2 = [int(n.get('GroupID')) for n in root2.iter() if n.get('GroupID')]
    # Assertion corrigée (SPEC, correction obligatoire nº 1) : unicitié
    # réelle des GroupID, compteurs et lignes confondus.
    assert len(gids2) == len(set(gids2))
    destination.write_bytes(out.encode('utf-8'))

    audit = {
        'source_sha256': hashlib.sha256(data).hexdigest(),
        'output_sha256': hashlib.sha256(out.encode('utf-8')).hexdigest(),
        'source_bytes': len(data), 'output_bytes': len(out.encode('utf-8')),
        'lines_before': len(list(root.iter('Line'))), 'lines_after': len(lines_after),
        'counters_after': len(list(root2.iter('Counter'))),
        'elements_counter_after': sum(len(c.findall('Element')) for c in root2.iter('Counter')),
        'mm_par_px': mm_par_px, 'expected': expected,
    }
    Path(str(destination) + '.audit.json').write_text(
        json.dumps(audit, ensure_ascii=False, indent=1), encoding='utf-8')
    return audit


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m src.cablage.inject_lines",
        description="Injecte les artères (lignes) d'un résumé JSON dans un .qpl.",
    )
    parser.add_argument("source", type=Path, help=".qpl source (non modifié)")
    parser.add_argument("summary", type=Path, help="arteres-summary.json (sortie de compute_arteres)")
    parser.add_argument("sortie", type=Path, help=".qpl de sortie")
    parser.add_argument("--couleur", default=COULEUR_DEFAUT,
                        help=f"couleur ARGB signée des lignes (défaut {COULEUR_DEFAUT} = orange)")
    parser.add_argument("--pen-width", type=int, default=PEN_WIDTH_DEFAUT,
                        help=f"épaisseur de plume (défaut {PEN_WIDTH_DEFAUT})")
    parser.add_argument("--mm-par-px", type=float, default=None,
                        help="rapport mm par pixel raster, pour la longueur attendue de l'audit "
                             "(ex. page_pt / raster_px × mm_par_pt)")
    parser.add_argument("--feuilles-precision", default=None,
                        help="feuilles à passer en Precision=2, séparées par des virgules (ex. E400,E401)")
    parser.add_argument("--force", action="store_true", help="écraser la sortie si elle existe")
    args = parser.parse_args(argv)
    feuilles = [s.strip() for s in args.feuilles_precision.split(",") if s.strip()] \
        if args.feuilles_precision else None
    audit = injecter(
        args.source, args.summary, args.sortie,
        couleur=args.couleur, pen_width=args.pen_width, mm_par_px=args.mm_par_px,
        feuilles_precision=feuilles, force=args.force,
    )
    print('lines', audit['lines_before'], '->', audit['lines_after'],
          'bytes', audit['output_bytes'])
    for e in audit['expected']:
        longueur = ('  %6.2f m' % e['expected_m']) if 'expected_m' in e else ''
        print('%-9s %-42s gid=%d%s' % (e['plan'], e['name'][:42], e['group_id'], longueur))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

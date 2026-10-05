# Construit le QPL v6 a partir du v5 natif :
#  - forme + couleur par famille alignees sur le releve de M. Dupuis (enum Plan Expert CounterShapeTypeEnum lu dans PlanExpert.exe :
#    0 Circle, 1 Square, 2 Diamond, 3 Triangle, 4 TriangleReversed, 5 Trapeze, 6 TrapezeReversed)
#  - correction : les 2 symboles "3R" du debarcadere 107 sont des bornes de recharge VE (E104 legende,
#    E406 texte "CC 3R" = coupe-circuit NEMA 3R), pas des appareils de chauffage -> F22/F23 retires
#  - legende deplacee a droite du dessin (X/Y en pixels du raster)
import re, sys, json, hashlib, xml.etree.ElementTree as ET

SRC = r'C:\Users\fvegi\.codex\workspaces\2026-09-08-install-planexpert\takeoff\verification\v5-native\files\Saint-Michel-Codex-Releve-v5-20260909.qpl'
OUT = r'C:\Users\fvegi\.codex\workspaces\2026-09-08-install-planexpert\takeoff\verification\Saint-Michel-Codex-Releve-v6-20260909.qpl'
AUDIT = OUT + '.audit.json'

def argb(r, g, b):
    v = 0xFF000000 | (r << 16) | (g << 8) | b
    return str(v - (1 << 32))  # entier signe 32 bits comme Plan Expert

# Palette/formes alignees sur M. Dupuis (rules_dupuis.py, couleurs echantillonnees dans ses legendes)
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rules_dupuis import RULES, CIRCLE, SQUARE, DIAMOND, TRI, TRI_REV, TRAP, TRAP_REV
RULES = [(re.compile(p), s, c, z) for p, s, c, z in RULES]

RENAME = {
    'Chauffage electrique 3R debarcadere - modele a confirmer':
    'Borne de recharge VE (BRVE) avec CC 3R - debarcadere 107 - alimentation non montree',
}
DROP_LINE_PREFIX = ('ART F22 ', 'ART F23 ')
LEGEND_XY = {'E400_Rev0': (4250, 1350), 'E401_Rev0': (4250, 1350), 'E402_Rev0': (4250, 1350), 'E403_Rev0': (4250, 1350),
             'E404_Rev0': (4250, 1350), 'E405_Rev0': (4250, 1350), 'E406_Rev0': (4250, 1350), 'E407_Rev0': (4250, 1350),
             'E408_Rev0': (4250, 1350), 'E409_Rev0': (4250, 1350), 'E200_Rev0': (4250, 1350), 'E600_Rev0': (4250, 1350)}

raw = open(SRC, 'rb').read().decode('utf-8-sig')
root = ET.fromstring(raw)
audit = {'source': SRC, 'source_sha256': hashlib.sha256(open(SRC, 'rb').read()).hexdigest(), 'rules': [], 'unmatched': [], 'renamed': [], 'dropped_lines': [], 'legend': {}}
seen = {}
for plan in root.findall('./Plans/Plan'):
    pn = plan.get('Name')
    for layer in plan.iter('Layer'):
        leg = layer.find('Legend')
        if leg is not None and pn in LEGEND_XY:
            leg.set('X', str(LEGEND_XY[pn][0])); leg.set('Y', str(LEGEND_XY[pn][1])); audit['legend'][pn] = LEGEND_XY[pn]
        for line in list(layer.findall('Line')):
            if line.get('Name', '').startswith(DROP_LINE_PREFIX):
                audit['dropped_lines'].append((pn, line.get('Name'), line.get('GroupID')))
                layer.remove(line)
        for c in layer.findall('Counter'):
            nm = c.get('Name')
            if nm in RENAME:
                audit['renamed'].append((pn, nm, RENAME[nm])); nm = RENAME[nm]; c.set('Name', nm)
            for rx, shape, col, size in RULES:
                if rx.search(nm):
                    c.set('Shape', str(shape)); c.set('Color', argb(*col)); c.set('FillColor', argb(*col)); c.set('DefaultSize', str(size))
                    for el in c.findall('Element'):
                        el.set('Width', str(size)); el.set('Height', str(size))
                    seen.setdefault(nm, (shape, col)); break
            else:
                audit['unmatched'].append((pn, nm))
# retirer les prix des groupes supprimes
dropped_gids = {g for _, _, g in audit['dropped_lines']}
prices = root.find('Prices')
for p in list(prices.findall('Price')):
    gid = p.get('Key').split(';')[0]
    if gid in dropped_gids:
        prices.remove(p)
audit['rules'] = sorted((k, v[0], v[1]) for k, v in seen.items())
audit['n_counters'] = len(list(root.iter('Counter'))); audit['n_lines'] = len(list(root.iter('Line')))
audit['n_elements'] = sum(len(c.findall('Element')) for c in root.iter('Counter'))
xml = ET.tostring(root, encoding='unicode')
open(OUT, 'w', encoding='utf-8').write('<?xml version="1.0"?>\n' + xml)
audit['out_sha256'] = hashlib.sha256(open(OUT, 'rb').read()).hexdigest(); audit['out_bytes'] = len(open(OUT, 'rb').read())
json.dump(audit, open(AUDIT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('counters', audit['n_counters'], 'lines', audit['n_lines'], 'elements', audit['n_elements'])
print('unmatched', audit['unmatched'])
print('renamed', audit['renamed'])
print('dropped', audit['dropped_lines'])
print('sha256', audit['out_sha256'], audit['out_bytes'])

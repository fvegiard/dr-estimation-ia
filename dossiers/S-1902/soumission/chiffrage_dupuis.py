#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S-1902 — chiffrage « méthode Dupuis » (ACCEO) : Σ qté × prix vendant d'assemblage (dernier Dupuis) + Σ qté × temps unitaire Dupuis,
heures arrondies vers le haut (multiple de 10) × 85 $/h (taux Dupuis août-octobre 2026). Lots fournisseur = allocations (comme ses PRIX DE LOT).
Sources : Catalogue-prix-temps-Dupuis.xlsx (Drive 19N8…), dossiers/*/reference-quantites.csv, Estimation_2 (quantités), Lumen 2026-10-07.
Sortie : chiffrage_dupuis.json + impression du sommaire par article de bordereau."""
import json, math
from collections import defaultdict

TAUX = 85.0          # $/h — Dupuis S-1797/S-1835/S-1854/S-1881 (août-oct. 2026)
PI = 3.28084         # m -> pi (catalogue Dupuis en $/pi et h/pi)

# (code, description, qté, unité, prix unitaire vendant Dupuis $, temps unitaire h, article bordereau, source)
L = []
def add(code, desc, q, u, p, h, art, src): L.append(dict(code=code, desc=desc, q=q, u=u, p=p, h=h, art=art, src=src))

# --- A / 5.19 DÉMANTÈLEMENT (Dupuis : 0 $, temps seulement) ---
add('A-01', 'Démantèlement luminaires existants RDC (E.A.E)', 39, 'u', 0, 0.50, '5.19', 'Dupuis « FIXTURE ENLEVE » 0,5 h (S-1844 ×204)')
add('A-02', 'Démantèlement luminaires existants étage (E.A.E)', 7, 'u', 0, 0.50, '5.19', 'idem')
add('A-03', 'Démantèlement services RDC (prises, boîtes, câbles) E.A.E', 34, 'u', 0, 0.35, '5.19', 'Dupuis « ENLEVER PRISE » 0,35 h')
add('A-04', 'Démantèlement services étage (E.A.E)', 10, 'u', 0, 0.35, '5.19', 'idem')
add('A-05', 'Relocalisation équipements services (E.A.R) RDC + étage', 13, 'u', 0, 1.50, '3.22', 'Dupuis « RELO PRISE » 1,5 h (dernier, S-1753 2026-05-05)')
add('A-06', 'Relocalisation luminaires (E.A.R) RDC + étage', 7, 'u', 0, 1.00, '3.22', 'Dupuis « RELO ENCASTRE » 1 h')
add('A-07', 'Relocalisation interrupteurs maîtres du hall (note 1 E-201)', 1, 'lot', 0, 6.0, '3.22', 'jugement (Estimation_2)')
add('A-08', 'FabLab 210 : retrait temporaire + réinstallation luminaires linéaires', 21, 'u', 0, 0.85, '3.22', 'Dupuis FIXTURE ENLEVE 0,5 + réinstall. 0,35 (ENLEVER FIXTURE 1X4)')
add('A-09', 'FabLab 210 : retrait temporaire + réinstallation encastrés', 24, 'u', 0, 0.75, '3.22', 'Dupuis 0,25 (FIXTURE ENCASTRE ENLEV) + 0,5 (réinstall.)')
add('A-10', 'Toit : débrancher/entreposer sectionneurs, isoler câbles, rebrancher ventilation (E.A.R)', 6, 'u', 0, 4.0, '3.22', 'jugement (Estimation_2)')
add('A-11', 'Continuité de service, traçage circuits, réalimentation circuits libérés', 1, 'lot', 0, 16.0, '3.22', 'jugement (Estimation_2)')

# --- B DISTRIBUTION ---
add('B-01', 'Panneau PP-3 NF 225 A 347/600 V 42 cct 14 kA (remplacement) — pose', 1, 'u', 0, 8.0, '3.24', 'Dupuis « PANN 200A 347/600V » 8 h ; fourniture au lot')
add('B-01b', 'Transfert des circuits existants dans PP-3 (14 cct)', 14, 'cct', 0, 0.75, '3.24', 'jugement : 0,75 h/cct')
add('B-02', 'Disjoncteurs NF 1P-15 A (pose)', 17, 'u', 0, 0.20, '3.25', 'Dupuis « DISJ15A1P » 0,2 h ; fourniture au lot')
add('B-03', 'Disjoncteurs NF 3P 15/20/40 A (pose)', 3, 'u', 0, 1.00, '3.25', 'Dupuis « DISJ 100A 3P » 1 h')
add('B-04', 'Disjoncteurs 1P-15 A DDFT et 1P-20 A (pose)', 3, 'u', 0, 0.40, '3.25', 'Dupuis « DISJ 15A2P » 0,4 h')
add('B-09', 'Mise à jour fiches + identification 9 panneaux', 9, 'u', 15.0, 1.0, '3.24', 'Dupuis lamicoïd ≈ 15 $ ; 1 h (Estimation_2)')
add('B-10', 'Tiroirs CCM-1 F15A — vérification/réutilisation (MCC)', 2, 'u', 15.0, 2.0, '3.26', 'jugement')

# --- C RACCORDEMENTS MÉCANIQUES ---
add('C-01', 'UTA-01 575 V/3Ø au toit — raccordement final LFMC + sectionneur d’usine', 1, 'u', 25.0, 1.0, '3.23', 'Dupuis « MOTEUR UAF-1 » 1 h / 25 $')
add('C-01b', 'Conduit EMT 1" 4 #8 (alim. UTA-01) incl. supports', 35 * PI, 'pi', 7.6607, 0.135, '3.23', 'Dupuis « CONDUIT 1 13C12 » 7,6607 $/pi, 0,135 h/pi (dernier 2026-10-07 ; ens. 1" #8 absent → proche)')
add('C-02', 'VE-02N 1,5 HP 575 V c/a VFD — raccordement', 1, 'u', 25.0, 0.75, '3.23', 'Dupuis « MOTEUR » 0,75 h / 25 $ (dernier)')
add('C-03', 'Chaudières CH-01/CH-02 — raccord final LFMC, tiroirs CCM', 2, 'u', 15.0, 0.5, '3.23', 'Dupuis « CHAUDIERE » 0,5 h / 15 $')
add('C-04', 'Humidificateurs HUM-1/2/3 — raccordement', 3, 'u', 15.0, 0.35, '3.23', 'Dupuis « HUMIDIFICATEUR » 0,35 h / 15 $')
add('C-04b', 'Sectionneurs 30 A sans fusible (HUM)', 3, 'u', 133.49, 1.0, '3.23', 'Dupuis « INTERR 30A 3P 600V » 1 h / 133,49 $')
add('C-07', 'Conduit EMT 3/4" 03c12 (VE-02N + HUM)', 80 * PI, 'pi', 4.2441, 0.1128, '3.23', 'Dupuis « CONDUIT 3/4 03C12 » 4,2441 $/pi, 0,1128 h/pi (dernier, S-1857 2026-09-25)')
add('C-08', 'Raccords flexibles LFMC + connecteurs (7 équipements)', 7, 'u', 40.0, 0.25, '3.23', 'Lumen Hydrotite 12,40 $/m + Conseal 15,14 $ ×2 ; 0,25 h')

# --- D / E SERVICES ---
add('D-01', 'Poste de travail intégré mobilier : JB + prise 15 A + prise 20 A + boîte data', 18, 'poste', 64.81 + 60.19 + 13.96 + 17.43, 1.175 + 1.225 + 0.63 + 0.5, '3.28', 'Dupuis prise 15A 64,81/1,175 + prise 15/20A 60,19/1,225 + tel/data 13,96/0,63 + boîte 12x12 17,43/0,5')
add('D-02', 'Tables c/a boîte d’électrification (5) : 2 prises doubles + 4 prises USB chacune (20 USB au relevé E-104)', 5, 'u', 2 * 64.81 + 4 * 77.45, 2 * 1.175 + 4 * 1.125, '3.27', 'Dupuis prise 15A 64,81/1,175 ; USB 77,45/1,125 ; relevé IA : PRISE USB INSTALLER 20')
add('D-03', 'Cabine/isoloir : prise double par JB', 2, 'u', 64.81, 1.175, '3.28', 'Dupuis prise 15A')
add('D-04', 'Écran mur/colonne : prise + data', 2, 'u', 64.81 + 13.96, 1.175 + 0.63, '3.28', 'Dupuis')
add('D-05', 'Kiosque TV : prise + data', 1, 'u', 64.81 + 13.96, 1.175 + 0.63, '3.28', 'Dupuis')
add('D-06', 'Prises doubles murales/colonne neuves', 8, 'u', 64.81, 1.175, '3.28', 'Dupuis prise 15A')
add('D-17', 'Prises MALT isolées (IG orange) — 22 dispositifs', 22, 'u', 64.81 + 12.0, 1.175, '3.29', 'Dupuis prise 15A + supplément dispositif IG (≈12 $, Lumen LEV5262IG non lu)')
add('D-07', 'Prise DDFT 15 A fontaine', 1, 'u', 65.38, 1.30, '3.30', 'Dupuis « PRISE DUPLEX 20A GFI » 65,38 $ / 1,3 h')
add('D-08', 'Sorties data murales/colonne : boîte + conduit 3/4" + corde (65 sorties au relevé − 24 déjà dans les postes/écrans/kiosque)', 41, 'u', 22.32, 0.89, '3.33', 'Dupuis « TEL/DATA 3/4 » 22,32 $ / 0,89 h ; relevé IA : SORTIE DATA INSTALLER 65 (E104 45 + E105 20)')
add('D-09', 'Barrière antivol : 2 JB + raccord panneau PU-1', 1, 'lot', 60.0, 4.0, '3.31', 'jugement (2 boîtes 12x12 + conduit) — Estimation_2 6 h')
add('D-10', 'Bornes de prêt / fontaine hall — JB', 1, 'u', 17.43, 1.0, '3.31', 'Dupuis boîte 12x12 1 h')
add('D-11', 'Boutons d’appel (3) et de panique (1) — boîte + conduit vide', 4, 'u', 15.0, 0.5, '3.31', 'Dupuis « GACHE »/« LECTEUR » 15 $ / 0,5 h (même nature)')
add('D-20', 'Portes à contrôle d’accès : lecteur + gâche (boîtes + conduits)', 7, 'u', 15.0 + 15.0, 0.5 + 0.35, '3.31', 'Dupuis « LECTEUR DE CARTE » 15 $/0,5 h + « GACHE » 15 $/0,35 h (dernier)')
add('D-21', 'Thermostats — boîte + conduit', 6, 'u', 35.0, 0.4, '3.31', 'Dupuis « THERMOSTAT » 35 $ / 0,4 h')
add('D-22', 'Sorties TV', 4, 'u', 15.0, 0.5, '3.33', 'Dupuis « SORTIE TV » 15 $ / 0,5 h')
add('D-12', 'Percements de dalle carottés + coupe-feu (RDC + étage)', 23, 'u', 150.0, 1.0, '3.31', 'Dupuis « PERCEMENT PLANCHER » 150 $ (S-1881) / 1 h')
add('D-12b', 'Coupe-feu (tubes)', 8, 'u', 13.53, 0.5, '3.31', 'Dupuis « COUPE FEU TUBE 10.1 FL O » 13,53 $ / 0,5 h (dernier 2026-03-09 ; Lumen 2026-10-07 : 26,22 $ — Dupuis prime)')
add('D-13', 'Conduit EMT 1" sous dalle (16 courses RDC + 7 étage), 5 cond. #12', (480 + 175) * PI, 'pi', 4.1197, 0.091, '3.31', 'Dupuis « CONDUIT 3/4 07C12 » 4,1197 $/pi, 0,091 h/pi (dernier 2026-09-25 ; 1" 05c12 absent → équivalent)')
add('D-14', 'Conduit EMT 3/4" data sous dalle, vide + corde (11 + 7 courses)', (330 + 175) * PI, 'pi', 1.4097, 0.056, '3.33', 'Dupuis « CONDUIT VIDE 3/4 » 1,4097 $/pi, 0,056 h/pi (dernier 2026-08-19)')
add('D-16', 'Boîtes de tirage 4-11/16, connecteurs, supports — sous dalle', 23, 'u', 9.26, 0.25, '3.31', 'Lumen 6,05 + 3,21 ; Dupuis boîte 0,25 h')
add('D-19', 'Scan dalle béton (GPR) avant carottage', 1, 'lot', 1250.0, 2.0, '3.32', 'Dupuis « SCAN DALLE BETON » 1 250 $ / 2 h')
add('E-02', 'Monuments de plancher Hubbell poke-through (prise 20 A + 2 RJ45)', 2, 'u', 1461.22, 1.0, '3.34', 'Lumen 1 461,22 $ ; Dupuis monument 1 h')
add('E-03', 'Boîtes de plancher refaites (salle 208)', 2, 'u', 250.0, 1.0, '3.34', 'Dupuis « MONUMENT PLANCHER » 250 $ / 1 h')
add('E-04', 'Cabines/salles étage : JB + prise', 3, 'u', 64.81, 1.175, '3.28', 'Dupuis prise 15A')
add('E-01', 'Postes aide au lecteur 227 : JB, 2 prises, data', 2, 'poste', 2 * 64.81 + 13.96, 2 * 1.175 + 0.63, '3.28', 'Dupuis')
add('E-05', 'Écran colonne étage : prise + data', 1, 'u', 64.81 + 13.96, 1.175 + 0.63, '3.28', 'Dupuis')

# --- F ÉCLAIRAGE ---
add('F-01', 'Luminaire A1 2x4 LED encastré — pose', 11, 'u', 0, 0.75, '3.35', 'Dupuis « FIXTURE TYPE A » 0,75 h ; fourniture au lot')
add('F-02', 'Luminaires C1 / C1_1 / C1_3 Axis (33 modules) — pose', 33, 'u', 0, 0.75, '3.35', 'Dupuis 0,75 h/luminaire')
add('F-05', 'Rangées linéaires suspendues (20) : suspension à la dalle, alimentation', 20, 'rangée', 50.0, 1.0, '3.35', 'Dupuis « DROP DE SWITCH »/alim. 0-10V 32-55 $ ; 1 h (Estimation_2)')
add('F-06', 'Luminaire E cylindre suspendu — pose', 3, 'u', 0, 0.75, '3.35', 'Dupuis 0,75 h ; 3 u (E-203)')
add('F-07', 'Enseignes de sortie Z6 — pose', 3, 'u', 0, 1.0, '3.35', 'Dupuis « ENSEIGNE SORTIE » 1 h')
add('F-11', 'Interrupteurs neufs 15 A', 5, 'u', 75.47, 1.075, '3.35', 'Dupuis « INTERRUPTEUR 15A 120V » 75,47 $ / 1,075 h')
add('F-08', 'Conduit EMT 3/4" 03c12 + flexible — raccordement luminaires (35 points)', 280 * PI, 'pi', 4.2441, 0.1128, '3.35', 'Dupuis « CONDUIT 3/4 03C12 » 4,2441 $/pi, 0,1128 h/pi (dernier)')
add('F-10', 'Chaînes de retenue à la dalle, boîtes de jonction, quincaillerie', 46, 'u', 8.0, 0.25, '3.35', 'Dupuis « PARASIMIC » 10 $ / 0,25 h (retenue) — 1 par luminaire')
add('F-LOT', 'PRIX DE LOT ÉCLAIRAGE : A1 ×11 (185 $), Axis SL1 4′×12 (290), 3′×15 (230), 1′×6 (110), trousses rangées (1 500), E ×3 (475), Z6 ×3 (161,60)',
    1, 'lot', 11 * 185 + 12 * 290 + 15 * 230 + 6 * 110 + 1500 + 3 * 475 + 3 * 161.60, 0, '3.35', 'Prix retenus (Gerrie prix réguliers / agents) — confirmés par Frank 2026-10-20')
add('B-LOT', 'PRIX DE LOT DISTRIBUTION : panneau NF 225 A 42 cct + 17 disj. 1P-15, 3 disj. 3P, 3 disj. 1P (DDFT/20 A)', 1, 'lot', 6200.0, 0, '3.24',
    'Schneider NF 225A 42cct 3 400 $ + EDB 1P 95 $ ×20 + EJB 3P 300 $ ×3 — confirmé par Frank 2026-10-20')

# --- G ALARME INCENDIE ---
add('G-01', 'Détecteurs de fumée adressables + base (fournis JCI) — pose', 2, 'u', 0, 0.5, '3.36', 'Dupuis « DETECTEUR A FUMEE » 0,5 h')
add('G-01b', 'Détecteurs Simplex 4098-9714 + base (fourniture JCI)', 2, 'u', 300.0, 0, '3.36', 'Détecteurs JCI — confirmé par Frank 2026-10-20')
add('G-02', 'Conduit EMT 3/4" boucle AI + câble FA 16/2', 30 * PI, 'pi', 1.4097 + 0.41, 0.056 + 0.028, '3.36', 'Dupuis conduit vide 3/4 1,4097 $/pi (dernier) + fil alarme 16 AWG 0,41 $/pi, 0,028 h/pi')
add('G-04', 'Relocalisation annonciateur Simplex', 1, 'u', 0, 8.0, '3.37', 'Dupuis « RELO PANN ANNOCIATEUR » 8 h')
add('G-05', 'Démontage / protection / réinstallation dispositifs AI existants (zones touchées)', 1, 'lot', 0, 12.0, '3.37', 'jugement (Estimation_2)')
add('G-06', 'Assistance électricien programmation / vérification ULC-S537', 1, 'lot', 0, 8.0, '3.38', 'jugement (Estimation_2)')
add('G-07', 'Services JCI/Simplex : bypass, programmation 4007ES, annonciateur, vérification partielle + certificat', 1, 'lot', 7400.0, 0, '3.38', 'Services JCI — confirmé par Frank 2026-10-20')

# --- H FRAIS DE CHANTIER (Dupuis : nacelle/plateforme au lot, sinon heures de jugement) ---
add('H-01', 'Mobilisation / démobilisation, plateforme roulante', 1, 'lot', 1250.0, 16.0, '3.31', 'Dupuis « NACELLE » 1 250 $ / 16 h (dernier, S-1811 2026-07-14)')
add('H-02', 'Coordination EG, dessins d’atelier, plans tels que construits', 1, 'lot', 0, 20.0, '3.31', 'jugement (Estimation_2)')
add('H-03', 'Essais, mise en service, vérification prises existantes (note 3), étiquetage', 1, 'lot', 0, 12.0, '3.31', 'jugement (Estimation_2)')
add('H-04', 'Nettoyage, gestion des déchets', 1, 'lot', 0, 8.0, '3.31', 'jugement (Estimation_2)')

mat = sum(x['q'] * x['p'] for x in L)
hrs = sum(x['q'] * x['h'] for x in L)
hrs_ch = math.ceil(hrs / 10) * 10
mo = hrs_ch * TAUX
total_acceo = mat + mo

# Répartition par article (matériel + MO au taux, les heures de chantier H-xx réparties dans 3.31 tel que codé)
by_art = defaultdict(lambda: [0.0, 0.0])
for x in L:
    by_art[x['art']][0] += x['q'] * x['p']
    by_art[x['art']][1] += x['q'] * x['h']
scale = mo / (hrs * TAUX)   # effet de l'arrondi des heures chargées réparti au prorata
out = {'taux': TAUX, 'materiel': round(mat, 2), 'heures_relevees': round(hrs, 3), 'heures_chargees': hrs_ch, 'main_doeuvre': round(mo, 2),
       'total_acceo': round(total_acceo, 2), 'lignes': L,
       'par_article': {a: {'materiel': round(v[0], 2), 'heures': round(v[1], 2), 'mo': round(v[1] * TAUX * scale, 2), 'total': round(v[0] + v[1] * TAUX * scale, 2)} for a, v in sorted(by_art.items())}}
import os
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chiffrage_dupuis.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f"Matériel (vendant Dupuis + lots) : {mat:,.2f} $")
print(f"Heures relevées : {hrs:,.2f} h  → chargées : {hrs_ch} h × {TAUX} $ = {mo:,.2f} $")
print(f"TOTAL ACCEO (style sommaire Dupuis) : {total_acceo:,.2f} $   part MO {mo/total_acceo:.1%}")
for k in (1.20, 1.244, 1.30, 1.35):
    print(f"  × {k:.3f} (passage au prix de vente, réf. S-1844) = {total_acceo*k:,.0f} $")
print("\nPar article :")
for a, v in sorted(by_art.items()):
    print(f"  {a}: mat {v[0]:9,.0f} $  h {v[1]:7.1f}  total {v[0] + v[1]*TAUX*scale:9,.0f} $")

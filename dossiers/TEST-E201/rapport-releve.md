# Rapport de relevé — E-201 « ÉCLAIRAGE ET ALARME INCENDIE — EXISTANT/DÉMOLITION — REZ-DE-CHAUSSÉE »

**Projet** : Technologie RFID — Bibliothèque Georgette-Lepage, Brossard — SP-GTER-26-0080 (HF experts-conseils, dossier 26-29)
**Feuilles** : E-001 (légende et liste de plans, rôle `legende`), E-201 (plan, échelle 1:100, émission 01 2026-09-16 « émis pour appel d'offre »)
**Entrée** : 2 pages PNG (7946 × 5613 px) converties en PDF A1 raster — aucune couche texte, relevé 100 % visuel.
**Dossier de travail** : `OUTBOX/TEST-E201/travail`

## 1. Méthode
1. Classement : E-001 `legende`, E-201 `plan` (feuille existant/démolition ; zones grises hors portée, R-002).
2. Légende d'abord : les sections ÉCLAIRAGE, ALARME INCENDIE, ÉCLAIRAGE D'URGENCE de E-001 lues au zoom et
   transcrites dans `legende.csv` (42 lignes, 20 comptées, 22 absentes avec zone vérifiée).
3. Appareils répétitifs (2'×2', encastrés) : appariement de gabarit sur le raster (OpenCV), puis lecture de
   chaque étiquette sur des planches de vignettes (72 vignettes) pour `designation` et `portee` (R-003).
4. Autres appareils : grille de 30 zooms de 170 × 130 pt (règles graduées) sur toute la zone blanche ; coordonnées
   interpolées entre graduations, centre du symbole.
5. Contrôle : `controle_qualite.py` → conforme.

## 2. Totaux E-201 (121 repères, 19 familles)

| Code | Famille | Conserver | Enlever | Relocaliser | À préciser | Total |
|---|---|--:|--:|--:|--:|--:|
| L2 | Appareil d'éclairage 2'×2' LED (dont 7 sur PP-U1) | 37 | 8 | | | 45 |
| EN | Appareil d'éclairage encastré (cercle + croix, dont 6 sur PP-U1) | 9 | 19 | | | 28 |
| EC | Cercle simple sans étiquette (R-005) | | | | 2 | 2 |
| LX | Appareil d'éclairage 'x4' (dont 3 sur PP-U1) | | 6 | | | 6 |
| RL | Rail d'éclairage (5 + 3 têtes, R-008) | | 2 | | | 2 |
| I3 | Interrupteur à 3 voies | 4 | 1 | | | 5 |
| IS | Interrupteur simple | 2 | | | | 2 |
| DM | Détecteur de mouvement | 2 | 1 | | | 3 |
| IM | Interrupteurs maîtres — note 1 (R-007) | | | 1 | | 1 |
| BC | Boîtier « C » hors légende (R-006) | 3 | 1 | | | 4 |
| EM | Enseigne de sortie au mur | 4 | 1 | | | 5 |
| EP | Enseigne de sortie au plafond | 2 | | | | 2 |
| AC | Accumulateur (R-009) | 1 | | | | 1 |
| SM | Station manuelle | 3 | | | | 3 |
| PZ | Piezo combiné à un strobe | 2 | | | | 2 |
| DF | Détecteur de fumée (R-004, 5 après vérification) | 4 | | 1 | | 5 |
| HP | Haut-parleur encastré au plafond | 2 | | | | 2 |
| ANN | Panneau annonciateur | | | 1 | | 1 |
| BJ | Boîte de jonction (tête de rail) | | 2 | | | 2 |
| | **Total** | **75** | **41** | **3** | **2** | **121** |

Circuits lus en `designation` : PP-2 3/5/6, PP-U1 2/7, P-2 39/41 ; zones (h,i)/(j,k)/(n)/(Mf)/(Ma).

## 3. Contrôles
- Décompte croisé 2'×2' : 44 appariements + 1 lecture manuelle = 45 ; 3 faux candidats écartés au zoom.
- Encastrés : 28 appariements, aucun doublon à < 4 pt ; 6 pleins (PP-U1) confirmés par mesure d'anneau et par
  l'étiquette PP-U1 lue sur la vignette.
- Chaque label des occurrences existe dans `nomenclature.csv` ; chaque famille cite sa ligne de légende.
- Aucune coordonnée sur grille mentale (Q10) : positions issues des centroïdes raster ou interpolées.

## 4. Ce qui n'a pas pu être relevé
- Neuf : sur E-203 (non fournie). Luminaires des zones grises : hors portée (R-002).
- Longueurs des rails : estimées depuis 1:100, à métrer (R-008).
- Détecteurs de fumée : 5 × A04 confirmés au zoom ×20 après vérification indépendante (R-004, R-012).
- Aucun devis, addenda ni référence d'estimateur : vérification incomplète au sens du critère d'acceptation.

## 5. Outils et modèle
Session interactive (route « session = agent », CLAUDE.md §Agents), modèle **Claude Fable 5.1** (observé dans le
contexte système). `prepare.py`, `zoom.py` (≈ 50 zooms), OpenCV (appariement de gabarit), `controle_qualite.py`.
`traits.py` inutilisable (entrée raster).

**STATUT : relevé complet de l'existant/démolition de E-201 ; À VÉRIFIER pour R-004, R-005, R-006, R-009.**

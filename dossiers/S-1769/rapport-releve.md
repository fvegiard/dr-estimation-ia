# Rapport de relevé — S-1769 CPE Soleil Souriant, agrandissement (St-Constant)

Date : 2026-09-22 · Entrée : `25-0075_E_PERM_SOUM_20260507_Signed.pdf` (7 pages, émission « Permis et soumission »
du 7 mai 2026, révision 2, Larocque Cournoyer). Aucun addenda, aucun export estimateur.

## Méthode
1. Classement des 7 pages sur les aperçus et les cartouches (`feuilles-classement.csv`). Numéros réels :
   E001 légende · E002/E003 devis · E004 tableaux et détails (`250075EPER-p04`) · E101 cédule panneau C + unifilaires
   (`250075EPER-p05`) · E201 localisation (`250075EPER-p06`) · E401 plans éclairage/alarme/services, démantèlement et
   réaménagement (nom provisoire `E004`).
2. Nomenclature (`nomenclature.csv`, 59 libellés) tirée de la légende E001, des tableaux de luminaires, de chauffage et de
   spécifications d'E004, de la cédule E101 et des notes d'E401.
3. Étiquettes texte : les plans sont presque entièrement vectorisés (sans texte) ; seul le symbole $ sort comme mot « S »
   (4 occurrences sur E401, `occurrences-texte.csv`).
4. Relevé visuel tuile par tuile (E401 : r1c1–r3c3 ; E201 : r2c2–r2c3), coordonnées lues sur les règles (± 5 pt).
   Neuf = trait noir ; existant = gris/hachuré, non relevé ; démolition = mention EE.
5. Articles sans symbole au plan : cédule/unifilaire E101 (interrupteur 200 A, borniers, artère, circuit 22),
   détail B d'E004 (porte électrifiée), devis E003 art. 2.22 (minuterie astronomique, détection de présence),
   notes E401 (boîtier de protection, plancher chauffant en 2 zones, sonde, thermostats maître/esclave).
6. Appariement cédule ↔ plan pour ne pas compter deux fois (réserve R-018).

## Totaux par feuille (141 marques)
| feuille (cartouche) | marques | détail |
|---|--:|---|
| E004 → **E401** | 123 | éclairage 37 (A 18, A1 4, B 8, B1 3, D 1, F 1, F1 1, G 1) · secours 6 · alarme 9 (détecteurs 5, klaxons 2, station ER 1, boîtier 1) · commandes 8 ($ 4, gradateurs 4) · prises 16 · chauffage 21 (A 1500 W 7, A 900 W 2, aéroconvecteur ER 1, thermostats 4, sonde 1, plancher 2 zones, RT 4) · mécanique 11 (SE 4, CD 2, AC 2, CE-1 1, ECH 2) · distribution 3 (panneau C, 2 sectionneurs 30 A SF) · porte électrifiée 1 · data 1 · à classer 1 · démolition 9 |
| 250075EPER-p06 → **E201** | 8 | E 4, C 3, D 1 (éclairage extérieur C,33) |
| 250075EPER-p05 → **E101** | 4 | interrupteur 200 A/F:200 A, remplacement des borniers, artère panneau C (à métrer), raccordement mécanique circuit 22 |
| 250075EPER-p04 → **E004** | 3 | porte électrifiée : BA, BJ, RA |
| 250075EPER-p03 → **E003** | 3 | minuterie astronomique 1, détecteurs de présence 2 (à confirmer) |
| E001, E002 | 0 | légende / devis |

Chaque libellé des deux fichiers d'occurrences existe dans `nomenclature.csv` (vérifié par `cut … | sort -u | comm` :
aucun libellé manquant, aucun libellé inutilisé).

## Ce qui n'a pas pu être relevé ou reste incertain
- Linéaires non mesurés : artère 3#250MCM-AL vers le panneau C, 3#12 TECK90 des mini-splits, câbles de la porte électrifiée,
  surface du plancher chauffant (R-012, R-014, R-017).
- Circuit de la plinthe du corridor en conflit avec la cédule (R-002) ; doublon possible du luminaire D entre E401 et
  E201 (R-004) ; F, G, thermostat esclave et UA plafond lus en bord de tuile (R-005, R-011, R-024).
- Détecteurs de présence exigés au devis mais non dessinés : quantité provisoire (R-013).
- Pas de comparaison avec l'estimateur : aucun export fourni (R-020).

## Limites
- Les outils `zoom.py`, `extract_occurrences.py` et `traits.py` n'ont pas pu être lancés (permission refusée dans cette
  session sans approbation) : pas de zoom de contrôle ni de lecture vectorielle neuf/existant ; distinction faite à l'œil
  (gris/hachuré). À relancer `extract_occurrences.py` et contrôler avec `zoom.py` avant de produire le .qpl.
- 28 réserves au total (`reserves.md`).

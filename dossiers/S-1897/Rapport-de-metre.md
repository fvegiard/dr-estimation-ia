# Rapport de métré (par plans) — S-1897

Généré le 2026-10-05 par le pipeline `releve/` (relevé automatique Claude + scripts déterministes). Chaque marque est une occurrence relevée sur le plan (étiquette texte vectorielle ou lecture visuelle) ; les quantités sont des comptes d'objets, sans métrage de câble.

## Résumé

| Feuille | Marques | Libellés |
|---|--:|--:|
| A801 | 66 | 14 |
| **Total** | **66** | **14** |

## Tous les plans

| Libellé | Famille | Quantité |
|---|---|--:|
| APPLIQUE MURALE | luminaire | 3 |
| DETECTEUR FUMEE | alarme | 5 |
| ENCASTRE | luminaire | 11 |
| INT | commande | 12 |
| INT 3 VOIES | commande | 1 |
| LUMINAIRE SUSPENDU | luminaire | 1 |
| PLAFONNIER DETECTEUR MOUVEMENT | luminaire | 4 |
| PLINTHE | chauffage | 10 |
| PRISE | prise | 1 |
| PRISE COMPTOIR | prise | 5 |
| PRISE CONTROLEE INTERRUPTEUR | prise | 7 |
| RACCORD DIRECT VRC | mecanique | 1 |
| THERMOSTAT | chauffage | 4 |
| VENTILATEUR | mecanique | 1 |

## A801

| Libellé | Ce plan | Tous les plans |
|---|--:|--:|
| APPLIQUE MURALE | 3 | 3 |
| DETECTEUR FUMEE | 5 | 5 |
| ENCASTRE | 11 | 11 |
| INT | 12 | 12 |
| INT 3 VOIES | 1 | 1 |
| LUMINAIRE SUSPENDU | 1 | 1 |
| PLAFONNIER DETECTEUR MOUVEMENT | 4 | 4 |
| PLINTHE | 10 | 10 |
| PRISE | 1 | 1 |
| PRISE COMPTOIR | 5 | 5 |
| PRISE CONTROLEE INTERRUPTEUR | 7 | 7 |
| RACCORD DIRECT VRC | 1 | 1 |
| THERMOSTAT | 4 | 4 |
| VENTILATEUR | 1 | 1 |

## Nomenclature (libellé → source de la lecture)

| Libellé | Famille | Description | Source |
|---|---|---|---|
| APPLIQUE MURALE | luminaire | Applique murale - salle d&#x27;attente (legende d&#x27;eclairage) | A-801 legende d&#x27;eclairage ligne 4 |
| DETECTEUR FUMEE | alarme | Detecteur de fumee D.F.E. (hors legende - R-001) | A-801 symbole triangle D.F.E. au plan; absent des legendes |
| ENCASTRE | luminaire | Encastre slim (legende d&#x27;eclairage) | A-801 legende d&#x27;eclairage ligne 1 |
| INT | commande | Interrupteur hauteur standard | A-801 legende electrique ligne 6 |
| INT 3 VOIES | commande | Interrupteur 3 voies hauteur standard | A-801 legende electrique ligne 7 |
| LUMINAIRE SUSPENDU | luminaire | Luminaire suspendu (legende d&#x27;eclairage) | A-801 legende d&#x27;eclairage ligne 2 |
| PLAFONNIER DETECTEUR MOUVEMENT | luminaire | Plafonnier detecteur de mouvement DM (legende d&#x27;eclairage) | A-801 legende d&#x27;eclairage ligne 3 |
| PLINTHE | chauffage | Plinthe electrique | A-801 legende electrique ligne 10 |
| PRISE | prise | Prise electrique hauteur standard | A-801 legende electrique ligne 1 |
| PRISE COMPTOIR | prise | Prise electrique hauteur comptoir PC | A-801 legende electrique ligne 2 |
| PRISE CONTROLEE INTERRUPTEUR | prise | Prise electrique controle par interrupteur C | A-801 legende electrique ligne 4 |
| RACCORD DIRECT VRC | mecanique | Raccord direct VRC (hors legende - R-001) | A-801 symbole VRC sous-sol; absent des legendes |
| THERMOSTAT | chauffage | Thermostat T | A-801 legende electrique ligne 5 |
| VENTILATEUR | mecanique | Ventilateur VENT. (raccordement) | A-801 legende electrique ligne 8 |

# Méthode et constats de l'agent

# Rapport de relevé — S-1897 BR Sorel, A-801

- Modèle réellement exécuté : session interactive Claude (Cowork, identifiant configuré claude-opus-5-5) tenant lieu d'agent ; aucun agent imbriqué lancé.
- Source : `3030 existant et 3036 suite 101 à 106_26-08-27_EF (1).pdf`, page 29/33 (A-801 rév. 16, 2026-08-26) — copie dans INBOX.
- Méthode : prepare.py réel → lecture des légendes (éclairage, électrique) → relevé visuel des deux plans (RDC, sous-sol) sur rendus 110/200 dpi, chaque symbole revérifié au zoom → nomenclature.csv (14 libellés, colonnes code/materiel/portee/modele/prescription remplies depuis la légende) → occurrences-visuel.csv.
- Aucune étiquette texte d'appareil (jeton_regex vide) : 0 occurrence texte ; les 5 mots « PC » de mots.csv coïncident avec les 5 prises comptoir relevées.
- Total : 66 repères / 14 familles sur 1 feuille ; 9 réserves (R-001 à R-009), dont 3 identifications à revalider (*).
- Non relevé : P.E. et prise sur cabinet (M) — en légende, non dessinés (R-005).
- Pas de relevé d'estimateur fourni pour S-1897 : aucune comparaison possible (vérification « pas pire que l'estimateur » incomplète).


# Réserves

# Réserves — S-1897 BR Sorel, feuille A-801 (unité type A)

R-001 — A-801 : symboles D.F.E. (triangle, 5) et VRC (1) présents au plan, absents des légendes électrique et d'éclairage — relevés sous libellé « hors légende », portée A PRECISER ; avertisseur autonome ou détecteur relié au réseau : non tranché par le plan.
R-002 — A-801 RDC W.C. 103A : prise comptoir au lavabo partiellement masquée par le dessin du lavabo — identification à revalider (*).
R-003 — A-801 RDC séjour 101A : prise classée hauteur standard — type à confirmer (*).
R-004 — A-801 RDC sous la poutre (salle à manger / séjour) : prise contrôlée par interrupteur ou standard — glyphe « C » ambigu (*).
R-005 — A-801 : PANNEAU ÉLECTRIQUE (P.E.) et PRISE ÉLECTRIQUE SUR CABINET (M) figurent dans la légende électrique mais aucun symbole n'est dessiné sur les deux plans (RDC, sous-sol) — vérifié tuile par tuile ; non relevés.
R-006 — A-801 : plan électrique « schématique, à titre de coordination et d'information seulement » (note *) ; case MÉC./ÉLEC. vide (pas d'ingénieur électrique) ; tampon « PLAN PAS POUR CONSTRUCTION ».
R-007 — A-801 : quantités = une unité type A ; l'unité type B est en miroir (titre de la feuille) — aucune multiplication par le nombre d'unités sur cette feuille (renvoi au nombre d'unités du projet, 59 logements selon AN25004E, à confirmer).
R-008 — A-801 : aucun circuit ni puissance (W) indiqué au plan ; plinthes « WATT À VALIDER PAR ÉLECTRICIEN » (légende).
R-009 — Sources : aucun devis électrique dans 01_SOURCES ; la directive dc03 porte sur l'entrée électrique (3030/3020), hors A-801 — aucune prescription ajoutée.

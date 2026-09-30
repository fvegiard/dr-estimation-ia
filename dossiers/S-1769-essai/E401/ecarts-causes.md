# S-1769 E401 — écarts IA vs Dupuis et CAUSES (boucle de correction 2026-09-29)
Statut de la cause : **vu** = confirmé sur la capture Plan Expert / le plan ; **probable** = déduit du tableau, à confirmer.

| Écart (famille) | IA / Dupuis | Cause | Statut | Règle (SKILL §5e) |
|---|---|---|---|---|
| Plinthes 1500 W vs 900 W | 11 (1500 + 900 confondus, + 2 sectionneurs) / 7 + 2 | l'IA a compté « plinthe hexagone kW » sans lire la valeur écrite dans l'hexagone (0,9 ou 1,5) | vu (zoom : hexagones « 1.5 » et « 0.9 ») | R1 |
| Sectionneur 30A/SF fondu dans les plinthes | 2 marques dans la famille plinthe / 2 « 30A NF WP » à part | un accessoire posé près d'un appareil a reçu le libellé de l'appareil | vu | R2 |
| Thermostat plancher chauffant | 4 « Thermostat T » / 2 + 2 | thermostat d'ambiance et thermostat du plancher chauffant (note + sonde) non distingués | vu (note « plancher chauffant » sur le plan) | R4 |
| Surface plancher chauffant | 0 surface / 382,5 pi² | l'IA compte des points, Dupuis mesure la surface de la zone | vu (surface magenta) | R7 |
| GFI | 5 « autres à confirmer » / 3 GFI 15/20 A + 1 GFI | le qualificatif GFI n'a pas créé de libellé propre ; symboles identiques regroupés en « à confirmer » | probable | R3 |
| Relais RELO | 0 / 2 | lignes de légende RELO (force flow, station manuelle) jamais cherchées sur le plan | vu (présentes dans la légende Dupuis) | R5 |
| Luminaire F / F1 vs détecteur de fumée | 7 « type F » / 5 détecteurs + F 1 + F1 1 | symboles de forme voisine identifiés par la lettre seule, sans vérifier la ligne de légende | probable | R6 |
| Interrupteur / prise 15-20 A | +1 / −1 | variantes de prise fondues (15/20 A, prise seule) | probable | R3 |
| Longueurs (3/12, 3/16, 21/12, 27/12, UR 3/10…) | non relevées / 6 lignes | l'IA ne mesure aucun linéaire ; pas de réserve « à métrer » | vu (liste Dupuis) | R7 |

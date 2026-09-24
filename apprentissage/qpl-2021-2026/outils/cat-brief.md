# Brief — classer les symboles d'estimation électrique (Plan Expert / DR Électrique, Québec)

Contexte : ces étiquettes viennent de 664 relevés d'estimation électrique réels (fichiers .qpl Plan Expert, 2021-2026) d'un entrepreneur électricien québécois. Chaque étiquette est un symbole compté sur des plans (une prise, un luminaire, un détecteur…). `occ` = nombre total d'occurrences dans le corpus, `projets` = nb de projets où il apparaît.

Ta tâche : pour CHAQUE étiquette de ton lot, produire un objet JSON :
```
{
 "label": "<étiquette exacte>",
 "categorie": "<une des catégories ci-dessous>",
 "sous_type": "<précision courte en français, ex. 'prise duplex 15A', 'luminaire type A', 'détecteur de fumée'>",
 "tension_bt": "BT" | "MT" | "BASSE_TENSION_COMM" | "",   // BT=basse tension puissance (120/347V), BASSE_TENSION_COMM=télécom/données/son, MT=moyenne tension/HT
 "fusion_vers": "<label canonique si ce symbole est une variante d'un autre plus général, sinon ''>",
 "rebut": true|false,   // true si c'est du bruit d'OCR/relevé (ex. 'COMPTEUR 1', 'LOG INT', code illisible) plutôt qu'un vrai symbole d'estimation
 "note": "<≤120 car>"
}
```

Catégories (choisis-en UNE) :
- `dispositif` : prises, interrupteurs, gradateurs, GFI, thermostats, sorties de câblage
- `luminaire` : fixtures/éclairage (FIXT TYPE x, ECL, 1000W, pot lumineux, enseigne de sortie/EXIT)
- `telecom_donnees` : téléphone, data, réseau, son (TEL, HAUT PARLEUR, HP, TEL/DATA, SORTIE TEL)
- `securite_incendie` : détecteurs, stations manuelles, klaxon/horn, strobe, EXIT lumineux d'urgence, caméra, carte d'accès
- `chauffage` : plinthes, serpentins, aérothermes, thermostats de chauffage
- `distribution` : panneaux, disjoncteurs, transformateurs, entrées électriques, boîtes de jonction
- `mecanique_moteur` : moteurs, démarreurs, sectionneurs, VFD
- `autre` : tout le reste identifiable
- `indetermine` : impossible à classer avec certitude

Règles : ne jamais inventer une signification que l'étiquette ne supporte pas — si ambigu, `categorie:"indetermine"` et explique. « ENL » = à enlever (démolition). Les abréviations courantes du milieu : INT=interrupteur, PRISE=réceptacle, TH=thermostat, KS=?, GFI=disjoncteur de fuite à la terre, STROB=stroboscope d'alarme.

Sortie : écris un tableau JSON (un objet par étiquette) au chemin de sortie donné. Valide-le avec python json.load. Message final : nombre d'étiquettes, combien en rebut, combien à fusionner.

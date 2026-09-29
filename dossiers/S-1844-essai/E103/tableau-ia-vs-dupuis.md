# S-1844 E103 — IA (à l'aveugle) vs Dupuis

Référence: `S-1844-Dupuis.qpl`, page « POUR SOUMISSION-page-00006 » (23 marques + 2 lignes de mesure: « B/V » 29 segments ≈ 7 827 px, « Distance 3 » 1 segment ≈ 247 px).
Appariement: affectation optimale marque à marque; échelle/translation ajustées
(×2,082 par rapport aux pt du PDF); seuil 1,2 % de la diagonale = 108 px; écarts réels 0,01-0,09 %.
Script: `scratch/cmp103b.py` (recopié ici: `cmp103.py`). Blind commit: 75cc5b8.

| Famille | IA | Dupuis | Écart | Appariées (position ET libellé) |
|---|---|---|---|---|
| DP1 (NPP16 D EFP 347) | 8 | 8 | 0 | 8/8 |
| DP2 (NPP PCD EFP) | 4 | 4 | 0 | 4/4 |
| PP1 (NPP20 PL BP) | 2 | 2 | 0 | 2/2 |
| SO3 (Dupuis « S03 ») | 2 | 2 | 0 | 2/2 |
| SO4 (Dupuis « S04 ») | 4 | 4 | 0 | 4/4 |
| SW1 (NPODMA) | 2 | 2 | 0 | 2/2 |
| SW6 (NPOD TOUCH) | 1 | 1 | 0 | 1/1 |
| **Total** | **23** | **23** | **0** | **23/23** |
| PS 150, RJ45, SN | réserves sans quantité | aucune marque | non comparable | — |
| Linéaire (câble CAT5e ?) | réserve « à métrer », aucune mesure | 2 lignes: « B/V » (29 seg.) + « Distance 3 » | ÉCART: Dupuis a mesuré, l'IA non | — (lignes jamais appariées) |

## Écarts
Marques: aucun. Lignes: 2 lignes Dupuis (mesures) sans équivalent IA. Seule différence de forme: libellé « SO3/SO4 » (IA, lu sur le plan) vs « S03/S04 » (Dupuis, zéro au lieu de la lettre O): cosmétique.
Marques Dupuis non appariées: 0. Marques IA non appariées: 0.

## Ce que la comparaison ne prouve pas
- Un seul dossier/feuille (23 marques, peu de familles, feuille de contrôle) — pas de preuve de généralité.
- PS 150, RJ45: Dupuis n'a rien posé; l'IA a mis des réserves. Non comparable. Nature exacte des lignes « B/V » / « Distance 3 » non identifiée (libellé seul; le lien avec CAT5e est une hypothèse).
- Le sous-agent avait le même système de fichiers que moi (isolement par consigne) et le SKILL.md contient R1-R8 tirées de S-1769/S-1844 E200; pas de chiffre de E103 dans les entrées données (le superviseur a validé la porte avant la pose).
- Point de départ: l'ambiguïté #16 (DP2 vs NPP16) a été tranchée par le code de commande, confirmée par Dupuis (DP2).

## Cause d'écart non couverte par R1-R8
Écart lignes: cause = la feuille n'a pas d'échelle (« AUCUNE »), donc rien à métrer; couvert par §5b (linéaire → réserve « à métrer »). Pas de R9 proposée; à confirmer par Francis si Dupuis a métré sur une échelle prise ailleurs (Plan Expert: calibrage manuel).

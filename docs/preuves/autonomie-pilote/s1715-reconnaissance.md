# S-1715 — reconnaissance partielle sur quatre feuilles actives

**VÉRIFICATION INCOMPLÈTE.** Ce relevé n'est ni une soumission, ni une validation contre Dupuis.
G8 reste ouverte et le dossier historique n'a pas été remplacé.

Le profil local `RELEVE_PROFIL_S1715=1` refuse une passe déjà gelée et vérifie les SHA-256 des trois
PDF, la [sélection des révisions](../../../releve/profils_revisions/s1715-feuilles.json) et les pages
actives avant d'écrire. La bibliothèque partagée n'a pas changé. Les repères exigent un glyphe et un
libellé, pas seulement du texte : un rectangle A1, un cercle à deux tiges orientables pour le duplex
USB, un PCA encadré dont le renvoi à la note 2 a été contrôlé, ou un contrôleur identifié dans le
schéma. Les deux mentions du modèle dans le détail de raccordement typique sont exclues, tout comme
la mention `PCA` dans une note générale.

| Feuille et source | Repères | Portée et quantité de travaux |
|---|---:|---|
| E-201, ELE-002 p.5 — type A1, recoupé avec E-002 p.2 et le tableau E-101 p.4 | 10 | Portée à confirmer ; quantité de travaux non établie. |
| E-301, ELE-002 p.6 — duplex 15 A, 120 V, avec port USB, légende E-002 p.2 | 2 | Portée à confirmer ; quantité de travaux non établie. |
| E-003, ELE-002 p.3 — contrôleur Wavelinx RSP-C-347-Z1 | 19 | Schéma seulement : pas de cumul dans les quantités de travaux. |
| T-201, soumission p.11 — panneau de contrôle d'accès, légende T-001 p.8 et note 2 de T-201 | 1 | Un panneau fourni et installé par l'entrepreneur selon cette note ; prix et heures non établis. |

Le CSV, le QPL et le PDF annoté contiennent **32 repères**. Le QPL référence les 12 feuilles actives ;
le PDF annoté couvre les quatre feuilles traitées et E-102, non relevée. Les 32 placements ont été
contrôlés sur le PDF produit : [E-201](S1715-E201-controle.png), [E-301](S1715-E301-controle.png),
[E-003](S1715-E003-controle.png) et [T-201](S1715-T201-controle.png). Les montages viennent de la
passe C ; les quatre planches de contrôle, les occurrences et le bordereau sont identiques dans E/F.
Ce contrôle ne prouve pas que les autres symboles, notes ou feuilles sont couverts. Il reste un Q1
sur E-102 et des signatures non reconnues. Aucun parcours de câble ou de conduit n'a été mesuré.

## Rejeu et séparation des preuves

- **484 tests passés**. Deux exécutions du jeu de référence historique sur cinq dossiers, sans
  régression, donnent les mêmes résultats et fichiers de comparaison que le passage précédent.
- Passes E et F, chacune sur une copie des trois PDF d'origine : **25 sorties identiques** octet
  pour octet ([liste et empreintes](S1715-EF-sorties-identiques.sha256), chemins relatifs à `OUTBOX/S-1715/`).
  [Gel E](S1715-E.sha256) et [gel F](S1715-F.sha256) : **32 empreintes par passe** revérifiées avant et après
  la comparaison, depuis `/home/fvdev-ubuntu26/work/preuves-estimation-autonomie/`.
- Comparaisons isolées : `comparaisons/S1715-EF/` sous ce même répertoire. Les deux comparaisons
  strictes restent **VÉRIFICATION INCOMPLÈTE** ; aucune paire de pages n'est attestée. Les CSV
  concordent ; seuls les chemins de provenance changent dans les rapports. Les 401 marques
  humaines restent visibles hors comparaison ; 242 d'entre elles se rattachent par nom à des
  versions présumées remplacées et ne sont pas reportées sur ELE-002.
- Chiffrage de travail E : trois postes non chiffrables ; prix, heures et total non renseignés.
  Aucun prix publié. Le chiffrage de travail, les fonds de Dupuis et le ZIP de revue restent locaux.

## Rejouer sur le poste

Depuis `/home/fvdev-ubuntu26/work/dr-estimation-ia-autonomie/`, prendre un `RELEVE_BASE` neuf :

```bash
RELEVE_BASE=/home/fvdev-ubuntu26/work/preuves-estimation-autonomie/rejeu-s1715-neuf \
RELEVE_DATE=2026-11-24 RELEVE_PROFIL_S1715=1 RELEVE_AGENT=blocs \
uv run releve/run.py --aveugle /home/fvdev-ubuntu26/work/preuves-estimation-autonomie/INBOX/S-1715
```

Pour reprendre l'acceptation : récupérer les avis écrits ELE-001/ELE-002 et les rasters exacts
référencés par Dupuis, puis [attester les fonds après gel](../../boucle-acceptation.md#recaler-les-fonds-en-plans-seuls).
Compléter les familles non couvertes, les métrés et le chiffrage sourcé avant de soumettre un dossier
neuf à la décision de Francis. L'ouverture native dans Plan Expert n'a pas été vérifiée.
# Pilote d'autonomie — preuves du 24 novembre 2026

**Ce pilote n'est pas une autorisation de soumettre.** Lire les décisions [S-1844](../../../dossiers/S-1844/ACCEPTATION.md)
et [S-1715](../../../dossiers/S-1715/ACCEPTATION.md). Les sorties historiques, le gold et la bibliothèque partagée n'ont pas été modifiés.

**Rejeu le plus récent :** [recalage des fonds et passe S-1844 F](recalage-et-d4.md) — 472 tests,
200 repères pour F, deux pilotes en **VÉRIFICATION INCOMPLÈTE** faute de rasters attestés. Les chiffres
ci-dessous décrivent le passage initial D/E/B et ses propres contrôles.

| Contrôle | Résultat |
|---|---|
| Pytest | 455 tests passés ; exit 0 |
| Jeu de référence QPL historique | 5 dossiers disposant des trois pièces ; deux exécutions exit 0, aucune régression, résultats Markdown et JSON identiques entre exécutions. Ce n'est pas le benchmark par poste des 11 dossiers. |
| Démarrage MCP stdio local | 5 essais, de 28,67 à 40,27 ms ; maximum < 200 ms |
| Service MCP local | Bearer tourné : `initialize` 200 avec la nouvelle clé, 401 avec l'ancienne. Image à journal d'accès désactivé : la sonde URL n'apparaît pas dans les journaux ; volume conservé. Connecteurs distants non reconfigurés. |
| Rendu HR26-14 | 87/87 pages, 2 177 repères, 8 196/8 196 cellules, 370/370 calques ; gold source inchangé. Vérifie le rendu, pas le relevé. |
| Rejeu S-1844 D/E | 199 repères, 19 sorties identiques, dont les trois PDF, QPL, quantités et planches. |
| Gel strict S-1844 D / S-1715 B | 33 / 25 fichiers vérifiés avant puis après comparaison. Rejeu avec sortie isolée : CSV identiques et archives historiques intactes. Les deux verdicts restent bloqués. |

Les manifestes `S1844-D.sha256`, `S1844-E.sha256` et `S1715-B.sha256` sont relatifs à
`/home/fvdev-ubuntu26/work/preuves-estimation-autonomie/`, pas à la racine Git. Ils couvrent les
PDF sources et les fichiers de la passe. Les dates, journaux et chemins locaux ne font pas
partie de la preuve de rejeu octet pour octet. Les premières comparaisons B/A avaient réécrit
le seul `controle-aveugle.json` de leur manifeste externe ; D/B valident explicitement la
correction de ce défaut. Les livrables de ces premières passes n'ont pas été modifiés.

## Rejouer sur le poste de travail

```bash
RELEVE_BASE=/home/fvdev-ubuntu26/work/preuves-estimation-autonomie/rejeu-neuf \
RELEVE_DATE=2026-11-24 RELEVE_PROFIL_S1844=1 \
uv run releve/run.py --aveugle /home/fvdev-ubuntu26/work/preuves-estimation-autonomie/INBOX/S-1844
```

Utiliser un dossier de comparaison contenant `reference/` **à part**. Passer le QPL exact de la
passe avec `--qpl-ia` (voir [la boucle](../../boucle-acceptation.md)). Produire le chiffrage
interne ensuite avec `python -m src.releve.chiffrage WORKDIR SORTIE S-1844`, jamais en injectant
le catalogue ou les exports de l'estimateur dans l'INBOX. Le profil contextuel est opt-in et lié
au SHA-256 du jeu 12 pages ; aucune nouvelle règle n'a été ajoutée à la bibliothèque globale.

## Reprise des données

Le connecteur Drive a refusé `files.list` (403, portée OAuth insuffisante). Il n'a ni téléchargé ni
modifié de fichiers. L'[inventaire Drive archivé](../../inventaire-drive-2026-09-23/README.md) permet
de localiser les dossiers, mais n'est pas une preuve que chaque pièce est disponible actuellement.
Priorités pour la reprise : avis de S-1715, plans/ADME de S-1857, plan d'AO et addenda de S-1769,
`Plans/00 Électricité_Plans_pour AO.pdf` et révisions de S-1811, puis `04-ÉLECTRICITÉ/01-PLANS/01-PLANS.pdf`
et addendas de S-1714. S-1689, S-1693, S-1695, S-1797 et S-1808 restent dans l'inventaire à vérifier.
La branche `releve/S-1902-georgette-lepage` ne fournit que des PDF de sortie, pas le plan brut.
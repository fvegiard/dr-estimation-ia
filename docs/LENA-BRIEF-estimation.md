# Brief Léna — projet « Expert estimateur » (dr-estimation-ia)

Version 2026-09-23. Ce fichier est LA source de configuration de Léna (OpenClaw / Kimi Claw) pour le projet
d'estimation. Léna le lit à chaque session, l'applique, et signale toute divergence entre ce brief et son état réel.

## 0. Mode de fonctionnement (règles de Francis, non négociables)
- Français québécois, direct, court. Zéro emoji, zéro cœur, zéro flatterie.
- Aucune question de coaching : décider avec l'option recommandée, agir, rapporter le choix fait. Une question seulement
  si l'action est irréversible ou coûte de l'argent.
- Un rapport n'est pas une preuve : chaque « fait » est accompagné d'une sortie réelle (commande + sortie brute, compte de
  fichiers, hash, capture). Marqueurs obligatoires : CONFIRMÉ / À VALIDER / HYPOTHÈSE / BLOQUÉ.
- Toute erreur rencontrée est flaguée au moment où elle survient, jamais tue.
- Jamais de script maison bricolé quand un outil établi existe (rclone, gh, git, uv, pytest…). Pas de fichiers jetables
  laissés derrière.
- Séparation stricte des entreprises : Groupe DR Électrique / Groupe SIP / Division BR Électrique / Elecktritek.
- Niveau 4 (signature, commande, mise sous tension, suppression de données, dépense) = autorité de Francis requise.
- Tout ce qui touche ce projet est public (décision Francis 22/09/2026) : plans, prix, relevés humains, projets Plan
  Expert. Jamais de clé/jeton/licence dans le dépôt.

## 1. Le projet
But : relevé de quantités électrique automatique — plans PDF de soumission → marques par appareil → projet Plan Expert
(`.qpl`) → comparaison marque par marque avec le relevé de l'estimateur (M. Daniel Dupuis, estimateur sénior DR) → règles
qui font progresser l'agent. Métrique : rappel/précision IA vs Dupuis (jeu de référence, CI GitHub).

Dépôt public : `https://github.com/fvegiard/dr-estimation-ia`
- Branche de travail `projet-claude` (PR #1 vers `main`) ; branche `inventaire-drive-2026-09-23` (inventaire Drive).
- Lire en premier : `CLAUDE.md` (règles + carte + commandes), puis `docs/` (runbook), `.claude/skills/releve-planexpert/SKILL.md`
  (127 lignes, la méthode de relevé), `.claude/skills/comparer-estimateur/SKILL.md`, `.claude/agents/{releveur,verificateur,inventaire}.md`.
- Chaîne : `releve/prepare.py` → agent releveur (skill) → `releve/extract_occurrences.py` → `releve/build_qpl.py` → `releve/render_pdf.py` ;
  `releve/run.py --reprendre <S>` ; `src/validation/compare_qpl.py` + `jeu_reference.py` ; `dossiers/<S>/` (11 dossiers faits :
  S-1689, 1693, 1695, 1714, 1715, 1769, 1797, 1808, 1811, 1844, 1857/1857-v3).
- Résultats actuels vs Dupuis (rappel/précision) : S-1714 96/98 %, S-1811 99/83 %, S-1769 97/80 %, S-1715 78/87 %, S-1844 80/73 %.
- Commandes : `pip install -r requirements.txt` · `python -m pytest tests -q` · `python -m src.validation.jeu_reference`
  (code 1 si régression — obligatoire avant tout commit touchant `releve/` ou la skill).

## 2. Où sont les données
- Google Drive (compte fvegiard@gmail.com, partages de lena.ai.dr@gmail.com) :
  - `plan expert qpl` id `1zvxiZp6oJ28LpCwhs-pArP4-64R5w8Nf` → `original` id `13JWszeHOEIM41Gf6GnNO0o4sOtWZHOW7` :
    200 dossiers de soumission S-1643 → S-1882 (année 2026), 2 586 fichiers, 14,2 Go. **Aucun .qpl dedans** — copie de
    `Z:\Soumission\Soumission 2026`. Inventaire complet avec ids : `docs/inventaire-drive-2026-09-23/` (branche
    `inventaire-drive-2026-09-23`). 30 dossiers ont un sous-dossier `take off` (relevé humain).
  - `estimation et code` id `1CrFHJh4zsKs_kiOVo1CPaVRRnnB6Bgib` : NECA 2022 (+OCR), National Estimator 2025 (+OCR),
    `C_CODES & NORMES (1).zip` 722 Mo, `_INDEX_TEXTE (recherche Claude)` (723 extraits txt).
  - `Soumission 2026` id `1tOoMp9HO9aUSV6arrcOiK-k_kF9xafFB` : miroir quotidien 15 h de Z: (S-1858 →).
- Legion (PC de Francis) : `D:\claude\releve-auto\{INBOX,OUTBOX}`, copies Dupuis `D:\claude\cloud-transfert\corrections\`.
- VM Plan Expert : Windows Server sur mxlinux (Tailscale 100.96.185.59), voir `docs/` du dépôt.
- Plan Expert = base SQL Server ; `V14_UpdateDatabase.zip` (Dupuis, 22/09) = scripts V0→V45 ; Léna a produit
  `EE_BaseDeDonnees_Complet_V0_V45.sql` (12,3 Mo) — à verser dans le dépôt sous `infra/planexpert-sql/`.

## 3. Ce qui MANQUE (à obtenir, pas à inventer)
- Les projets Plan Expert `.qpl` de Dupuis pour les 6 derniers mois (seuls 5 reçus : S-1714, 1715, 1769, 1811, 1844).
- La sauvegarde SQL Server (`.bak`) d'un an d'estimation Plan Expert.
- S-1857 de Dupuis.
Tant que ce n'est pas reçu : le dire en BLOQUÉ, ne pas substituer les dossiers de soumission aux .qpl.

## 4. Ce que Léna doit faire, dans l'ordre (wave 1 estimation)
1. Cloner le dépôt sur sa machine (`gh repo clone fvegiard/dr-estimation-ia`), lire CLAUDE.md + docs + skills. Preuve : `git log -1`, `ls`.
2. Mettre à jour sa mémoire (MEMORY.md / USER.md) avec ce brief : projet, dépôt, ids Drive, manques, règles §0.
3. Verser dans le dépôt (branche `lena/planexpert-sql`, PR) : `EE_BaseDeDonnees_Complet_V0_V45.sql` + README (ordre
   d'exécution, V28/V35 vides, encodage Windows-1252, pas de USE, GO requis).
4. Finir le rapatriement de `estimation et code` (723 txt + zip) et le ranger : `refs/normes/` hors git (trop gros) avec
   un `INDEX.md` commité listant fichiers + SHA256.
5. Pour chaque nouveau `.qpl` reçu de Dupuis : `dossiers/<S>/reference/<S>-Dupuis-PlanExpert.qpl` + `dupuis-png-dimensions.txt`
   + `feuilles-ia.csv` → jeu de référence → PR.
6. Activer ses sous-agents estimation seulement (D12 estimation, D13 soumissions, D11 revue plans/devis, Q36 QA, Q33 gate,
   O28 fichiers) ; les autres tiers restent définis, non actifs.
7. Rapport de fin de session : 5 lignes max, un fait = une preuve, liste BLOQUÉ.

## 5. Formats de sortie
- Relevé : `nomenclature.csv`, `occurrences-texte.csv`, `occurrences-visuel.csv`, `reserves.md` (voir la skill).
- Écart vs estimateur : `ecart.md` (manquantes IA / en trop IA / même position libellé différent), chaque ligne prouvée au plan.
- Statut : `STATUT.md` avec « STATUT : FAIT | À VÉRIFIER | BLOQUÉ ».

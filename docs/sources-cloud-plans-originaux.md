# Sources cloud des plans originaux — accès et procédure (2026-09-30)

Deux emplacements cloud fournis par Francis, vérifiés en **lecture seule** depuis ce bac à sable. Ni l'un
ni l'autre n'a été modifié (aucune permission créée/changée, aucun fichier client téléchargé).

## 1. Google Drive — « plan expert qpl »

- Dossier : https://drive.google.com/drive/folders/1zvxiZp6oJ28LpCwhs-pArP4-64R5w8Nf
- Accès : **anyone-with-link**, vérifié par une requête anonyme simple (`curl`/`requests`, aucun jeton).
- Sous-dossiers immédiats, **confirmés en exécutant le snippet ci-dessous sur ce dossier précis** (pas
  seulement un HTTP 200 sur la page — la sortie du snippet a été comparée aux 3 noms attendus) :
  | Nom | id Drive | rôle |
  |---|---|---|
  | `original` | `13JWszeHOEIM41Gf6GnNO0o4sOtWZHOW7` | dossiers de soumission (mélange, voir rôle des fichiers ci-dessous) |
  | `EXEMPLE SORTIE LLM AI` | `1A3rH5sSboC43Nl0fGU7od35I0x1DQDT6` | **sortie déjà produite** — jamais un plan brut |
  | `SORTIE LLM AI - S-1849 SIP CHUM` | `1gwWpbhCn1LtO0PiQ7up4hHEkPvZUfqbD` | **sortie déjà produite** — jamais un plan brut |

  Les deux dossiers « SORTIE LLM AI » sont nommément des résultats déjà produits (résultat d'IA), pas des
  plans source : ne jamais les traiter comme entrée d'un relevé, seulement comme référence de style
  (c'est déjà le statut de `apprentissage/hr26-14-exemplaire/`, origine EXEMPLE.pdf).

- **Rôle réel des fichiers dans `original`** (vérifié sur un dossier de soumission, pas supposé) : mélange
  de PDF de plan, courriels (`.msg`/`.pdf`), documents Word, **sous-dossier `Prix`** (devis/prix) et
  `Thumbs.db`. Conséquence pour l'identification à l'aveugle (§Critère d'acceptation, `CLAUDE.md`) :
  - **Exclure** le sous-dossier `Prix` et tout ce qui donne un prix, un devis ou la réponse de
    l'estimateur — ce n'est jamais une entrée de relevé.
  - **Ne pas exclure par principe** une pièce jointe de courriel : un plan ou un addenda réellement joint
    à un `.msg`/`.pdf` de correspondance reste une source légitime une fois son contenu extrait et son
    rôle vérifié individuellement (c'est bien un plan, pas un échange administratif). La vérification est
    **par fichier**, pas par type de contenant.

- **Test d'accès minimal, réutilisable** (liste seulement, ne télécharge aucun fichier) :
  ```bash
  curl -sS -L --max-time 25 -o /tmp/drive-folder.html \
    "https://drive.google.com/drive/folders/<ID_DOSSIER>"
  python3 -c "
  import re
  html = open('/tmp/drive-folder.html', encoding='utf-8').read()
  blocks = re.findall(r'AF_initDataCallback\((\{.*?\})\);', html, re.S)
  b = blocks[-1]                  # DERNIER bloc injecté (pas le plus gros en octets : sur ce dossier,
                                   # blocks[2] fait ~28 Ko et n'est pas la liste ; blocks[-1] (~5 Ko) l'est —
                                   # vérifié en listant les tailles et en comparant la sortie aux 3 noms
                                   # attendus, pas supposé par la taille)
  tokens = re.findall(r'\"((?:[^\"\\\\]|\\\\.)*)\"', b)
  mimere = re.compile(r'^(application|image|text)/')
  for i, t in enumerate(tokens):
      if mimere.match(t):
          print(t, '|', tokens[i-1])                # mimeType | nom
  "
  ```
  Repose sur le bloc `AF_initDataCallback` que Drive incorpore dans le HTML public pour tout dossier
  « anyone with link » — pas d'API key, pas de jeton, pas de cookie à conserver. Fragile par construction
  (dépend du format interne de la page Drive, et de la position du bloc utile parmi ceux injectés, qui
  pourrait changer) : **un code HTTP 200 seul ne prouve pas un listing réussi** — toujours vérifier que la
  sortie contient les noms attendus avant de conclure quoi que ce soit sur le contenu d'un dossier. Ce
  snippet, exécuté verbatim le 2026-09-30 sur le dossier racine ci-dessus, a émis les 3 noms attendus.

- **S-1253 — fait mesuré, pas une conclusion d'inexistence** : une recherche textuelle brute
  (`grep -o ".\{30\}1253.\{30\}"`) sur le HTML retourné pour le sous-dossier `original` n'a trouvé **aucun
  nom de dossier contenant « 1253 »**. Limites connues de cette vérification, qui l'empêchent d'être
  une preuve d'absence :
  - La page HTML de `original` n'a livré qu'**environ 50 entrées structurées**, alors que le catalogue déjà
    connu (`docs/inventaire-drive-2026-09-23/`) dénombre ~200 dossiers dans cette même arborescence : la
    vue chargée par un simple GET est **paginée/tronquée** côté Drive (défilement ou requête suivante non
    faits ici) — une bonne partie du contenu réel de `original` n'a tout simplement pas été vue.
  - Seule la liste de premier niveau a été examinée : aucune descente récursive dans les sous-dossiers (un
    dossier `S-1253` pourrait exister imbriqué ailleurs, ou sous un nom de projet non numérique).
  - Seul ce dossier `original` a été interrogé, pas les deux autres sous-dossiers « SORTIE LLM AI », ni un
    éventuel autre emplacement Drive.
  **Conclusion correcte : aucun nom de dossier contenant « 1253 » n'a été trouvé dans les listings
  immédiats examinés — cela ne permet pas de conclure à une absence générale** (dossier imbriqué, autre
  nom, autre racine, page non chargée par la pagination).

## 2. SharePoint — « Mes projets » (Daniel Dupuis)

**Ce dossier est d'abord l'emplacement de référence de l'estimateur** (le module qui le lit,
`src/apprentissage/sharepoint.py::MesProjets`, est explicitement écrit pour « ne rapatrier que ce qui sert
à l'apprentissage : chaque `.qpl` et les pages PNG posées à côté » — c'est-à-dire le relevé et les réponses
de Daniel Dupuis lui-même). Il ne faut **pas** présenter l'ensemble de son contenu comme un corpus de plans
bruts : un dossier de projet peut contenir le `.qpl` de l'estimateur et ses PNG marqués (= la réponse à
comparer, jamais à lire avant l'identification à l'aveugle, §Critère d'acceptation) mélangés à des plans
source. Chaque fichier destiné à l'identification doit être vérifié individuellement comme plan/addenda
original non annoté avant usage — ne jamais présumer qu'un fichier de ce dossier est une entrée de relevé
simplement parce qu'il s'y trouve.

- Site : https://drelectrique-my.sharepoint.com/personal/ddupuis_dreelectrique_com
- Dossier réel : `/personal/ddupuis_dreelectrique_com/Documents/Documents/DANIEL-FRANCIS-JO/Mes projets`
  (⚠️ différent de la racine par défaut codée dans `src/apprentissage/sharepoint.py::RACINE`, qui pointe
  vers l'ancien chemin `Documents/Documents/Plan Expert/Mes projets` — toujours passer `racine=` explicite
  pour ce dossier-ci, ne pas se fier au défaut).
- Lien public (« Anyone », sans expiration, téléchargement autorisé — confirmé par le comportement observé,
  pas seulement rapporté) :
  `https://drelectrique-my.sharepoint.com/:f:/g/personal/ddupuis_dreelectrique_com/IgANwhkY6XozQqRGlFYpejPCASNd72FSk0lM4uryKdA3kHM`
- Accès : le module **existant** `src/apprentissage/sharepoint.py::MesProjets` supporte déjà les
  surcharges `lien=`/`site=`/`racine=` — aucun nouveau code nécessaire, seulement les bons paramètres :
  ```python
  from src.apprentissage.sharepoint import MesProjets

  mp = MesProjets(
      lien="https://drelectrique-my.sharepoint.com/:f:/g/personal/ddupuis_dreelectrique_com/"
           "IgANwhkY6XozQqRGlFYpejPCASNd72FSk0lM4uryKdA3kHM",
      site="https://drelectrique-my.sharepoint.com/personal/ddupuis_dreelectrique_com",
      racine="/personal/ddupuis_dreelectrique_com/Documents/Documents/DANIEL-FRANCIS-JO/Mes projets",
  )
  projets = mp.projets()              # liste seulement — ne PAS appeler mp.telecharger(...) pour un audit d'accès
  fichiers = mp.fichiers(f"{mp.racine}/<nom du projet>")   # noms + tailles, sans télécharger le contenu
  ```
- **Résultat de l'accès** : succès — jeton FedAuth d'invité obtenu dès la première requête (`__init__`),
  **388 dossiers** listés à la racine (réponse JSON complète de l'API REST SharePoint, pas de pagination
  constatée sur cet appel — contrairement au Google Drive ci-dessus).
- **S-1253 — fait mesuré** : aucun des 388 noms ne contient « 1253 » (recherche directe `"1253" in nom`, et
  recherche par numéro extrait `1230 ≤ n ≤ 1300`). Les dossiers numérotés autour de cette période existent
  bel et bien (`S-1216` le 16 septembre 2024, puis `S-1262` le 24 octobre 2024) : un écart de ~46 numéros
  et 5 semaines dans cette liste précise. Cela ne couvre que les 388 noms de premier niveau sous cette
  racine — pas une descente récursive, pas d'autre root SharePoint, pas un nom de projet non numérique qui
  contiendrait S-1253 sans l'avoir dans son propre nom de dossier.

## S-1253 — état de la vérification (pas une conclusion définitive)

Sur les deux sources, aux endroits et avec la méthode décrits ci-dessus : **aucun nom de dossier contenant
« 1253 » n'a été trouvé dans les listings immédiats examinés.** Ce n'est ni une limite d'accès de ce bac à
sable (les deux sources répondent, en lecture anonyme, sans jeton ni cookie à conserver), ni une preuve
que le dossier n'existe pas ou n'a « jamais été classé » : la pagination Drive (§1), l'absence de descente
récursive et l'absence d'autres racines/noms possibles laissent plusieurs façons dont S-1253 pourrait
exister sans avoir été vu ici. Aucun takeoff n'a été commencé pour S-1253 et aucune réponse d'estimateur
n'a été consultée pendant cette vérification ; aucune recherche supplémentaire n'a été relancée depuis
(sur demande explicite de Francis).

## Portée de cette vérification

Uniquement un audit d'accès : lister des noms/tailles/types, pas de corpus téléchargé, pas de nouveau
serveur ni connecteur activé. Les identifiants extraits des pages (jetons de session, clé API interne au
client web Drive vue dans le HTML public) n'ont pas été conservés ni réutilisés au-delà de cette
vérification, et ne sont pas reproduits dans ce document.

# Sources cloud des plans originaux — accès et procédure (2026-09-30)

Deux emplacements cloud fournis par Francis, vérifiés en **lecture seule** depuis ce bac à sable. Ni l'un
ni l'autre n'a été modifié (aucune permission créée/changée, aucun fichier client téléchargé).

## 1. Google Drive — « plan expert qpl »

- Dossier : https://drive.google.com/drive/folders/1zvxiZp6oJ28LpCwhs-pArP4-64R5w8Nf
- Accès : **anyone-with-link**, vérifié par une requête anonyme simple (`curl`/`requests`, aucun jeton).
- Sous-dossiers immédiats (confirmés par lecture directe, pas seulement par métadonnées rapportées) :
  | Nom | id Drive | rôle |
  |---|---|---|
  | `original` | `13JWszeHOEIM41Gf6GnNO0o4sOtWZHOW7` | dossiers de soumission bruts (S-16xx → S-18xx) |
  | `EXEMPLE SORTIE LLM AI` | `1A3rH5sSboC43Nl0fGU7od35I0x1DQDT6` | **sortie déjà produite** — jamais un plan brut |
  | `SORTIE LLM AI - S-1849 SIP CHUM` | `1gwWpbhCn1LtO0PiQ7up4hHEkPvZUfqbD` | **sortie déjà produite** — jamais un plan brut |

  Les deux dossiers « SORTIE LLM AI » sont nommément des résultats déjà produits (résultat d'IA), pas des
  plans source : ne jamais les traiter comme entrée d'un relevé, seulement comme référence de style
  (c'est déjà le statut de `apprentissage/hr26-14-exemplaire/`, origine EXEMPLE.pdf).

- **Rôle réel des fichiers dans `original`** (vérifié sur un dossier de soumission, pas supposé) : mélange
  de PDF de plan, courriels (`.msg`/`.pdf`), documents Word, **sous-dossier `Prix`** (devis/prix) et
  `Thumbs.db`. Avant tout relevé, sélectionner explicitement les PDF de plan — ne jamais inclure le
  sous-dossier `Prix` ni les pièces jointes de correspondance dans le jeu à relever.

- **Test d'accès minimal, réutilisable** (liste seulement, ne télécharge aucun fichier) :
  ```bash
  curl -sS -L --max-time 25 -o /tmp/drive-folder.html \
    "https://drive.google.com/drive/folders/<ID_DOSSIER>"
  python3 -c "
  import re
  html = open('/tmp/drive-folder.html', encoding='utf-8').read()
  blocks = re.findall(r'AF_initDataCallback\((\{.*?\})\);', html, re.S)
  b = blocks[-1]                                    # le plus gros bloc = la liste du dossier
  tokens = re.findall(r'\"((?:[^\"\\\\]|\\\\.)*)\"', b)
  mimere = re.compile(r'^(application|image|text)/')
  for i, t in enumerate(tokens):
      if mimere.match(t):
          print(t, '|', tokens[i-1])                # mimeType | nom
  "
  ```
  Repose sur le bloc `AF_initDataCallback` que Drive incorpore dans le HTML public pour tout dossier
  « anyone with link » — pas d'API key, pas de jeton, pas de cookie à conserver. Fragile par construction
  (dépend du format interne de la page Drive) : si ça casse, `curl -sS -o /dev/null -w "%{http_code}\n"`
  donne d'abord le code HTTP exact pour diagnostiquer.

- **S-1253** : recherche textuelle brute (`grep -o ".\{30\}1253.\{30\}"`) sur le HTML complet du dossier
  `original` → **aucune correspondance**. La liste commence à S-1643 (même point de départ que
  `docs/inventaire-drive-2026-09-23/`, cohérent avec un même périmètre : « toute l'année 2026 »). Un
  dossier `S-1253...` triée par ordre alphabétique se serait placé avant S-1643 dans la liste — sa place
  est vide, pas seulement non vue.

## 2. SharePoint — « Mes projets » (Daniel Dupuis)

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
  **388 dossiers** listés à la racine.
- **S-1253** : absent des 388 noms (recherche `"1253" in nom` et recherche par numéro extrait `1230 ≤ n ≤
  1300`). Les dossiers numérotés autour de cette période existent bel et bien (`S-1216` le 16 septembre
  2024, puis saut direct à `S-1262` le 24 octobre 2024) : **un vrai trou de ~46 numéros et 5 semaines**,
  pas un problème de nommage ou de casse — S-1253 n'a simplement jamais été classé sous ce chemin
  SharePoint, quelle qu'en soit la raison côté Drive/SharePoint de Francis.

## Conclusion sur S-1253

Vérifié en direct sur les deux sources (pas seulement sur un catalogue local déjà périmé) :
**aucun dossier S-1253 n'existe ni dans Google Drive → `original`, ni dans SharePoint → `Mes projets`.**
Ce n'est plus une limite d'accès de ce bac à sable (les deux sources répondent, en lecture anonyme, sans
jeton ni cookie à conserver) — c'est une absence réelle constatée aux deux emplacements fournis. Si
Francis sait que ce dossier existe ailleurs (autre compte, autre root SharePoint, nom de projet non
numérique), il faudra un troisième chemin ; aucun takeoff n'a été commencé pour S-1253 et aucune réponse
d'estimateur n'a été consultée.

## Portée de cette vérification

Uniquement un audit d'accès : lister des noms/tailles/types, pas de corpus téléchargé, pas de nouveau
serveur ni connecteur activé. Les identifiants extraits des pages (jetons de session, clé API interne au
client web Drive vue dans le HTML public) n'ont pas été conservés ni réutilisés au-delà de cette
vérification, et ne sont pas reproduits dans ce document.

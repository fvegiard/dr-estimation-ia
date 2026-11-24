# Conteneurs locaux — P0 à P2

- **P0** : l’instantané d’état avant modification est sous `.omc/container-preflight/` (ignoré par Git et exclu des builds). Il contient les identifiants d’images, les montages, les ports, le HEAD du dépôt canonique et les empreintes des fichiers d’origine. Il ne contient ni valeurs d’environnement ni données de volume. Ce n’est pas une sauvegarde de production. Le registre personnel externe n’est pas utilisé.
- **P1** : `dev` et `work` partagent l’image construite avec `Dockerfile.dev` et gardent leurs montages distincts. Le `.git` de `work` reste en lecture seule. Vérifier que son répertoire hôte existe avant toute utilisation. `DR_ESTIMATION_GIT_DIR` permet de choisir un autre chemin absolu si l’arborescence est différente de celle du poste actuel. Les noms de conteneurs correspondent à l’existant : ne pas lancer Compose en parallèle des conteneurs qui portent déjà ces noms.
- **Serveur** : profil `server` explicite, port 8765 publié sur `127.0.0.1` uniquement, volume Compose `estim` dédié à `/data`. Le Dockerfile existant exige une clé pour l’écoute hors boucle locale *dans* le conteneur. La configuration transmet uniquement une clé déjà fournie dans l’environnement ; elle n’en définit aucune. Le contrôle HTTP sans clé attend `401` et le défi `Bearer`. Cela vérifie la joignabilité et le refus, pas une session MCP authentifiée.

## Vérifier sans déployer

```sh
podman compose -f /home/fvdev-ubuntu26/work/dr-estimation-ia-container/infra/containers/compose.yml --profile server config --quiet
sh /home/fvdev-ubuntu26/work/dr-estimation-ia-container/infra/containers/verify.sh dev
sh /home/fvdev-ubuntu26/work/dr-estimation-ia-container/infra/containers/verify.sh work
```

La première commande nécessite un fournisseur Compose. Le script ne démarre ni ne recrée aucun conteneur. Les modes `dev` et `work` vérifient la CLI, les dépendances, le transport stdio et Git. Le mode `server` échoue si l’endpoint local ne répond pas comme attendu. `all` exécute les trois contrôles et échoue si l’un d’eux échoue.

## Rotation du bearer du service sur le poste

`rotation_bearer.py` migre l'ancien conteneur `expert-estimateur-svc` d'une variable d'environnement
en clair dans sa configuration vers un secret Podman injecté au démarrage. Sans `--appliquer`, il
n'effectue que l'essai isolé. Il exige l'ancien déploiement (nom, port et volume `estim` attendus)
et le pré-vol `expert-estimateur-mcp` enregistré dans Legion. L'exécution avec `--appliquer`
préserve le digest d'image et le volume, vérifie le nouveau bearer (initialisation MCP : 200),
ainsi que les refus sans bearer et avec l'ancien (401). Ne pas restaurer l'ancien secret après
une rotation réussie ; un retour d'image réutilise le **nouveau** secret.

Pour remettre en service un client distant, configurer `Authorization: Bearer` via son coffre
ou le canal sécurisé de l'équipe, puis vérifier `initialize`. Ne pas coller la valeur dans un
ticket, un message, un paramètre de commande ou un journal. Si le client impose une clé en URL,
ne l'activer qu'après avoir vérifié que **chaque** proxy et serveur désactive ou masque la query
string dans ses logs. La rotation seule ne reconfigure pas les clients ni les anciens liens signés.
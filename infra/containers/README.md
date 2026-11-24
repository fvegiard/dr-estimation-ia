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
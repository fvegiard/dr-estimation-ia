# Reprise de la VM Windows Plan Expert

L’ancien hôte `mxlinux` est retiré. Aucun hôte de remplacement ni démarrage de la sauvegarde n’a été validé. Les tests Python et le jeu de référence restent exécutables sans la VM (voir le [README](../README.md)). Ils ne remplacent pas la validation native dans Plan Expert.

## Gestion depuis l’hôte

Le Yoga Pro Linux est le candidat au remplacement : QEMU est installé et `/dev/kvm` est accessible. Garder le dépôt, les tests, les sauvegardes et la gestion du cycle de vie de la VM sur l’hôte ; exécuter Plan Expert et les opérations natives `.qpl` dans Windows. Ne pas réutiliser le disque d’une autre VM de développement. La configuration de démarrage dépend du format et du mode de démarrage du disque sauvegardé.

## Restauration

1. Dans le Google Drive autorisé, rechercher `FV-LEGION-BACKUP/mxlinux-planexpert`. Le [runbook historique](mxlinux/README.md#sauvegarde) indique cet emplacement pour la copie de `storage/` et le manifeste `SHA256SUMS` ; leur présence n’est pas confirmée.
2. Télécharger la sauvegarde dans un espace privé hors Git. Vérifier sa taille et son intégrité ; si le manifeste est présent, exécuter `sha256sum -c SHA256SUMS` depuis le dossier de sauvegarde et arrêter la restauration en cas d’écart. Conserver l’original intact et travailler sur une copie.
3. Identifier le format du disque et choisir un hôte disposant de la virtualisation et de l’espace libre nécessaires. Si la configuration Podman historique sert de point de départ, adapter les volumes et la liaison réseau au nouvel hôte. Ne pas réutiliser les anciennes adresses ni exposer les ports de la VM à Internet.
4. Démarrer la copie dans un environnement isolé. Vérifier Windows, puis l’ouverture et l’activation de Plan Expert. Tester l’import d’un `.qpl` de référence autorisé et l’export natif attendu. Si l’automatisation est requise, vérifier aussi Windows-MCP sur le nouvel hôte.
5. Consigner le résultat des contrôles et les instructions du nouvel hôte sans ajouter au dépôt de disque, d’identifiants, de clés de licence ni de fichiers de sauvegarde.
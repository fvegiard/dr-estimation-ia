# Plan Expert sur mxlinux — Windows Server 2025 dans Podman

Recette reproductible qui fait tourner **Plan Expert** (application Windows .NET de Groupe DR
Électrique) sur le **Mac mini 2012 « mxlinux »**, dans une VM Windows Server 2025 pilotée par
Podman (image `dockurr/windows`). Elle remplace la VM Hyper-V hébergée sur FV_LEGION.

- Hôte : MX Linux 25.2 « Infinity » (Debian 13 trixie), SysVinit, Podman 5.4.2, podman-compose 1.3.0
- Machine : Macmini6,1 — i5-3210M (2 c / 4 t, VT-x + EPT), 15,9 Go RAM, 458 Go disque
- Réseau : Tailscale `100.96.185.59` (LAN `10.0.0.30`)
- VM : Windows Server 2025 Évaluation (180 jours, 2 sessions RDP), 2 vCPU / 4 Go / 40 Go, fr-CA

## Accès

| Service | Adresse | Notes |
|---|---|---|
| Visionneuse web (installation + écran) | `http://100.96.185.59:8006` | noVNC intégré à l'image |
| Bureau à distance (RDP) | `100.96.185.59:3389` | utilisateur `francis` |
| SSH dans la VM Windows | `ssh -p 2222 francis@100.96.185.59` | OpenSSH Server + clés des agents |

Les trois ports sont liés **uniquement** à l'adresse Tailscale : rien n'est exposé au LAN ni à Internet.

## Arborescence

```
/srv/planexpert/
├── compose.yml            # définition du conteneur
├── .env                   # BIND_IP, WIN_USER, WIN_PASSWORD  (jamais commité)
├── .env.example
├── planexpert.initd       # copié dans /etc/init.d/planexpert (démarrage automatique)
├── oem/                   # exécuté à la fin de l'installation de Windows
│   ├── install.bat        # copie Plan Expert vers Program Files (x86)
│   ├── post-install.ps1   # OpenSSH, clés, fuseau, clavier, veille, raccourcis
│   ├── authorized_keys    # clés publiques des agents (fv-legion + mxlinux)
│   └── PlanExpert/        # binaire Plan Expert — hors Git (licence)
├── shared/                # visible dans Windows comme lecteur réseau — hors Git
│   ├── S-1857-Saint-Michel/
│   └── S-1787-Bioscript/
└── storage/               # disque virtuel Windows — hors Git
```

## Installation depuis zéro

```bash
sudo apt-get install -y podman podman-compose aardvark-dns uidmap slirp4netns passt catatonit
sudo mkdir -p /srv/planexpert && sudo chown $USER /srv/planexpert
git clone https://github.com/fvegiard/planexpert-mxlinux.git /srv/planexpert
cd /srv/planexpert && cp .env.example .env && $EDITOR .env
# déposer le dossier Plan Expert dans oem/PlanExpert/ et les projets dans shared/
sudo podman-compose up -d
sudo cp planexpert.initd /etc/init.d/planexpert && sudo chmod 755 /etc/init.d/planexpert
sudo update-rc.d planexpert defaults
```

Suivre l'installation de Windows sur `http://100.96.185.59:8006` (30 à 60 min sur ce CPU de 2012).

## Pare-feu (UFW)

UFW est actif sur mxlinux et bloque par défaut le trafic **routé** : sans règle, le conteneur n'a
aucun accès réseau (« Could not resolve host »). Règles ajoutées :

```bash
sudo ufw route allow in on podman1 out on wlan0
sudo ufw route allow in on wlan0  out on podman1
sudo ufw route allow in on podman1 out on tailscale0
sudo ufw allow in on podman1
```

## Exploitation

```bash
sudo service planexpert start|stop|restart|status
sudo podman logs -f planexpert
```

Journal de l'installation dans la VM : `C:\OEM\install.log`, marqueur `C:\OEM\INSTALL-OK.txt`.

## Sauvegarde

Conteneur arrêté, copier `storage/` (disque Windows) vers
`G:\My Drive\FV-LEGION-BACKUP\mxlinux-planexpert\` avec un fichier `SHA256SUMS`.

## Limites connues

- **Activation Plan Expert** : TurboActivate lie la licence à la machine ; cette VM consomme une
  deuxième activation.
- **Essai 180 jours** : ensuite, conversion en Windows Server Standard avec une clé, ou
  reconstruction sur `VERSION "10l"` / `"11"` avec une clé Pro (≈ 30 min).
- **CPU de 2012** : l'installation et le premier démarrage sont lents ; l'usage courant reste fluide.
- **Disponibilité** : le Mac mini doit rester allumé et en ligne sur le tailnet.

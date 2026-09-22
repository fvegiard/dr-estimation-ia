# Vérification — 10 septembre 2026

Toutes les valeurs ci-dessous ont été relevées sur les machines, pas estimées.

## Hôte mxlinux

| Élément | Valeur relevée |
|---|---|
| Machine | Macmini6,1 — Intel Core i5-3210M (2 c / 4 t), VT-x + EPT |
| Système | MX Linux 25.2 « Infinity » — Debian 13.6, SysVinit |
| Mémoire / disque | 15 906 Mo — `/dev/sda2` 458 Go |
| KVM | `kvm-ok` → « INFO: /dev/kvm exists / KVM acceleration can be used » |
| Podman | 5.4.2 · podman-compose 1.3.0 · crun 1.21 · netavark 1.14.0 · aardvark-dns 1.14.0 · passt |
| Réseau | Tailscale `100.96.185.59` — conteneur `10.89.0.x`, VM `172.30.0.2` |

## Conteneur et VM

| Élément | Valeur relevée |
|---|---|
| Image | `docker.io/dockurr/windows:latest` — « Starting Windows for Podman v6.05 », QEMU 11.1.0 |
| ISO | Windows Server 2025 (Evaluation) **en français**, serveurs Microsoft, 8 178 149 376 octets |
| Windows | Windows Server 2025 Standard Evaluation — build 26100.ge_release.240331-1435 — 180 jours |
| Nom / utilisateur | `WIN-FQ1G9D51B8D` — `francis`, session console 1, ouverture de session automatique |
| Ressources | 2 vCPU, 4 Go, disque 40 Go (`data.img`, 14 Go réellement occupés) |
| Langue / clavier | Interface française, indicateur clavier **FRA** (fr-CA + en-US) |

## Accès (testés depuis FV_LEGION via Tailscale)

| Service | Test | Résultat |
|---|---|---|
| Visionneuse web `:8006` | `curl -o /dev/null -w %{http_code}` | **200** |
| RDP `:3389` | négociation X.224 + RDP Negotiation Request | **RDP_OK, protocole 2 = CredSSP (NLA)** |
| SSH `:2222` | `ssh -p 2222 francis@100.96.185.59` par clé ed25519 | session ouverte, PowerShell 5.1.26100.7462 |

## Plan Expert

| Élément | Valeur relevée |
|---|---|
| Emplacement | `C:\Program Files (x86)\Plan Expert` — 152 fichiers copiés par `install.bat` |
| Version | `PlanExpert.exe` **3.0.17.0** (identique à la VM Hyper-V) |
| Préférences | Groupe DR Electrique / Francis Vegiard / système **Métrique** |
| **Activation** | **Réussie** — « Activation effectuée avec succès ! Votre copie de Plan Expert est maintenant activée et prête à l'utilisation. » Clé de produit fournie par Acceo (Martin Gauthier), conservée hors dépôt. |

### Bogue rencontré et corrigé : noms de fichiers accentués

Le partage Linux → Windows livre les noms de fichiers en **octets UTF-8** : `Français.xml`
arrivait sous la forme `FranÃ§ais.xml` (caractères 195 + 167 au lieu de 231). TurboActivate ne
trouvait donc plus son fichier de langue et affichait *« Activation Error — The language file
failed to load »*, ce qui rendait toute activation impossible. Six fichiers étaient touchés :
`Français.xml`, `Español.xml`, `Béton.xml`, `Générique.xml`, `Isolation.LaineSoufflée.xml`,
`Revêtement.Canexel.xml`. La correction (reconversion des octets) est intégrée à
`oem/post-install.ps1`, étape 6b — une reconstruction n'aura plus le problème.

## Projets — SHA-256 identiques de bout en bout

```
c898425a608b37dace7fb9f4b4c766678acaf2df981bcc19daba5e28897e9118  Saint-Michel-Codex-Releve-v5-20260909.qpl
765f0e08bb82829c1c113b7ed5f5d606f43a73af2ddc332c6a988e0a6595a080  Saint-Michel-Codex-Releve-v6-20260909.qpl
283381049ee15471ea9d80ce8feb45384f0223a11d1d460e1c69287dd1c48f71  Saint-Michel-Codex-Releve-v2-20260908.qpl
9289eb6b2d9b3434413c8b0e8f8ee53b07cafad831c52f60891de37cfead0826  Saint-Michel-Codex-Releve-20260908.qpl
e014a48332e7dae7c897bf7c8470a5251b552262f1a1464852c1a6f3d7d1dfb7  Saint-Michel-Codex-Releve-agrege-20260908.qpl
a82dcee5bb37ac3180457c8ed4a54508c058a83f14469c848811cd62637b1867  maison st-michel test (8-Septembre-2026).qpl
d33838292450d2d39caef67d32b4d04ed8e827d126ec25d85a08cfdc3619a6f5  S-1787-Bioscript-Releve-v2-20260909.qpl
```

Le hachage de la v6 correspond exactement à celui inscrit au dossier S-1857 (`765f0e08…`).

## Ouverture des projets et ré-export des rapports

| Projet | Ouverture | Rapport ré-exporté | Comparaison au rapport natif (VM Hyper-V) |
|---|---|---|---|
| S-1857 v5 | plan E406_Rev0 affiché, légende, 21 plans, compteurs listés | `…-Rapport-de-métré-(par-plans).xls`, **74 752 octets**, 35 pages | **7 octets de différence sur 74 752** |
| S-1787 v2 | plan E-000 affiché, 15 plans | `…-Rapport-de-métré-(par-plans).xls`, **28 672 octets** | **7 octets de différence sur 28 672** |

Les 7 octets sont, dans les deux cas, le seul enregistrement `WRITEACCESS` du format BIFF, qui
contient le nom de l'utilisateur Windows : `test vm` (ancienne VM Hyper-V) → `francis` (nouvelle VM).
**Aucune donnée de métré ne diffère.**

## Démarrage automatique

`sudo service planexpert stop` puis `start` : conteneur recréé, **SSH de la VM répond après 20 s**,
`LastBootUpTime` = 2026-09-10 02:22:27 (démarrage réel de Windows, pas une reprise).
Lien `/etc/rc3.d/S03planexpert → ../init.d/planexpert` en place.

## Correctifs appliqués à l'hôte (à connaître)

1. **UFW bloquait tout le trafic routé des conteneurs** (`Default: deny (routed)`) : le conteneur
   n'avait aucun accès réseau (« Could not resolve host: www.microsoft.com »). Règles ajoutées :
   `ufw route allow in on podman1 out on wlan0`, l'inverse, `… out on tailscale0`, `ufw allow in on podman1`.
2. **aardvark-dns** manquait (DNS des conteneurs) : installé.
3. **dpkg était déjà cassé avant notre intervention** : les modules DKMS Wi-Fi `8812au/5.13.6` et
   `rtl8821cu/5.12.0` ne compilent pas sur le noyau `6.12.101+deb13-amd64`, ce qui laisse
   `linux-image-6.12.101+deb13-amd64`, `linux-headers-*` et `linux-image-amd64` non configurés.
   Sans effet sur Plan Expert, mais à corriger un jour (retirer ces deux modules DKMS ou les mettre à jour).

## Points d'attention

- La fenêtre « Préférences personnelles » réapparaît à chaque lancement tant que Plan Expert n'a pas
  été fermé normalement une fois (nous l'avons arrêté par `Stop-Process` pendant la mise au point).
- L'export Excel dépose le fichier dans `C:\Users\francis\Documents\Plan Expert\Mes rapports\` puis
  demande avec quelle application l'ouvrir : aucun tableur n'est installé dans la VM. Le fichier est
  bien écrit ; il suffit de fermer la boîte de dialogue.
- L'évaluation Windows expire dans 180 jours : conversion en Standard avec une clé, ou reconstruction
  sur `VERSION "10l"` / `"11"` avec une clé Pro (≈ 30 min).

<#
.SYNOPSIS
    Automatisation serie de Plan Expert dans la VM (conteneur "planexpert" sur l'hote mx) :
    ouverture d'un projet .qpl existant, generation + export du rapport de metre
    (Excel et PDF) et des plans annotes (PDF), fermeture propre de l'application,
    puis depot des livrables dans \\host.lan\Data\sorties\<nom-du-projet>\ (partage
    expose par le conteneur, physiquement /srv/planexpert/shared/sorties/... sur mx).

    Ne touche JAMAIS au fichier .qpl (lecture seule pour Plan Expert).
    S'execute entierement par SSH (WSL -> mx -> VM), sans clic humain.

.PARAMETER QplPath
    Chemin du fichier .qpl DANS LA VM, ex:
    C:\Projets\S-1787-Bioscript\S-1787-Bioscript-Releve-v2-20260909.qpl

.PARAMETER LocalCopyDir
    Optionnel. Si fourni, une copie locale (sur fv-legion) des livrables est aussi
    rapatriee ici via scp, pour verification/hash cote hote.

.EXAMPLE
    C:\Users\fvegi\.codex\mx\pe-batch.ps1 `
        -QplPath 'C:\Projets\S-1787-Bioscript\S-1787-Bioscript-Releve-v2-20260909.qpl' `
        -LocalCopyDir 'C:\Users\fvegi\.codex\mx\out'

.NOTES
    Chaine d'execution (aucune etape ne demande de clic humain) :
      fv-legion (ce script, PowerShell)
        -> wsl.exe -e bash -lc "ssh -p 2222 francis@<vm> ..."   (commandes PowerShell dans la VM)
        -> wsl.exe -e bash -lc "ssh mx '~/.venv-vnc/bin/vncdo -s <ip-conteneur>::5900 ...'"
           (pilotage clavier/souris + captures d'ecran de la VM, sans navigateur)

    Prerequis deja en place sur cette VM (voir tache "PE-Launch") :
      - Preferences personnelles deja remplies (Entreprise, Representant, systeme)
        et enregistrees proprement (Fichier > Quitter) au moins une fois : fichier
        C:\Users\francis\Documents\Plan Expert\Mes donnees\Settings.bak
        (cles CompanyName / CompanyRepresentative / DefaultSystemType).
      - Association .xls -> Bloc-notes deja fixee pour l'utilisateur francis
        (HKCU\...\Explorer\FileExts\.xls\UserChoice, ProgId=Applications\notepad.exe) :
        l'export Excel ne pose plus aucune question. Ce script verifie cette
        association et avertit si elle a disparu (nouveau profil, VM restauree, etc.)
        au lieu de deviner une valeur.

    Un seul executeur a la fois dans Plan Expert (VM) : ne pas lancer ce script en
    parallele d'une session interactive sur la meme VM.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$QplPath,

    [string]$VmHost = '100.96.185.59',
    [int]$VmSshPort = 2222,
    [string]$VmUser = 'francis',
    [string]$MxAlias = 'mx',
    [string]$TaskName = 'PE-Launch',
    [string]$PlanExpertExe = 'C:\Program Files (x86)\Plan Expert\PlanExpert.exe',
    [string]$OutShare = '\\host.lan\Data\sorties',
    [string]$LocalCopyDir,
    [int]$TimeoutSeconds = 180
)

$ErrorActionPreference = 'Stop'
$ProjectName = [System.IO.Path]::GetFileNameWithoutExtension($QplPath)

function Write-Step {
    param([string]$Message)
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] $Message"
}

# ---------------------------------------------------------------------------
# Bas niveau : tout passe par WSL (seul chemin reseau valide vers mx / la VM
# depuis fv-legion, cf. HANDOFF). On utilise l'operateur d'appel avec un seul
# argument de commande pour eviter toute reinterpretation de quotes.
# ---------------------------------------------------------------------------
function Invoke-Wsl {
    param([Parameter(Mandatory)][string]$BashCommand)
    $out = & wsl.exe -e bash -lc $BashCommand 2>&1
    return ($out -join "`n")
}

# Execute une commande PowerShell DANS LA VM via SSH, encodee en base64
# (UTF-16LE) pour ne jamais avoir a echapper des guillemets a travers
# PowerShell -> bash -> ssh -> PowerShell distant.
function Invoke-VM {
    param([Parameter(Mandatory)][string]$Command)
    # $ProgressPreference='SilentlyContinue' evite que PowerShell -EncodedCommand
    # (mode non interactif, sans vraie console) n'injecte un bloc "#< CLIXML"
    # (flux Progress serialise) dans la sortie qu'on parse cote fv-legion.
    $Command = "`$ProgressPreference='SilentlyContinue'; " + $Command
    $bytes = [System.Text.Encoding]::Unicode.GetBytes($Command)
    $b64 = [Convert]::ToBase64String($bytes)
    $sshCmd = "ssh -o BatchMode=yes -o LogLevel=ERROR -p $VmSshPort $VmUser@$VmHost `"powershell -NoProfile -NonInteractive -EncodedCommand $b64`""
    return Invoke-Wsl -BashCommand $sshCmd
}

# Recupere l'IP actuelle du conteneur podman "planexpert" sur mx (peut changer
# apres un redemarrage du conteneur : on ne la fige jamais en dur).
function Get-ContainerIp {
    $cmd = "ssh -o LogLevel=ERROR $MxAlias `"sudo -n podman inspect planexpert --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'`""
    $ip = (Invoke-Wsl -BashCommand $cmd).Trim()
    if ([string]::IsNullOrWhiteSpace($ip)) {
        throw "Impossible d'obtenir l'IP du conteneur planexpert sur $MxAlias."
    }
    return $ip
}

# Pilote l'ecran de la VM via vncdo (souris/clavier/captures), sans navigateur.
function Invoke-Vnc {
    param(
        [Parameter(Mandatory)][string]$VncdoArgs,
        [Parameter(Mandatory)][string]$ContainerIp
    )
    $cmd = "ssh -o LogLevel=ERROR $MxAlias '~/.venv-vnc/bin/vncdo -s ${ContainerIp}::5900 $VncdoArgs'"
    return Invoke-Wsl -BashCommand $cmd
}

function Move-Click {
    param([int]$X, [int]$Y, [string]$ContainerIp, [double]$PauseAfter = 1.0)
    Invoke-Vnc -ContainerIp $ContainerIp -VncdoArgs "move $X $Y click 1 pause $PauseAfter" | Out-Null
}

function Send-Key {
    param([string]$Key, [string]$ContainerIp, [double]$PauseAfter = 1.0)
    Invoke-Vnc -ContainerIp $ContainerIp -VncdoArgs "key $Key pause $PauseAfter" | Out-Null
}

# Attend qu'un fichier existe et ait ete modifie apres $Since, dans la VM.
function Wait-VmFile {
    param(
        [Parameter(Mandatory)][string]$Path,
        [Parameter(Mandatory)][datetime]$Since,
        [int]$TimeoutSec = 60
    )
    $sinceStr = $Since.ToString('o')
    $deadline = (Get-Date).AddSeconds($TimeoutSec)
    while ((Get-Date) -lt $deadline) {
        $check = "if (Test-Path '$Path') { `$f = Get-Item '$Path'; if (`$f.LastWriteTime -gt [datetime]'$sinceStr') { Write-Output ('OK|' + `$f.Length) } }"
        $res = (Invoke-VM -Command $check).Trim()
        if ($res -match '^OK\|(\d+)$') {
            return [int64]$Matches[1]
        }
        Start-Sleep -Seconds 2
    }
    throw "Timeout en attendant le fichier '$Path' dans la VM."
}

# Ferme proprement Plan Expert (Fichier > Quitter), avec plusieurs tentatives :
# le clic sur l'onglet "Fichier" (menu applicatif, pas un vrai onglet de ruban)
# n'ouvre pas toujours le panneau au premier clic (latence VNC/reseau) ; on
# reessaie donc la sequence complete avant d'abandonner.
function Invoke-CloseCleanly {
    param([string]$ContainerIp, [int]$MaxAttempts = 3)
    for ($attempt = 1; $attempt -le $MaxAttempts; $attempt++) {
        Move-Click -X 35 -Y 43 -ContainerIp $ContainerIp -PauseAfter 3     # onglet Fichier (backstage)
        Move-Click -X 65 -Y 381 -ContainerIp $ContainerIp -PauseAfter 3   # Quitter
        $deadline = (Get-Date).AddSeconds(20)
        while ((Get-Date) -lt $deadline) {
            $p = (Invoke-VM -Command "(Get-Process PlanExpert -ErrorAction SilentlyContinue).Id -join ','").Trim()
            if (-not $p) { return $true }
            Start-Sleep -Seconds 2
        }
    }
    return $false
}

# ---------------------------------------------------------------------------
# Etape 0 : verifications de depart (jamais de valeur inventee : on lit l'etat
# reel de la VM avant d'agir).
# ---------------------------------------------------------------------------
Write-Step "Projet : $ProjectName ($QplPath)"

$qplCheck = (Invoke-VM -Command "if (Test-Path '$QplPath') { Write-Output 'EXISTS' } else { Write-Output 'MISSING' }").Trim()
if ($qplCheck -ne 'EXISTS') {
    throw "Le fichier .qpl est introuvable dans la VM : $QplPath"
}

$assocCheck = (Invoke-VM -Command "(Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.xls\UserChoice' -ErrorAction SilentlyContinue).ProgId").Trim()
if ($assocCheck -ne 'Applications\notepad.exe') {
    Write-Warning "Association .xls non trouvee ou differente (ProgId='$assocCheck'). L'export Excel risque d'afficher une boite de dialogue. Refaire une fois : Rapports > Exporter vers Excel > choisir Bloc-notes > Toujours."
}

$runningBefore = (Invoke-VM -Command "(Get-Process PlanExpert -ErrorAction SilentlyContinue).Id -join ','").Trim()
if ($runningBefore) {
    throw "Plan Expert est deja en cours d'execution dans la VM (PID $runningBefore). Un seul executeur a la fois : arreter la session en cours avant de relancer ce script."
}

$containerIp = Get-ContainerIp
Write-Step "Conteneur planexpert : $containerIp"

# ---------------------------------------------------------------------------
# Etape 1 : ouvrir le projet (lance PlanExpert.exe avec le .qpl en argument,
# via la tache planifiee PE-Launch qui tourne dans la session interactive).
# ---------------------------------------------------------------------------
Write-Step "Ouverture du projet dans Plan Expert..."
$launchCmd = @"
`$a = New-ScheduledTaskAction -Execute '$PlanExpertExe' -Argument '"$QplPath"' -WorkingDirectory 'C:\Program Files (x86)\Plan Expert'
Set-ScheduledTask -TaskName '$TaskName' -Action `$a | Out-Null
Start-ScheduledTask -TaskName '$TaskName'
"@
Invoke-VM -Command $launchCmd | Out-Null

# Attente du chargement (fenetre + processus stable).
$deadline = (Get-Date).AddSeconds(60)
$loaded = $false
while ((Get-Date) -lt $deadline) {
    Start-Sleep -Seconds 3
    $p = (Invoke-VM -Command "(Get-Process PlanExpert -ErrorAction SilentlyContinue).Id -join ','").Trim()
    if ($p) { $loaded = $true; break }
}
if (-not $loaded) { throw "Plan Expert n'a pas demarre dans la VM (timeout)." }

# Le processus demarre bien avant que la fenetre/le projet ait fini de se
# charger (peut prendre plusieurs dizaines de secondes selon la taille du
# projet). On laisse du temps, puis on clique a quelques reprises sur les
# coordonnees du bouton OK de l'avertissement "Echelle non configuree." (un
# clic dans le vide est sans effet si la boite n'est pas/plus affichee) : un
# clic souris est plus fiable qu'un "Entree" clavier, cette boite n'ayant pas
# toujours le focus clavier attendu.
Start-Sleep -Seconds 10
for ($i = 0; $i -lt 3; $i++) {
    Move-Click -X 797 -Y 484 -ContainerIp $containerIp -PauseAfter 3
}

# ---------------------------------------------------------------------------
# Etape 2 : rapport de metre -> Export Excel + PDF (onglet "Rapports").
#   Coordonnees mesurees fenetre Plan Expert maximisee, resolution VM 1280x800.
# ---------------------------------------------------------------------------
Write-Step "Generation et export du rapport de metre (Excel + PDF)..."
Move-Click -X 212 -Y 43 -ContainerIp $containerIp -PauseAfter 3   # onglet Rapports (laisse le rapport se peupler)

$repDir = "C:\Users\$VmUser\Documents\Plan Expert\Mes rapports"
$xlsGlob = "$repDir\$ProjectName-Rapport-de-m*tr*-(par-plans).xls"
$pdfRepGlob = "$repDir\$ProjectName-Rapport-de-m*tr*-(par-plans).pdf"
$t0 = Get-Date

Move-Click -X 257 -Y 95 -ContainerIp $containerIp -PauseAfter 2   # Exporter vers Excel
$xlsSize = Wait-VmFile -Path $xlsGlob -Since $t0 -TimeoutSec 60
Write-Step "  -> rapport Excel ecrit ($xlsSize octets)"
# Le fichier .xls s'ouvre automatiquement dans Bloc-notes (association fixee pour
# supprimer la boite "Choisir une application") : on ferme cette fenetre avant de
# poursuivre, sinon les clics suivants sur le ruban de Plan Expert atterrissent
# sur Bloc-notes au lieu du bouton attendu.
Move-Click -X 981 -Y 67 -ContainerIp $containerIp -PauseAfter 2   # fermer Bloc-notes (X)

Move-Click -X 438 -Y 95 -ContainerIp $containerIp -PauseAfter 2   # Exporter vers PDF (rapport)
$pdfRepSize = Wait-VmFile -Path $pdfRepGlob -Since $t0 -TimeoutSec 60
Write-Step "  -> rapport PDF ecrit ($pdfRepSize octets)"
# Le rapport PDF s'ouvre automatiquement dans une fenetre Edge (visionneuse PDF),
# qui reste au premier plan et intercepte les clics suivants destines au ruban
# de Plan Expert : "Echap" ne ferme pas une fenetre de navigateur, il faut
# cliquer sur le bouton de fermeture (X) de la fenetre Edge.
Move-Click -X 1029 -Y 30 -ContainerIp $containerIp -PauseAfter 2   # fermer Edge (X)

# ---------------------------------------------------------------------------
# Etape 3 : plans annotes -> Export PDF (onglet "Plans"), tous les plans dans
# un seul fichier.
# ---------------------------------------------------------------------------
Write-Step "Export des plans annotes (PDF)..."
Move-Click -X 151 -Y 43 -ContainerIp $containerIp -PauseAfter 4   # onglet Plans (laisse charger les miniatures)
Move-Click -X 539 -Y 90 -ContainerIp $containerIp -PauseAfter 2   # Exporter vers PDF (plans)
Move-Click -X 613 -Y 714 -ContainerIp $containerIp -PauseAfter 1  # Selectionner tout
$t1 = Get-Date
Move-Click -X 867 -Y 714 -ContainerIp $containerIp -PauseAfter 2  # Confirmer l'exportation

$plansPdfGlob = "C:\Users\$VmUser\Documents\Plan Expert\Mes plans PDF\Fichiers export*s\$ProjectName\$ProjectName.pdf"
$plansPdfSize = Wait-VmFile -Path $plansPdfGlob -Since $t1 -TimeoutSec $TimeoutSeconds
Write-Step "  -> plans PDF ecrits ($plansPdfSize octets)"
# Ferme la boite "Fichier cree avec succes." (boite native Plan Expert, pas une
# fenetre de navigateur : "Echap" ne suffit pas de facon fiable, on clique sur
# son bouton de fermeture (X) par coordonnees).
Move-Click -X 845 -Y 251 -ContainerIp $containerIp -PauseAfter 2

# ---------------------------------------------------------------------------
# Etape 4 : fermeture PROPRE de l'application (jamais Stop-Process) :
#   Fichier > Quitter. C'est cette fermeture propre qui ecrit
#   Mes donnees\Settings.bak et evite la reapparition de la fenetre
#   "Preferences personnelles" au prochain lancement.
# ---------------------------------------------------------------------------
Write-Step "Fermeture propre de Plan Expert (Fichier > Quitter)..."
$closed = Invoke-CloseCleanly -ContainerIp $containerIp
if (-not $closed) {
    Write-Warning "Plan Expert ne s'est pas ferme proprement dans le delai imparti (fenetre de sauvegarde inattendue ?)."
}

# ---------------------------------------------------------------------------
# Etape 5 : depot des livrables dans \\host.lan\Data\sorties\<projet>\
#   (cote hote mx : /srv/planexpert/shared/sorties/<projet>/), copie faite
#   DEPUIS LA VM (seule a resoudre host.lan).
# ---------------------------------------------------------------------------
Write-Step "Depot des livrables dans $OutShare\$ProjectName ..."
$copyCmd = @"
`$dest = '$OutShare\$ProjectName'
New-Item -ItemType Directory -Force -Path `$dest | Out-Null
Copy-Item -Path '$xlsGlob' -Destination `$dest -Force
Copy-Item -Path '$pdfRepGlob' -Destination `$dest -Force
Copy-Item -Path '$plansPdfGlob' -Destination `$dest -Force
Get-ChildItem `$dest -File | ForEach-Object {
    `$h = Get-FileHash -Algorithm SHA256 -Path `$_.FullName
    Write-Output (`$_.Name + '|' + `$_.Length + '|' + `$h.Hash)
}
"@
$manifest = Invoke-VM -Command $copyCmd
Write-Step "Livrables deposes :"
$manifest -split "`n" | Where-Object { $_ -match '\|' } | ForEach-Object { Write-Host "    $_" }

# ---------------------------------------------------------------------------
# Etape 6 (optionnelle) : rapatrier une copie locale sur fv-legion pour
# verification/hash cote hote, via le partage mx (mx: /srv/planexpert/shared).
# ---------------------------------------------------------------------------
if ($LocalCopyDir) {
    Write-Step "Copie locale vers $LocalCopyDir\$ProjectName ..."
    $localDest = Join-Path $LocalCopyDir $ProjectName
    New-Item -ItemType Directory -Force -Path $localDest | Out-Null
    # scp via WSL ecrit directement sur le systeme de fichiers Windows via /mnt/c ;
    # on passe par une destination Windows convertie en chemin WSL.
    $wslDest = ($localDest -replace '\\', '/') -replace '^([A-Za-z]):', { "/mnt/$($_.Groups[1].Value.ToLower())" }
    Invoke-Wsl -BashCommand "scp $MxAlias`:/srv/planexpert/shared/sorties/$ProjectName/* '$wslDest/'" | Out-Null
    Get-ChildItem $localDest -File | ForEach-Object {
        $h = Get-FileHash -Algorithm SHA256 -Path $_.FullName
        Write-Host ("    {0}  {1,10} octets  {2}" -f $_.Name, $_.Length, $h.Hash)
    }
}

Write-Step "Termine pour $ProjectName."

# ===================================================================
#  Plan Expert — configuration post-installation (Windows Server 2025)
#  Appele par C:\OEM\install.bat. Journal : C:\OEM\install.log
# ===================================================================
$ErrorActionPreference = 'Continue'
function Log($m) { Write-Output ("[{0}] {1}" -f (Get-Date -Format 'HH:mm:ss'), $m) }

Log "post-install.ps1 debut"

# --- 1) Fuseau horaire et regionalisation --------------------------
try { Set-TimeZone -Id 'Eastern Standard Time'; Log "fuseau: Eastern Standard Time" } catch { Log "fuseau ERREUR $_" }
try {
  $l = New-WinUserLanguageList fr-CA
  $l.Add('en-US')
  Set-WinUserLanguageList $l -Force
  Set-WinSystemLocale -SystemLocale fr-CA
  Set-WinHomeLocation -GeoId 39
  Log "clavier/locale fr-CA + en-US"
} catch { Log "locale ERREUR $_" }

# --- 2) Jamais de veille, ecran toujours actif ----------------------
powercfg /change standby-timeout-ac 0
powercfg /change monitor-timeout-ac 0
powercfg /change disk-timeout-ac 0
powercfg /change hibernate-timeout-ac 0
Log "veille desactivee"

# --- 3) IE Enhanced Security Configuration : OFF --------------------
try {
  Set-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Active Setup\Installed Components\{A509B1A7-37EF-4b3f-8CFC-4F3A74704073}' -Name IsInstalled -Value 0 -ErrorAction SilentlyContinue
  Set-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Active Setup\Installed Components\{A509B1A8-37EF-4b3f-8CFC-4F3A74704073}' -Name IsInstalled -Value 0 -ErrorAction SilentlyContinue
  Log "IE ESC desactive"
} catch { Log "IE ESC ERREUR $_" }

# --- 4) Server Manager ne demarre pas automatiquement ---------------
try {
  New-Item -Path 'HKLM:\SOFTWARE\Microsoft\ServerManager' -Force | Out-Null
  Set-ItemProperty 'HKLM:\SOFTWARE\Microsoft\ServerManager' -Name DoNotOpenServerManagerAtLogon -Value 1
  Log "Server Manager: pas de demarrage auto"
} catch { Log "ServerManager ERREUR $_" }

# --- 5) OpenSSH Server ----------------------------------------------
try {
  $cap = Get-WindowsCapability -Online -Name 'OpenSSH.Server*'
  if ($cap.State -ne 'Installed') { Add-WindowsCapability -Online -Name $cap.Name | Out-Null }
  Set-Service -Name sshd -StartupType Automatic
  Start-Service sshd
  New-ItemProperty -Path 'HKLM:\SOFTWARE\OpenSSH' -Name DefaultShell -Value 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe' -PropertyType String -Force | Out-Null
  if (-not (Get-NetFirewallRule -Name 'sshd-22' -ErrorAction SilentlyContinue)) {
    New-NetFirewallRule -Name 'sshd-22' -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22 | Out-Null
  }
  Log "OpenSSH Server installe et demarre"
} catch { Log "OpenSSH ERREUR $_" }

# --- 6) Cles publiques autorisees (agents) --------------------------
try {
  if (Test-Path 'C:\OEM\authorized_keys') {
    $ak = 'C:\ProgramData\ssh\administrators_authorized_keys'
    Copy-Item 'C:\OEM\authorized_keys' $ak -Force
    icacls $ak /inheritance:r | Out-Null
    # SID plutot que noms : les comptes integres sont traduits en francais
    icacls $ak /grant '*S-1-5-18:(F)' | Out-Null      # SYSTEM
    icacls $ak /grant '*S-1-5-32-544:(F)' | Out-Null  # Administrateurs
    Log "administrators_authorized_keys installe"
  } else { Log "aucun C:\OEM\authorized_keys" }
} catch { Log "authorized_keys ERREUR $_" }

# --- 6b) Noms de fichiers accentues -----------------------------------
# Le partage Linux -> Windows livre les noms en octets UTF-8 : « Francais.xml »
# arrive sous la forme « FranAais.xml ». TurboActivate ne trouve alors plus son
# fichier de langue et l'activation est impossible. On refait la conversion.
try {
  $peDir = 'C:\Program Files (x86)\Plan Expert'
  if (Test-Path $peDir) {
    $n = 0
    foreach ($f in (Get-ChildItem -LiteralPath $peDir -Recurse -File)) {
      $name = $f.Name
      $has = $false
      foreach ($c in $name.ToCharArray()) { if ([int]$c -gt 127) { $has = $true } }
      if (-not $has) { continue }
      $bytes = New-Object byte[] $name.Length
      for ($i = 0; $i -lt $name.Length; $i++) { $bytes[$i] = [byte][int]$name[$i] }
      $newName = [System.Text.Encoding]::UTF8.GetString($bytes)
      if ($newName -eq $name) { continue }
      $dest = Join-Path $f.DirectoryName $newName
      if (Test-Path -LiteralPath $dest) { Remove-Item -LiteralPath $dest -Force }
      Rename-Item -LiteralPath $f.FullName -NewName $newName -Force
      $n++
    }
    Log "noms de fichiers accentues corriges : $n"
  }
} catch { Log "noms accentues ERREUR $_" }

# --- 7) Raccourcis Plan Expert --------------------------------------
try {
  $exe = 'C:\Program Files (x86)\Plan Expert\PlanExpert.exe'
  if (Test-Path $exe) {
    $ws = New-Object -ComObject WScript.Shell
    foreach ($dir in @("$env:PUBLIC\Desktop", "$env:ProgramData\Microsoft\Windows\Start Menu\Programs")) {
      if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
      $lnk = $ws.CreateShortcut((Join-Path $dir 'Plan Expert.lnk'))
      $lnk.TargetPath = $exe
      $lnk.WorkingDirectory = 'C:\Program Files (x86)\Plan Expert'
      $lnk.Description = 'Plan Expert — releve de quantites'
      $lnk.Save()
    }
    Log "raccourcis crees"
  } else { Log "PlanExpert.exe absent : pas de raccourci" }
} catch { Log "raccourcis ERREUR $_" }

# --- 8) Dossier de travail des projets ------------------------------
try {
  New-Item -ItemType Directory -Path 'C:\Projets' -Force | Out-Null
  Log "C:\Projets pret (lecteur reseau partage = \\host.lan\Data)"
} catch { Log "C:\Projets ERREUR $_" }

# --- 9) Marqueur de fin ---------------------------------------------
"$(Get-Date -Format o)" | Out-File 'C:\OEM\INSTALL-OK.txt' -Encoding ascii
Log "post-install.ps1 fin"

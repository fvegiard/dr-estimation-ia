#Requires -Version 7
# Passe 5 - CORRECTION finale: rust-mcp-filesystem + cloud-run-mcp dans le profil, env bind-allowlist dans claude_desktop_config.json, dry-run.
$ErrorActionPreference = 'Continue'
$out = "$env:USERPROFILE\Desktop\_claude_mcp_diag.txt"
$L = [System.Collections.Generic.List[string]]::new()
function Add([string]$s) { $script:L.Add($s) }
function Mask([string]$s) { return ($s -replace '((?:KEY|TOKEN|SECRET|PASSWORD)[A-Za-z0-9_]*"?\s*[:=]\s*"?)[^"\s]+', '$1***') }
function RunArgs([string]$title, [string[]]$argv) {
    Add "=== $title  [docker $($argv -join ' ')]"
    $t = [Diagnostics.Stopwatch]::StartNew()
    $o = & docker @argv 2>&1 | Out-String
    Add ("exit=$LASTEXITCODE  ({0:n1}s)" -f $t.Elapsed.TotalSeconds)
    Add (Mask $o.TrimEnd())
    return $LASTEXITCODE
}
$repo = 'D:/github/dr-estimation-ia'
$adc = "$env:APPDATA\gcloud\application_default_credentials.json"
$adcDir = ($env:APPDATA -replace '\\', '/') + '/gcloud'
Add "=== DATE: $(Get-Date -Format o)"

# 1) Profil: rust-mcp-filesystem
$rc = RunArgs 'Set rust-mcp-filesystem' @('mcp', 'profile', 'config', 'claude', '--set', "rust-mcp-filesystem.allowed_directories=[`"$repo`"]", '--set', 'rust-mcp-filesystem.allow_write=true', '--set', 'rust-mcp-filesystem.enable_roots=false')
Add "rust rc=$rc"

# 2) Profil: cloud-run-mcp (seulement si les credentials ADC gcloud existent)
Add "=== ADC gcloud present: $(Test-Path $adc)  ($adc)"
$allowedRo = ''
if (Test-Path $adc) {
    $rc = RunArgs 'Set cloud-run-mcp.credentials_path' @('mcp', 'profile', 'config', 'claude', '--set', "cloud-run-mcp.credentials_path=$(($adc -replace '\\', '/'))")
    Add "cloudrun rc=$rc"
    $allowedRo = $adcDir
} else { Add 'cloud-run-mcp: credentials_path non defini (ADC absent) -> ce serveur restera inactif; `gcloud auth application-default login` le reglera.' }
RunArgs 'Config profil apres' @('mcp', 'profile', 'config', 'claude', '--get-all') | Out-Null

# 3) claude_desktop_config.json: ajouter les variables d'allowlist de montage
$cfg = "$env:APPDATA\Claude\claude_desktop_config.json"
$bak = "$cfg.bak-$(Get-Date -Format yyyyMMdd_HHmmss)"
Copy-Item $cfg $bak -Force
Add "=== Sauvegarde config: $bak  present=$(Test-Path $bak)  octets=$((Get-Item $bak).Length)"
$raw = Get-Content $cfg -Raw
$j = $raw | ConvertFrom-Json -AsHashtable -Depth 64
$envMap = $j['mcpServers']['MCP_DOCKER']['env']
if ($null -eq $envMap) { $envMap = @{}; $j['mcpServers']['MCP_DOCKER']['env'] = $envMap }
$envMap['MCP_GATEWAY_DOCKER_BIND_ALLOW_WRITABLE_PATHS'] = $repo
if ($allowedRo) { $envMap['MCP_GATEWAY_DOCKER_BIND_ALLOWED_PATHS'] = $allowedRo }
$new = $j | ConvertTo-Json -Depth 64
# validation avant ecriture: reparse + memes cles de premier niveau + MCP_DOCKER intact
$chk = $new | ConvertFrom-Json -AsHashtable -Depth 64
$ok = ($chk.Keys.Count -eq $j.Keys.Count) -and ($chk['mcpServers']['MCP_DOCKER']['command'] -eq 'docker') -and ($chk['mcpServers']['MCP_DOCKER']['args'] -join ' ' -eq 'mcp gateway run --profile claude') -and ($chk['preferences'].Keys.Count -eq $j['preferences'].Keys.Count)
Add "=== Validation JSON avant ecriture: $ok  (cles racine=$($chk.Keys.Count), prefs=$($chk['preferences'].Keys.Count))"
if ($ok) {
    [IO.File]::WriteAllText($cfg, $new, [Text.UTF8Encoding]::new($false))
    $re = Get-Content $cfg -Raw | ConvertFrom-Json -AsHashtable -Depth 64
    Add "=== Relecture apres ecriture: taille=$((Get-Item $cfg).Length)"
    Add ("MCP_DOCKER env: " + (($re['mcpServers']['MCP_DOCKER']['env'].GetEnumerator() | ForEach-Object { "$($_.Key)=$($_.Value)" }) -join ' | '))
} else { Add 'ABANDON ecriture config: validation echouee.' }

# 4) Dry-run avec exactement l'env que Claude Desktop injectera
$env:MCP_GATEWAY_DOCKER_BIND_ALLOW_WRITABLE_PATHS = $repo
if ($allowedRo) { $env:MCP_GATEWAY_DOCKER_BIND_ALLOWED_PATHS = $allowedRo }
$rc = RunArgs 'DRY-RUN gateway profil claude (avec env)' @('mcp', 'gateway', 'run', '--profile', 'claude', '--dry-run')
Add "DRYRUN rc=$rc"

$L | Set-Content -Path $out -Encoding UTF8
Write-Output "DONE lines=$($L.Count) dryrun_rc=$rc -> $out"
exit $rc

# Refresh everything after a Lumen price update in ACCEO (run from the host PC):
#   1. export EEWin tables from the VM   2. rebuild data\dre.sqlite   3. run tests   4. push to Supabase
param([switch]$SkipCloud)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
Push-Location $root
try {
    & "$root\scripts\extract_from_eewin.ps1"
    uv run python scripts/build_db.py
    if ($LASTEXITCODE) { throw 'build_db failed' }
    uv run pytest -q
    if ($LASTEXITCODE) { throw 'tests failed - cloud not updated' }
    if (-not $SkipCloud) {
        uv run python scripts/sync_cloud.py
        if ($LASTEXITCODE) { throw 'cloud sync failed' }
    }
} finally { Pop-Location }

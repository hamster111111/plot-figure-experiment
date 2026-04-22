$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot

python (Join-Path $PSScriptRoot "sync_from_workspace.py")
python (Join-Path $PSScriptRoot "gen_index.py")

Write-Host "Site updated in $(Join-Path $root 'work')"

param(
    [string]$Message = "",
    [switch]$NoPush
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot

& (Join-Path $PSScriptRoot "update_site.ps1")

$pathsToStage = @(
    ".github",
    ".gitignore",
    "README.md",
    "scripts",
    "work"
)

$statusArgs = @("-C", $root, "status", "--short", "--") + $pathsToStage
$status = & git @statusArgs

if (-not $status) {
    Write-Host "No changes to publish."
    exit 0
}

& git -C $root add -- $pathsToStage

if (-not $Message) {
    $Message = "Update site $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
}

& git -C $root commit -m $Message

if ($NoPush) {
    Write-Host "Committed locally. Push skipped."
    exit 0
}

& git -C $root push origin main
Write-Host "Published to origin/main"

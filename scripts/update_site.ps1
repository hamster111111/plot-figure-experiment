$ErrorActionPreference = "Stop"

function Get-PythonCommand {
    if (Get-Command py -ErrorAction SilentlyContinue) {
        return @("py", "-3")
    }
    if (Get-Command python -ErrorAction SilentlyContinue) {
        return @("python")
    }
    throw "Python was not found in PATH."
}

function Invoke-PythonScript {
    param(
        [string]$ScriptPath
    )

    if ($python.Length -gt 1) {
        & $python[0] $python[1..($python.Length - 1)] $ScriptPath
        return
    }

    & $python[0] $ScriptPath
}

$root = Split-Path -Parent $PSScriptRoot
$python = Get-PythonCommand

Invoke-PythonScript -ScriptPath (Join-Path $PSScriptRoot "sync_from_workspace.py")
Invoke-PythonScript -ScriptPath (Join-Path $PSScriptRoot "gen_index.py")

Write-Host "Site updated in $(Join-Path $root 'work')"

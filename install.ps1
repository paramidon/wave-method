<#
Installs the wave skill set into a project:
  <Target>\.claude\skills\wave-*         copies of skills\wave-*
  <Target>\.agents\skills\wave-*         junctions to them, for Codex, Antigravity and Gemini CLI
                                         (skip with -NoAgents; -NoCodex is the old name)

Usage:
  .\install.ps1 -Target D:\work\my-project
  .\install.ps1 -Target D:\work\my-project -Force      # replace existing wave-* skill folders
  .\install.ps1 -Target D:\work\my-project -NoAgents
#>
param(
    [Parameter(Mandatory = $true)][string]$Target,
    [switch]$Force,
    [Alias('NoCodex')][switch]$NoAgents
)

$ErrorActionPreference = 'Stop'
$skills = @('wave-triage', 'wave-plan', 'wave-run', 'wave-status')
$source = Join-Path $PSScriptRoot 'skills'
$targetRoot = (Resolve-Path -LiteralPath $Target).Path
$claudeSkills = Join-Path $targetRoot '.claude\skills'
$agentSkills = Join-Path $targetRoot '.agents\skills'

New-Item -ItemType Directory -Path $claudeSkills -Force | Out-Null
foreach ($name in $skills) {
    $from = Join-Path $source $name
    $to = Join-Path $claudeSkills $name
    if (Test-Path -LiteralPath $to) {
        if (-not $Force) { throw "$to already exists; re-run with -Force to replace it" }
        Remove-Item -LiteralPath $to -Recurse -Force
    }
    Copy-Item -LiteralPath $from -Destination $to -Recurse
    Get-ChildItem -LiteralPath $to -Recurse -Directory -Filter '__pycache__' | Remove-Item -Recurse -Force
    Write-Host "installed $to"
}

if (-not $NoAgents) {
    New-Item -ItemType Directory -Path $agentSkills -Force | Out-Null
    foreach ($name in $skills) {
        $link = Join-Path $agentSkills $name
        $dest = Join-Path $claudeSkills $name
        if (Test-Path -LiteralPath $link) {
            $item = Get-Item -LiteralPath $link -Force
            if ($item.LinkType -eq 'Junction' -and $item.Target -eq $dest) { continue }
            throw "$link exists and is not a junction to $dest"
        }
        New-Item -ItemType Junction -Path $link -Target $dest | Out-Null
        Write-Host "linked  $link"
    }
    Write-Host "Add '.agents/' to the project's .gitignore: git does not keep junctions."
}

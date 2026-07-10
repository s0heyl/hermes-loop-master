param(
    [string]$Target = "$HOME/.hermes/skills/hermes-loop-master",
    [switch]$DryRun,
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Target = $Target.TrimEnd('\', '/')
if ([string]::IsNullOrWhiteSpace($Target) -or $Target -eq $HOME) {
    throw "Refusing unsafe install target: $Target"
}

& python "$Root/scripts/validate_skill.py" "$Root/SKILL.md"
if ($LASTEXITCODE -ne 0) { throw "SKILL.md validation failed" }

function Test-RecognizedInstall([string]$Path) {
    $Skill = Join-Path $Path "SKILL.md"
    if (-not (Test-Path $Path -PathType Container) -or -not (Test-Path $Skill -PathType Leaf)) { return $false }
    foreach ($Directory in @("templates", "scripts", "examples", "references")) {
        if (-not (Test-Path (Join-Path $Path $Directory) -PathType Container)) { return $false }
    }
    $Lines = Get-Content $Skill
    if ($Lines.Count -lt 3 -or $Lines[0] -ne "---") { return $false }
    $Closing = [Array]::IndexOf($Lines, "---", 1)
    if ($Closing -lt 2) { return $false }
    return [bool]($Lines[1..($Closing - 1)] -match '^name:\s*hermes-loop-master\s*$')
}

$Exists = Test-Path $Target
if ($Exists -and -not $Force) {
    if (-not $DryRun) { throw "Destination exists; use -Force: $Target" }
}
if ($Exists -and $Force -and -not (Test-RecognizedInstall $Target)) {
    throw "Refusing -Force: target is not a Hermes Loop Master installation: $Target"
}
if ($DryRun) {
    Write-Host "Dry run: would install Hermes Loop Master to $Target"
    exit 0
}

$Parent = Split-Path -Parent $Target
$Name = Split-Path -Leaf $Target
New-Item -ItemType Directory -Force -Path $Parent | Out-Null
$Staging = Join-Path $Parent "$Name.tmp.$PID"
$Backup = $null
try {
    New-Item -ItemType Directory -Force -Path $Staging | Out-Null
    Copy-Item "$Root/SKILL.md" "$Staging/SKILL.md"
    foreach ($Directory in @("templates", "scripts", "examples", "references")) {
        Copy-Item -Recurse "$Root/$Directory" "$Staging/$Directory"
    }
    & python "$Staging/scripts/validate_skill.py" "$Staging/SKILL.md"
    if ($LASTEXITCODE -ne 0) { throw "Staged skill validation failed" }
    if ($Exists) {
        $Backup = "$Target.backup.$(Get-Date -Format yyyyMMdd_HHmmss)"
        Move-Item $Target $Backup
    }
    Move-Item $Staging $Target
} catch {
    if (Test-Path $Staging) { Remove-Item -Recurse -Force $Staging }
    if ($Backup -and (Test-Path $Backup) -and -not (Test-Path $Target)) {
        Move-Item $Backup $Target
    }
    throw
}

Write-Host "Installed Hermes Loop Master to: $Target"
if ($Backup) { Write-Host "Previous install backed up to: $Backup" }

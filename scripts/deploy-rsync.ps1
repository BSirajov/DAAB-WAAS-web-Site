# Upload DAAB static site via rsync over SSH (WSL or Git Bash rsync required).
# Usage:  .\scripts\deploy-rsync.ps1
$ErrorActionPreference = "Stop"

$Root = Split-Path $PSScriptRoot -Parent
Set-Location $Root

$EnvFile = Join-Path $Root "scripts\deploy.env"
if (-not (Test-Path $EnvFile)) {
    Write-Error "Missing scripts\deploy.env — copy scripts\deploy.env.example and edit."
}

Get-Content $EnvFile | ForEach-Object {
    if ($_ -match '^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$') {
        Set-Variable -Name $Matches[1] -Value $Matches[2].Trim('"') -Scope Script
    }
}

if (-not $DEPLOY_HOST -or -not $DEPLOY_USER -or -not $DEPLOY_PATH) {
    Write-Error "Set DEPLOY_HOST, DEPLOY_USER, and DEPLOY_PATH in scripts\deploy.env"
}

$DeployPort = if ($DEPLOY_PORT) { $DEPLOY_PORT } else { "22" }
$SkipValidate = if ($SKIP_VALIDATE -eq "1") { $true } else { $false }

if (-not $SkipValidate) {
    Write-Host "==> Validating site..."
    python helpers/_validate_site.py
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

$Rsync = $null
foreach ($candidate in @("rsync", "wsl rsync")) {
    $cmd = $candidate.Split(" ")[0]
    if (Get-Command $cmd -ErrorAction SilentlyContinue) {
        $Rsync = $candidate
        break
    }
}
if (-not $Rsync) {
    Write-Error @"
rsync not found. Install one of:
  - Git for Windows (includes rsync in some builds), or
  - WSL: wsl --install, then: sudo apt install rsync openssh-client
Then run:  bash ./scripts/deploy-rsync.sh
"@
}

$DeployIgnore = Join-Path $Root ".deployignore"
$Dest = "${DEPLOY_USER}@${DEPLOY_HOST}:${DEPLOY_PATH}/"

$Args = @(
    "-avz",
    "--human-readable",
    "--progress",
    "--exclude-from=$DeployIgnore",
    "-e", "ssh -p $DeployPort",
    "./",
    $Dest
)

if ($DEPLOY_DELETE -eq "1") {
    Write-Warning "DEPLOY_DELETE=1 — remote files not in local tree will be removed."
    $Args = @("-avz", "--delete") + $Args[1..($Args.Length - 1)]
}

Write-Host "==> Uploading to $Dest"
if ($Rsync -eq "wsl rsync") {
    $WslRoot = wsl wslpath -a $Root
    wsl rsync -avz --human-readable --progress "--exclude-from=$(wsl wslpath -a $DeployIgnore)" `
        -e "ssh -p $DeployPort" "$WslRoot/" "$Dest"
} else {
    & rsync @Args
}

Write-Host "==> Done. Smoke-test: https://daab-waas.com/az/index.html"

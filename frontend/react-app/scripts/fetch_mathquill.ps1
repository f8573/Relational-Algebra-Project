Param(
    [string]$Repo = 'https://github.com/mathquill/mathquill.git',
    [string]$Ref = 'master',
    [string]$Target = 'public/vendor/mathquill'
)

# Fetch and prepare MathQuill locally for development.
# Usage (PowerShell):
#   ./scripts/fetch_mathquill.ps1
#   ./scripts/fetch_mathquill.ps1 -Repo 'https://github.com/mathquill/mathquill.git' -Ref 'release'

$root = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $root

if (-Not (Get-Command git -ErrorAction SilentlyContinue)){
    Write-Error "git is required but not found in PATH. Install Git for Windows and retry."
    exit 1
}

$dest = Join-Path (Get-Location) $Target
if (Test-Path $dest) {
    Write-Host "Target exists at $dest. Updating repository..."
    Push-Location $dest
    git fetch origin
    git checkout $Ref
    git pull --ff-only origin $Ref
    Pop-Location
} else {
    Write-Host "Cloning $Repo -> $dest"
    git clone $Repo $dest
    Push-Location $dest
    git checkout $Ref
    Pop-Location
}

# Build instructions (MathQuill may use Node build tooling). If package.json exists, install and build.
$pkg = Join-Path $dest 'package.json'
if (Test-Path $pkg) {
    Write-Host "Found package.json, running npm install && npm run build"
    Push-Location $dest
    if (-Not (Get-Command npm -ErrorAction SilentlyContinue)){
        Write-Warning "npm not found; skip build. Install Node.js to build MathQuill locally."
    } else {
        npm install
        if (Get-Content package.json | Select-String -Pattern '"build"'){
            npm run build
            Write-Host "Build complete. Copy built assets (e.g., dist/) into $Target and update references in MathEditor.jsx if necessary."
        } else {
            Write-Host "No build script detected; you may need to manually prepare the distribution files."
        }
    }
    Pop-Location
} else {
    Write-Host "No package.json; MathQuill sources cloned. Review repository for build or dist directory."
}

# Attempt to auto-copy built artifacts into the public vendor folder.
Write-Host "Searching for built artifacts to copy into $Target..."
$publicTarget = Join-Path (Get-Location) $Target
New-Item -ItemType Directory -Force -Path $publicTarget | Out-Null

# Common build output dirs to search for
$candidates = @('dist','build','release','lib')
$foundJs = $null
$foundCss = $null

foreach ($d in $candidates) {
    $p = Join-Path $dest $d
    if (Test-Path $p) {
        Write-Host "Inspecting $p for distribution files..."
        $js = Get-ChildItem -Path $p -Recurse -Include '*.min.js','*mathquill*.js' -ErrorAction SilentlyContinue | Select-Object -First 1
        $css = Get-ChildItem -Path $p -Recurse -Include '*.css','*mathquill*.css' -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($js) { $foundJs = $js.FullName }
        if ($css) { $foundCss = $css.FullName }
        if ($foundJs -and $foundCss) { break }
    }
}

if (-not $foundJs -or -not $foundCss) {
    # try root of repo
    $js = Get-ChildItem -Path $dest -Recurse -Include '*.min.js','*mathquill*.js' -ErrorAction SilentlyContinue | Select-Object -First 1
    $css = Get-ChildItem -Path $dest -Recurse -Include '*.css','*mathquill*.css' -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($js) { $foundJs = $js.FullName }
    if ($css) { $foundCss = $css.FullName }
}

if ($foundJs) {
    $targetJs = Join-Path $publicTarget 'mathquill.min.js'
    Copy-Item -Force -Path $foundJs -Destination $targetJs
    Write-Host "Copied JS -> $targetJs"
} else { Write-Host "No JS artifact found automatically. You may need to copy mathquill.min.js manually." }

if ($foundCss) {
    $targetCss = Join-Path $publicTarget 'mathquill.css'
    Copy-Item -Force -Path $foundCss -Destination $targetCss
    Write-Host "Copied CSS -> $targetCss"
} else { Write-Host "No CSS artifact found automatically. You may need to copy mathquill.css manually." }

Write-Host "Done. Verify the files under $publicTarget (mathquill.min.js, mathquill.css) and commit them to your repo to pin vendor assets."
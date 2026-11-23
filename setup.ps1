$ErrorActionPreference = "Stop"

Push-Location $PSScriptRoot

# Find Python 3.12
$PY = $null
foreach ($candidate in @("python3.12", "python3", "python")) {
    $cmd = Get-Command $candidate -ErrorAction SilentlyContinue
    if ($cmd) {
        $ver = & $candidate -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
        if ($ver -eq "3.12") {
            $PY = $candidate
            break
        }
    }
}

if (-not $PY) {
    Write-Host "Python 3.12 not found."
    Write-Host "Install it with:"
    Write-Host "  winget: winget install Python.Python.3.12"
    Write-Host "  scoop: scoop install python@3.12"
    Write-Host "  python.org: https://www.python.org/downloads/release/python-3120/"
    Pop-Location
    exit 1
}

Write-Host "==> Using $PY ($(& $PY --version))"

# Check for iverilog
if (-not (Get-Command iverilog -ErrorAction SilentlyContinue)) {
    Write-Host ""
    Write-Host "WARNING: Icarus Verilog (iverilog) not found."
    Write-Host "Install it before running simulations:"
    Write-Host "  scoop: scoop install iverilog"
    Write-Host "  Download: https://bleyer.org/icarus/"
    Write-Host ""
}

# Create venv and install
Write-Host "==> Creating virtual environment..."
& $PY -m venv .venv
& .\.venv\Scripts\Activate.ps1

Write-Host "==> Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt

Pop-Location

Write-Host ""
Write-Host "Done! Activate the environment with:"
Write-Host "  .\.venv\Scripts\Activate.ps1"

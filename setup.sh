#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Find Python 3.12
PY=""
for candidate in python3.12 python3; do
    if command -v "$candidate" &>/dev/null; then
        ver=$("$candidate" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
        if [ "$ver" = "3.12" ]; then
            PY="$candidate"
            break
        fi
    fi
done

if [ -z "$PY" ]; then
    echo "Python 3.12 not found."
    echo "Install it with your package manager:"
    echo "  Arch/Manjaro: sudo pacman -S python312"
    echo "  Ubuntu/Debian: sudo apt install python3.12 python3.12-venv"
    echo "  macOS: brew install python@3.12"
    echo "  mise: mise install python@3.12"
    exit 1
fi

echo "==> Using $PY ($($PY --version))"

# Check for iverilog
if ! command -v iverilog &>/dev/null; then
    echo ""
    echo "WARNING: Icarus Verilog (iverilog) not found."
    echo "Install it before running simulations:"
    echo "  Arch/Manjaro: sudo pacman -S iverilog"
    echo "  Ubuntu/Debian: sudo apt install iverilog"
    echo "  macOS: brew install icarus-verilog"
    echo ""
fi

# Create venv and install
echo "==> Creating virtual environment..."
$PY -m venv .venv
source .venv/bin/activate

echo "==> Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt

echo ""
echo "Done! Activate the environment with:"
echo "  source .venv/bin/activate"

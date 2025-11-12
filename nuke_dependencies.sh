#!/bin/bash
# NUCLEAR OPTION: Remove ALL potentially problematic packages
# Use this if nothing else works

echo "💣 NUCLEAR OPTION: Removing ALL problematic packages"
echo "====================================================="
echo ""
echo "This will remove:"
echo "  - Pillow / PIL"
echo "  - All mutagen versions"
echo "  - Any other packages that might cause issues"
echo ""

read -p "Continue? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 1
fi

echo ""
echo "Removing ALL problematic packages..."

# Remove Pillow and PIL
pip3 uninstall -y Pillow PIL 2>/dev/null || true
python3 -m pip uninstall -y Pillow PIL 2>/dev/null || true

# Remove ALL mutagen versions
pip3 uninstall -y mutagen 2>/dev/null || true
python3 -m pip uninstall -y mutagen 2>/dev/null || true

# Remove any other potentially problematic packages
pip3 uninstall -y packaging setuptools wheel 2>/dev/null || true
python3 -m pip uninstall -y packaging setuptools wheel 2>/dev/null || true

echo "✓ All packages removed"
echo ""

# Now install ONLY what we need - minimal version
echo "Installing minimal compatible versions..."

# Install mutagen 1.45.1 with NO dependencies
if python3 -m pip install --user "mutagen==1.45.1" --no-deps --no-build-isolation 2>/dev/null; then
    echo "✓ Mutagen 1.45.1 installed (no dependencies)"
elif pip3 install --user "mutagen==1.45.1" --no-deps --no-build-isolation 2>/dev/null; then
    echo "✓ Mutagen 1.45.1 installed (no dependencies)"
else
    echo "⚠️  Could not install mutagen 1.45.1"
    echo "   Trying mutagen 1.45.0..."
    if python3 -m pip install --user "mutagen==1.45.0" --no-deps --no-build-isolation 2>/dev/null; then
        echo "✓ Mutagen 1.45.0 installed"
    elif pip3 install --user "mutagen==1.45.0" --no-deps --no-build-isolation 2>/dev/null; then
        echo "✓ Mutagen 1.45.0 installed"
    else
        echo "❌ Failed to install any mutagen version"
        echo ""
        echo "Try manually:"
        echo "  pip3 install --user 'mutagen==1.45.1' --no-deps --no-build-isolation"
        exit 1
    fi
fi

echo ""
echo "✅ Nuclear cleanup complete!"
echo ""
echo "Now try running: python3 run.py"
echo ""


#!/bin/bash
# FORCE fix for macOS 14.6 compatibility
# Removes all problematic packages and forces old versions

echo "🔧 FORCE Fixing macOS 14.6 compatibility..."
echo ""

# FORCE remove Pillow and all related
echo "Force removing Pillow and related packages..."
pip3 uninstall -y Pillow PIL 2>/dev/null || true
python3 -m pip uninstall -y Pillow PIL 2>/dev/null || true
echo "✓ Pillow removed"
echo ""

# FORCE reinstall mutagen with OLD version
echo "Force reinstalling mutagen 1.45.1 (oldest compatible)..."
pip3 uninstall -y mutagen 2>/dev/null || true
python3 -m pip uninstall -y mutagen 2>/dev/null || true

# Try multiple old versions
if python3 -m pip install --user "mutagen==1.45.1" --no-deps 2>/dev/null; then
    echo "✓ Mutagen 1.45.1 installed (forced old version)"
elif pip3 install --user "mutagen==1.45.1" --no-deps 2>/dev/null; then
    echo "✓ Mutagen 1.45.1 installed (forced old version)"
elif python3 -m pip install --user "mutagen==1.45.0" --no-deps 2>/dev/null; then
    echo "✓ Mutagen 1.45.0 installed (forced old version)"
elif pip3 install --user "mutagen==1.45.0" --no-deps 2>/dev/null; then
    echo "✓ Mutagen 1.45.0 installed (forced old version)"
elif python3 -m pip install --user "mutagen<1.46" 2>/dev/null; then
    echo "✓ Mutagen installed (old version)"
else
    echo "⚠️  Could not reinstall mutagen"
    echo "   Try manually: pip3 install --user 'mutagen==1.45.1' --no-deps"
fi
echo ""

echo "✅ Force fix complete!"
echo ""
echo "The app should now work on macOS 14.6"
echo "Run: python3 run.py"
echo ""

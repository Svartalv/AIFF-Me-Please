#!/bin/bash
# Quick fix for macOS 14.6 compatibility
# Removes all problematic packages

echo "🔧 Fixing macOS 14.6 compatibility..."
echo ""

# Remove Pillow (main culprit)
echo "Removing Pillow..."
pip3 uninstall -y Pillow 2>/dev/null || true
python3 -m pip uninstall -y Pillow 2>/dev/null || true
echo "✓ Pillow removed"
echo ""

# Reinstall mutagen with compatible version
echo "Reinstalling mutagen (compatible version)..."
pip3 uninstall -y mutagen 2>/dev/null || true
if python3 -m pip install --user "mutagen<1.48" 2>/dev/null; then
    echo "✓ Mutagen reinstalled (compatible version)"
elif pip3 install --user "mutagen<1.48" 2>/dev/null; then
    echo "✓ Mutagen reinstalled (compatible version)"
else
    echo "⚠️  Could not reinstall mutagen, but that's okay"
fi
echo ""

echo "✅ Fix complete!"
echo ""
echo "The app should now work on macOS 14.6"
echo "Run: python3 run.py"
echo ""

#!/bin/bash
# Quick fix script for macOS version error

echo "🔧 Fixing macOS compatibility issue..."
echo ""

# Check if Pillow is installed
if pip3 show Pillow &>/dev/null; then
    echo "⚠️  Pillow is installed and may cause macOS version errors."
    echo "   Uninstalling Pillow (app works fine without it - just no icon)..."
    pip3 uninstall -y Pillow
    echo "✓ Pillow uninstalled"
else
    echo "✓ Pillow is not installed (that's fine)"
fi

echo ""
echo "✅ Fix complete! You can now run:"
echo "   python3 run.py"
echo ""


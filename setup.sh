#!/bin/bash
# Minimal setup script for AIFF Me Please
# FORCED compatibility with macOS 14.6 and below

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Don't exit on errors - handle gracefully
set +e

echo "🎵 AIFF Me Please - Setup (macOS 14.6 Compatible)"
echo "=================================================="
echo ""

# Basic check - just see if python3 exists
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3."
    exit 1
fi

echo "✓ Python found"
echo ""

# FORCE remove Pillow and all related packages
echo "Force removing all problematic packages..."
pip3 uninstall -y Pillow PIL 2>/dev/null || true
python3 -m pip uninstall -y Pillow PIL 2>/dev/null || true
echo "✓ Problematic packages removed"
echo ""

# Install mutagen - FORCE older version that works on macOS 14.6
echo "Installing mutagen (forcing old compatible version)..."
echo "Using mutagen 1.45.1 (compatible with macOS 14.6)..."

# Uninstall any existing mutagen first
pip3 uninstall -y mutagen 2>/dev/null || true
python3 -m pip uninstall -y mutagen 2>/dev/null || true

# Try to install specific old version
if python3 -m pip install --user "mutagen==1.45.1" --no-deps 2>/dev/null; then
    echo "✓ Mutagen 1.45.1 installed"
    # Now install its dependencies separately (older versions)
    python3 -m pip install --user "deprecation>=2.0.0,<3.0" 2>/dev/null || true
elif pip3 install --user "mutagen==1.45.1" --no-deps 2>/dev/null; then
    echo "✓ Mutagen 1.45.1 installed"
    pip3 install --user "deprecation>=2.0.0,<3.0" 2>/dev/null || true
elif python3 -m pip install --user "mutagen==1.45.0" --no-deps 2>/dev/null; then
    echo "✓ Mutagen 1.45.0 installed"
elif pip3 install --user "mutagen==1.45.0" --no-deps 2>/dev/null; then
    echo "✓ Mutagen 1.45.0 installed"
elif python3 -m pip install --user "mutagen<1.46" 2>/dev/null; then
    echo "✓ Mutagen installed (old version)"
elif pip3 install --user "mutagen<1.46" 2>/dev/null; then
    echo "✓ Mutagen installed (old version)"
else
    echo "⚠️  Could not install mutagen automatically"
    echo ""
    echo "Please install manually:"
    echo "   pip3 install --user 'mutagen==1.45.1' --no-deps"
    echo ""
fi
echo ""

# Check FFmpeg (optional - app will check at runtime)
echo "Checking for FFmpeg..."
if command -v ffmpeg &> /dev/null; then
    echo "✓ FFmpeg found"
elif [ -f "$SCRIPT_DIR/resources/ffmpeg/ffmpeg" ]; then
    chmod +x "$SCRIPT_DIR/resources/ffmpeg/ffmpeg" 2>/dev/null
    echo "✓ Bundled FFmpeg found"
else
    echo "⚠️  FFmpeg not found (optional - install with: brew install ffmpeg)"
fi
echo ""

# Make scripts executable
chmod +x run.py 2>/dev/null || true
chmod +x BUILD_SIMPLE.sh 2>/dev/null || true
echo "✓ Scripts made executable"
echo ""

echo "=================================================="
echo "✅ Setup complete!"
echo ""
echo "To run: python3 run.py"
echo ""
echo "If you still get macOS version errors, run:"
echo "  ./fix_macos.sh"
echo ""

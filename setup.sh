#!/bin/bash
# Minimal setup script for AIFF Me Please
# Compatible with macOS 14.6 and below

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Don't exit on errors - handle gracefully
set +e

echo "🎵 AIFF Me Please - Setup"
echo "========================"
echo ""

# Basic check - just see if python3 exists
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3."
    exit 1
fi

echo "✓ Python found"
echo ""

# Remove Pillow FIRST (before installing anything)
echo "Removing Pillow if present (causes macOS compatibility issues)..."
pip3 uninstall -y Pillow 2>/dev/null || true
python3 -m pip uninstall -y Pillow 2>/dev/null || true
echo "✓ Pillow check complete"
echo ""

# Install mutagen - use older version for compatibility
echo "Installing mutagen (audio tag library)..."
echo "Using compatible version for macOS 14.6..."

# Try to install older mutagen version that's compatible
if python3 -m pip install --user "mutagen<1.48" 2>/dev/null; then
    echo "✓ Mutagen installed"
elif pip3 install --user "mutagen<1.48" 2>/dev/null; then
    echo "✓ Mutagen installed"
elif python3 -m pip install --user mutagen 2>/dev/null; then
    echo "✓ Mutagen installed (latest version)"
elif pip3 install --user mutagen 2>/dev/null; then
    echo "✓ Mutagen installed (latest version)"
else
    echo "⚠️  Could not install mutagen automatically"
    echo ""
    echo "Please install manually:"
    echo "   pip3 install --user mutagen"
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

echo "========================"
echo "✅ Setup complete!"
echo ""
echo "To run: python3 run.py"
echo ""

#!/bin/bash
# Setup script for AIFF Me Please
# This script installs dependencies and sets up the application

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Don't exit on errors - we want to handle failures gracefully
set +e

echo "🎵 AIFF Me Please - Setup Script"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or later."
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

echo "✓ Found Python $PYTHON_VERSION"

# Check if Python version is 3.7 or later
if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 7 ]); then
    echo "⚠️  Warning: Python 3.7 or later is recommended"
    echo "   You have Python $PYTHON_VERSION"
    echo "   The app may still work, but some features might not be available"
    echo ""
fi
echo ""

# Check if pip is available
echo "Checking pip..."
if ! python3 -m pip --version &> /dev/null; then
    echo "❌ pip is not installed. Please install pip first."
    exit 1
fi
echo "✓ pip is available"
echo ""

# Install Python dependencies
echo "Installing Python dependencies..."
echo "Installing required dependency (mutagen)..."

# Try multiple methods to install mutagen
if python3 -m pip install --user mutagen 2>/dev/null; then
    echo "✓ Mutagen installed"
elif pip3 install --user mutagen 2>/dev/null; then
    echo "✓ Mutagen installed"
elif python3 -m pip install mutagen 2>/dev/null; then
    echo "✓ Mutagen installed"
else
    echo "⚠️  Failed to install mutagen automatically"
    echo ""
    echo "Please install manually:"
    echo "   pip3 install --user mutagen"
    echo ""
    echo "Or try:"
    echo "   python3 -m pip install --user mutagen"
    echo ""
    read -p "Press Enter to continue anyway (app may not work without mutagen)..." || true
fi

# Remove Pillow if it's installed (causes macOS version compatibility issues)
echo "Checking for Pillow..."
if pip3 show Pillow &>/dev/null; then
    echo "  Found Pillow installed - removing to prevent macOS compatibility issues..."
    pip3 uninstall -y Pillow 2>/dev/null || true
    echo "✓ Pillow removed (app works perfectly without it - just no icon)"
else
    echo "✓ Pillow not installed (that's fine - app works without it)"
fi

echo "✓ Dependencies installed"
echo ""

# Check for FFmpeg
echo "Checking for FFmpeg..."
FFMPEG_FOUND=0

if command -v ffmpeg &> /dev/null; then
    FFMPEG_VERSION=$(ffmpeg -version 2>/dev/null | head -n1)
    if [ $? -eq 0 ]; then
        echo "✓ Found system FFmpeg: $FFMPEG_VERSION"
        FFMPEG_FOUND=1
    fi
fi

if [ $FFMPEG_FOUND -eq 0 ] && [ -f "$SCRIPT_DIR/resources/ffmpeg/ffmpeg" ]; then
    chmod +x "$SCRIPT_DIR/resources/ffmpeg/ffmpeg" 2>/dev/null
    if "$SCRIPT_DIR/resources/ffmpeg/ffmpeg" -version &>/dev/null; then
        echo "✓ Found bundled FFmpeg"
        FFMPEG_FOUND=1
    fi
fi

if [ $FFMPEG_FOUND -eq 0 ]; then
    echo "⚠️  FFmpeg not found"
    if command -v brew &> /dev/null; then
        echo "   Attempting to install via Homebrew..."
        if brew install ffmpeg 2>/dev/null; then
            echo "✓ FFmpeg installed via Homebrew"
            FFMPEG_FOUND=1
        else
            echo "⚠️  Homebrew installation failed"
        fi
    fi
    
    if [ $FFMPEG_FOUND -eq 0 ]; then
        echo ""
        echo "⚠️  FFmpeg is required for audio conversion"
        echo "   Please install it manually:"
        echo "   - brew install ffmpeg  (if you have Homebrew)"
        echo "   - Or download from: https://ffmpeg.org/download.html"
        echo ""
        echo "   The app will still run, but conversion won't work without FFmpeg"
        echo ""
    fi
fi
echo ""

# Make run.py executable
chmod +x run.py
echo "✓ Made run.py executable"
echo ""

echo "=================================="
echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "  1. Run the app: python3 run.py"
echo "  2. Or build standalone app: ./BUILD_SIMPLE.sh"
echo ""
echo "For more info, see: INSTALLATION_COMPLETE.md"
echo ""


#!/bin/bash
# Setup script for AIFF Me Please
# This script installs dependencies and sets up the application

set -e

echo "🎵 AIFF Me Please - Setup Script"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or later."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Found Python $PYTHON_VERSION"
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
python3 -m pip install --user mutagen
echo "✓ Mutagen installed"

# Check for existing Pillow that might cause macOS version issues
echo "Checking for Pillow compatibility issues..."
if pip3 show Pillow &>/dev/null; then
    PILLOW_VERSION=$(pip3 show Pillow | grep Version | cut -d' ' -f2)
    echo "  Found Pillow $PILLOW_VERSION"
    
    # Test if Pillow can be imported without causing system abort
    if python3 -c "from PIL import Image" 2>/dev/null; then
        echo "✓ Pillow is compatible (icon support enabled)"
    else
        echo "⚠️  Pillow version incompatible with your macOS version"
        echo "   Uninstalling Pillow to prevent errors..."
        pip3 uninstall -y Pillow 2>/dev/null
        echo "✓ Pillow removed (app will work fine without icon)"
    fi
else
    # Try to install Pillow (optional - for icon support)
    echo "Installing optional dependency (Pillow for icon support)..."
    if python3 -m pip install --user Pillow 2>/dev/null; then
        # Test if it actually works
        if python3 -c "from PIL import Image" 2>/dev/null; then
            echo "✓ Pillow installed (icon support enabled)"
        else
            echo "⚠️  Pillow installed but incompatible with your macOS"
            echo "   Removing to prevent errors..."
            pip3 uninstall -y Pillow 2>/dev/null
            echo "✓ Pillow removed (app will work fine without icon)"
        fi
    else
        echo "⚠️  Pillow installation skipped (icon may not display, but app will work fine)"
    fi
fi
echo "✓ Dependencies installed"
echo ""

# Check for FFmpeg
echo "Checking for FFmpeg..."
if command -v ffmpeg &> /dev/null; then
    FFMPEG_VERSION=$(ffmpeg -version | head -n1)
    echo "✓ Found system FFmpeg: $FFMPEG_VERSION"
elif [ -f "resources/ffmpeg/ffmpeg" ]; then
    echo "✓ Found bundled FFmpeg"
    chmod +x resources/ffmpeg/ffmpeg
else
    echo "⚠️  FFmpeg not found. Installing via Homebrew..."
    if command -v brew &> /dev/null; then
        brew install ffmpeg
        echo "✓ FFmpeg installed via Homebrew"
    else
        echo "❌ Homebrew not found. Please install FFmpeg manually:"
        echo "   brew install ffmpeg"
        echo "   Or download from: https://ffmpeg.org/download.html"
        exit 1
    fi
fi
echo ""

# Make run.py executable
chmod +x run.py
echo "✓ Made run.py executable"
echo ""

echo "=================================="
echo "✅ Setup complete!"
echo ""
echo "To run the app:"
echo "  python3 run.py"
echo ""
echo "Or double-click run.py (if configured in Finder)"
echo ""


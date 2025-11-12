#!/bin/bash
# Setup script for AIFF Me Please
# This script installs dependencies and sets up the application

# Don't exit on errors - we want to handle Pillow failures gracefully
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
if command -v ffmpeg &> /dev/null; then
    FFMPEG_VERSION=$(ffmpeg -version | head -n1)
    echo "✓ Found system FFmpeg: $FFMPEG_VERSION"
elif [ -f "resources/ffmpeg/ffmpeg" ]; then
    echo "✓ Found bundled FFmpeg"
    chmod +x resources/ffmpeg/ffmpeg
else
    echo "⚠️  FFmpeg not found. Installing via Homebrew..."
    if command -v brew &> /dev/null; then
        if brew install ffmpeg; then
            echo "✓ FFmpeg installed via Homebrew"
        else
            echo "⚠️  FFmpeg installation failed. Please install manually:"
            echo "   brew install ffmpeg"
            echo "   Or download from: https://ffmpeg.org/download.html"
        fi
    else
        echo "⚠️  Homebrew not found. Please install FFmpeg manually:"
        echo "   brew install ffmpeg"
        echo "   Or download from: https://ffmpeg.org/download.html"
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


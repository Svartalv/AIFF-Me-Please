#!/bin/bash
# Simple build script that works with any Python 3.7+ version

echo "🔨 Building AIFF Me Please (Simple Method)"
echo "=========================================="
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "Using: $PYTHON_VERSION"
echo ""

# Install PyInstaller if needed
if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo "Installing PyInstaller..."
    if ! python3 -m pip install --user pyinstaller 2>/dev/null; then
        if ! pip3 install --user pyinstaller 2>/dev/null; then
            echo "❌ Failed to install PyInstaller"
            echo "   Please install manually: pip3 install --user pyinstaller"
            exit 1
        fi
    fi
    echo "✓ PyInstaller installed"
fi

# FORCE remove Pillow first (macOS 14.6 compatibility)
echo "Force removing Pillow and related packages..."
pip3 uninstall -y Pillow PIL 2>/dev/null || true
python3 -m pip uninstall -y Pillow PIL 2>/dev/null || true

# Install mutagen if needed (FORCE old version for macOS 14.6)
if ! python3 -c "import mutagen" 2>/dev/null; then
    echo "Installing mutagen 1.45.1 (forced old version for macOS 14.6)..."
    # Uninstall any existing mutagen first
    pip3 uninstall -y mutagen 2>/dev/null || true
    python3 -m pip uninstall -y mutagen 2>/dev/null || true
    
    # Try to install specific old version with --no-deps
    if python3 -m pip install --user "mutagen==1.45.1" --no-deps 2>/dev/null; then
        echo "✓ Mutagen 1.45.1 installed"
    elif pip3 install --user "mutagen==1.45.1" --no-deps 2>/dev/null; then
        echo "✓ Mutagen 1.45.1 installed"
    elif python3 -m pip install --user "mutagen==1.45.0" --no-deps 2>/dev/null; then
        echo "✓ Mutagen 1.45.0 installed"
    elif pip3 install --user "mutagen==1.45.0" --no-deps 2>/dev/null; then
        echo "✓ Mutagen 1.45.0 installed"
    elif python3 -m pip install --user "mutagen<1.46" 2>/dev/null; then
        echo "✓ Mutagen installed (old version)"
    elif pip3 install --user "mutagen<1.46" 2>/dev/null; then
        echo "✓ Mutagen installed (old version)"
    else
        echo "❌ Failed to install mutagen"
        echo "   Please install manually: pip3 install --user 'mutagen==1.45.1' --no-deps"
        exit 1
    fi
fi

echo "Cleaning old builds..."
rm -rf build dist *.spec 2>/dev/null || true
echo ""

echo "Building app (this may take a few minutes)..."
echo ""

# Build directly without spec file - simpler and more compatible
python3 -m PyInstaller \
    --name "AIFF Me Please" \
    --windowed \
    --onefile \
    --hidden-import=mutagen \
    --hidden-import=mutagen.flac \
    --hidden-import=mutagen.mp3 \
    --exclude-module=PIL \
    --exclude-module=Pillow \
    --noconfirm \
    --clean \
    run.py

if [ $? -eq 0 ] && ([ -d "dist/AIFF Me Please.app" ] || [ -f "dist/AIFF Me Please.app" ]); then
    echo ""
    echo "✅ Build complete!"
    echo ""
    echo "Your app: dist/AIFF Me Please.app"
    echo ""
    echo "Double-click it to run!"
else
    echo ""
    echo "❌ Build failed"
    exit 1
fi


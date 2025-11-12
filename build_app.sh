#!/bin/bash
# Build script to create a standalone macOS .app bundle

echo "🔨 Building AIFF Me Please macOS App"
echo "===================================="
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if PyInstaller is installed
if ! python3 -m pip show pyinstaller &>/dev/null; then
    echo "Installing PyInstaller (only needed for building)..."
    python3 -m pip install --user pyinstaller
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install PyInstaller"
        echo "   Please install manually: pip3 install --user pyinstaller"
        exit 1
    fi
    echo ""
fi

# Remove Pillow first (compatibility)
echo "Removing Pillow if present (for macOS compatibility)..."
pip3 uninstall -y Pillow 2>/dev/null || true
python3 -m pip uninstall -y Pillow 2>/dev/null || true

# Check if mutagen is installed (required for the app)
if ! python3 -m pip show mutagen &>/dev/null; then
    echo "Installing mutagen (compatible version for macOS 14.6)..."
    if ! python3 -m pip install --user "mutagen<1.48" 2>/dev/null; then
        # Fallback to latest
        python3 -m pip install --user mutagen
    fi
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install mutagen"
        echo "   Please install manually: pip3 install --user mutagen"
        exit 1
    fi
    echo ""
fi

echo "Cleaning previous builds..."
rm -rf build dist 2>/dev/null || true
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "Building .app bundle using spec file..."
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}' | cut -d'.' -f1,2)
echo "Using Python $PYTHON_VERSION"
echo ""

# Check if spec file exists
if [ ! -f "$SCRIPT_DIR/AIFF_Me_Please.spec" ]; then
    echo "⚠️  Spec file not found! Generating it..."
    python3 -m PyInstaller --name "AIFF Me Please" \
        --windowed \
        --onefile \
        --hidden-import=mutagen \
        --hidden-import=mutagen.flac \
        --hidden-import=mutagen.mp3 \
        --hidden-import=mutagen.id3 \
        --hidden-import=mutagen._util \
        --collect-all mutagen \
        --exclude-module=PIL \
        --exclude-module=Pillow \
        --noconfirm \
        --clean \
        run.py
    
    # Check if spec was generated (PyInstaller creates it with spaces in name)
    if [ -f "$SCRIPT_DIR/AIFF Me Please.spec" ]; then
        echo "✓ Spec file generated, building app..."
        python3 -m PyInstaller "$SCRIPT_DIR/AIFF Me Please.spec" --clean --noconfirm
    elif [ -f "$SCRIPT_DIR/AIFF_Me_Please.spec" ]; then
        echo "✓ Spec file found, building app..."
        python3 -m PyInstaller "$SCRIPT_DIR/AIFF_Me_Please.spec" --clean --noconfirm
    else
        echo "❌ Failed to generate spec file"
        echo "Trying direct build without spec..."
        python3 -m PyInstaller --name "AIFF Me Please" \
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
    fi
else
    # Build using the spec file
    echo "Using existing spec file..."
    python3 -m PyInstaller "$SCRIPT_DIR/AIFF_Me_Please.spec" --clean --noconfirm
fi

if [ $? -eq 0 ] && ([ -d "dist/AIFF Me Please.app" ] || [ -f "dist/AIFF Me Please.app" ]); then
    echo ""
    echo "✅ Build complete!"
    echo ""
    echo "Your app is located at:"
    echo "  $(pwd)/dist/AIFF Me Please.app"
    echo ""
    echo "You can:"
    echo "  1. Double-click 'AIFF Me Please.app' to run"
    echo "  2. Drag to Applications folder to install"
    echo "  3. Share the .app file with your friend"
    echo ""
    echo "Note: The app includes all dependencies (mutagen, etc.)"
    echo "      Your friend doesn't need to install Python or anything else!"
    echo ""
else
    echo ""
    echo "❌ Build failed. Check the errors above."
    exit 1
fi


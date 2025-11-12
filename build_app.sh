#!/bin/bash
# Build script to create a standalone macOS .app bundle

echo "🔨 Building AIFF Me Please macOS App"
echo "===================================="
echo ""

# Check if PyInstaller is installed
if ! python3 -m pip show pyinstaller &>/dev/null; then
    echo "Installing PyInstaller..."
    python3 -m pip install --user pyinstaller
    echo ""
fi

# Check if mutagen is installed
if ! python3 -m pip show mutagen &>/dev/null; then
    echo "Installing mutagen (required for build)..."
    python3 -m pip install --user mutagen
    echo ""
fi

echo "Cleaning previous builds..."
rm -rf build dist 2>/dev/null || true
echo ""

echo "Building .app bundle using spec file..."
echo ""

# Build using the spec file
python3 -m PyInstaller AIFF_Me_Please.spec --clean --noconfirm

if [ $? -eq 0 ] && [ -d "dist/AIFF Me Please.app" ]; then
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


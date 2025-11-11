#!/bin/bash
# Setup script to download/copy ffmpeg binary

set -e

FFMPEG_DIR="resources/ffmpeg"
FFMPEG_PATH="$FFMPEG_DIR/ffmpeg"

echo "Setting up ffmpeg binary for FLAC2AIFF..."

# Create directory if it doesn't exist
mkdir -p "$FFMPEG_DIR"

# Check if ffmpeg already exists
if [ -f "$FFMPEG_PATH" ]; then
    echo "ffmpeg already exists at $FFMPEG_PATH"
    exit 0
fi

# Try to find ffmpeg in common locations
if command -v ffmpeg &> /dev/null; then
    SYSTEM_FFMPEG=$(which ffmpeg)
    echo "Found system ffmpeg at $SYSTEM_FFMPEG"
    echo "Copying to $FFMPEG_PATH..."
    cp "$SYSTEM_FFMPEG" "$FFMPEG_PATH"
    chmod +x "$FFMPEG_PATH"
    echo "✓ ffmpeg copied successfully"
    exit 0
fi

# Try Homebrew location (Apple Silicon)
if [ -f "/opt/homebrew/bin/ffmpeg" ]; then
    echo "Found ffmpeg in Homebrew (Apple Silicon)"
    cp "/opt/homebrew/bin/ffmpeg" "$FFMPEG_PATH"
    chmod +x "$FFMPEG_PATH"
    echo "✓ ffmpeg copied successfully"
    exit 0
fi

# Try Homebrew location (Intel)
if [ -f "/usr/local/bin/ffmpeg" ]; then
    echo "Found ffmpeg in Homebrew (Intel)"
    cp "/usr/local/bin/ffmpeg" "$FFMPEG_PATH"
    chmod +x "$FFMPEG_PATH"
    echo "✓ ffmpeg copied successfully"
    exit 0
fi

echo "❌ ffmpeg not found. Please install it first:"
echo ""
echo "Option 1: Install via Homebrew"
echo "  brew install ffmpeg"
echo ""
echo "Option 2: Download static build from"
echo "  https://evermeet.cx/ffmpeg/"
echo ""
echo "Then run this script again, or manually copy ffmpeg to:"
echo "  $FFMPEG_PATH"
exit 1


#!/bin/bash
# Simple script to help install ffmpeg

echo "Checking for ffmpeg..."

# Check if already installed
if command -v ffmpeg &> /dev/null; then
    echo "✓ ffmpeg is already installed!"
    ffmpeg -version | head -1
    exit 0
fi

# Check for Homebrew
if command -v brew &> /dev/null; then
    echo "Installing ffmpeg via Homebrew..."
    brew install ffmpeg
    if [ $? -eq 0 ]; then
        echo "✓ ffmpeg installed successfully!"
        exit 0
    fi
fi

echo ""
echo "FFmpeg installation options:"
echo "1. Install via Homebrew: brew install ffmpeg"
echo "2. Download static build from: https://evermeet.cx/ffmpeg/"
echo "3. Or use MacPorts: sudo port install ffmpeg"
echo ""
echo "After installing, restart the FLAC2AIFF app."


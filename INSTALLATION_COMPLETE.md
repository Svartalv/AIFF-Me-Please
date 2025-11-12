# Installation Complete! 🎉

## Quick Start

1. **Run the app**:
   ```bash
   python3 run.py
   ```

2. **Or build a standalone app** (no Python needed):
   ```bash
   ./BUILD_SIMPLE.sh
   ```
   Then double-click `dist/AIFF Me Please.app`

## What Was Installed

- ✅ **mutagen** - For reading/writing audio tags
- ✅ **FFmpeg** - For audio conversion (if available)

## Using the App

1. Click "Choose" next to "Input folder" → Select your FLAC or MP3 files
2. Click "Choose" next to "Output folder" → Choose where to save AIFF files
3. Click "Start Conversion"
4. Done!

## Troubleshooting

**App won't start?**
- Check: `python3 --version` (needs 3.7+)
- Check: `pip3 list | grep mutagen`

**FFmpeg not found?**
- Install: `brew install ffmpeg`
- Or download from: https://ffmpeg.org/download.html

**Need help?** Check README.md or INSTALL.md


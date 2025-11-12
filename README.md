# AIFF Me Please

Convert your audio files (FLAC, MP3) to AIFF format for DJ use.

## Installation

### Easiest Way: Double-Click Installer

1. **Double-click** `Install.command` in Finder
2. Follow the prompts in Terminal
3. Done!

### Or Use Terminal

1. **Open Terminal**
2. **Run**:
   ```bash
   cd "/path/to/AIFF Me Please"
   ./setup.sh
   ```
3. **Launch**:
   ```bash
   python3 run.py
   ```

### Build Standalone App (No Python Needed!)

**Simple method** (recommended):
```bash
./BUILD_SIMPLE.sh
```

**Or advanced method**:
```bash
./build_app.sh
```

Then double-click `dist/AIFF Me Please.app` - no installation needed!

## Quick Start

1. Select your audio files (FLAC or MP3)
2. Choose output folder  
3. Click "Start Conversion"
4. Done!

## What You Need

- **macOS** (10.14 or later, including macOS 14.6)
- **Python 3.7+** (check with `python3 --version`)
- **FFmpeg** (installer will help you get it)

**macOS 14.6 Compatibility**: The installer automatically forces compatible package versions. If you get macOS version errors, run `./fix_macos.sh` to force downgrade all dependencies.

## Troubleshooting

**macOS Version Error** (macOS 14.6 or earlier):
```
macOS 14 (1407) or later required, have instead 14 (1406) !
```
- **Quick fix**: Run `./fix_macos.sh` to force downgrade dependencies
- Or manually: `pip3 uninstall Pillow && pip3 install --user 'mutagen==1.45.1' --no-deps`
- The app works perfectly without Pillow (just no icon display)

**"FFmpeg not found"**
- Run: `brew install ffmpeg`

**"No module named 'mutagen'"**
- Run: `pip3 install --user 'mutagen==1.45.1' --no-deps`
- Or run: `./setup.sh` (it will install the compatible version)

**App won't start**
- Check Python: `python3 --version` (needs 3.7+)
- Check dependencies: `pip3 list | grep mutagen`
- If on macOS 14.6: Run `./fix_macos.sh` first

## Features

- ✅ Converts FLAC and MP3 to AIFF
- ✅ Preserves all metadata
- ✅ CDJ-optimized (44.1kHz, 16-bit, stereo)
- ✅ Smart filename sanitization
- ✅ Dark, modern interface
- ✅ Works offline

For detailed installation instructions, see [INSTALL.md](INSTALL.md)

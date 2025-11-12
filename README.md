# AIFF Me Please

Convert your audio files (FLAC, MP3) to AIFF format for DJ use.

## Quick Install

### Option 1: Use the Installer (Easiest)

1. **Download the project** (or clone with `git clone`)
2. **Open Terminal** and run:
   ```bash
   cd "/path/to/AIFF Me Please"
   ./setup.sh
   ```
3. **Done!** Run the app with:
   ```bash
   python3 run.py
   ```

### Option 2: Build Standalone App

Create a double-clickable `.app` file:

```bash
./build_app.sh
```

Then double-click `dist/AIFF Me Please.app` - no Python needed!

## What You Need

- **macOS** (any recent version)
- **Python 3.7+** (usually pre-installed)
- **FFmpeg** (installer will help you get it)

## Manual Installation

If the installer doesn't work:

1. **Install mutagen**:
   ```bash
   pip3 install --user mutagen
   ```

2. **Install FFmpeg**:
   ```bash
   brew install ffmpeg
   ```
   (Or download from [ffmpeg.org](https://ffmpeg.org/download.html))

3. **Run the app**:
   ```bash
   python3 run.py
   ```

## Using the App

1. Click **"Choose"** next to "Input folder" and select your FLAC or MP3 files
2. Click **"Choose"** next to "Output folder" to pick where converted files go
3. Click **"Start Conversion"**
4. Wait for the completion message

Your files will be converted to AIFF format (44.1kHz, 16-bit, stereo) with all metadata preserved.

## Troubleshooting

**"FFmpeg not found"**
- Install FFmpeg: `brew install ffmpeg`
- Or download from [ffmpeg.org](https://ffmpeg.org/download.html)

**"No module named 'mutagen'"**
- Run: `pip3 install --user mutagen`

**App won't start**
- Make sure Python 3.7+ is installed: `python3 --version`
- Check dependencies: `pip3 list | grep mutagen`

## Features

- ✅ Converts FLAC and MP3 to AIFF
- ✅ Preserves all metadata (Artist, Title, Album, etc.)
- ✅ CDJ-optimized (44.1kHz, 16-bit, stereo)
- ✅ Smart filename sanitization for CDJ compatibility
- ✅ Dark, modern interface
- ✅ Works offline

## License

Free to use for personal projects.

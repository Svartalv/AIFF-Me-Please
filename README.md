# AIFF Me Please

A simple, reliable macOS application for converting FLAC and MP3 audio files to AIFF format, optimized for Pioneer CDJ/XDJ use.

## Features

- **Simple drag-and-drop workflow**: Select files → Click Convert
- **Format support**: FLAC and MP3 input → AIFF output
- **CDJ-optimized**: 44.1 kHz, 16-bit, stereo (PCM uncompressed)
- **Metadata preservation**: Automatically preserves and writes tags to AIFF
- **Smart filenames**: Uses "Artist - Title.aiff" format with automatic sanitization
- **Dark, modern UI**: Clean, minimal interface inspired by Cursor
- **Offline operation**: No internet connection required

## Requirements

- **macOS** (tested on macOS 10.14+)
- **Python 3.7+**
- **FFmpeg** (installation instructions below)

## ⚠️ macOS Compatibility

**Pillow has been removed** from this app to ensure compatibility with all macOS versions (including macOS 14.6 and earlier). 

The app works perfectly without Pillow - you just won't see the cat icon in the title bar. All file conversion features work normally.

## Installation

### Quick Setup (Recommended)

**For first-time users, use the automated setup script:**

```bash
cd "/path/to/AIFF Me Please"
./setup.sh
```

This script will automatically:
- Check Python version
- Install required dependency (mutagen only - Pillow removed for compatibility)
- Remove Pillow if it's installed (prevents macOS version errors)
- Check for FFmpeg and install it if needed via Homebrew
- Make the app ready to run

Then run the app:
```bash
python3 run.py
```

### Manual Setup

**Step 1: Install Python Dependencies**

Open Terminal and run:

```bash
cd "/path/to/AIFF Me Please"
pip3 install --user -r requirements.txt
```

Or if you prefer a virtual environment:

```bash
cd "/path/to/AIFF Me Please"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Step 2: Install FFmpeg

**Option A: Using Homebrew (Recommended)**
```bash
brew install ffmpeg
```

**Option B: Manual Installation**
1. Download FFmpeg from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Extract and add to your PATH, or place the binary in `/usr/local/bin/`

**Option C: Download FFmpeg Manually**
If you can't use Homebrew, download FFmpeg from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html) and add it to your PATH.

**Note**: The repository does not include the FFmpeg binary due to size limitations. You must install FFmpeg separately using one of the methods above.

### Step 3: Run the Application

**Method 1: Direct Python execution**
```bash
cd "/path/to/AIFF Me Please"
python3 run.py
```

**Method 2: Using the main module**
```bash
cd "/path/to/AIFF Me Please"
python3 -m app.main
```

## Usage

1. **Launch the app** by running `python3 run.py`

2. **Select input files**:
   - Click "Choose" next to "Input folder"
   - Select one or more FLAC or MP3 files (or select a folder containing audio files)

3. **Select output folder**:
   - Click "Choose" next to "Output folder"
   - Choose where you want the converted AIFF files saved
   - Default: Creates a folder named `[input_folder]_AIFF`

4. **Review the file list**:
   - The app shows which files will be converted
   - Output filenames are automatically generated from metadata (Artist - Title.aiff)
   - Special characters are sanitized for CDJ compatibility

5. **Start conversion**:
   - Click "Start Conversion"
   - Watch the progress as files are converted
   - A summary dialog appears when complete

## Output Format

- **Format**: AIFF (Audio Interchange File Format)
- **Sample Rate**: 44.1 kHz (CD quality)
- **Bit Depth**: 16-bit PCM
- **Channels**: Stereo
- **Metadata**: Preserved from source files (Artist, Title, Album, etc.)

## Filename Rules

- **Template**: `Artist - Title.aiff`
- **Sanitization**: Only ASCII letters, numbers, spaces, and `- _ ( )` are allowed
- **Collision handling**: If a file already exists, appends `(2)`, `(3)`, etc.
- **Fallback**: If metadata is missing, uses original filename (sanitized)

## Troubleshooting

### "FFmpeg not found"
- Install FFmpeg using one of the methods above
- Make sure FFmpeg is in your PATH: `which ffmpeg`
- The app will try to use the bundled FFmpeg in `resources/ffmpeg/ffmpeg` as a fallback

### "No module named 'mutagen'"
- Install mutagen: `pip3 install --user mutagen`

### Icon not showing
The app icon is not displayed because Pillow has been removed for macOS compatibility. This is normal and expected. All app features work perfectly - you just won't see the cat icon in the title bar.

### Files not converting
- Check that input files are valid FLAC or MP3
- Check that output folder is writable
- Check terminal output for error messages

### Icon not showing
- The app icon (`app/aiffmeplease.png`) should load automatically
- If it doesn't appear, the app will still function normally

## Technical Details

- **GUI Framework**: Tkinter
- **Audio Processing**: FFmpeg
- **Tag Handling**: Mutagen
- **Icon Support**: PIL/Pillow

## License

This project is provided as-is for personal use.

## Credits

Icon: Black cat image (`aiffmeplease.png`)


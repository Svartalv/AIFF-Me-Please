# Quick Start Guide

## ⚠️ IMPORTANT: macOS Compatibility

**If you have macOS 14.6 or earlier**, you may get a version error. The setup script handles this automatically, but if you see:
```
macOS 14 (1407) or later required, have instead 14 (1406) !
```

**Just run**: `./fix_macos.sh` and then `python3 run.py`

The app works perfectly without Pillow - you just won't see the icon.

## For Your Friend - Simple Setup Instructions

### Option 1: Automated Setup (Easiest)

1. **Open Terminal** (Press `Cmd + Space`, type "Terminal", press Enter)

2. **Navigate to the project folder**:
   ```bash
   cd "/path/to/AIFF Me Please"
   ```

3. **Run the setup script**:
   ```bash
   ./setup.sh
   ```
   
   This will automatically:
   - Check Python version
   - Install required dependencies (mutagen)
   - Handle Pillow compatibility automatically
   - Check for FFmpeg and install it if needed
   - Make everything ready to run

4. **If you get macOS version errors**, run:
   ```bash
   ./fix_macos.sh
   ```

5. **Run the app**:
   ```bash
   python3 run.py
   ```

### Option 2: Manual Setup

If the setup script doesn't work, follow these steps:

1. **Install Python dependencies**:
   ```bash
   pip3 install --user mutagen Pillow
   ```

2. **Install FFmpeg** (choose one):
   - **Using Homebrew** (if installed):
     ```bash
     brew install ffmpeg
     ```
   - **Or download manually** from [ffmpeg.org](https://ffmpeg.org/download.html)

3. **Run the app**:
   ```bash
   python3 run.py
   ```

## Using the App

1. **Launch**: Run `python3 run.py` in Terminal

2. **Select files**: Click "Choose" next to "Input folder" and select your FLAC or MP3 files

3. **Choose output**: Click "Choose" next to "Output folder" to pick where converted files go

4. **Convert**: Click "Start Conversion" and wait for the completion message

That's it! Your AIFF files will be ready for your CDJ.

## Troubleshooting

**"No module named 'mutagen'"**
- Run: `pip3 install --user mutagen`

**macOS Version Error** (most common on macOS 14.6 or earlier)
```
macOS 14 (1407) or later required, have instead 14 (1406) !
```
- **Fix**: `pip3 uninstall Pillow` or run `./fix_macos.sh`
- The app works perfectly without Pillow (just no icon)

**"FFmpeg not found"**
- Install FFmpeg: `brew install ffmpeg` (if you have Homebrew)
- Or download from [ffmpeg.org](https://ffmpeg.org/download.html)

**App won't start**
- Make sure you're using Python 3.7 or later: `python3 --version`
- Check that mutagen is installed: `pip3 list | grep mutagen`
- If you see macOS version errors, uninstall Pillow: `pip3 uninstall Pillow`

## Need Help?

Check the full README.md for detailed information.


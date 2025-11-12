# Quick Start

## Installation (2 Steps)

1. **Run the installer**:
   ```bash
   ./setup.sh
   ```

2. **Run the app**:
   ```bash
   python3 run.py
   ```

That's it!

## Or Build a Standalone App

Want a double-clickable app? Run:
```bash
./build_app.sh
```

Then double-click `dist/AIFF Me Please.app` - no Terminal needed!

## Using the App

1. Select your audio files (FLAC or MP3)
2. Choose output folder
3. Click "Start Conversion"
4. Done!

## Need Help?

- **FFmpeg missing?** Run: `brew install ffmpeg`
- **Python error?** Make sure you have Python 3.7+: `python3 --version`
- **Dependencies?** Run: `pip3 install --user mutagen`

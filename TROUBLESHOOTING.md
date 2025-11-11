# Troubleshooting Guide

## macOS Version Error

**Error**: `macOS 14 (1407) or later required, have instead 14 (1406)`

This error comes from Pillow (PIL), which is only needed for displaying the app icon. The app will work perfectly fine without it!

### Solution 1: Skip Pillow Installation (Recommended)

The app works without Pillow - you just won't see the cat icon. Install only the required dependency:

```bash
pip3 install --user mutagen
```

Then run the app normally:
```bash
python3 run.py
```

### Solution 2: Install Older Pillow Version

If you want the icon, try installing an older Pillow version that supports your macOS:

```bash
pip3 install --user "Pillow<11.0"
```

### Solution 3: Upgrade macOS

If possible, upgrade to macOS 14.7 or later, then install all dependencies normally.

## Other Common Issues

### "No module named 'mutagen'"

Install it:
```bash
pip3 install --user mutagen
```

### "FFmpeg not found"

Install FFmpeg:
```bash
brew install ffmpeg
```

Or if you don't have Homebrew:
1. Install Homebrew: https://brew.sh
2. Then: `brew install ffmpeg`

### "Permission denied" when running setup.sh

Make it executable:
```bash
chmod +x setup.sh
./setup.sh
```

### App won't start

1. Check Python version: `python3 --version` (needs 3.7+)
2. Check dependencies: `pip3 list | grep mutagen`
3. Try running directly: `python3 run.py`

## Running Without Icon

The app is fully functional without Pillow. You just won't see the cat icon in the window title bar or message boxes. All other features work normally.


# Installation Guide

## Method 1: Automated Installer (Recommended)

1. **Open Terminal**
2. **Navigate to the project folder**:
   ```bash
   cd "/path/to/AIFF Me Please"
   ```
3. **Run the installer**:
   ```bash
   ./setup.sh
   ```
4. **Launch the app**:
   ```bash
   python3 run.py
   ```

The installer automatically:
- ✅ Removes problematic packages (Pillow)
- ✅ Installs compatible dependencies (mutagen 1.45.1 for macOS 14.6)
- ✅ Checks for FFmpeg
- ✅ Sets everything up

## Method 2: Build Standalone App

Create a double-clickable macOS app:

```bash
./build_app.sh
```

The app will be created at: `dist/AIFF Me Please.app`

**Benefits:**
- No Python installation needed
- No dependencies to install
- Just double-click and run
- Easy to share with friends

## Method 3: Manual Installation

If you prefer to install manually:

1. **Remove Pillow** (causes macOS compatibility issues):
   ```bash
   pip3 uninstall -y Pillow
   ```

2. **Install Python dependencies** (compatible version for macOS 14.6):
   ```bash
   pip3 install --user 'mutagen==1.45.1' --no-deps
   ```

3. **Install FFmpeg**:
   ```bash
   brew install ffmpeg
   ```
   (If you don't have Homebrew, install it from [brew.sh](https://brew.sh))

4. **Run the app**:
   ```bash
   python3 run.py
   ```

## Requirements

- **macOS** (10.14 or later, including macOS 14.6)
- **Python 3.7+** (check with `python3 --version`)
- **FFmpeg** (for audio conversion)

**macOS 14.6 Compatibility**: The installer automatically forces compatible package versions (mutagen 1.45.1) to work on macOS 14.6 and earlier. If you encounter macOS version errors, run `./fix_macos.sh`.

## Troubleshooting

### "Command not found: ./setup.sh"
Make the script executable:
```bash
chmod +x setup.sh
./setup.sh
```

### "FFmpeg not found"
Install FFmpeg:
```bash
brew install ffmpeg
```

Or download from: https://ffmpeg.org/download.html

### "No module named 'mutagen'"
Install the compatible version:
```bash
pip3 install --user 'mutagen==1.45.1' --no-deps
```
Or run `./setup.sh` which will install the correct version automatically.

### macOS Version Error (macOS 14.6)
If you see:
```
macOS 14 (1407) or later required, have instead 14 (1406) !
```

**Quick fix**:
```bash
./fix_macos.sh
```

**Or manually**:
```bash
pip3 uninstall -y Pillow
pip3 install --user 'mutagen==1.45.1' --no-deps
```

The app works perfectly without Pillow (you just won't see the icon).

### "Python version too old"
You need Python 3.7 or later. Check your version:
```bash
python3 --version
```

If it's too old, install a newer version from [python.org](https://www.python.org/downloads/)

## Next Steps

After installation, see [QUICKSTART.md](QUICKSTART.md) for how to use the app.


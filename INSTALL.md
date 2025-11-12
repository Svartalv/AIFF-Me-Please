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
- ✅ Checks Python version
- ✅ Installs required dependencies
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

1. **Install Python dependencies**:
   ```bash
   pip3 install --user mutagen
   ```

2. **Install FFmpeg**:
   ```bash
   brew install ffmpeg
   ```
   (If you don't have Homebrew, install it from [brew.sh](https://brew.sh))

3. **Run the app**:
   ```bash
   python3 run.py
   ```

## Requirements

- **macOS** (10.14 or later)
- **Python 3.7+** (check with `python3 --version`)
- **FFmpeg** (for audio conversion)

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
Install it:
```bash
pip3 install --user mutagen
```

### "Python version too old"
You need Python 3.7 or later. Check your version:
```bash
python3 --version
```

If it's too old, install a newer version from [python.org](https://www.python.org/downloads/)

## Next Steps

After installation, see [QUICKSTART.md](QUICKSTART.md) for how to use the app.


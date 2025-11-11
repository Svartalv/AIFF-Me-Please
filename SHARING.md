# Sharing AIFF Me Please with Your Friend

## How to Share

### Option 1: Git Repository (Recommended)

If your friend has Git installed:

```bash
# Your friend can clone the repository
git clone <repository-url>
cd "AIFF Me Please"
./setup.sh
python3 run.py
```

### Option 2: Zip File

1. **Create a zip file** of the entire project folder:
   - Right-click the "AIFF Me Please" folder
   - Select "Compress"
   - Share the zip file

2. **Your friend should**:
   - Extract the zip file
   - Open Terminal
   - Navigate to the extracted folder
   - Run `./setup.sh`
   - Run `python3 run.py`

### Option 3: Share Specific Files

**Essential files to share:**
- `app/` folder (all Python files)
- `app/aiffmeplease.png` (icon)
- `resources/ffmpeg/ffmpeg` (bundled FFmpeg binary)
- `run.py` (entry point)
- `requirements.txt` (dependencies)
- `setup.sh` (setup script)
- `README.md` (documentation)
- `QUICKSTART.md` (quick guide)

## What Your Friend Needs

1. **macOS** (the app is macOS-specific)
2. **Python 3.7+** (usually pre-installed on macOS)
3. **Terminal access** (built into macOS)
4. **Internet connection** (for initial setup to download dependencies)

## Setup Instructions for Your Friend

**Send them this:**

1. Extract the zip file (if shared as zip)
2. Open Terminal (Cmd + Space, type "Terminal")
3. Navigate to the folder:
   ```bash
   cd "/path/to/AIFF Me Please"
   ```
4. Run the setup:
   ```bash
   ./setup.sh
   ```
5. Run the app:
   ```bash
   python3 run.py
   ```

That's it! The setup script handles everything automatically.

## Troubleshooting for Your Friend

**If setup.sh doesn't work:**
- Make sure it's executable: `chmod +x setup.sh`
- Or run manually: `bash setup.sh`

**If Python dependencies fail:**
- Try: `pip3 install --user mutagen Pillow`
- Or: `python3 -m pip install --user mutagen Pillow`

**If FFmpeg is missing:**
- Install Homebrew first: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
- Then: `brew install ffmpeg`

**If the app won't start:**
- Check Python version: `python3 --version` (needs 3.7+)
- Check dependencies: `pip3 list | grep mutagen`
- Check FFmpeg: `which ffmpeg` or `ffmpeg -version`

## File Size Considerations

The project includes:
- Source code: ~50 KB
- Icon image: ~200 KB
- Bundled FFmpeg: ~50-100 MB (large!)

**To reduce size for sharing:**
- You can exclude `resources/ffmpeg/ffmpeg` if your friend can install FFmpeg via Homebrew
- The app will try to use system FFmpeg first, then fall back to bundled version

## Version Information

- **App Name**: AIFF Me Please
- **Version**: 1.0.0
- **Python**: 3.7+
- **Platform**: macOS


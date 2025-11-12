# Building the macOS App

## Quick Build

Run the build script:
```bash
./build_app.sh
```

This will create a standalone `AIFF Me Please.app` in the `dist/` folder.

## What Gets Built

The `.app` bundle includes:
- Python runtime
- All dependencies (mutagen, etc.)
- Application code
- Icon file

**Your friend can just double-click the .app file - no installation needed!**

## Requirements for Building

- Python 3.7+
- PyInstaller (installed automatically by build script)
- mutagen (installed automatically by build script)

## Manual Build

If you prefer to build manually:

```bash
# Install PyInstaller
pip3 install --user pyinstaller

# Build using the spec file
pyinstaller AIFF_Me_Please.spec --clean --noconfirm
```

## Distribution

After building, you'll find:
- `dist/AIFF Me Please.app` - The standalone application

You can:
1. **Test it**: Double-click to run
2. **Install it**: Drag to Applications folder
3. **Share it**: Send the .app file to your friend

## Note

The built app is self-contained. Your friend doesn't need:
- Python installed
- mutagen installed
- Any dependencies

Just double-click and run!


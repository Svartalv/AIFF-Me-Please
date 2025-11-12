# Fix for macOS Version Error

If you're getting this error:
```
macOS 14 (1407) or later required, have instead 14 (1406) !
zsh: abort      python3 run.py
```

## Quick Fix

**Uninstall Pillow** (it's only needed for the icon, app works fine without it):

```bash
pip3 uninstall Pillow
```

Then run the app:
```bash
python3 run.py
```

## Why This Happens

Pillow (PIL) version 11.3.0+ requires macOS 14.7+, but you have macOS 14.6. The app doesn't actually need Pillow - it's only used to display the cat icon. All core functionality (converting files) works perfectly without it.

## Alternative: Install Older Pillow

If you really want the icon, try installing an older Pillow version:

```bash
pip3 uninstall Pillow
pip3 install --user "Pillow<11.0"
```

Then try running the app again.

## Verify It Works

After uninstalling Pillow, the app should start normally. You'll see the GUI, but the icon won't appear in the title bar. Everything else works perfectly!


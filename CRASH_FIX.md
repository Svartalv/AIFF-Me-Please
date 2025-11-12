# Fixing App Crashes on macOS

If the app crashes immediately when you try to open it, follow these steps:

## Step 1: Run Diagnostic

```bash
python3 diagnose_crash.py
```

This will tell you exactly where the crash is happening.

## Step 2: Nuclear Cleanup

If dependencies are the problem:

```bash
./nuke_dependencies.sh
```

This removes ALL potentially problematic packages and reinstalls only what's needed.

## Step 3: Common Crash Causes

### Tkinter Issues

If the crash happens during Tkinter initialization:

```bash
# Install Tkinter support (if missing)
brew install python-tk
```

Or try running from Terminal instead of double-clicking:
```bash
cd "/path/to/AIFF Me Please"
python3 run.py
```

### Python Version Issues

Check your Python version:
```bash
python3 --version
```

If it's too old (< 3.7), install a newer version:
```bash
brew install python@3.9
```

### Missing Dependencies

```bash
# Remove problematic packages
pip3 uninstall -y Pillow

# Install compatible version
pip3 install --user 'mutagen==1.45.1' --no-deps --no-build-isolation
```

### macOS Security/Permissions

If macOS blocks the app:
1. Go to System Settings → Privacy & Security
2. Allow the app to run
3. Or run from Terminal (bypasses some security checks)

## Step 4: Check Crash Report

If you see a crash report, look for:
- **"Library not loaded"** → Missing system library
- **"Symbol not found"** → Python version mismatch
- **"Abort trap"** → Usually dependency issue

## Still Not Working?

1. Run: `python3 diagnose_crash.py` and share the output
2. Check: `pip3 list | grep -E 'Pillow|mutagen'`
3. Try: `python3 test_minimal.py`
4. Check Python: `which python3` and `python3 --version`


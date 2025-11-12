#!/usr/bin/env python3
"""Minimal test to see what's causing the crash."""

import sys
print("Python version:", sys.version)
print("Python path:", sys.executable)
print()

# Test basic imports
print("Testing basic imports...")
try:
    import tkinter as tk
    print("✓ tkinter works")
except Exception as e:
    print(f"✗ tkinter failed: {e}")
    sys.exit(1)

try:
    from pathlib import Path
    print("✓ pathlib works")
except Exception as e:
    print(f"✗ pathlib failed: {e}")
    sys.exit(1)

try:
    import threading
    print("✓ threading works")
except Exception as e:
    print(f"✗ threading failed: {e}")
    sys.exit(1)

try:
    import subprocess
    print("✓ subprocess works")
except Exception as e:
    print(f"✗ subprocess failed: {e}")
    sys.exit(1)

# Test mutagen
print("\nTesting mutagen...")
try:
    import mutagen
    version = getattr(mutagen, '__version__', 'unknown')
    print(f"✓ mutagen works (version: {version})")
except Exception as e:
    print(f"✗ mutagen failed: {e}")
    print("\nTo fix: pip3 install --user 'mutagen==1.45.1' --no-deps --no-build-isolation")
    sys.exit(1)

try:
    from mutagen.flac import FLAC
    print("✓ mutagen.flac works")
except Exception as e:
    print(f"✗ mutagen.flac failed: {e}")

try:
    from mutagen.mp3 import MP3
    print("✓ mutagen.mp3 works")
except Exception as e:
    print(f"✗ mutagen.mp3 failed: {e}")

# Test creating a simple window
print("\nTesting Tkinter window creation...")
try:
    root = tk.Tk()
    root.withdraw()  # Hide it immediately
    print("✓ Tkinter window created successfully")
    root.destroy()
except Exception as e:
    print(f"✗ Tkinter window creation failed: {e}")
    sys.exit(1)

print("\n✅ All basic tests passed!")
print("The crash might be in the app code itself.")
print("Try running: python3 run.py")


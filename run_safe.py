#!/usr/bin/env python3
"""Safe entry point with better error handling."""
import sys
import os
import traceback
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

print("Starting AIFF Me Please...")
print(f"Python: {sys.version}")
print(f"Python path: {sys.executable}")
print()

# Test imports one by one
print("Testing imports...")
try:
    import tkinter as tk
    print("✓ tkinter")
except Exception as e:
    print(f"✗ tkinter failed: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    from tkinter import ttk, filedialog, messagebox
    print("✓ tkinter submodules")
except Exception as e:
    print(f"✗ tkinter submodules failed: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    import mutagen
    print("✓ mutagen")
except Exception as e:
    print(f"✗ mutagen failed: {e}")
    print("\nFix: pip3 install --user 'mutagen==1.45.1' --no-deps --no-build-isolation")
    traceback.print_exc()
    sys.exit(1)

try:
    from mutagen.flac import FLAC
    from mutagen.mp3 import MP3
    print("✓ mutagen submodules")
except Exception as e:
    print(f"✗ mutagen submodules failed: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\nAll imports successful. Starting app...")
print()

try:
    from app.gui import main
    print("✓ Imported app.gui.main")
    print("Creating GUI...")
    main()
except KeyboardInterrupt:
    print("\n\nInterrupted by user")
    sys.exit(0)
except SystemExit as e:
    if e.code != 0:
        print(f"\n\nSystemExit with code {e.code}")
        traceback.print_exc()
    sys.exit(e.code if e.code else 0)
except Exception as e:
    print(f"\n\nFATAL ERROR: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
    print("\n" + "="*60)
    print("TROUBLESHOOTING:")
    print("="*60)
    print("1. Run: ./nuke_dependencies.sh")
    print("2. Or manually: pip3 uninstall -y Pillow && pip3 install --user 'mutagen==1.45.1' --no-deps --no-build-isolation")
    print("3. Check Python version: python3 --version (needs 3.7+)")
    print("4. Try: python3 test_minimal.py")
    sys.exit(1)


#!/usr/bin/env python3
"""Diagnostic script to find what's causing the crash."""
import sys
import os
import traceback

print("="*60)
print("AIFF Me Please - Crash Diagnostic")
print("="*60)
print()
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Platform: {sys.platform}")
print()

# Test 1: Basic imports
print("TEST 1: Basic Python imports")
print("-" * 60)
try:
    import os
    import sys
    import re
    import threading
    import subprocess
    from pathlib import Path
    print("✓ All basic imports successful")
except Exception as e:
    print(f"✗ FAILED: {e}")
    traceback.print_exc()
    sys.exit(1)

# Test 2: Tkinter
print("\nTEST 2: Tkinter import")
print("-" * 60)
try:
    import tkinter as tk
    print("✓ tkinter imported")
except Exception as e:
    print(f"✗ FAILED: {e}")
    traceback.print_exc()
    sys.exit(1)

# Test 3: Tkinter submodules
print("\nTEST 3: Tkinter submodules")
print("-" * 60)
try:
    from tkinter import ttk, filedialog, messagebox
    print("✓ tkinter submodules imported")
except Exception as e:
    print(f"✗ FAILED: {e}")
    traceback.print_exc()
    sys.exit(1)

# Test 4: Create root window (this is often where crashes happen)
print("\nTEST 4: Create Tkinter root window")
print("-" * 60)
try:
    root = tk.Tk()
    print("✓ Root window created")
    root.withdraw()  # Hide it
    print("✓ Root window hidden")
    root.destroy()
    print("✓ Root window destroyed")
except Exception as e:
    print(f"✗ FAILED: {e}")
    traceback.print_exc()
    print("\n⚠️  CRASH LIKELY HAPPENS HERE - Tkinter initialization issue")
    sys.exit(1)

# Test 5: Mutagen
print("\nTEST 5: Mutagen import")
print("-" * 60)
try:
    import mutagen
    print("✓ mutagen imported")
except Exception as e:
    print(f"✗ FAILED: {e}")
    traceback.print_exc()
    print("\n⚠️  Install: pip3 install --user 'mutagen==1.45.1' --no-deps --no-build-isolation")
    sys.exit(1)

# Test 6: Mutagen submodules
print("\nTEST 6: Mutagen submodules")
print("-" * 60)
try:
    from mutagen.flac import FLAC
    from mutagen.mp3 import MP3
    print("✓ mutagen submodules imported")
except Exception as e:
    print(f"✗ FAILED: {e}")
    traceback.print_exc()
    sys.exit(1)

# Test 7: Import app module
print("\nTEST 7: Import app.gui")
print("-" * 60)
try:
    from pathlib import Path
    project_root = Path(__file__).parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    from app import gui
    print("✓ app.gui imported")
except Exception as e:
    print(f"✗ FAILED: {e}")
    traceback.print_exc()
    sys.exit(1)

# Test 8: Create app instance (this might crash)
print("\nTEST 8: Create app instance")
print("-" * 60)
try:
    root = tk.Tk()
    root.withdraw()  # Hide immediately
    
    app = gui.FLAC2AIFFApp(root)
    print("✓ App instance created")
    
    root.destroy()
    print("✓ App destroyed")
except Exception as e:
    print(f"✗ FAILED: {e}")
    traceback.print_exc()
    print("\n⚠️  CRASH LIKELY HAPPENS HERE - App initialization issue")
    sys.exit(1)

print("\n" + "="*60)
print("✅ ALL TESTS PASSED - App should work!")
print("="*60)
print("\nIf the app still crashes, the issue might be:")
print("1. System-level Tkinter issue (try: brew install python-tk)")
print("2. Display server issue (try running from Terminal, not double-click)")
print("3. macOS security/permissions issue")
print()


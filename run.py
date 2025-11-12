#!/usr/bin/env python3
"""Development entry point for running the app directly."""
import sys
import os
import traceback
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Pillow is not used - removed to prevent macOS compatibility issues

# Set environment variables to prevent crashes
os.environ['TK_SILENCE_DEPRECATION'] = '1'

try:
    # Test basic imports first
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox
    
    # Test mutagen
    try:
        import mutagen
        from mutagen.flac import FLAC
        from mutagen.mp3 import MP3
    except ImportError as e:
        print(f"\n❌ Error: mutagen not installed")
        print(f"   {e}")
        print("\nFix: pip3 install --user 'mutagen==1.45.1' --no-deps --no-build-isolation")
        print("Or run: ./setup.sh")
        sys.exit(1)
    
    # Now import and run the app
    from app.gui import main
    
    if __name__ == "__main__":
        main()
        
except KeyboardInterrupt:
    print("\n\nInterrupted by user")
    sys.exit(0)
except SystemExit as e:
    # Handle system exit gracefully
    if e.code != 0:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Run diagnostic: python3 diagnose_crash.py")
        print("2. Run fix: ./nuke_dependencies.sh")
        print("3. Check: pip3 list | grep -E 'Pillow|mutagen'")
    sys.exit(e.code if e.code else 0)
except Exception as e:
    print(f"\n❌ FATAL ERROR: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
    print("\n" + "="*60)
    print("TROUBLESHOOTING:")
    print("="*60)
    print("1. Run diagnostic: python3 diagnose_crash.py")
    print("2. Run nuclear fix: ./nuke_dependencies.sh")
    print("3. Check dependencies: pip3 list | grep -E 'Pillow|mutagen'")
    print("4. If Tkinter issue: brew install python-tk")
    print("5. Try running from Terminal (not double-click)")
    sys.exit(1)

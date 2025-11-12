#!/usr/bin/env python3
"""Development entry point for running the app directly."""
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Pillow is not used - removed to prevent macOS compatibility issues

try:
    from app.gui import main
    
    if __name__ == "__main__":
        main()
except SystemExit as e:
    # Handle system exit gracefully
    if e.code != 0:
        print(f"\nError: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure mutagen is installed: pip3 install --user mutagen")
        print("2. If you get macOS version errors, uninstall Pillow:")
        print("   pip3 uninstall Pillow")
        print("   (The app works fine without Pillow - you just won't see the icon)")
    sys.exit(e.code)
except Exception as e:
    print(f"\nError starting application: {e}")
    print("\nTroubleshooting:")
    print("1. Install required dependency: pip3 install --user mutagen")
    print("2. If you see macOS version errors, uninstall Pillow:")
    print("   pip3 uninstall Pillow")
    print("3. Then run: python3 run.py")
    sys.exit(1)

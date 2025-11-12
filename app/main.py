"""Main entry point for AIFF Me Please application."""
import sys
import os
from pathlib import Path

# Prevent Pillow from causing system abort on older macOS versions
os.environ.setdefault('PILLOW_DISABLE_VERSION_CHECK', '1')

# Add parent directory to path if running as script
if __name__ == "__main__":
    parent_dir = Path(__file__).parent.parent
    if str(parent_dir) not in sys.path:
        sys.path.insert(0, str(parent_dir))

try:
    from app.gui import main
    
    if __name__ == "__main__":
        main()
except SystemExit as e:
    if e.code != 0:
        print(f"\nError: {e}")
        print("\nTroubleshooting:")
        print("1. Install mutagen: pip3 install --user mutagen")
        print("2. If macOS version error, uninstall Pillow: pip3 uninstall Pillow")
    sys.exit(e.code)
except Exception as e:
    print(f"\nError: {e}")
    print("\nTroubleshooting:")
    print("1. Install mutagen: pip3 install --user mutagen")
    print("2. Uninstall Pillow if you get macOS version errors: pip3 uninstall Pillow")
    sys.exit(1)

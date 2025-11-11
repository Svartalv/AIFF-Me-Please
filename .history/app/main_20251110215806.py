"""Main entry point for FLAC2AIFF application."""
import sys
from pathlib import Path

# Add parent directory to path if running as script
if __name__ == "__main__":
    parent_dir = Path(__file__).parent.parent
    if str(parent_dir) not in sys.path:
        sys.path.insert(0, str(parent_dir))

from app.gui import main

if __name__ == "__main__":
    main()


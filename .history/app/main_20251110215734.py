"""Main entry point for FLAC2AIFF application."""
import sys
from pathlib import Path

# Add app directory to path if running as script
if __name__ == "__main__":
    app_dir = Path(__file__).parent
    if str(app_dir) not in sys.path:
        sys.path.insert(0, str(app_dir))

from app.gui import main

if __name__ == "__main__":
    main()


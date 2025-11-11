#!/usr/bin/env python3
"""Development entry point for running the app directly."""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from app.gui import main

if __name__ == "__main__":
    main()

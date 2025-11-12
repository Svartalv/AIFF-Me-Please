#!/bin/bash
# Double-clickable installer for AIFF Me Please
# This file can be double-clicked in Finder to run the installer

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Make sure setup.sh is executable
chmod +x "$DIR/setup.sh" 2>/dev/null

# Open Terminal and run setup
osascript <<EOF
tell application "Terminal"
    activate
    do script "cd '$DIR' && ./setup.sh && echo '' && echo '✅ Installation complete! Press any key to exit...' && read -n 1"
end tell
EOF


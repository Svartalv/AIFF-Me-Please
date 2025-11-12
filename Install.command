#!/bin/bash
# Double-clickable installer for AIFF Me Please
# This file can be double-clicked in Finder to run the installer

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Open Terminal and run setup
osascript -e "tell application \"Terminal\" to do script \"cd '$DIR' && ./setup.sh && echo '' && echo 'Press any key to exit...' && read -n 1\""


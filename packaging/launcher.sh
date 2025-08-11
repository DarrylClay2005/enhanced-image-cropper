#!/bin/bash

# Enhanced Image Cropper Launcher Script
# This script handles the application startup with proper environment setup

APPDIR="$(dirname "$(readlink -f "$0")")"
PYTHON_EXECUTABLE="$APPDIR/usr/bin/python3"
APP_SCRIPT="$APPDIR/usr/bin/enhanced_main.py"

# Set up environment variables
export PYTHONPATH="$APPDIR/usr/lib/python3.12/site-packages:$PYTHONPATH"
export LD_LIBRARY_PATH="$APPDIR/usr/lib:$LD_LIBRARY_PATH"
export QT_PLUGIN_PATH="$APPDIR/usr/lib/qt5/plugins:$QT_PLUGIN_PATH"

# Fallback to system Python if bundled Python not found
if [ ! -f "$PYTHON_EXECUTABLE" ]; then
    PYTHON_EXECUTABLE="python3"
fi

# Fallback to relative path if absolute path not found
if [ ! -f "$APP_SCRIPT" ]; then
    APP_SCRIPT="$APPDIR/enhanced_main.py"
fi

# Launch the application
exec "$PYTHON_EXECUTABLE" "$APP_SCRIPT" "$@"

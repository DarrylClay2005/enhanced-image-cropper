#!/bin/bash

set -e

APP_NAME="Enhanced-Image-Cropper-Kowalski"
APP_VERSION="1.0.3.C"
APP_DIR="Enhanced-Image-Cropper.AppDir"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "🚀 Building AppImage for Enhanced Image Cropper v$APP_VERSION - Kowalski Edition"

# Clean previous build
rm -rf "$PROJECT_DIR/dist/$APP_DIR"
mkdir -p "$PROJECT_DIR/dist/$APP_DIR"

cd "$PROJECT_DIR/dist"

# Create AppDir structure
mkdir -p "$APP_DIR/usr/"{bin,lib,share/{applications,icons/hicolor/scalable/apps}}

# Install Python and dependencies in virtual environment
echo "📦 Setting up Python environment..."
python3 -m venv "$APP_DIR/usr"
source "$APP_DIR/usr/bin/activate"

# Install dependencies
pip install --upgrade pip
pip install -r "$PROJECT_DIR/requirements.txt"

# Copy application files
echo "📁 Copying application files..."
cp "$PROJECT_DIR/enhanced_main.py" "$APP_DIR/usr/bin/"
cp "$PROJECT_DIR/packaging/launcher.sh" "$APP_DIR/AppRun"
chmod +x "$APP_DIR/AppRun"

# Copy desktop entry and icon
cp "$PROJECT_DIR/enhanced-image-cropper.desktop" "$APP_DIR/"
cp "$PROJECT_DIR/enhanced-image-cropper.desktop" "$APP_DIR/usr/share/applications/"
# Copy Kowalski icon
cp "$PROJECT_DIR/icons/app_icon.png" "$APP_DIR/usr/share/icons/hicolor/scalable/apps/enhanced-image-cropper.png" 2>/dev/null || echo "Warning: Icon not found"
cp "$PROJECT_DIR/icons/app_icon.png" "$APP_DIR/enhanced-image-cropper.png" 2>/dev/null || echo "Warning: Icon not found"

# Create symlinks for AppImage (PNG icon instead of SVG)
ln -sf "enhanced-image-cropper.png" "$APP_DIR/.DirIcon"

# Download AppImage tools if not present
if [ ! -f "appimagetool-x86_64.AppImage" ]; then
    echo "⬇️ Downloading AppImage tools..."
    wget -q "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
    chmod +x appimagetool-x86_64.AppImage
fi

# Build AppImage
echo "🔨 Building AppImage..."
ARCH=x86_64 ./appimagetool-x86_64.AppImage "$APP_DIR" "Enhanced-Image-Cropper-$APP_VERSION-x86_64.AppImage"

if [ -f "Enhanced-Image-Cropper-$APP_VERSION-x86_64.AppImage" ]; then
    echo "✅ AppImage created successfully: Enhanced-Image-Cropper-$APP_VERSION-x86_64.AppImage"
    ls -lh "Enhanced-Image-Cropper-$APP_VERSION-x86_64.AppImage"
else
    echo "❌ AppImage build failed"
    exit 1
fi

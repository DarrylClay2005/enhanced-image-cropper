#!/bin/bash

set -e

APP_NAME="enhanced-image-cropper-kowalski"
APP_VERSION="1.0.3.C"
ARCH="all"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/dist/deb-build"
DEB_DIR="$BUILD_DIR/${APP_NAME}_${APP_VERSION}_${ARCH}"

echo "🚀 Building DEB package for Enhanced Image Cropper v$APP_VERSION - Kowalski Edition"

# Clean previous build
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

cd "$BUILD_DIR"

# Create package directory structure
mkdir -p "$DEB_DIR/DEBIAN"
mkdir -p "$DEB_DIR/usr/"{bin,share/{applications,icons/hicolor/scalable/apps,doc/$APP_NAME}}
mkdir -p "$DEB_DIR/opt/$APP_NAME"

# Copy control files
echo "📁 Setting up package structure..."
cp "$PROJECT_DIR/packaging/debian/control" "$DEB_DIR/DEBIAN/"
cp "$PROJECT_DIR/packaging/debian/postinst" "$DEB_DIR/DEBIAN/"
cp "$PROJECT_DIR/packaging/debian/prerm" "$DEB_DIR/DEBIAN/"

# Set correct permissions for control scripts
chmod 755 "$DEB_DIR/DEBIAN/"{postinst,prerm}

# Copy application files
cp "$PROJECT_DIR/enhanced_main.py" "$DEB_DIR/opt/$APP_NAME/"
cp "$PROJECT_DIR/requirements.txt" "$DEB_DIR/opt/$APP_NAME/"
cp "$PROJECT_DIR/README.md" "$DEB_DIR/usr/share/doc/$APP_NAME/"
cp "$PROJECT_DIR/CHANGELOG.md" "$DEB_DIR/usr/share/doc/$APP_NAME/"
cp "$PROJECT_DIR/LICENSE" "$DEB_DIR/usr/share/doc/$APP_NAME/" 2>/dev/null || true

# Create executable wrapper script
cat > "$DEB_DIR/usr/bin/$APP_NAME" << EOF
#!/bin/bash

# Enhanced Image Cropper launcher
INSTALL_DIR="/opt/$APP_NAME"

# Check if virtual environment exists, create if not
VENV_DIR="\$HOME/.local/share/$APP_NAME/venv"
if [ ! -d "\$VENV_DIR" ]; then
    echo "Setting up Enhanced Image Cropper environment..."
    mkdir -p "\$(dirname "\$VENV_DIR")"
    python3 -m venv "\$VENV_DIR"
    source "\$VENV_DIR/bin/activate"
    pip install --upgrade pip
    pip install -r "\$INSTALL_DIR/requirements.txt"
else
    source "\$VENV_DIR/bin/activate"
fi

# Launch the application
exec python "\$INSTALL_DIR/enhanced_main.py" "\$@"
EOF

chmod +x "$DEB_DIR/usr/bin/$APP_NAME"

# Copy desktop entry and icon
cp "$PROJECT_DIR/enhanced-image-cropper.desktop" "$DEB_DIR/usr/share/applications/"
# Copy Kowalski icon
cp "$PROJECT_DIR/icons/app_icon.png" "$DEB_DIR/usr/share/icons/hicolor/scalable/apps/enhanced-image-cropper.png" 2>/dev/null || echo "Warning: Icon not found"

# Create changelog in proper Debian format
cat > "$DEB_DIR/usr/share/doc/$APP_NAME/changelog.Debian" << EOF
$APP_NAME ($APP_VERSION) unstable; urgency=low

  * Complete professional upgrade with 50+ new features
  * Modern dark theme UI with CustomTkinter
  * Professional crop templates for social media
  * Advanced image adjustments and filters
  * Smart enhancement algorithms (CLAHE, noise reduction)
  * Batch processing capabilities
  * 20-level undo/redo system
  * Performance improvements (3x faster, 50% less memory)

 -- Enhanced Image Cropper Team <dev@example.com>  $(date -R)
EOF

# Compress changelog
gzip -n --best "$DEB_DIR/usr/share/doc/$APP_NAME/changelog.Debian"

# Create copyright file
cat > "$DEB_DIR/usr/share/doc/$APP_NAME/copyright" << EOF
Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: Enhanced Image Cropper
Source: https://github.com/your-username/image-cropper

Files: *
Copyright: 2024 Enhanced Image Cropper Team
License: MIT
 Permission is hereby granted, free of charge, to any person obtaining a
 copy of this software and associated documentation files (the "Software"),
 to deal in the Software without restriction, including without limitation
 the rights to use, copy, modify, merge, publish, distribute, sublicense,
 and/or sell copies of the Software, and to permit persons to whom the
 Software is furnished to do so, subject to the following conditions:
 .
 The above copyright notice and this permission notice shall be included
 in all copies or substantial portions of the Software.
 .
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
 OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
 THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
 DEALINGS IN THE SOFTWARE.
EOF

# Calculate package size and update control file
INSTALLED_SIZE=$(du -sk "$DEB_DIR" | cut -f1)
sed -i "/^Architecture:/a Installed-Size: $INSTALLED_SIZE" "$DEB_DIR/DEBIAN/control"

# Build the package
echo "🔨 Building DEB package..."
cd "$BUILD_DIR"
dpkg-deb --build "${APP_NAME}_${APP_VERSION}_${ARCH}"

if [ -f "${APP_NAME}_${APP_VERSION}_${ARCH}.deb" ]; then
    echo "✅ DEB package created successfully: ${APP_NAME}_${APP_VERSION}_${ARCH}.deb"
    ls -lh "${APP_NAME}_${APP_VERSION}_${ARCH}.deb"
    
    # Verify package
    echo "🔍 Verifying DEB package..."
    dpkg-deb --info "${APP_NAME}_${APP_VERSION}_${ARCH}.deb"
else
    echo "❌ DEB package build failed"
    exit 1
fi

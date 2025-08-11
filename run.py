#!/usr/bin/env python3
"""
Launch script for Enhanced Image Cropper v1.0.3.C - Kowalski Edition
This script handles environment setup and launches the application
"""

import sys
import os
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    return True

def check_virtual_environment():
    """Check if running in virtual environment"""
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def launch_application():
    """Launch the Enhanced Image Cropper application"""
    print("🚀 Launching Enhanced Image Cropper v1.0.3.C - Kowalski Edition...")
    try:
        import enhanced_main
        if hasattr(enhanced_main, 'print_info'):
            enhanced_main.print_info()
        
        app = enhanced_main.EnhancedImageCropper()
        app.run()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Try installing dependencies: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Application error: {e}")
        return False
    
    return True

def main():
    """Main entry point"""
    print("="*60)
    print("🖼️  Enhanced Image Cropper v1.0.3.C - Kowalski Edition")
    print("   Professional Photo Editing Suite")
    print("="*60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check if in virtual environment
    if not check_virtual_environment():
        print("⚠️  Warning: Not running in virtual environment")
        print("💡 Recommended: python -m venv venv && source venv/bin/activate")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            sys.exit(0)
    
    # Check if dependencies are installed
    try:
        import customtkinter
        import cv2
        import numpy
        from PIL import Image
    except ImportError:
        print("📦 Dependencies not found. Installing...")
        if not install_dependencies():
            sys.exit(1)
    
    # Launch application
    if not launch_application():
        sys.exit(1)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Setup script for Enhanced Image Cropper v1.0.2
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="enhanced-image-cropper-kowalski",
    version="1.0.3.C",
    author="Enhanced Image Cropper Team",
    author_email="dev@example.com",
    description="A comprehensive photo editing application with modern features, professional-grade tools, and Kowalski Edition enhancements",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/image-cropper",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Multimedia :: Graphics :: Editors",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "enhanced-image-cropper=enhanced_main:main",
        ],
    },
    keywords="image cropper photo editor gui tkinter opencv pillow",
    project_urls={
        "Bug Reports": "https://github.com/your-username/image-cropper/issues",
        "Source": "https://github.com/your-username/image-cropper",
        "Documentation": "https://github.com/your-username/image-cropper#readme",
    },
)

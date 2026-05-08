#!/bin/bash

# Build script for cross-compiling bmsg to Windows executable using Nuitka

set -e

echo "Setting up Windows cross-compilation environment..."

# Install mingw-w64 for Windows cross-compilation
if ! command -v x86_64-w64-mingw32-gcc &> /dev/null; then
    echo "Installing mingw-w64 for Windows cross-compilation..."
    if command -v pacman &> /dev/null; then
        sudo pacman -S mingw-w64-gcc
    elif command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install mingw-w64
    else
        echo "Please install mingw-w64 manually for your distribution"
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating Nuitka virtual environment..."
source ./nuitka_env/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create output directory
mkdir -p dist

# Run Nuitka with Windows cross-compilation flags
echo "Starting Windows cross-compilation..."
python -m nuitka \
    --standalone \
    --onefile \
    --windows-disable-console \
    --windows-icon-from-ico=bkd.png \
    --include-data-files=bkd.png=bkd.png \
    --include-data-files=jingle.wav=jingle.wav \
    --include-data-files=config.ini=config.ini \
    --include-data-dir=languages=languages \
    --include-data-dir="nuitka_env/lib/python3.14/site-packages/ttkthemes/themes=ttkthemes/themes" \
    --include-data-dir="nuitka_env/lib/python3.14/site-packages/ttkthemes/gif=ttkthemes/gif" \
    --include-data-dir="nuitka_env/lib/python3.14/site-packages/ttkthemes/png=ttkthemes/png" \
    --include-data-dir="nuitka_env/lib/python3.14/site-packages/ttkthemes/advanced=ttkthemes/advanced" \
    --include-module=tkinter \
    --include-module=ttkthemes \
    --include-module=playsound3 \
    --include-module=rsa \
    --output-filename=bmsg.exe \
    --mingw64 \
    gui.py

echo "Build completed!"
echo "Windows executable should be available as bmsg.exe"

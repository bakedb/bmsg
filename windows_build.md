# Windows Cross-Compilation Instructions for bmsg

## Prerequisites

Before you can cross-compile bmsg for Windows, you need to install the following:

### System Packages:
1. **MinGW-w64 toolchain** (for Windows cross-compilation)
2. **patchelf** (required for Nuitka standalone mode on Linux)

### On Arch Linux / Manjaro:
```bash
sudo pacman -S mingw-w64-gcc mingw-w64-binutils mingw-w64-crt mingw-w64-headers mingw-w64-winpthreads patchelf
```

### On Ubuntu / Debian:
```bash
sudo apt-get update
sudo apt-get install mingw-w64 patchelf
```

### On Fedora:
```bash
sudo dnf install mingw64-gcc mingw64-binutils mingw64-crt mingw64-headers mingw64-winpthreads patchelf
```

## Build Process

### Option 1: Using the Shell Script (Recommended)
```bash
./build_windows.sh
```

### Option 2: Using the Python Script
```bash
python3 build_windows.py
```

### Option 3: Manual Nuitka Command
```bash
# Activate the virtual environment first
source ./nuitka_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Nuitka
python -m nuitka \
    --standalone \
    --onefile \
    --windows-disable-console \
    --windows-icon-from-ico=bkd.png \
    --include-data-files=bkd.png=bkd.png \
    --include-data-files=jingle.wav=jingle.wav \
    --include-data-files=config.ini=config.ini \
    --include-data-files="languages/English (US).json=languages/English (US).json" \
    --include-data-files="languages/Engwish (owo).json=languages/Engwish (owo).json" \
    --include-module=tkinter \
    --include-module=ttkthemes \
    --include-module=playsound3 \
    --include-module=rsa \
    --output-filename=bmsg.exe \
    --mingw64 \
    gui.py
```
add any other files that might be missing.

## What Gets Included

The build process includes:
- Main GUI application (`gui.py`)
- Startup script (`startup.py`)
- Cryptography module (`crypt.py`)
- All dependencies from `requirements.txt` (rsa, playsound3, ttkthemes)
- Asset files:
  - `bkd.png` (application icon)
  - `jingle.wav` (startup sound)
  - `config.ini` (default configuration)
  - Language files in `languages/` directory

## Output

After successful compilation, you'll get:
- `bmsg.exe` - A standalone Windows executable
- The executable will not show a console window (`--windows-disable-console`)
- All dependencies are bundled, so no separate installation is needed on Windows

## Troubleshooting

### Disk Space Issues
If you encounter "not enough free disk space" errors during MinGW installation:
- Free up disk space on your system partition
- Consider using a different partition with more space
- The MinGW toolchain requires several hundred MB of space

### Missing Dependencies
If Nuitka complains about missing modules:
- Ensure all requirements are installed: `pip install -r requirements.txt`
- Check that the virtual environment is activated
- Verify MinGW-w64 is properly installed and in PATH

### Permission Issues
If you get permission errors:
- Make sure the build scripts are executable: `chmod +x build_windows.sh build_windows.py`
- Use `sudo` only for installing system packages (MinGW), not for the build process

## Testing on Windows

To test the compiled executable:
1. Copy `bmsg.exe` to a Windows machine
2. Run it directly - no installation required
3. The application should start with the startup animation and then show the main GUI

## Notes

- The cross-compilation process can take several minutes
- The resulting executable may be larger than expected due to bundled dependencies
- Audio playback (`playsound3`) may require additional Windows components on some systems

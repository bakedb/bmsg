#!/usr/bin/env python3
"""
Build script for cross-compiling bmsg to Windows executable using Nuitka
"""

import os
import sys
import subprocess
import shutil

def run_command(cmd, cwd=None):
    """Run a command and return the result"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print(result.stdout)
    return True

def main():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Install dependencies first
    print("Installing dependencies...")
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", cwd=script_dir):
        print("Failed to install dependencies")
        return 1
    
    # Nuitka command for Windows cross-compilation
    nuitka_cmd = f"""
    {sys.executable} -m nuitka \\
    --standalone \\
    --onefile \\
    --windows-disable-console \\
    --windows-icon-from-ico=bkd.png \\
    --include-data-files=bkd.png=bkd.png \\
    --include-data-files=jingle.wav=jingle.wav \\
    --include-data-files=config.ini=config.ini \\
    --include-data-dir=languages=languages \\
    --include-module=tkinter \\
    --include-module=ttkthemes \\
    --include-module=playsound3 \\
    --include-module=rsa \\
    --output-filename=bmsg.exe \\
    --mingw64 \\
    gui.py
    """
    
    print("Starting Windows cross-compilation with Nuitka...")
    if not run_command(nuitka_cmd, cwd=script_dir):
        print("Failed to compile with Nuitka")
        return 1
    
    print("Build completed successfully!")
    print(f"Windows executable should be in: {os.path.join(script_dir, 'bmsg.exe')}")
    return 0

if __name__ == "__main__":
    sys.exit(main())

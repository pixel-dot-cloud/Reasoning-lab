import PyInstaller.__main__
import sys
import os

separator = ";" if sys.platform == "win32" else ":"

args = [
    "main.py",
    "--name=ReasoningLab",
    "--windowed",
    "--noconfirm",
]

if sys.platform == "win32":
    args.append("--onedir")   # required for PySide6 DLL resolution on Windows
else:
    args.append("--onefile")  # single binary on Linux/macOS

PyInstaller.__main__.run(args)

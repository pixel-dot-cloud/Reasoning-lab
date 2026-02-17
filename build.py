import PyInstaller.__main__
import sys
import os

separator = ";" if sys.platform == "win32" else ":"

PyInstaller.__main__.run([
    "main.py",
    "--name=ReasoningLab",
    "--onefile",
    "--windowed",
    f"--add-data=assets{separator}assets",
    "--noconfirm",
])

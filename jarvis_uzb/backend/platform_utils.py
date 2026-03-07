import os
import subprocess
import sys

def open_path(path: str):
    """Operatsion tizimga mos ravishda fayl yoki havolani ochadi."""
    if sys.platform == 'win32':
        os.startfile(path)
    elif sys.platform == 'darwin':
        subprocess.call(['open', path])
    else:
        # Linux uchun
        subprocess.call(['xdg-open', path])
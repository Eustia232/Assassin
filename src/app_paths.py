import os
import sys
from pathlib import Path


def get_app_dir() -> Path:
    appimage = os.environ.get("APPIMAGE")
    if appimage:
        return Path(appimage).parent
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).parent.parent


def get_data_dir() -> Path:
    return get_app_dir()

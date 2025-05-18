import os
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parents[2] / "config" / "rules.json"

# CONFIG_PATH = "../config/rules.json"
FOLDER_TO_WATCH = os.path.expanduser("~/Downloads")

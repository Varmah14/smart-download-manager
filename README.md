# Smart Download Folder Manager

A Python-based file automation tool that monitors your Downloads folder (or any directory) and automatically organizes files based on configurable rules — similar to macOS's Hazel, but open-source and scriptable.

---

## Features

- Real-time folder monitoring using `watchdog`
- Auto-move files based on extension, filename, or content
- Rule-based actions: move, delete, rename
- Auto-create destination directories if they don't exist
- Logs all actions to both console and `logs.txt`
- Optional support for reading file content before sorting (coming soon)

---

## Installation

```bash
cd smart-download-manager
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

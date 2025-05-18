import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
from pathlib import Path
import json
from util.util import CONFIG_PATH, FOLDER_TO_WATCH


def load_rules():
    if not os.path.exists(CONFIG_PATH):
        print(f"No config file found at {CONFIG_PATH}. Exiting.")
        exit(1)
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)


def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)

def apply_rules(file_path, rules):
    filename = os.path.basename(file_path)

    for rule in rules:
        match = rule.get("match", {})
        extension = match.get("extension")
        name_contains = match.get("name_contains")

        # Check extension match
        ext_ok = True if not extension else filename.endswith(extension)

        # Check name_contains match
        name_ok = True if not name_contains else name_contains in filename

        if ext_ok and name_ok:
            action = rule.get("action", "move")

            if action == "move":
                dest = os.path.expanduser(rule.get("destination", "~/Downloads/Sorted"))  # default fallback
                ensure_dir(dest)
                shutil.move(file_path, os.path.join(dest, filename))
                print(f"Moved {filename} to {dest}")
            elif action == "delete":
                os.remove(file_path)
                print(f"Deleted {filename}")
            else:
                print(f"Unknown action: {action}")
            break  # stop after first matching rule


class DownloadHandler(FileSystemEventHandler):
    def __init__(self, rules):
        self.rules = rules

    def on_created(self, event):
        if event.is_directory:
            return
        if wait_until_stable(event.src_path):
            apply_rules(event.src_path, self.rules)
        else:
            print(f"File {event.src_path} did not stabilize in time.")
        # time.sleep(1)  # wait for file to be fully written


def wait_until_stable(file_path, wait_time=1.5, check_interval=0.5, max_retries=20):
    """Wait until file is fully written by checking size stability."""
    previous_size = -1
    stable_count = 0

    for _ in range(max_retries):
        try:
            current_size = os.path.getsize(file_path)
        except FileNotFoundError:
            current_size = -1

        if current_size == previous_size:
            stable_count += 1
            if stable_count * check_interval >= wait_time:
                return True
        else:
            stable_count = 0
            previous_size = current_size

        time.sleep(check_interval)

    return False  # Timed out waiting for file to stabilize


def start_watcher():
    rules = load_rules()
    event_handler = DownloadHandler(rules)
    observer = Observer()
    observer.schedule(event_handler,FOLDER_TO_WATCH , recursive = True)
    observer.start()
    print("started Watching folder",FOLDER_TO_WATCH)
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    start_watcher()
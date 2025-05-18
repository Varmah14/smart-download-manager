import logging
import time
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
from pathlib import Path
import json
from util.util import CONFIG_PATH, FOLDER_TO_WATCH
from logger_setup import setup_logger


def load_rules():
    if not os.path.exists(CONFIG_PATH):
        logging.error(f"No config file found at {CONFIG_PATH}. Exiting.")
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
                logging.info(f"Moved {filename} to {dest}")
            elif action == "delete":
                os.remove(file_path)
                logging.info(f"Deleted {filename}")
            else:
                logging.error(f"Unknown action: {action}")
            break  # stop after first matching rule

class DownloadHandler(FileSystemEventHandler):
    def __init__(self, rules):
        self.rules = rules
        self.recently_handled = {}

    def on_created(self, event):
        if event.is_directory:
            return

        path = event.src_path

        # Skip recently handled files (e.g., in last 3 seconds)
        now = time.time()
        if path in self.recently_handled and now - self.recently_handled[path] < 3:
            return

        if wait_until_stable(path):
            apply_rules(path, self.rules)
            self.recently_handled[path] = now
        else:
            logging.warning(f"File {path} did not stabilize in time.")



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
    observer.schedule(event_handler, FOLDER_TO_WATCH, recursive=True)
    observer.start()
    logging.info("Started watching folder:%s", FOLDER_TO_WATCH)

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        logging.info("\nINFO - Keyboard interrupt received. Stopping watcher...")
        observer.stop()
    except Exception as e:
        logging.error(f"ERROR - Unexpected error: {e}\n\n")
        observer.stop()
    finally:
        observer.join()
        logging.info("INFO - Watcher exited cleanly.\n")



if __name__ == "__main__":
    setup_logger()
    start_watcher()

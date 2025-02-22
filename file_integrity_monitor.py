import os
import json
import hashlib
import time
import threading
import tkinter as tk
from tkinter import messagebox, filedialog
from plyer import notification
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

BASELINE_FILE = "baseline.json"

# Load or create a baseline file
def load_baseline():
    """Load the baseline JSON file and check for corruption."""
    try:
        with open(BASELINE_FILE, "r") as f:
            return json.load(f)  # Attempt to parse JSON
    except json.JSONDecodeError:
        print("[ERROR] Baseline file is corrupted! Recreating it...")
        return {}  # Start fresh if JSON is invalid
    except FileNotFoundError:
        return {}  # Start fresh if file is missing

# Save baseline data
def save_baseline(baseline):
    """Save baseline data to JSON."""
    with open(BASELINE_FILE, "w") as f:
        json.dump(baseline, f, indent=4)

# Calculate file hash (with retry logic for permission issues)
def calculate_file_hash(file_path, retries=3, delay=1):
    """Calculate SHA-256 hash of a file, retrying if permission is denied."""
    hasher = hashlib.sha256()
    for attempt in range(retries):
        try:
            with open(file_path, "rb") as f:
                while chunk := f.read(4096):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except PermissionError:
            print(f"[WARNING] Permission denied: {file_path} (Attempt {attempt + 1}/{retries})")
            time.sleep(delay)  # Wait and retry
        except Exception as e:
            print(f"[ERROR] Could not hash {file_path}: {e}")
            return None
    print(f"[ERROR] Skipping file due to repeated permission issues: {file_path}")
    return None  # Skip file after max retries

# Notify user with pop-ups
def notify_user(event_type, file_path):
    """Display user-friendly notifications."""
    messages = {
        "modified": f"⚠️ File Modified:\n{file_path}",
        "new_file": f"📂 New File Added:\n{file_path}",
        "deleted": f"❌ File Deleted:\n{file_path}"
    }
    notification.notify(
        title="File Integrity Alert",
        message=messages.get(event_type, "Unknown Change"),
        timeout=5  # Show for 5 seconds
    )

# Class for monitoring file changes
class FileMonitorHandler(FileSystemEventHandler):
    def __init__(self, baseline):
        self.baseline = baseline

    def on_modified(self, event):
        if event.is_directory:
            return
        file_hash = calculate_file_hash(event.src_path)
        if file_hash and self.baseline.get(event.src_path) != file_hash:
            print(f"[MODIFIED] {event.src_path}")
            notify_user("modified", event.src_path)
            self.baseline[event.src_path] = file_hash
            save_baseline(self.baseline)

    def on_created(self, event):
        if event.is_directory:
            return
        file_hash = calculate_file_hash(event.src_path)
        if file_hash:
            print(f"[NEW FILE] {event.src_path}")
            notify_user("new_file", event.src_path)
            self.baseline[event.src_path] = file_hash
            save_baseline(self.baseline)

    def on_deleted(self, event):
        if event.is_directory:
            return
        if event.src_path in self.baseline:
            print(f"[DELETED] {event.src_path}")
            notify_user("deleted", event.src_path)
            del self.baseline[event.src_path]
            save_baseline(self.baseline)

# GUI for user choices
def get_user_choice():
    """Ask user if they want to create a new baseline or use an existing one."""
    root = tk.Tk()
    root.withdraw()  # Hide main window
    return messagebox.askyesno("File Integrity Monitor", "Do you want to create a new baseline?")

def select_directory():
    """Ask the user to choose a directory via GUI."""
    root = tk.Tk()
    root.withdraw()  # Hide main window
    return filedialog.askdirectory(title="Select Directory to Monitor")

# Function to create a new baseline
def create_new_baseline(directory):
    """Create a new baseline for the specified directory."""
    baseline = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = calculate_file_hash(file_path)
            if file_hash:
                baseline[file_path] = file_hash
    save_baseline(baseline)
    print(f"[INFO] New baseline created for {directory}")
    return baseline

# Start monitoring
def start_monitoring(directory, baseline):
    """Start real-time monitoring of the directory."""
    print(f"[INFO] Monitoring started for {directory}...")
    event_handler = FileMonitorHandler(baseline)
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Main function
def main():
    """Main script execution."""
    while True:  # Keep asking until user makes a valid choice or exits
        user_wants_new_baseline = get_user_choice()
        
        if user_wants_new_baseline is None:  # User closed the dialog
            print("[INFO] User closed the prompt. Exiting...")
            return
        
        monitored_directory = select_directory()
        
        if not monitored_directory:  
            exit_choice = messagebox.askyesno("Exit", "No directory selected. Do you want to exit?")
            if exit_choice:
                print("[INFO] User chose to exit.")
                return  # Exit the script
            continue  # Reprompt user to select a directory
        
        if user_wants_new_baseline:
            baseline = create_new_baseline(monitored_directory)
        else:
            baseline = load_baseline()
            if not baseline:
                messagebox.showwarning("Warning", "No existing baseline found. Creating a new one...")
                baseline = create_new_baseline(monitored_directory)

        # Start monitoring after user makes a valid choice
        start_monitoring(monitored_directory, baseline)
        break  # Exit loop after monitoring starts

# Run script
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[ERROR] Unexpected issue: {e}")

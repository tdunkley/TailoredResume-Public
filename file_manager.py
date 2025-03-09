import os
import sys
import shutil
import zipfile
from datetime import datetime

# Dynamically add the project root to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))  # Move up two levels
sys.path.append(project_root)

from modules.utils.path_manager import PATHS, add_project_to_sys_path

# ✅ Ensure correct paths are loaded
add_project_to_sys_path()

# ✅ Ensure directory exists
def ensure_directory_exists(directory):
    """Creates the directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)

# ✅ Move file to a target directory
def move_file(source_path, destination_dir):
    """
    Moves a file to the specified directory.
    """
    ensure_directory_exists(destination_dir)
    destination_path = os.path.join(destination_dir, os.path.basename(source_path))
    shutil.move(source_path, destination_path)
    return destination_path

# ✅ Extract zip files and rename specific CSV
def extract_and_rename_csv(zip_path, extract_to=None, target_prefix="USER_JOBS_USER_FULL_DATA_DOWNLOAD", renamed_file="huntr_export.csv"):
    """
    Extracts a zip file, finds the CSV file that starts with the target_prefix,
    renames it to 'huntr_export.csv', and moves it to the appropriate directory.
    """
    if extract_to is None:
        extract_to = PATHS["downloads"]
    
    ensure_directory_exists(extract_to)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

    # Identify and rename the correct CSV file
    for file in os.listdir(extract_to):
        if file.startswith(target_prefix) and file.endswith(".csv"):
            original_path = os.path.join(extract_to, file)
            renamed_path = os.path.join(extract_to, renamed_file)
            os.rename(original_path, renamed_path)
            return renamed_path

    raise FileNotFoundError(f"No file matching '{target_prefix}*.csv' found in extracted contents.")

# ✅ Cleanup old downloads
def cleanup_downloads(directory, keep_recent=3):
    """
    Deletes old files in the download directory, keeping only the most recent ones.
    """
    ensure_directory_exists(directory)
    
    files = sorted(
        [os.path.join(directory, f) for f in os.listdir(directory)],
        key=os.path.getmtime,
        reverse=True
    )

    for old_file in files[keep_recent:]:
        os.remove(old_file)


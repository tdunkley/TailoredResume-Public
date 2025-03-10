import os
import sys

# ✅ Dynamically add the project root to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))  # Move up two levels
sys.path.append(project_root)

# ✅ Import modules correctly
from modules.utils.path_manager import PATHS
from datetime import datetime

def enforce_naming_convention(file_path):
    """
    Ensures the Huntr CSV file follows the correct naming convention.
    """
    directory, filename = os.path.split(file_path)

    if filename.startswith("USER_JOBS_USER_FULL_DATA_DOWNLOAD"):
        new_name = "huntr_export.csv"
        new_path = os.path.join(directory, new_name)
        os.rename(file_path, new_path)
        return new_path
    return file_path

def validate_file(file_path):
    """
    Validates that the Huntr CSV file is not empty.
    """
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        print(f"❌ File {file_path} is missing or empty.")
        return False
    return True

def cleanup_temp_files():
    """
    Deletes unnecessary files from the Huntr download folder.
    """
    download_folder = PATHS.get("huntr_downloads", "./downloads")
    
    for file in os.listdir(download_folder):
        if file.endswith(".zip") or file.startswith("USER_JOBS"):
            os.remove(os.path.join(download_folder, file))
            print(f"🧹 Removed {file}")

    print("✅ Cleanup complete.")

import os
import json
import hashlib
import subprocess
from datetime import datetime

# Configuration
TRACKED_DIR = os.path.abspath("tracked_files")  # Ensure correct path
FILE_INDEX = os.path.join(TRACKED_DIR, "file_index.json")
LFS_EXTENSIONS = {".pdf", ".json", ".csv", ".zip"}  # Track large file types in Git LFS
AUTO_PUSH = True  # Set to False to disable auto-commit & push

def get_file_hash(file_path):
    """Generate SHA-256 checksum for file integrity tracking"""
    hasher = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        print(f"Error hashing {file_path}: {e}")
        return None

def scan_files():
    """Scan directory and return metadata for each file"""
    file_data = {}
    for root, _, files in os.walk(TRACKED_DIR):
        for file in files:
            if file == "file_index.json":  # Skip the index file itself
                continue

            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, TRACKED_DIR)
            size = os.path.getsize(file_path)
            modified_time = datetime.utcfromtimestamp(os.path.getmtime(file_path)).isoformat()
            sha256_hash = get_file_hash(file_path)

            file_data[relative_path] = {
                "file_name": file,
                "relative_path": relative_path,
                "size_kb": round(size / 1024, 2),
                "last_modified": modified_time,
                "sha256": sha256_hash,
                "github_url": f"YOUR_GITHUB_REPO_URL/blob/main/tracked_files/{relative_path}"
            }
    return file_data

def update_file_index():
    """Update file_index.json with scanned data"""
    existing_data = {}

    if os.path.exists(FILE_INDEX):
        with open(FILE_INDEX, "r", encoding="utf-8") as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                print("Warning: file_index.json is corrupted, recreating...")

    new_data = scan_files()
    
    # Detect deleted files
    deleted_files = set(existing_data.keys()) - set(new_data.keys())
    if deleted_files:
        print(f"Deleted files detected: {deleted_files}")

    # Write updated JSON
    with open(FILE_INDEX, "w", encoding="utf-8") as f:
        json.dump(new_data, f, indent=4)

    return deleted_files

def setup_git_lfs():
    """Ensure Git LFS is set up and tracking large files"""
    subprocess.run(["git", "lfs", "install"], check=True)
    subprocess.run(["git", "lfs", "track"] + [f"*{ext}" for ext in LFS_EXTENSIONS], check=True)

def commit_and_push():
    """Commit and push changes to GitHub"""
    subprocess.run(["git", "add", "tracked_files"], check=True)
    subprocess.run(["git", "commit", "-m", "Auto-update file_index.json"], check=True)
    subprocess.run(["git", "push"], check=True)

if __name__ == "__main__":
    print("🔍 Scanning tracked_files directory...")
    deleted_files = update_file_index()

    print("📌 Ensuring Git LFS is tracking large files...")
    setup_git_lfs()

    if AUTO_PUSH:
        print("🚀 Committing and pushing updates to GitHub...")
        commit_and_push()

    print("✅ Done! file_index.json updated.")

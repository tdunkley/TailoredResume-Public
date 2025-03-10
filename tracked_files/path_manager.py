import os
import sys
import json

# ✅ Dynamically determine the project root (TailoredResume folder)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))  # Move up three levels

# ✅ Load config.json for dynamic paths
config_path = os.path.join(project_root, "config", "config.json")

# ✅ Default paths dictionary
PATHS = {
    "project_root": project_root,
    "src_dir": os.path.join(project_root, "src"),
    "modules_dir": os.path.join(project_root, "src", "modules"),
    "scripts_dir": os.path.join(project_root, "src", "modules", "processing"),
    "data_dir": os.path.join(project_root, "data"),
    "config_dir": os.path.join(project_root, "config"),
    "logs_dir": os.path.join(project_root, "logs"),
    "output_dir": os.path.join(project_root, "output"),
    "audit_dir": os.path.join(project_root, "data", "audit_logs"),  # ✅ Add this line
    "huntr_downloads": os.path.join(project_root, "downloads", "huntr_downloads"),  # Added this line
    "huntr_extracted": os.path.join(project_root, "data", "huntr_extracted"),  # Added this line

    # ✅ File paths
    "config_file": config_path,
    ##"resume_file": os.path.join(project_root, "data", "resume_tdunkley.json"),
    "resume_file": os.path.join(project_root, "data", "full_cv.docx"),
    "resume_pdf": os.path.join(project_root, "data", "full_cv.pdf"),
    "job_description_file": os.path.join(project_root, "data", "huntr_job_descriptions.json"),
    "huntr_csv": os.path.join(project_root, "data", "huntr_export.csv"),
    "full_cv": os.path.join(project_root, "data", "full_cv.docx"),
    "extracted_text": os.path.join(project_root, "data", "extracted_text.txt"),
    "validation_log": os.path.join(project_root, "logs", "validation_log.txt"),
    "best_practices_config": os.path.join(project_root, "data", "best_practices_config.json"),

    # ✅ Staging and JSON paths
    "staging_json": os.path.join(project_root, "data", "staging.json"),
    "structured_json": os.path.join(project_root, "data", "structured.json"),
    "resume_output_json": os.path.join(project_root, "data", "resume_output_json"),
    "schema_file": os.path.join(project_root, "data", "resume_schema.json"),  # ✅ Fixed for correct filename

    # ✅ OCR and Image paths
    "temp_pdf": os.path.join(project_root, "data", "resume_image_output", "temp.pdf"),
    "image_output": os.path.join(project_root, "data", "resume_image_output"),
    "ocr_extracted_text": os.path.join(project_root, "data", "ocr_extracted_text"),

    # ✅ Audit paths
    "audit_logs": "c:/BlackNisus/Initiatives/TailoredResume/data/audit_logs"  # ✅ Add this line

}

# ✅ Scripts mapping for modular execution
PATHS["scripts"] = {
    "extract_raw_text": os.path.join(PATHS["modules_dir"], "extraction", "extract_raw_text.py"),
    "preprocess_resume": os.path.join(PATHS["modules_dir"], "extraction", "preprocess_resume.py"),
    "convert_docx_to_image": os.path.join(PATHS["modules_dir"], "extraction", "convert_docx_to_image.py"),
    "validate_resume_with_ocr": os.path.join(PATHS["modules_dir"], "extraction", "validate_resume_with_ocr.py"),
    "compare_extracted_texts": os.path.join(PATHS["modules_dir"], "validation", "compare_extracted_texts.py"),
}

# ✅ Load additional scripts dynamically from config.json
try:
    with open(config_path, "r", encoding="utf-8") as file:
        config_data = json.load(file)
        PATHS.update(config_data.get("scripts", {}))  # ✅ Merge `scripts` into PATHS
except FileNotFoundError:
    print("⚠️ Warning: config.json not found. Using default paths.")
except json.JSONDecodeError:
    print("❌ Error: config.json is not properly formatted.")

# ✅ Ensure all required directories exist
for key, path in PATHS.items():
    if key.endswith("_dir") and not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

# ✅ Function to add project paths dynamically to sys.path
def add_project_to_sys_path():
    """Ensure essential directories are in `sys.path` dynamically."""
    for path in [PATHS["project_root"], PATHS["src_dir"], PATHS["modules_dir"], PATHS["scripts_dir"]]:
        if path not in sys.path:
            sys.path.append(path)

# ✅ Print paths for debugging
if __name__ == "__main__":
    add_project_to_sys_path()
    print("✅ Project paths configured successfully:")
    for key, value in PATHS.items():
        print(f"{key}: {value}")

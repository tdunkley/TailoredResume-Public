import sys
import os
import json
import datetime

# ✅ Dynamically add the project root to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))  # Move up two levels
sys.path.append(project_root)

# ✅ Import Required Modules
from modules.utils.path_manager import PATHS
from datetime import datetime

# ✅ Function to Load Best Practices Config
def load_best_practices_config():
    """Load best practices configuration from JSON file."""
    config_path = PATHS.get("best_practices_config", None)  # Ensure this key exists
    if config_path and os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

BEST_PRACTICES_CONFIG = load_best_practices_config()

# ✅ Apply Best Practices Based on Processing Phase
def apply_best_practices(data, phase):
    """Apply best practices dynamically based on the phase of the process."""
    print(f"[INFO] Applying best practices for {phase}...")

    if phase == "File Management":
        process_huntr_downloads()  # ✅ Ensure Huntr Data is Processed First
    elif phase == "Phase 1":
        data = enforce_crisp_dm(data)
        data = validate_extraction(data)
    elif phase == "Phase 2":
        data = enforce_validation_standards(data)
        data = standardize_sections(data)
    elif phase == "Phase 3":
        data = optimize_for_ats(data)
        data = inject_industry_trends(data)
    elif phase == "Tailoring":
        data = enhance_job_alignment(data)
    elif phase == "Rendering":
        data = optimize_resume_data(data)

    log_best_practice_usage(phase, "Best practices applied successfully")
    return data

# ✅ Logging Function
def log_best_practice_usage(phase, details):
    """Log best practice applications for tracking and analysis."""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "phase": phase,
        "details": details
    }
    print(f"[LOG] Best Practice Applied: {log_entry}")

# ✅ Import Specific Functions from Best Practices Modules
from modules.best_practices.crisp_dm_rules import enforce_crisp_dm
from modules.best_practices.ats_optimization import optimize_for_ats
from modules.best_practices.efficiency_tuning import optimize_resume_data
from modules.best_practices.validation_standards import enforce_validation_standards
from modules.best_practices.industry_trends import inject_industry_trends
from modules.best_practices.file_management import process_huntr_downloads  # ✅ File Management Integration
from modules.validation.validation_engine import validate_extraction
from modules.formatting.formatting_engine import standardize_sections
from modules.tailoring.resume_tailoring import enhance_job_alignment

# ✅ MAIN EXECUTION
if __name__ == "__main__":
    # Ensure Huntr File Processing is Handled First
    apply_best_practices({}, "File Management")

    sample_data = {"Experience": "Software Engineer", "Skills": ["Python", "SQL"]}
    processed_data = apply_best_practices(sample_data, "Phase 3")

    print("Final Processed Data:", processed_data)

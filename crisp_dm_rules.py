import sys
import os
import json
import re


# Dynamically add the project root to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))  # Move up two levels
sys.path.append(project_root)

# Now, you can safely import modules
from modules.utils.path_manager import PATHS


"""
crisp_dm_rules.py
Ensures the process follows CRISP-DM methodology for structured workflows.
"""

def enforce_crisp_dm(data):
    """Ensure CRISP-DM methodology is followed for structured workflows."""
    steps = [
        "Business Understanding",
        "Data Understanding",
        "Data Preparation",
        "Modeling",
        "Evaluation",
        "Deployment"
    ]
    
    current_stage = data.get("workflow_stage", "Unknown Stage")
    
    if current_stage not in steps:
        print(f"⚠️ [CRISP-DM] Invalid stage detected: {current_stage}. Defaulting to 'Business Understanding'.")
        current_stage = "Business Understanding"
    
    print(f"✅ [CRISP-DM] Processing in '{current_stage}' phase.")
    data["workflow_stage"] = current_stage
    return data


if __name__ == "__main__":
    sample_data = {"workflow_stage": "Data Preparation"}
    processed_data = enforce_crisp_dm(sample_data)
    print("Validated Workflow Stage:", processed_data)


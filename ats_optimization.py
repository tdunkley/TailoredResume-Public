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
ats_optimization.py
Implements ATS compliance checks for resume structuring and tailoring.
"""

import re

# ATS Optimization Rules
def optimize_for_ats(data):
    """Ensure the resume meets ATS compliance standards."""
    ats_rules = {
        "keyword_density": 3,  # Minimum required occurrences per key skill
        "max_bullet_points": 5,
        "required_sections": ["Work Experience", "Education", "Skills"]
    }
    
    # Ensure required sections exist
    for section in ats_rules["required_sections"]:
        if section not in data:
            data[section] = "[MISSING]"
    
    # Validate bullet points
    for section in ["Work Experience", "Education"]:
        if isinstance(data.get(section, []), list) and len(data[section]) > ats_rules["max_bullet_points"]:
            data[section] = data[section][:ats_rules["max_bullet_points"]]
    
    print("[ATS Optimization] Resume adjusted for ATS compliance.")
    return data

if __name__ == "__main__":
    sample_data = {
        "Work Experience": ["Managed a team", "Developed a web app", "Optimized SQL queries", "Led Agile meetings", "Implemented CI/CD", "Extra bullet"],
        "Education": ["BSc in Computer Science"],
        "Skills": ["Python", "SQL"]
    }
    processed_data = optimize_for_ats(sample_data)
    print("ATS Optimized Data:", processed_data)

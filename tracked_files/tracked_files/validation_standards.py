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
validation_standards.py
Enforces data integrity rules, flagging missing or inconsistent entries.
"""

def enforce_validation_standards(data):
    """Enforce structural integrity and flag missing or inconsistent data."""
    required_fields = ["Work Experience", "Education", "Skills", "Certifications"]
    flagged_issues = []
    
    for field in required_fields:
        if field not in data or not data[field]:
            flagged_issues.append(f"Missing required field: {field}")
    
    if "Experience" in data and len(data["Experience"]) < 2:
        flagged_issues.append("Experience section should have at least 2 entries.")
    
    if flagged_issues:
        data["validation_warnings"] = flagged_issues
        print("[Validation] Issues detected:", flagged_issues)
    else:
        print("[Validation] All required fields are present.")
    
    return data


def validate_extraction(sections):
    """
    Validates and corrects extracted resume sections.
    Ensures data is placed correctly and logs missing fields.
    """
    validation_errors = []
    
    # Ensure sections are not empty
    for section, content in sections.items():
        if not content.strip():
            validation_errors.append(f"Missing content in section: {section}")

    # Fix misplaced data (e.g., Summary appearing in Work Experience)
    if "Work Experience" in sections and "Summary" in sections:
        if len(sections["Summary"]) < 50:  # Assuming Summary is short, not long
            sections["Summary"] = sections["Work Experience"].split("\n")[0]  # Take the first line
            sections["Work Experience"] = "\n".join(sections["Work Experience"].split("\n")[1:])
            validation_errors.append("Summary was found inside Work Experience and was extracted properly.")

    return sections, validation_errors


if __name__ == "__main__":
    sample_data = {"Experience": ["Software Engineer"], "Skills": ["Python", "SQL"]}
    processed_data = enforce_validation_standards(sample_data)
    print("Validated Data:", processed_data)

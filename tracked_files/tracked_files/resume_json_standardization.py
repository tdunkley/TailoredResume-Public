import json
import re
from modules.utils.path_manager import PATHS

SCHEMA_PATH = PATHS["resume_schema"]
NEW_SECTIONS_LOG = PATHS["new_sections_json"]

# Define best practice standard resume sections
STANDARD_SECTIONS = {
    "Header": ["Contact Information", "Name", "Phone", "Email", "LinkedIn"],
    "Summary": ["Professional Summary", "Career Summary", "Profile"],
    "Experience": ["Work Experience", "Employment", "Work History", "Job"],
    "Education": ["Degrees", "Certifications", "Academic Background"],
    "Skills": ["Technical Skills", "Soft Skills", "Expertise"],
    "Projects": ["Selected Projects", "Key Projects"],
    "Key Achievements": ["Accomplishments", "Awards", "Recognition"],
    "Strengths": ["Strengths", "Competencies"],
}

def load_schema():
    """ Load the existing schema or return an empty template if missing. """
    try:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"title": "Resume Schema", "type": "object", "properties": {}}

def save_schema(schema):
    """ Save the updated schema back to the file. """
    with open(SCHEMA_PATH, "w", encoding="utf-8") as file:
        json.dump(schema, file, indent=4)

def standardize_sections(resume_json):
    """ Aligns resume sections to best practices and updates the schema dynamically. """
    schema = load_schema()
    standardized_resume = {}
    new_sections = {}

    for section, content in resume_json.items():
        found_match = None

        # Try to match existing standard sections
        for standard, variants in STANDARD_SECTIONS.items():
            if section.lower() in [v.lower() for v in variants] or re.search(r"\b" + section + r"\b", " ".join(variants), re.IGNORECASE):
                found_match = standard
                break

        if found_match:
            # Assign the correct section name
            standardized_resume.setdefault(found_match, []).append(content)
        else:
            # Log the new section for review
            new_sections[section] = content

    # Save newly discovered sections for later review
    if new_sections:
        with open(NEW_SECTIONS_LOG, "w", encoding="utf-8") as file:
            json.dump(new_sections, file, indent=4)
        print("🔍 New sections detected and logged for review.")

    return standardized_resume

def validate_resume_json(resume_json):
    """ Ensures the resume follows best practices before saving. """
    required_sections = ["Header", "Summary", "Experience", "Education"]
    missing_sections = [sec for sec in required_sections if sec not in resume_json]

    if missing_sections:
        print(f"⚠️ Warning: Missing critical resume sections: {', '.join(missing_sections)}")

    return resume_json

def process_resume_json(resume_json):
    """ Standardizes, validates, and ensures best practices in resume JSON. """
    standardized_json = standardize_sections(resume_json)
    validated_json = validate_resume_json(standardized_json)
    return validated_json

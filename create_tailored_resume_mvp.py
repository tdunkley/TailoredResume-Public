import sys
import os
from jira_manager import create_jira_epic, create_jira_story, create_jira_task, create_jira_subtask

# ✅ Dynamically set the path to ensure imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# ✅ Define Epic Details
epic_title = "Tailored Resume MVP"
epic_description = (
    "This Epic focuses on developing the minimum viable product (MVP) "
    "for an AI-driven tailored resume system that automates job description analysis "
    "and custom resume formatting."
)

# ✅ Create the Epic
epic_key = create_jira_epic(epic_title, epic_description)
if not epic_key:
    print("❌ Epic creation failed. Exiting script.")
    sys.exit(1)

print(f"✅ Created Epic: {epic_key}")

# ✅ Define Stories and Associated Tasks
stories = [
    {
        "title": "Resume Formatting Fixes",
        "description": (
            "Ensure ATS-friendly formatting.\n"
            "Why: ATS systems may reject resumes with incorrect formatting.\n"
            "Projected Outcome: Resumes that pass ATS screening more efficiently."
        ),
        "tasks": [
            {"title": "Standardize bullet points", "description": "Ensure bullet points are uniform."},
            {"title": "Adjust margins", "description": "Fix margin inconsistencies for better readability."},
            {"title": "Fix font inconsistencies", "description": "Ensure font consistency across resumes."},
        ]
    },
    {
        "title": "Resume Hygiene Module",
        "description": (
            "Standardize text & clean data.\n"
            "Why: Consistency improves readability and ATS compliance.\n"
            "Projected Outcome: Cleaner, more standardized resumes."
        ),
        "tasks": [
            {"title": "Remove duplicate words", "description": "Ensure words are not repeated unnecessarily."},
            {"title": "Normalize phone & email formats", "description": "Standardize contact information formatting."},
        ]
    },
    {
        "title": "Resume Validation Module",
        "description": (
            "Implement AI-driven validation.\n"
            "Why: Ensures experience & skills alignment.\n"
            "Projected Outcome: Resumes that accurately match job descriptions."
        ),
        "tasks": [
            {"title": "Ensure experience & skills alignment", "description": "Check that job experience matches required skills."},
            {"title": "Detect inconsistencies", "description": "Find gaps or mismatches in resume details."},
        ]
    },
    {
        "title": "Automated Job Parsing",
        "description": (
            "Extract relevant job description details.\n"
            "Why: AI-driven job parsing saves time and ensures accurate keyword extraction.\n"
            "Projected Outcome: A structured dataset of parsed job descriptions."
        ),
        "tasks": [
            {"title": "Develop job parser", "description": "Build logic to extract job title, skills, and requirements."},
            {"title": "Validate parsing accuracy", "description": "Test and refine parsing model against sample data."},
        ]
    },
    {
        "title": "Resume Rendering Engine",
        "description": (
            "Generate .docx & PDF resumes dynamically.\n"
            "Why: Job seekers need multiple formats for various ATS systems.\n"
            "Projected Outcome: A rendering engine that outputs properly formatted resumes."
        ),
        "tasks": [
            {"title": "Implement styling rules", "description": "Define style templates for consistent output."},
            {"title": "Test rendering pipeline", "description": "Ensure resume outputs meet formatting standards."},
        ]
    },
    {
        "title": "Schedule Job Processing",
        "description": (
            "Automate tailored resume creation.\n"
            "Why: Automated job processing ensures timely resume updates.\n"
            "Projected Outcome: A scheduler that triggers resume updates based on job postings."
        ),
        "tasks": [
            {"title": "Implement job queue", "description": "Develop queue system for processing resumes in batches."},
            {"title": "Test batch processing", "description": "Ensure system processes large volumes efficiently."},
        ]
    },
    {
        "title": "CI/CD for Resume Generation",
        "description": (
            "Automate deployment pipeline.\n"
            "Why: Continuous Integration ensures rapid updates and minimal downtime.\n"
            "Projected Outcome: A fully automated deployment pipeline."
        ),
        "tasks": [
            {"title": "Set up GitHub Actions", "description": "Configure CI/CD for automated builds."},
            {"title": "Implement automated testing", "description": "Ensure end-to-end test coverage."},
        ]
    },
    {
        "title": "Marketplace Strategy",
        "description": (
            "Define pricing, user onboarding, sales strategy.\n"
            "Why: A clear strategy is needed for user acquisition and revenue generation.\n"
            "Projected Outcome: A documented strategy and marketing collateral."
        ),
        "tasks": [
            {"title": "Conduct competitor analysis", "description": "Research pricing and features of competing platforms."},
            {"title": "Create marketing collateral", "description": "Develop sales decks and promotional material."},
        ]
    }
]

# ✅ Create Stories and Store Their Jira Keys
story_keys = {}

for story in stories:
    story_key = create_jira_story(story["title"], story["description"], epic_key)  # ✅ Story under Epic
    if not story_key:
        print(f"❌ Failed to create Story: {story['title']}")
        continue

    print(f"✅ Created Story: {story_key}")
    story_keys[story["title"]] = story_key  # Store Story Key for later Task linking

# ✅ Create Tasks under Each Story
for story_title, story_key in story_keys.items():
    story_data = next(s for s in stories if s["title"] == story_title)
    
    for task in story_data["tasks"]:
        task_description = task["description"]
        task_title = task["title"]

        # 🚀 Create Tasks as Subtasks under the Story
        task_key = create_jira_subtask(task_title, task_description, story_key)  

        if not task_key:
            print(f"❌ Failed to create Task: {task_title}")
        else:
            print(f"✅ Created Task under Story {story_key}: {task_key}")

print("🚀 Tailored Resume MVP Jira import completed successfully!")

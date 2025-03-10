import sys
import os
import json
import re
import datetime
import requests

# Dynamically add the project root to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))  # Move up two levels
sys.path.append(project_root)

# Now, you can safely import modules
from modules.utils.path_manager import PATHS

# Load industry trends from external sources or stored datasets
def fetch_industry_trends():
    """Fetches latest industry trends from an API or a stored dataset."""
    try:
        # Example: Fetching from a placeholder API (Replace with actual API endpoint)
        response = requests.get("https://api.example.com/job-trends")
        if response.status_code == 200:
            return response.json()
        else:
            print("Warning: Unable to fetch live industry trends. Using fallback data.")
    except Exception as e:
        print(f"Error fetching industry trends: {e}")
    
    # Fallback industry trends (if API fails)
    return {
        "Data Science": ["Machine Learning", "AI Ethics", "MLOps"],
        "Software Engineering": ["Cloud Computing", "Microservices", "DevOps"],
        "Cybersecurity": ["Zero Trust", "Identity Management", "Threat Intelligence"],
    }

# Inject relevant industry trends into the resume

def inject_industry_trends(data):
    """
    Injects real-time industry job trends into the resume.
    Uses an external API or mock data for now.
    """
    # TEMP FIX: Mock industry trends instead of calling the API
    industry_trends_mock = {
        "General": ["Python", "Machine Learning", "Cloud Computing"],
        "Data Science": ["SQL", "Deep Learning", "Big Data"]
    }

    industry = data.get("industry", "General")
    if not isinstance(industry, dict):  # Ensure it's not a string
        industry = industry_trends_mock.get(industry, industry_trends_mock["General"])


    data["industry_trends"] = industry
    return data

# Example usage
if __name__ == "__main__":
    sample_resume = {"Skills": [{"industry": "Data Science", "skills": ["Python", "SQL"]}]}
    enhanced_resume = inject_industry_trends(sample_resume)
    print(json.dumps(enhanced_resume, indent=4))
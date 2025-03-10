import os
import sys
import json
import requests

# Get the absolute path of the project root dynamically
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))

# Ensure the project root is in sys.path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Ensure src directory is in sys.path
src_dir = os.path.join(project_root, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Debugging: Print sys.path to check paths
print("✅ Updated sys.path:", sys.path)

# Import modules using absolute paths relative to 'src'
from modules.utils.path_manager import PATHS
from modules.security.jira_secrets import get_secret

# Retrieve Jira credentials from AWS Secrets Manager
secret_name = "BN-Jira-Credentials"
region_name = "us-east-2"

jira_secrets = get_secret(secret_name, region_name)
if not jira_secrets:
    raise ValueError("❌ Failed to retrieve Jira secrets from AWS.")

JIRA_EMAIL = jira_secrets["JIRA_USER_EMAIL"]
JIRA_API_TOKEN = jira_secrets["JIRA_API_TOKEN"]
JIRA_PROJECT_KEY = jira_secrets["JIRA_PROJECT_KEY"]
JIRA_BASE_URL = jira_secrets["JIRA_BASE_URL"]

JIRA_AUTH = (JIRA_EMAIL, JIRA_API_TOKEN)
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

# JQL Query to Find Test Issues
JQL_QUERY = f'project = "{JIRA_PROJECT_KEY}" AND (summary ~ "Test" OR description ~ "Test")'

def get_test_issues():
    """Fetches all test issues from Jira."""
    search_url = f"{JIRA_BASE_URL}/rest/api/3/search"
    params = {"jql": JQL_QUERY, "maxResults": 50}
    
    response = requests.get(search_url, headers=HEADERS, auth=JIRA_AUTH, params=params)
    
    if response.status_code == 200:
        issues = response.json().get("issues", [])
        return issues
    else:
        print(f"❌ Failed to fetch test issues: {response.json()}")
        return []

def delete_jira_issue(issue_key):
    """Deletes a Jira issue by its key."""
    delete_url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}"
    
    response = requests.delete(delete_url, headers=HEADERS, auth=JIRA_AUTH)
    
    if response.status_code == 204:
        print(f"✅ Deleted issue: {issue_key}")
    else:
        print(f"❌ Failed to delete {issue_key}: {response.json()}")

if __name__ == "__main__":
    print("\n🚀 Fetching Test Issues for Deletion...\n")
    test_issues = get_test_issues()

    if not test_issues:
        print("✅ No test issues found. Nothing to delete!")
    else:
        for issue in test_issues:
            issue_key = issue["key"]
            delete_jira_issue(issue_key)

        print("\n✅ All test issues deleted successfully!\n")

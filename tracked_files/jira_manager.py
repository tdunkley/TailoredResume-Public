import os
import sys
import json
import requests

# ----------------------------------------------
# 🚀 Section 1: Imports & Configuration
# ----------------------------------------------

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

# Import modules using absolute paths relative to 'src'
from modules.utils.path_manager import PATHS
from modules.security.jira_secrets import get_secret
from modules.security.security_manager import SECURITY_MANAGER  # ✅ Use centralized security

# Retrieve Jira credentials from AWS Secrets Manager
secret_name = "BN-Jira-Credentials"
region_name = "us-east-2"

jira_secrets = get_secret(secret_name, region_name)

if not jira_secrets:
    raise ValueError("❌ Failed to retrieve Jira secrets from AWS.")

# Extract Jira credentials
JIRA_EMAIL = jira_secrets.get("JIRA_USER_EMAIL")
JIRA_API_TOKEN = jira_secrets.get("JIRA_API_TOKEN")
JIRA_PROJECT_KEY = jira_secrets.get("JIRA_PROJECT_KEY")
JIRA_BASE_URL = jira_secrets.get("JIRA_BASE_URL")

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

JIRA_AUTH = (JIRA_EMAIL, JIRA_API_TOKEN)

# ----------------------------------------------
# 🚀 Section 2: Issue Creation Functions
# ----------------------------------------------
def create_jira_issue(issue_type_id, title, description, fields=None):
    """Creates a Jira issue with validated fields."""
    issue_data = {
        "fields": {
            "project": {"key": JIRA_PROJECT_KEY},  # ✅ Ensuring correct project key
            "summary": title,
            "description": description,
            "issuetype": {"id": issue_type_id},  # ✅ Using ID to avoid name mismatch
            "customfield_10036": 1  # ✅ Default Story Points (modify as needed)
        }
    }

    if fields:
        issue_data["fields"].update(fields)  # ✅ Merge any additional fields

    response = requests.post(f"{JIRA_BASE_URL}/rest/api/3/issue", headers=HEADERS, auth=JIRA_AUTH, json=issue_data)

    if response.status_code == 201:
        issue_key = response.json().get("key")
        print(f"✅ Created Issue {issue_type_id}: {title} ({issue_key})")
        return issue_key
    else:
        print(f"❌ Failed to create Issue {issue_type_id}: {title} | Error: {response.text}")
        return None

# 🚀 Create Specific Issue Types
def create_jira_initiative(title, description):
    return create_jira_issue("10012", title, description)  # ✅ Initiative ID

def create_jira_epic(title, description, initiative_key):
    """Creates an Epic in Jira and ensures it is linked to an Initiative."""
    epic_key = create_jira_issue("10000", title, description)  # ✅ Epic ID

    if epic_key and initiative_key:
        link_issues(epic_key, initiative_key, "Parent-Child")  # ✅ Link Epic to Initiative
        print(f"🔗 Linked Epic {epic_key} to Initiative {initiative_key}")

    return epic_key

def create_jira_story(title, description, epic_key):
    """Creates a Jira Story under an Epic."""
    return create_jira_issue("10001", title, description, {"parent": {"key": epic_key}})  # ✅ Story ID

def create_jira_task(title, description, story_key):
    """Creates a Jira Task under a Story."""
    return create_jira_issue("10002", title, description, {"parent": {"key": story_key}})  # ✅ Task ID

def create_jira_subtask(title, description, task_key):
    """Creates a Jira Subtask under a Task."""
    return create_jira_issue("10003", title, description, {"parent": {"key": task_key}})  # ✅ Sub-task ID


# ----------------------------------------------
# 🚀 Section 3: Epic, Story, Task Retrieval Functions
# ----------------------------------------------

def get_epic_key(epic_name):
    """Retrieve the Jira issue key for an Epic based on its summary."""
    search_url = f"{JIRA_BASE_URL}/rest/api/3/search"
    jql_query = f'project = "{JIRA_PROJECT_KEY}" AND issuetype = "Epic" AND summary ~ "{epic_name}"'
    payload = {"jql": jql_query, "fields": ["key"]}

    response = requests.get(search_url, headers=HEADERS, auth=JIRA_AUTH, json=payload)
    
    if response.status_code == 200 and response.json()["issues"]:
        return response.json()["issues"][0]["key"]
    else:
        print(f"❌ Epic '{epic_name}' not found in Jira!")
        return None


def get_stories_under_epic(epic_key):
    """Retrieve all Story issue keys under an Epic."""
    search_url = f"{JIRA_BASE_URL}/rest/api/3/search"
    jql_query = f'project = "{JIRA_PROJECT_KEY}" AND "Epic Link" = "{epic_key}" AND issuetype = "Story"'
    payload = {"jql": jql_query, "fields": ["key", "summary"]}

    response = requests.get(search_url, headers=HEADERS, auth=JIRA_AUTH, json=payload)

    if response.status_code == 200:
        return {issue["fields"]["summary"]: issue["key"] for issue in response.json()["issues"]}
    else:
        print(f"❌ Failed to retrieve stories under Epic {epic_key}: {response.json()}")
        return {}
    
def get_tasks_under_story(story_key):
    """Retrieve all Task issue keys under a Story."""
    search_url = f"{JIRA_BASE_URL}/rest/api/3/search"
    jql_query = f'project = "{JIRA_PROJECT_KEY}" AND "parent" = "{story_key}" AND issuetype = "Task"'
    payload = {"jql": jql_query, "fields": ["key", "summary"]}

    response = requests.get(search_url, headers=HEADERS, auth=JIRA_AUTH, json=payload)

    if response.status_code == 200:
        return {issue["fields"]["summary"]: issue["key"] for issue in response.json()["issues"]}
    else:
        print(f"❌ Failed to retrieve tasks under Story {story_key}: {response.json()}")
        return {}


def get_subtasks_under_task(task_key):
    """Retrieve all Subtask issue keys under a Task."""
    search_url = f"{JIRA_BASE_URL}/rest/api/3/search"
    jql_query = f'project = "{JIRA_PROJECT_KEY}" AND "parent" = "{task_key}" AND issuetype = "Sub-task"'
    payload = {"jql": jql_query, "fields": ["key", "summary"]}

    response = requests.get(search_url, headers=HEADERS, auth=JIRA_AUTH, json=payload)

    if response.status_code == 200:
        return {issue["fields"]["summary"]: issue["key"] for issue in response.json()["issues"]}
    else:
        print(f"❌ Failed to retrieve subtasks under Task {task_key}: {response.json()}")
        return {}


# ----------------------------------------------
# 🚀 Section 4: Issue Linking & Status Updates
# ----------------------------------------------

def link_issues(issue_key_1, issue_key_2, link_type="Relates"):
    """Links two Jira issues together."""
    link_payload = {
        "type": {"name": link_type},
        "inwardIssue": {"key": issue_key_1},
        "outwardIssue": {"key": issue_key_2},
    }

    response = requests.post(f"{JIRA_BASE_URL}/rest/api/3/issueLink", headers=HEADERS, auth=JIRA_AUTH, json=link_payload)

    if response.status_code == 201:
        print(f"✅ Linked {issue_key_1} and {issue_key_2} ({link_type})")
    else:
        print(f"❌ Failed to link issues: {response.text}")


def update_jira_issue_status(issue_key, new_status):
    """Update the status of a Jira issue."""
    update_url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}/transitions"

    transition_payload = {
        "transition": {"id": new_status}
    }

    response = requests.post(update_url, headers=HEADERS, auth=JIRA_AUTH, json=transition_payload)

    if response.status_code == 204:
        print(f"✅ Updated Jira Issue: {issue_key} to {new_status}")
    else:
        print(f"❌ Failed to update Jira Issue {issue_key}: {response.text}")


# ----------------------------------------------
# 🚀 Section 5: Logging & Notifications
# ----------------------------------------------

def log_jira_update(task_key, task_summary, old_status, new_status):
    """Logs the Jira update process for tracking."""
    log_entry = f"Updated {task_key} ({task_summary}): {old_status} → {new_status}"
    print(log_entry)
    with open("jira_update_log.txt", "a") as f:
        f.write(log_entry + "\n")


def log_error(error_message):
    """Logs errors that occur during the Jira update process."""
    print(f"❌ ERROR: {error_message}")
    with open("jira_error_log.txt", "a") as f:
        f.write(error_message + "\n")


def send_slack_notification(message):
    """Sends a Slack notification when a Jira update occurs."""
    slack_webhook_url = "YOUR_SLACK_WEBHOOK_URL"
    payload = {"text": message}
    response = requests.post(slack_webhook_url, json=payload)
    
    if response.status_code == 200:
        print("✅ Slack Notification Sent")
    else:
        print(f"❌ Slack Notification Failed: {response.text}")
        
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email_notification(subject, body, recipient_email):
    """Sends an email notification when a Jira update occurs using securely stored credentials."""
    email_creds = SECURITY_MANAGER.get_email_credentials()

    SMTP_SERVER = email_creds["SMTP_SERVER"]
    SMTP_PORT = int(email_creds["SMTP_PORT"])  # Ensure port is an integer
    EMAIL_SENDER = email_creds["EMAIL_SENDER"]

    if not all([SMTP_SERVER, SMTP_PORT, EMAIL_SENDER]):
        print("❌ Missing email credentials. Ensure they are set in AWS Secrets Manager or .env")
        return

    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.sendmail(EMAIL_SENDER, recipient_email, msg.as_string())
        server.quit()
        print(f"📧 Email sent successfully to {recipient_email}")
    except Exception as e:
        print(f"❌ Email failed to send: {e}")

import os
import json
import base64
import boto3
from dotenv import load_dotenv

# ✅ Load Environment Variables (if `.env` file exists)
load_dotenv()

class SecurityManager:
    """Centralized Security & Authentication Manager (Supports AWS Secrets & .env)"""
    _cached_auth = None  # Store credentials after first retrieval

    def __init__(self, aws_region="us-east-2"):
        self.credentials = {}
        self.aws_region = aws_region
        self.secrets_client = boto3.client("secretsmanager", region_name=self.aws_region)

    def get_secret(self, key, required=True):
        """Retrieve secret from environment variables (Fallback Method)"""
        value = os.getenv(key)
        if required and not value:
            raise ValueError(f"❌ Missing required security key: {key}")
        return value

    def get_aws_secret(self, secret_name):
        """Retrieve a secret from AWS Secrets Manager"""
        try:
            response = self.secrets_client.get_secret_value(SecretId=secret_name)
            return json.loads(response["SecretString"])
        except self.secrets_client.exceptions.ResourceNotFoundException:
            print(f"⚠️ AWS Secret '{secret_name}' not found, falling back to .env")
            return None
        except Exception as e:
            print(f"❌ AWS SecretsManager Error: {str(e)}")
            return None

    def get_jira_auth(self):
        """Fetch Jira authentication credentials securely"""
        
        if self._cached_auth:  # Return cached credentials if available
            return self._cached_auth

        print("DEBUG: Checking environment variables first...")
        email = self.get_secret("JIRA_USER_EMAIL", required=False)
        api_token = self.get_secret("JIRA_API_TOKEN", required=False)
        base_url = self.get_secret("JIRA_BASE_URL", required=False)

        if not email or not api_token:
            print("❌ Missing Jira credentials! Checking AWS Secrets Manager...")
            aws_secrets = self.get_aws_secret("BN-Jira-Credentials")

            if aws_secrets:
                print("✅ Retrieved credentials from AWS Secrets Manager")
                email = aws_secrets.get("JIRA_USER_EMAIL")
                api_token = aws_secrets.get("JIRA_API_TOKEN")
                base_url = aws_secrets.get("JIRA_BASE_URL")
            else:
                print("❌ Failed to retrieve credentials from AWS Secrets Manager")
        
        if not email or not api_token:
            raise ValueError("❌ Jira authentication credentials are missing!")

        print(f"✅ Final JIRA Email: {email}")
        print(f"✅ Final JIRA Token: {api_token[:6]}********")  # Mask most of the token
        print(f"✅ Final JIRA URL: {base_url}")

        self._cached_auth = (email, api_token, base_url)  # Cache credentials for future use
        return email, api_token, base_url  # Return the final credentials and base URL


    def get_jira_headers(self):
        """Return secure headers for Jira API requests"""
        email, api_token, base_url = self.get_jira_auth()

        # Create the authentication string
        auth_string = f"{email}:{api_token}".encode("utf-8")
        encoded_auth = base64.b64encode(auth_string).decode("utf-8")

        print(f"DEBUG: Jira Email -> {email}")  # Debug: Verify email is correct
        print(f"DEBUG: Jira API Token -> {api_token[:6]}********")  # Masked for security
        print(f"DEBUG: Encoded Auth -> {encoded_auth}")  # Verify if encoding is correct

        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Basic {encoded_auth}",
        }


    def get_huntr_auth(self):
        """Fetch Huntr authentication credentials from AWS Secrets Manager or .env"""
        aws_secrets = self.get_aws_secret("huntr_credentials")

        if aws_secrets:
            return aws_secrets["huntr_email"], aws_secrets["huntr_password"]
        else:
            return self.get_secret("HUNTR_EMAIL"), self.get_secret("HUNTR_PASSWORD")

    def get_email_credentials(self):
        """Retrieve email credentials securely from AWS Secrets Manager or .env"""
        aws_secrets = self.get_aws_secret("email_credentials")

        if aws_secrets:
            return {
                "SMTP_SERVER": aws_secrets.get("SMTP_SERVER"),
                "SMTP_PORT": aws_secrets.get("SMTP_PORT"),
                "EMAIL_SENDER": aws_secrets.get("EMAIL_SENDER"),
                "EMAIL_USERNAME": aws_secrets.get("EMAIL_USERNAME"),
                "EMAIL_PASSWORD": aws_secrets.get("EMAIL_PASSWORD"),  # 🔹 Ensure this is included
            }
        else:
            return {
                "SMTP_SERVER": self.get_secret("SMTP_SERVER"),
                "SMTP_PORT": self.get_secret("SMTP_PORT"),
                "EMAIL_SENDER": self.get_secret("EMAIL_SENDER"),
                "EMAIL_USERNAME": self.get_secret("EMAIL_USERNAME"),
                "EMAIL_PASSWORD": self.get_secret("EMAIL_PASSWORD"),  # 🔹 Ensure this is included
            }


# ✅ Singleton Instance
SECURITY_MANAGER = SecurityManager()

# ✅ Test AWS Secrets Retrieval
huntr_email, huntr_password = SECURITY_MANAGER.get_huntr_auth()
print(f"✅ Huntr Email: {huntr_email} (Password Hidden)")

# ✅ Test Email Credentials Retrieval
email_creds = SECURITY_MANAGER.get_email_credentials()
#print(f"✅ SMTP Server: {email_creds['SMTP_SERVER']} | Sender: {email_creds['EMAIL_SENDER']} | Username: {email_creds['EMAIL_USERNAME']} | Password: {email_creds['EMAIL_PASSWORD']}")

# ✅ Test Jira Credentials Retrieval
email, api_token, base_url = SECURITY_MANAGER.get_jira_auth()
#print(f"✅ API: {jira_creds['JIRA_API_TOKEN']} | Email: {jira_creds['JIRA_USER_EMAIL']} | Project: {jira_creds['JIRA_PROJECT_KEY']} | URL: {jira_creds['JIRA_BASE_URL']}")
print(f"✅ Jira Email: {email} | Jira URL: {base_url} | (Password Hidden)")


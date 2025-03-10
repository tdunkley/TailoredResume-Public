import boto3
import json

def get_secret(secret_name, region_name="us-east-2"):
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)
    
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response["SecretString"]
        
        # Parse JSON
        secret_dict = json.loads(secret)
        
        return secret_dict  # Returns dictionary with JIRA credentials
    
    except Exception as e:
        print(f"❌ Error retrieving secret: {e}")
        return None

# Retrieve the secret
secret_data = get_secret("BN-Jira-Credentials")

if secret_data:
    print(f"✅ Retrieved Secret: {secret_data}")  # Debugging - Remove in Production
else:
    print("❌ Failed to retrieve secret")


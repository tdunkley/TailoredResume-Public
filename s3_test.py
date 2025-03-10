import boto3
from s3_manager import upload_to_s3

# Test Upload
test_file = "test_upload.txt"
with open(test_file, "w") as f:
    f.write("S3 upload test successful!")

upload_to_s3(test_file, "logs/test_upload.txt")
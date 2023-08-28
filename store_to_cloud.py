import os
import boto3
import botocore.exceptions

# Read AWS credentials from a configuration file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    aws_access_key_id = config.get('aws_access_key_id')
    aws_secret_access_key = config.get('aws_secret_access_key')

# Set the bucket name and file name
bucket_name = 'you're_bucket_name_goes_here'
file_name = 'your-file-name-goes-here.txt'

# Initialize an S3 client
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

def upload_file():
    try:
        s3.upload_file(file_name, bucket_name, file_name)
        print(f"{file_name} uploaded to {bucket_name} successfully.")
    except botocore.exceptions.NoCredentialsError:
        print("Credentials not available")
    except botocore.exceptions.ClientError as e:
        print(f"An error occurred: {e}")

def download_file():
    try:
        s3.download_file(bucket_name, file_name, f"downloaded_{file_name}")
        print(f"{file_name} downloaded successfully.")
    except botocore.exceptions.NoCredentialsError:
        print("Credentials not available")
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print(f"{file_name} does not exist in {bucket_name}.")
        else:
            print(f"An error occurred: {e}")

def list_objects():
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            print(f"Objects in {bucket_name}:")
            for obj in response['Contents']:
                print(f"- {obj['Key']}")
        else:
            print(f"No objects found in {bucket_name}.")
    except botocore.exceptions.NoCredentialsError:
        print("Credentials not available")
    except botocore.exceptions.ClientError as e:
        print(f"An error occurred: {e}")

# Call the functions
upload_file()
download_file()
list_objects()

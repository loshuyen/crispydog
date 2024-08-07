import os
import dotenv
import boto3
from uuid import uuid4

dotenv.load_dotenv()
aws_access_key_id = os.getenv("AWS_ACCESS_KEY")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_s3_bucket_name = os.getenv("AWS_S3_BUCKET_NAME")
s3 = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

def upload_file(file, file_type):
    try:
        s3_obj_name = str(uuid4()) + "." + file_type.lower()
        s3.upload_fileobj(file, aws_s3_bucket_name, s3_obj_name)
        file_url = os.getenv("AWS_CLOUDFRONT_DOMAIN_NAME") + s3_obj_name
        response = s3.head_object(Bucket=aws_s3_bucket_name, Key=s3_obj_name)
        file_size = response['ContentLength'] / (1024 * 1024)
        file_size = round(file_size, 2)
        print("Upload Successful", s3_obj_name)
        return {"file_url": file_url, "file_size": file_size}
    except Exception as e:
        print(f"Upload Failed: {str(e)}")
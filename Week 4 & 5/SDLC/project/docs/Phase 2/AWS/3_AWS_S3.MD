# S3 - Simple Storage System:
- AWS service to store objects (different types of files) in the cloud
- Allows file versioning:
    - If enabled, when I upload a same file with same filename twice then it will store as version1 (old file), version2(new file)
    - When disabled, it replaces the old file with new one.


#### AWS Storage Class
- Categorizes files in AWS S3 bucket based on their accessibility and usage.
1. Standard
2. Intelligent-Tiering
3. Standard-IA ...


---

# Setup

1. Configure AWS CLI:
- Download and install AWS CLI in terminal (win/lin/mac)
- run `aws configure` to login to your AWS within the terminal

2. Interact with AWS using boto3 python package
- create python venv and run `pip install boto3[crt]`, this will enable boto3 to use terminal configured AWS account

3. Upload & Download files from bucket
- Manually upload/download files to/from S3 via AWS console
- or upload/download using python (refer: 'Week N/AWS/02_AWS_S3/access_s3_contents_using_python/main.py')

4. Empty or Delete Bucket
- Finally when a bucket is not in use delete it
- MUST empty before deletion

---

###### Resources:
- S3 Basics YT: https://www.youtube.com/watch?v=lKPnz27rCPQ
- boto3 Pyhton functions: https://docs.aws.amazon.com/boto3/latest/reference/services/s3.html

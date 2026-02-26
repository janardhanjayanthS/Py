"""
REQUIRES to login with aws using aws cli
"""

import boto3

s3_client = boto3.client("s3")
s3_resource = boto3.resource("s3")

# to view all buckets
# response = s3_client.list_buckets()
# for bucket in response["Buckets"]:
#     print(response)


# to list all objects within a bucket
# response = s3_client.list_objects_v2(Bucket="aws-s3-sample-bucket-one1")
# for obj in response.get("Contents", []):
#     print(obj)

# Download particular file from bucket (use the prev implementations to get bucket name and file key)
# s3_client.download_file(
#     Bucket="aws-s3-sample-bucket-one1",
#     Key="hello_world.txt",
#     Filename="hw_downloaded.txt",
# )


# Enable Versioning through code!
# s3_client.put_bucket_versioning(
#     Bucket="aws-s3-sample-bucket-one1", VersioningConfiguration={"Status": "Enabled"}
# )

print("---")
# List different versions of the files in S3
response = s3_client.list_object_versions(
    Bucket="aws-s3-sample-bucket-one1",
    Prefix="hello_world.txt",  # file name
)

for version in response["Versions"]:
    print(version)

# Download a specific version of the file (use the above method to get verisonID)
# s3_client.download_file(
#     Bucket="aws-s3-sample-bucket-one1",
#     Key="hello_world.txt",  # file name in bucket
#     Filename="hw_ver1.txt",  # downloaded file name
#     ExtraArgs={"VersionId": "lHt2pWPWPzOdB7gOfX12kCaRXLNKkqIv"},
# )
#
# s3_client.download_file(
#     Bucket="aws-s3-sample-bucket-one1",
#     Key="hello_world.txt",  # file name in bucket
#     Filename="hw_ver2.txt",  # downloaded file name
#     ExtraArgs={"VersionId": "null"},
# )

# Upload a file
# s3_client.upload_file(
#     Filename="hello_world.txt",
#     Bucket="aws-s3-sample-bucket-one1",
#     Key="hello_world_new_version.txt",  # the name inside s3
#     ExtraArgs={"ContentType": "text/plain"},
# )

# delete file
s3_client.delete_object(
    Bucket="aws-s3-sample-bucket-one1", Key="hello_world_new_version.txt"
)

import json
import os

import boto3
from fastapi import HTTPException


def get_postgresql_password() -> str:
    if os.getenv("AWS_LAMBDA_FUNCTION_NAME") and not os.getenv("AWS_SAM_LOCAL"):
        try:
            session = boto3.session.Session()
            client = session.client(
                service_name="secretsmanager", region_name="us-east-1"
            )
            # secret_name: string identifier used to tell the AWS Secrets Manager service
            # exactly which "vault" or "folder" of secrets you want to open.
            secret_name = "openai/api_key"
            response = client.get_secret_value(SecretId=secret_name)
            secret_dict = json.loads(response["SecretString"])
            return secret_dict["POSTGRESQL_PWD"]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Cloud Secret Error: {e}")

    else:
        pg_password = os.getenv("POSTGRESQL_PWD")

        if not pg_password:
            raise HTTPException(
                status_code=500,
                detail="POSTGRESQL_PWD not found in environment or locals.json",
            )
        return pg_password

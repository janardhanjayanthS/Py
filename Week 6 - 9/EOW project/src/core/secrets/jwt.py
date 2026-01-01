import json
import os
from typing import Optional

import boto3
from fastapi import HTTPException


def get_jwt_secret_key() -> Optional[str]:
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
            return secret_dict["JWT_SECRET_KEY"]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Cloud Secret Error: {e}")

    else:
        jwt_secret_key = os.getenv("JWT_SECRET_KEY")

        if not jwt_secret_key:
            raise HTTPException(
                status_code=500,
                detail="POSTGRESQL_PWD not found in environment or locals.json",
            )
        return jwt_secret_key

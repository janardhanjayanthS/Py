import json
import os

import boto3
from fastapi import HTTPException


def get_openai_key() -> str:
    # Check if we are in real AWS (Not Local SAM)
    if os.getenv("AWS_LAMBDA_FUNCTION_NAME") and not os.getenv("AWS_SAM_LOCAL"):
        try:
            session = boto3.session.Session()
            client = session.client(
                service_name="secretsmanager", region_name="us-east-1"
            )

            response = client.get_secret_value(SecretId="openai/api_key")
            secret_dict = json.loads(response["SecretString"])
            return secret_dict["OPENAI_API_KEY"]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Cloud Secret Error: {e}")

    # Local Dev or SAM Local
    else:
        key = os.getenv("OPENAI_API_KEY")
        if not key:
            raise HTTPException(
                status_code=500, detail="OPENAI_API_KEY not found in environment"
            )
        return key

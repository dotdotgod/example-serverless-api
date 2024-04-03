import base64
import hashlib
import hmac

import boto3

from api.v1.auth.dtos.cognito_data import CognitoData
from config.settings import Settings

settings = Settings()


def initialize_cognito():
    project_name = settings.PROJECT_NAME
    stage = settings.STAGE
    region = settings.REGION

    if settings.STAGE == "dev":
        cognito_data = CognitoData(
            cognito_user_pool_id=settings.COGNITO_USER_POOL_ID,
            cognito_user_pool_client_id=settings.COGNITO_USER_POOL_CLIENT_ID,
            cognito_user_poll_client_secret=settings.COGNITO_USER_POOL_CLIENT_SECRET,
            cognito_domain_url=settings.COGNITO_DOMAIN_URL,
            cognito_region=settings.REGION,
        )
        return cognito_data

    ssm = boto3.client("ssm")
    cognito_user_pool_id = ssm.get_parameter(
        Name=f"{project_name}-{stage}-cognito-user-pool-id", WithDecryption=True
    )["Parameter"]["Value"]

    cognito_user_pool_client_id = ssm.get_parameter(
        Name=f"{project_name}-{stage}-cognito-user-pool-client-id",
        WithDecryption=True,
    )["Parameter"]["Value"]

    cognito_user_pool_client_secret = ssm.get_parameter(
        Name=f"{project_name}-{stage}-cognito-user-pool-client-secret",
        WithDecryption=True,
    )["Parameter"]["Value"]

    cognito_cognito_domain_url = ssm.get_parameter(
        Name=f"{project_name}-{stage}-cognito-domain-url",
        WithDecryption=True,
    )["Parameter"]["Value"]

    cognito_data = CognitoData(
        cognito_user_pool_id=cognito_user_pool_id,
        cognito_user_pool_client_id=cognito_user_pool_client_id,
        cognito_user_poll_client_secret=cognito_user_pool_client_secret,
        cognito_domain_url=cognito_cognito_domain_url,
        cognito_region=region,
    )

    return cognito_data


def get_basic_secret_hash(client_id: str, client_secret: str):
    msg = client_id + ":" + client_secret
    encoded_bytes = base64.b64encode(msg.encode("utf-8"))
    encoded_string = encoded_bytes.decode("utf-8")
    return encoded_string


def get_user_secret_hash(user_name: str, client_id: str, client_secret: str):
    secret_hash = hmac.new(
        key=client_secret.encode("utf-8"),
        msg=(user_name + client_id).encode("utf-8"),
        digestmod=hashlib.sha256,
    ).digest()

    # base64 인코딩을 통해 최종 Secret Hash 문자열을 얻음
    secret_hash_string = base64.b64encode(secret_hash).decode()
    return secret_hash_string

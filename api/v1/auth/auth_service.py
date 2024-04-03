import boto3
import requests
from fastapi import HTTPException

from api.v1.auth.dtos.auth_dto import SignUpReqDTO, ConfirmSignUpReqDTO, SignInReqDTO
from api.v1.auth.dtos.cognito_idp_response import CognitoIdpResponse
from api.v1.auth.dtos.token_dto import TokenDTO
from config.cognito import (
    initialize_cognito,
    get_basic_secret_hash,
    get_user_secret_hash,
)
from config.settings import Settings

settings = Settings()
cognito = initialize_cognito()
client = boto3.client("cognito-idp", region_name=settings.REGION)


async def sign_up(dto: SignUpReqDTO):
    # 사용자 등록
    try:
        response = client.sign_up(
            ClientId=cognito.cognito_user_pool_client_id,
            SecretHash=get_user_secret_hash(
                dto.email,
                cognito.cognito_user_pool_client_id,
                cognito.cognito_user_poll_client_secret,
            ),
            Username=dto.email,
            Password=dto.password,
            UserAttributes=[
                {
                    "Name": "email",  # 이메일 주소를 식별자로 사용
                    "Value": dto.email,
                },
            ],
        )
        return CognitoIdpResponse(**response)
    except client.exceptions.InvalidPasswordException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def confirm_sign_up(dto: ConfirmSignUpReqDTO):
    # 이메일 인증
    try:
        response = client.confirm_sign_up(
            ClientId=cognito.cognito_user_pool_client_id,
            SecretHash=get_user_secret_hash(
                dto.email,
                cognito.cognito_user_pool_client_id,
                cognito.cognito_user_poll_client_secret,
            ),
            Username=dto.email,
            ConfirmationCode=dto.confirmation_code,  # 이메일 또는 전화번호로 받은 인증 코드
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def resend_confirm_code(dto):
    try:
        response = client.resend_confirmation_code(
            ClientId=cognito.cognito_user_pool_client_id,
            SecretHash=get_user_secret_hash(
                dto.email,
                cognito.cognito_user_pool_client_id,
                cognito.cognito_user_poll_client_secret,
            ),
            Username=dto.email,
        )
        return CognitoIdpResponse(**response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def sign_in(dto: SignInReqDTO):
    # 사용자 풀에서 사용자를 인증하고, 인증 토큰을 받음
    try:
        response = client.initiate_auth(
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": dto.email,
                "PASSWORD": dto.password,
                "SECRET_HASH": get_user_secret_hash(
                    dto.email,
                    cognito.cognito_user_pool_client_id,
                    cognito.cognito_user_poll_client_secret,
                ),
            },
            ClientId=cognito.cognito_user_pool_client_id,
        )

        return TokenDTO(
            token_type=response["AuthenticationResult"]["TokenType"],
            access_token=response["AuthenticationResult"]["AccessToken"],
            refresh_token=response["AuthenticationResult"]["RefreshToken"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def sign_up_ui(redirect_url):
    url: str = (
        f"{cognito.cognito_domain_url}/signup?response_type=code&client_id={cognito.cognito_user_pool_client_id}"
        f"&state=state&scope=email+aws.cognito.signin.user.admin&redirect_uri={redirect_url}"
    )
    return url


def sign_in_ui(redirect_url):
    url: str = (
        f"{cognito.cognito_domain_url}/login?response_type=code&client_id={cognito.cognito_user_pool_client_id}"
        f"&state=state&scope=email+aws.cognito.signin.user.admin&redirect_uri={redirect_url}"
    )
    return url


def google_login_url(redirect_url: str):
    url: str = (
        f"{cognito.cognito_domain_url}/oauth2/authorize?response_type=code&client_id={cognito.cognito_user_pool_client_id}"
        f"&identity_provider=Google&state=state&scope=email&redirect_uri={redirect_url}"
    )
    return url


async def get_access_token(code: str, redirect_url: str):

    encoded_string = get_basic_secret_hash(
        cognito.cognito_user_pool_client_id, cognito.cognito_user_poll_client_secret
    )

    token_endpoint = cognito.cognito_domain_url + "/oauth2/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": cognito.cognito_user_pool_client_id,
        "code": code,
        "redirect_uri": redirect_url,
    }

    # 헤더 설정
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic " + encoded_string,
    }

    response = requests.post(token_endpoint, headers=headers, data=payload)
    json_data = response.json()
    access_token = json_data.get("access_token")
    refresh_token = json_data.get("refresh_token")

    # # 토큰 파싱 예시
    # id_token = json_data.get("id_token")
    # result = jwt_sync.decode(
    #     id_token, cognito.cognito_region, cognito.cognito_user_pool_id, cognito.cognito_user_pool_client_id
    # )

    token_dto = TokenDTO(access_token=access_token, refresh_token=refresh_token)
    return token_dto


async def get_refresh_token(token: str):

    encoded_string = get_basic_secret_hash(
        cognito.cognito_user_pool_client_id, cognito.cognito_user_poll_client_secret
    )

    token_endpoint = cognito.cognito_domain_url + "/oauth2/token"
    payload = {
        "grant_type": "refresh_token",
        "client_id": cognito.cognito_user_pool_client_id,
        "refresh_token": token,
    }

    # 헤더 설정
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic " + encoded_string,
    }

    response = requests.post(token_endpoint, headers=headers, data=payload)
    json_data = response.json()
    access_token = json_data.get("access_token")
    token_dto = TokenDTO(access_token=access_token, refresh_token=token)
    return token_dto

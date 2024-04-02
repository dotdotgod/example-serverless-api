# import base64
#
# import requests
# from cognitojwt import jwt_sync
#
#
# settings = Settings()
# ddb = initialize_dynamodb()
# user_table = ddb.Table("user")
# cognito = initialize_cognito()
#
#

import boto3
from fastapi import HTTPException

from api.v1.auth.dtos.auth_dto import SignUpReqDTO, ConfirmSignUpReqDTO, SignInReqDTO
from api.v1.auth.dtos.cognito_idp_response import CognitoIdpResponse
from api.v1.auth.dtos.token_dto import TokenDTO
from config.cognito import initialize_cognito, get_secret_hash
from config.settings import Settings

settings = Settings()
cognito = initialize_cognito()
client = boto3.client("cognito-idp", region_name=settings.REGION)


async def sign_up(dto: SignUpReqDTO):
    # 사용자 등록
    try:
        response = client.sign_up(
            ClientId=cognito.cognito_user_pool_client_id,
            SecretHash=get_secret_hash(
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
            SecretHash=get_secret_hash(
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
            SecretHash=get_secret_hash(
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
                "SECRET_HASH": get_secret_hash(
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


# async def get_refresh_token(token: str):
#     cognito_client_id = cognito.cognito_client_id
#     cognito_client_password = cognito.cognito_client_password
#     cognito_domain = cognito.cognito_domain
#
#     base_encode = cognito_client_id + ":" + cognito_client_password
#     encoded_bytes = base64.b64encode(base_encode.encode("utf-8"))
#     encoded_string = encoded_bytes.decode("utf-8")
#
#     token_endpoint = cognito_domain + "/oauth2/token"
#     payload = {
#         "grant_type": "refresh_token",
#         "client_id": cognito_client_id,
#         "refresh_token": token,
#     }
#
#     # 헤더 설정
#     headers = {
#         "Content-Type": "application/x-www-form-urlencoded",
#         "Authorization": "Basic " + encoded_string,
#     }
#
#     response = requests.post(token_endpoint, headers=headers, data=payload)
#     json_data = response.json()
#     access_token = json_data.get("access_token")
#     token_dto = TokenDto(access_token=access_token, refresh_token=token)
#     return token_dto
#
#
# async def get_access_token(code: str):
#     cognito_client_id = cognito.cognito_client_id
#     cognito_client_password = cognito.cognito_client_password
#     redirect_uri = cognito.redirect_uri
#     cognito_domain = cognito.cognito_domain
#     cognito_userpool_region = cognito.cognito_userpool_region
#     cognito_userpool_id = cognito.cognito_userpool_id
#
#     base_encode = cognito_client_id + ":" + cognito_client_password
#     encoded_bytes = base64.b64encode(base_encode.encode("utf-8"))
#     encoded_string = encoded_bytes.decode("utf-8")
#
#     token_endpoint = cognito_domain + "/oauth2/token"
#     payload = {
#         "grant_type": "authorization_code",
#         "client_id": cognito_client_id,
#         "code": code,
#         "redirect_uri": redirect_uri,
#     }
#
#     # 헤더 설정
#     headers = {
#         "Content-Type": "application/x-www-form-urlencoded",
#         "Authorization": "Basic " + encoded_string,
#     }
#
#     response = requests.post(token_endpoint, headers=headers, data=payload)
#     json_data = response.json()
#     access_token = json_data.get("access_token")
#     refresh_token = json_data.get("refresh_token")
#     id_token = json_data.get("id_token")
#     result = jwt_sync.decode(
#         id_token, cognito_userpool_region, cognito_userpool_id, cognito_client_id
#     )
#     email = result.get("email")
#     cognito_id = result.get("sub")
#
#     user = await user_service.get_user(cognito_id)
#     if not user:
#         create_user_dto = UserDto(
#             email=email, id=cognito_id, created_at=get_current_time()
#         )
#         user_table.put_item(Item=create_user_dto.dict())
#
#     token_dto = TokenDto(access_token=access_token, refresh_token=refresh_token)
#     return token_dto

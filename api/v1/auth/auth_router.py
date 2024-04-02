from fastapi import APIRouter
from fastapi.security import HTTPBearer

from api.v1.auth import auth_service
from api.v1.auth.dtos.auth_dto import (
    SignUpReqDTO,
    ConfirmSignUpReqDTO,
    ResendReqDTO,
    SignInReqDTO,
)
from api.v1.auth.dtos.cognito_idp_response import CognitoIdpResponse
from api.v1.auth.dtos.token_dto import TokenDTO

auth = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()


# @auth.get("/token")
# async def get_token(code: str):
#     return await auth_service.get_access_token(code)
#
#
# @auth.get("/token/refresh")
# async def get_refresh_token(credentials: HTTPAuthorizationCredentials = Security(security)):
#     token = credentials.credentials
#     return await auth_service.get_refresh_token(token)


@auth.get("/token")
async def get_token():
    return {"body": "get_token"}


@auth.get("/token/refresh")
async def get_refresh_token():
    return {"body": "get_refresh"}


@auth.post("/sign-up", response_model=CognitoIdpResponse)
async def sign_up(dto: SignUpReqDTO):
    return await auth_service.sign_up(dto)


@auth.post("/sign-up/confirm", response_model=None)
async def confirm_sign_up(dto: ConfirmSignUpReqDTO):
    return await auth_service.confirm_sign_up(dto)


@auth.post("/sign-up/resend", response_model=CognitoIdpResponse)
async def resend_confirm_code(dto: ResendReqDTO):
    return await auth_service.resend_confirm_code(dto)


@auth.post("/sign-in", response_model=TokenDTO)
async def sign_in(dto: SignInReqDTO):
    return await auth_service.sign_in(dto)

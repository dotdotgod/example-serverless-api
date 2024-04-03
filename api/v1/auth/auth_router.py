from fastapi import APIRouter, Query, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.responses import RedirectResponse

from api.v1.auth import auth_service
from api.v1.auth.dtos.auth_dto import (
    SignUpReqDTO,
    ConfirmSignUpReqDTO,
    ResendReqDTO,
    SignInReqDTO,
)
from api.v1.auth.dtos.cognito_idp_response import CognitoIdpResponse
from api.v1.auth.dtos.token_dto import TokenDTO
from config.settings import Settings

auth = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()
settings = Settings()


@auth.get("/token")
async def get_token(
    code: str = Query(...),
    redirect_url: str = Query(default="http://localhost:5001/api/v1/auth/token"),
):
    return await auth_service.get_access_token(code, redirect_url)


@auth.get("/token/refresh")
async def get_refresh_token(
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    token = credentials.credentials
    return await auth_service.get_refresh_token(token)


@auth.get("/sign-in/ui")
async def sign_in_ui(
    redirect_url: str = Query(default=settings.REDIRECT_URL),
):
    url = auth_service.sign_in_ui(redirect_url)
    return RedirectResponse(url=url)


@auth.get("/sign-up/ui")
async def sign_up_ui(
    redirect_url: str = Query(default=settings.REDIRECT_URL),
):
    url = auth_service.sign_up_ui(redirect_url)
    return RedirectResponse(url=url)


@auth.get("/sign-in/google")
async def google_login_url(
    redirect_url: str = Query(default=settings.REDIRECT_URL),
):
    url = auth_service.google_login_url(redirect_url)
    return RedirectResponse(url=url)


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

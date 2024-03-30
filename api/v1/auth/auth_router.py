from fastapi import APIRouter, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from api.v1.auth import auth_service

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


@auth.post("/sign-up")
async def sign_up():
    auth_service.sign_up()
    return {"body": "login"}

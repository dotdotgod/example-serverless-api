from cognitojwt import jwt_sync
from fastapi import Request, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from config.cognito import initialize_cognito

cognito = initialize_cognito()
security = HTTPBearer()


# This middleware function is used to add user info to the request state.
async def add_user_info(
    request: Request, credentials: HTTPAuthorizationCredentials = Security(security)
) -> Request:
    token = credentials.credentials
    if not token:
        raise HTTPException(status_code=401, detail="Authorization Token is required")

    try:
        result = jwt_sync.decode(
            token,
            cognito.cognito_region,
            cognito.cognito_user_pool_id,
            cognito.cognito_user_pool_client_id,
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

    user_id = result.get("sub")
    request.state.user_id = user_id
    return request

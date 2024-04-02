from pydantic import BaseModel


class CognitoData(BaseModel):
    cognito_user_pool_id: str
    cognito_user_pool_client_id: str
    cognito_user_poll_client_secret: str
    cognito_domain_url: str
    cognito_region: str

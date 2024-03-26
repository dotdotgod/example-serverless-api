from pydantic import BaseModel


class CognitoData(BaseModel):
    cognito_client_id: str
    cognito_client_password: str
    redirect_uri: str
    cognito_domain: str
    cognito_userpool_region: str
    cognito_userpool_id: str

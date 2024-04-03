from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "example"
    REGION: str = "ap-northeast-2"
    STAGE: str = "dev"
    COGNITO_USER_POOL_ID: str
    COGNITO_USER_POOL_CLIENT_ID: str
    COGNITO_USER_POOL_CLIENT_SECRET: str
    COGNITO_DOMAIN_URL: str
    REDIRECT_URL: str

    class Config:
        env_file = ".env"

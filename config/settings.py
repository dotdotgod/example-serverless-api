from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "example"
    REGION: str = "ap-northeast-2"
    STAGE: str = "dev"

    class Config:
        env_file = ".env_example"

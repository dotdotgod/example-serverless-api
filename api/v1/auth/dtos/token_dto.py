from pydantic import BaseModel


class TokenDTO(BaseModel):
    token_type: str = "Bearer"

    access_token: str

    refresh_token: str

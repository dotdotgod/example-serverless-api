from pydantic import BaseModel, EmailStr


class SignUpReqDTO(BaseModel):
    email: EmailStr
    password: str


class ConfirmSignUpReqDTO(BaseModel):
    email: EmailStr
    confirmation_code: str


class ResendReqDTO(BaseModel):
    email: EmailStr


class SignInReqDTO(BaseModel):
    email: EmailStr
    password: str

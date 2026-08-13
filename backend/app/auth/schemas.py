from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str
    grade_id: int


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
from pydantic import BaseModel, EmailStr

class SignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    access_token: str
    refresh_token: str

    class Config:
        from_attributes = True

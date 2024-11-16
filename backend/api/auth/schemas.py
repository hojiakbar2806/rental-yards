import fastapi
from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    first_name: str = Field(..., min_length=3, max_length=100)
    last_name: str = Field(..., min_length=3, max_length=100)
    phone_number: str = Field(..., max_length=12, min_length=12)
    username: str = Field(..., min_length=5, max_length=100)


class UserIn(UserSchema):
    hashed_password: str = Field(..., min_length=5, alias="password")

    class Config:
        strict = True
        from_attributes = True


class UserOut(UserSchema):
    id: int


class Login(BaseModel):
    username: str = Field(..., min_length=5)
    password: str = Field(..., min_length=5)

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    type: str = "Bearer"


class ResponseModel(BaseModel):
    user: UserOut
    message: str = Field(..., example="Foydalanuvchi qo'shildi")
    status: bool
    status_code: int = Field(..., example=201)

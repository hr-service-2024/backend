from pydantic import BaseModel
from typing import Optional


class UserAuthSchema(BaseModel):
    username: str
    password: str


class UserCreateSchema(UserAuthSchema):
    is_superuser: bool = False


class UserUpdateSchema(BaseModel):
    username: Optional[str] = None
    hashtag: Optional[str] = None
    specialist: Optional[str] = None
    phone: Optional[str] = None


class UserSchema(BaseModel):
    id: int
    username: str
    hashed_password: bytes
    hashtag: str = ''
    specialist: str = ''
    phone: str = ''
    is_active: bool = True
    is_superuser: bool = False

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'Bearer'

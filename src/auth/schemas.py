from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    username: str
    password: str


UserAuthSchema = UserCreateSchema


class UserSchema(BaseModel):
    id: int
    username: str
    hashed_password: bytes
    is_active: bool = True

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str

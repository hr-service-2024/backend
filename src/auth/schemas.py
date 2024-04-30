from pydantic import BaseModel, field_validator
from typing import Optional, List


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'Bearer'


class UserAuthSchema(BaseModel):
    username: str
    password: str


class UserCreateSchema(UserAuthSchema):
    is_superuser: bool = False


class UserUpdateSchema(BaseModel):
    hashtag: Optional[str] = None
    specialist: Optional[str] = None
    phone: Optional[str] = None


class UpdateSchema(UserUpdateSchema):
    tg_id: Optional[int] = None
    vk_id: Optional[int] = None


class ChannelSchema(BaseModel):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class UserSchema(BaseModel):
    id: int
    username: str
    hashed_password: bytes
    hashtag: str = ''
    specialist: str = ''
    phone: str = ''
    tg_channels: List[int]
    vk_channels: List[int]
    is_active: bool
    is_superuser: bool

    @field_validator('tg_channels', 'vk_channels', mode='before')
    def transform(cls, channels: List[ChannelSchema]) -> List[int]:
        channels_ids = [channel.id for channel in channels]
        return channels_ids

    class Config:
        from_attributes = True

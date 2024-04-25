from typing import List
from fastapi import status
from fastapi.exceptions import HTTPException

from src.utils import AbstractRepository
from src.auth.schemas import UserCreateSchema, UserSchema, UserAuthSchema
from src.auth.secure import get_password_hash, verify_password


class UserService:
    def __init__(self, repo: AbstractRepository):
        self.repo: AbstractRepository = repo()

    async def add(self, data: UserCreateSchema) -> int:
        data = dict(
            username=data.username,
            hashed_password=get_password_hash(data.password)
        )
        user_id = await self.repo.add_one(data)
        return user_id

    async def get_all(self) -> List[UserSchema]:
        users = await self.repo.find_all()
        return users

    async def get_by_id(self, id: int) -> UserSchema:
        user = await self.repo.find_by_id(id)
        return user

    async def get_by_username(self, username: str) -> UserSchema:
        user = await self.repo.find_by_username(username)
        return user

    async def auth_user(self, data: UserAuthSchema) -> UserSchema:
        user = await self.get_by_username(data.username)
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User is not active',
                headers={'WWW-Authenticate': 'Bearer'}
            )
        if not verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Password is not correct'
            )
        return user



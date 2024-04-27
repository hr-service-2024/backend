from typing import List, Optional
from fastapi import status
from fastapi.exceptions import HTTPException

from src.utils import AbstractRepository
from src.auth.schemas import UserCreateSchema, UserSchema, UserAuthSchema, UserUpdateSchema
from src.auth.secure import get_password_hash, verify_password


class UserService:
    def __init__(self, repo: AbstractRepository):
        self.repo: AbstractRepository = repo()

    async def add(self, data: UserCreateSchema) -> UserSchema:
        if not await self.is_existing_user(username=data.username):
            data = dict(
                username=data.username,
                hashed_password=get_password_hash(data.password)
            )
            user = await self.repo.add_one(data)
            return user
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='User with this username already exists'
            )

    async def delete(self, user_id: int) -> None:
        if await self.is_existing_user(user_id=user_id):
            await self.repo.delete_one(user_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User with this id not found'
            )

    async def update(self, user_id: int, data: UserUpdateSchema) -> UserSchema:
        data = data.dict(exclude_none=True)
        user = await self.repo.update_one(user_id, data)
        return user

    async def get_all(self) -> List[UserSchema]:
        users = await self.repo.find_all()
        return users

    async def get_by_id(self, user_id: int) -> UserSchema:
        user = await self.repo.find_by_id(user_id)
        return user

    async def get_by_username(self, username: str) -> UserSchema:
        user = await self.repo.find_by_username(username)
        return user

    async def is_existing_user(self, user_id: Optional[int] = None, username: Optional[str] = None):
        try:
            user = await self.get_by_id(user_id) if user_id else await self.get_by_username(username)
            return True
        except HTTPException:
            return False

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



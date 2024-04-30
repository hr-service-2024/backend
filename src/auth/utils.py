from fastapi import Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from typing import Annotated

from src.auth.secure import JWT
from src.auth.service import UserService
from src.auth.dependencies import get_user_service
from src.auth.schemas import UserSchema

http_bearer = HTTPBearer()


async def is_active_user(user: UserSchema) -> None:
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User is not active',
            headers={'WWW-Authenticate': 'Bearer'}
        )


async def get_current_user(credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
                           user_service: Annotated[UserService, Depends(get_user_service)]) -> UserSchema:
    token = credentials.credentials
    user_id = JWT.decode_jwt(token, expected_type='access')
    user = await user_service.get_by_id(user_id)
    await is_active_user(user)
    return user


async def get_current_user_by_refresh(credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
                                      user_service: Annotated[UserService, Depends(get_user_service)]) -> UserSchema:
    token = credentials.credentials
    user_id = JWT.decode_jwt(token, expected_type='refresh')
    user = await user_service.get_by_id(user_id)
    await is_active_user(user)
    return user

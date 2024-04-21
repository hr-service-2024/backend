from fastapi import Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from typing import Annotated

from src.auth.secure import decode_jwt
from src.auth.service import UserService
from src.auth.dependencies import get_user_service
from src.auth.schemas import UserSchema

http_bearer = HTTPBearer()


async def get_current_user(credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
                           user_service: Annotated[UserService, Depends(get_user_service)]) -> UserSchema:
    token = credentials.credentials
    id = decode_jwt(token)
    user = await user_service.get_by_id(id)
    return user


async def get_current_active_user(current_user: Annotated[UserSchema, Depends(get_current_user)]) -> UserSchema:
    if not current_user.is_active:
        raise HTTPException(detail='User is not active', status_code=status.HTTP_400_BAD_REQUEST)
    return current_user

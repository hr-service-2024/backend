from fastapi import APIRouter, Depends, status
from typing import Annotated, Union, Optional, List

from src.config import settings
from src.auth.service import UserService
from src.auth.dependencies import get_user_service
from src.auth.schemas import UserCreateSchema, UserSchema, UserAuthSchema, UserUpdateSchema, Token
from src.auth.secure import encode_jwt
from src.auth.utils import get_current_user, get_current_user_by_refresh

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post('/create', response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def add_user(data: UserCreateSchema, user_service: Annotated[UserService, Depends(get_user_service)]):
    user = await user_service.add(data)
    return user


@router.get('/get', response_model=Union[UserSchema, List[UserSchema]], status_code=status.HTTP_200_OK)
async def get_user(user_service: Annotated[UserService, Depends(get_user_service)], user_id: Optional[int] = None):
    if user_id:
        resp = await user_service.get_by_id(user_id)
    else:
        resp = await user_service.get_all()
    return resp


@router.delete('/delete', response_model=None, status_code=status.HTTP_200_OK)
async def delete_user(user_id: Optional[int], user_service: Annotated[UserService, Depends(get_user_service)]):
    await user_service.delete(user_id)


@router.post('/auth', response_model=Token, status_code=status.HTTP_201_CREATED)
async def auth_user(data: UserAuthSchema, user_service: Annotated[UserService, Depends(get_user_service)]):
    user = await user_service.auth_user(data)
    access_token = encode_jwt(user, token_type='access', expire_minutes=settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token = encode_jwt(user, token_type='refresh', expire_minutes=settings.jwt.REFRESH_TOKEN_EXPIRE_MINUTES)
    token = Token(access_token=access_token, refresh_token=refresh_token)
    return token


@router.post('/refresh_tokens', response_model=Token, status_code=status.HTTP_201_CREATED)
async def refresh_tokens(user: Annotated[UserSchema, Depends(get_current_user_by_refresh)]):
    access_token = encode_jwt(user, token_type='access', expire_minutes=settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token = encode_jwt(user, token_type='refresh', expire_minutes=settings.jwt.REFRESH_TOKEN_EXPIRE_MINUTES)
    token = Token(access_token=access_token, refresh_token=refresh_token)
    return token


@router.get('/profile', response_model=UserSchema, status_code=status.HTTP_200_OK)
async def get_profile(user: Annotated[UserSchema, Depends(get_current_user)]):
    return user


@router.patch('/update', response_model=UserSchema, status_code=status.HTTP_200_OK)
async def update_user(data: UserUpdateSchema, user: Annotated[UserSchema, Depends(get_current_user)],
                      user_service: Annotated[UserService, Depends(get_user_service)]):
    user = await user_service.update(user.id, data)
    return user

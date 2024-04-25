from fastapi import APIRouter, Depends, status
from typing import Annotated, Union, Optional, List

from src.auth.service import UserService
from src.auth.dependencies import get_user_service
from src.auth.schemas import UserCreateSchema, UserSchema, UserAuthSchema, Token
from src.auth.secure import encode_jwt
from src.auth.utils import get_current_user, get_current_user_by_refresh

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post('/add', response_model=int, status_code=status.HTTP_201_CREATED)
async def add_user(data: UserCreateSchema, user_service: Annotated[UserService, Depends(get_user_service)]):
    user_id = await user_service.add(data)
    return user_id


@router.get('/get', response_model=Union[UserSchema, List[UserSchema]], status_code=status.HTTP_200_OK)
async def get_user(user_service: Annotated[UserService, Depends(get_user_service)], user_id: Optional[int] = None,
                   username: Optional[str] = None):
    if user_id:
        resp = await user_service.get_by_id(user_id)
    elif username:
        resp = await user_service.get_by_username(username)
    else:
        resp = await user_service.get_all()
    return resp


@router.post('/auth', response_model=Token, status_code=status.HTTP_201_CREATED)
async def auth_user(data: UserAuthSchema, user_service: Annotated[UserService, Depends(get_user_service)]):
    user = await user_service.auth_user(data)
    access_token = encode_jwt(user, token_type='access', expire_minutes=1)
    refresh_token = encode_jwt(user, token_type='refresh', expire_minutes=30 * 24 * 60)
    token = Token(access_token=access_token, refresh_token=refresh_token)
    return token


@router.post('/refresh_tokens', response_model=Token, status_code=status.HTTP_201_CREATED)
async def refresh_tokens(user: Annotated[UserSchema, Depends(get_current_user_by_refresh)]):
    access_token = encode_jwt(user, token_type='access', expire_minutes=15)
    refresh_token = encode_jwt(user, token_type='refresh', expire_minutes=30 * 24 * 60)
    token = Token(access_token=access_token, refresh_token=refresh_token)
    return token


@router.get('/me', response_model=UserSchema, status_code=status.HTTP_200_OK)
async def get_user(user: Annotated[UserSchema, Depends(get_current_user)]):
    return user

from fastapi import APIRouter, Depends, status
from typing import Annotated, Union, Optional, List

from src.auth.service import UserService
from src.auth.dependencies import get_user_service
from src.auth.schemas import UserCreateSchema, UserSchema, UserAuthSchema, Token
from src.auth.secure import encode_jwt
from src.auth.utils import get_current_active_user

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post('/add', response_model=int, status_code=status.HTTP_201_CREATED)
async def add_user(data: UserCreateSchema, user_service: Annotated[UserService, Depends(get_user_service)]):
    user_id = await user_service.add(data)
    return user_id


@router.get('/get', response_model=Union[UserSchema, List[UserSchema]], status_code=status.HTTP_200_OK)
async def get_user(user_service: Annotated[UserService, Depends(get_user_service)], id: Optional[int] = None,
                   username: Optional[str] = None):
    if id:
        resp = await user_service.get_by_id(id)
    elif username:
        resp = await user_service.get_by_username(username)
    else:
        resp = await user_service.get_all()
    return resp


@router.post('/auth', response_model=Token, status_code=status.HTTP_201_CREATED)
async def auth_user(data: UserAuthSchema, user_service: Annotated[UserService, Depends(get_user_service)]):
    user = await user_service.auth_user(data)
    token = Token(access_token=encode_jwt(user), token_type='Bearer')
    return token


@router.get('/me', response_model=UserSchema, status_code=status.HTTP_200_OK)
async def get_user(user: Annotated[UserSchema, Depends(get_current_active_user)]):
    return user

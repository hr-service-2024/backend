from fastapi import status
from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta

from src.config import settings
from src.auth.schemas import UserSchema

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class Password:
    @classmethod
    def get_password_hash(cls, password: str):
        return pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: bytes) -> bool:
        return pwd_context.verify(plain_password, hashed_password)


class JWT:
    @classmethod
    def encode_jwt(cls, user: UserSchema, token_type: str, expire_minutes: int,
                   secrete_key: str = settings.jwt.JWT_SECRET_KEY,
                   algorithm: str = settings.jwt.JWT_ALGORITHM):
        payload = dict(
            sub=str(user.id),
            type=token_type,
            iat=datetime.utcnow(),
            exp=datetime.utcnow() + timedelta(minutes=expire_minutes)
        )
        encoded_jwt = jwt.encode(payload, secrete_key, algorithm=algorithm)
        return encoded_jwt

    @classmethod
    def decode_jwt(cls, token, expected_type: str, secrete_key: str = settings.jwt.JWT_SECRET_KEY,
                   algorithm: str = settings.jwt.JWT_ALGORITHM) -> int:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )
        try:
            payload = jwt.decode(token, secrete_key, algorithms=[algorithm])
            token_type = payload.get('type')
            if token_type != expected_type:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"Invalid token type {token_type!r} expected {expected_type!r}",
                    headers={'WWW-Authenticate': 'Bearer'}
                )
            user_id = int(payload.get('sub'))
            if user_id is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        return user_id

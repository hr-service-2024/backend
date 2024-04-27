from sqlalchemy import select
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.exc import NoResultFound
from fastapi import status
from fastapi.exceptions import HTTPException

from src.utils import SQLAlchemyRepository
from src.database import async_session_maker
from src.auth.models import User


class UserRepository(SQLAlchemyRepository):
    model = User

    async def find_by_username(self, username: str) -> BaseModel:
        async with async_session_maker() as session:
            try:
                query = select(self.model).where(func.lower(self.model.username) == username.lower())
                res = await session.execute(query)
                res = res.scalar_one().to_read_model()
                return res
            except NoResultFound:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='User with this username not found'
                )

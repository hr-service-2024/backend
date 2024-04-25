from abc import ABC, abstractmethod
from sqlalchemy import insert, select
from sqlalchemy.exc import NoResultFound
from fastapi import status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from typing import List

from src.database import async_session_maker


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one():
        raise NotImplementedError

    @abstractmethod
    async def find_by_id():
        raise NotImplementedError

    @abstractmethod
    async def find_all():
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add_one(self, data: dict) -> int:
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            res = res.scalar_one()
            await session.commit()
            return res

    async def find_by_id(self, id: int) -> BaseModel:
        async with async_session_maker() as session:
            try:
                query = select(self.model).where(self.model.id == id)
                res = await session.execute(query)
                res = res.scalar_one().to_read_model()
            except NoResultFound:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='User with this id not found'
                )
            return res

    async def find_all(self) -> List[BaseModel]:
        async with async_session_maker() as session:
            query = select(self.model)
            res = await session.execute(query)
            res = [row[0].to_read_model() for row in res.all()]
            return res

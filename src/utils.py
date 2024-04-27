from abc import ABC, abstractmethod
from sqlalchemy import insert, delete, update, select
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
    async def delete_one():
        raise NotImplementedError

    @abstractmethod
    async def update_one():
        raise NotImplementedError

    @abstractmethod
    async def find_by_id():
        raise NotImplementedError

    @abstractmethod
    async def find_all():
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add_one(self, data: dict) -> BaseModel:
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model)
            res = await session.execute(stmt)
            res = res.scalar_one().to_read_model()
            await session.commit()
            return res

    async def delete_one(self, obj_id: int) -> None:
        async with async_session_maker() as session:
            stmt = delete(self.model).where(self.model.id == obj_id)
            await session.execute(stmt)
            await session.commit()

    async def update_one(self, obj_id: int, data: dict) -> BaseModel:
        async with async_session_maker() as session:
            stmt = update(self.model).values(**data).where(self.model.id == obj_id).returning(self.model)
            res = await session.execute(stmt)
            res = res.scalar_one().to_read_model()
            await session.commit()
            return res

    async def find_by_id(self, obj_id: int) -> BaseModel:
        async with async_session_maker() as session:
            try:
                query = select(self.model).where(self.model.id == obj_id)
                res = await session.execute(query)
                res = res.scalar_one().to_read_model()
                return res
            except NoResultFound:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='User with this id not found'
                )

    async def find_all(self) -> List[BaseModel]:
        async with async_session_maker() as session:
            query = select(self.model)
            res = await session.execute(query)
            res = [row[0].to_read_model() for row in res.all()]
            return res

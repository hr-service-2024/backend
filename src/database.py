from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from typing import AsyncGenerator

from src.config import settings

DATABASE_URL = f'postgresql+asyncpg://{settings.db.DB_USER}:{settings.db.DB_PASS}@{settings.db.DB_HOST}:{settings.db.DB_PORT}/{settings.db.DB_NAME}'
Base: DeclarativeMeta = declarative_base()

engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

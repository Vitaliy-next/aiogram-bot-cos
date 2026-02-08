
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from bot.config import DATABASE_URL


engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # видно SQL в логах — ОЧЕНЬ полезно
)

Base = declarative_base()

async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

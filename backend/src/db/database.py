from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


async def async_session(asyncpg_url: str) -> AsyncEngine:
    engine = create_async_engine(asyncpg_url, echo=True)
    _async_session = sessionmaker(
        engine,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
        class_=AsyncSession,
    )
    return _async_session, engine

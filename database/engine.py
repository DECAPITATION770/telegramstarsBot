from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import DATABASE_URL
from database.models import Base

_engine = None
_async_session_factory = None


def get_engine():
    return _engine


def async_session_factory():
    return _async_session_factory


async def init_engine():
    global _engine, _async_session_factory
    _engine = create_async_engine(
        DATABASE_URL,
        echo=False,
    )
    _async_session_factory = async_sessionmaker(
        _engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )


async def dispose_engine():
    global _engine
    if _engine:
        await _engine.dispose()
        _engine = None

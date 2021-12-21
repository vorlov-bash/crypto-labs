from contextlib import asynccontextmanager
from typing import AsyncContextManager, Callable

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session, sessionmaker
from ..models.base import Base


class SQLiteProxy:
    def __init__(self, file_path):
        self.uri = 'sqlite+aiosqlite:///' + str(file_path)
        self._engine = create_async_engine(self.uri)
        self._session_factory = sessionmaker(autocommit=False, autoflush=False, bind=self._engine, class_=AsyncSession)

    @asynccontextmanager  # type: ignore
    async def session(self) -> Callable[..., AsyncContextManager[Session]]:  # type: ignore
        session = self._session_factory()
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()

    async def run_create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

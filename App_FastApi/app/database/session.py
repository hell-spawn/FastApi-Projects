from loguru import logger
import contextlib
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
    AsyncConnection,
)
from typing import AsyncIterator

from app.config import settings
from app.core.config import HOST_DB, PORT_DB, USER_DB, PASS_DB, NAME_DB
from app.exceptions.exceptions import ServiceError
from sqlalchemy.exc import SQLAlchemyError


class DatabaseSessionManager:
    def __init__(self, url: str,  host: str, port: int, user: str, password: str, database_name: str):
        path_conection = url.format(user, password, host, port, database_name)
        self.engine: AsyncEngine | None = create_async_engine(path_conection)
        self._sessionmaker: async_sessionmaker[AsyncSession] = async_sessionmaker(
            autocommit=False, bind=self.engine
        )

    async def close(self):
        if self.engine is None:
            raise ServiceError
        await self.engine.dispose()
        self.engine = None
        self._sessionmaker = None  # type: ignore

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self.engine is None:
            raise ServiceError

        async with self.engine.begin() as connection:
            try:
                yield connection
            except SQLAlchemyError:
                await connection.rollback()
                logger.error("Connection error occurred")
                raise ServiceError

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if not self._sessionmaker:
            logger.error("Sessionmaker is not available")
            raise ServiceError

        session = self._sessionmaker()
        try:
            yield session
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Session error could not be established {e}")
            raise ServiceError
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(settings.database_url,
                                        HOST_DB, PORT_DB, USER_DB, PASS_DB, NAME_DB)


async def get_db_session():
    async with sessionmanager.session() as session:
        yield session

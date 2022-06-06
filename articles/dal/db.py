"""DAL DB init.

Author: Dmitry Sergeev <realnexusway@gmail.com>
"""

import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from .exception import DALException


def get_database_url() -> str:
    """Making database url.

    Function making SQLAlchemy database url based on
    DATABASE_URL enviroment variable.

    :returns: SQLAlchemy database url
    :raises DALException: If enviroment var DATABASE_URL is not setted
    """
    env_url = os.getenv("DATABASE_URL")

    if not env_url:
        raise DALException("No DATABASE_URL enviroment variable is setted.")

    _, creds = env_url.split("://")

    return "mysql+aiomysql" + "://" + creds


engine = create_async_engine(
    get_database_url(),
    echo=False,
    pool_size=10,
    max_overflow=5,
    pool_pre_ping=True,
    isolation_level="READ_COMMITTED",
)


def async_session() -> AsyncSession:
    """AsyncSession fabric function.

    :returns: AsyncSession instance.
    """
    return AsyncSession(engine, expire_on_commit=False)


async def check_connection() -> None:
    """Checking database connection."""
    async with engine.begin():
        pass


async def shutdown() -> None:
    """Shutdown."""
    await engine.dispose()

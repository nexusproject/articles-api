"""DAL DB init.

Author: Dmitry Sergeev <realnexusway@gmail.com>
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


engine = create_async_engine(
    "mysql+aiomysql://root:@localhost/articles",
    echo=False,
    pool_size=10,
    max_overflow=5,
    pool_pre_ping=True,
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

import pytest
from articles.dal import engine
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture(autouse=True, scope="function")
async def cleanup(session: AsyncSession):
    async with session, session.begin():
        await session.execute("TRUNCATE TABLE articles")

    yield


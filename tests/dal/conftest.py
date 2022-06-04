import pytest
from articles.dal.db import engine
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy


@pytest.fixture(autouse=True, scope="function")
async def xxx(session: sqlalchemy.orm.Session):
    async with session, session.begin():
        await session.execute("TRUNCATE TABLE articles")

    yield


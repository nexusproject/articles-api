import pytest
from articles.dal import engine
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy


@pytest.fixture
def session():
    yield AsyncSession(engine)
    engine.sync_engine.dispose()


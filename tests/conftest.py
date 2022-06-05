"""Conftest file.

Author: Dmitry Sergeev <realnexusway@gmail.com>
"""

from articles.dal import engine

import pytest

from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture()
def session() -> AsyncSession:
    """Fixture returns session for tests.

    :yields: SQLAlchemy AsyncSession
    """
    yield AsyncSession(engine)
    engine.sync_engine.dispose()

"""Conftest file for testing DAL.

Author: Dmitry Sergeev <realnexusway@gmail.com>
"""

import pytest

from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture(autouse=True)
async def _cleanup(session: AsyncSession) -> None:  # noqa PT022
    """Cleanup DB state for each case function.

    :param session: SQLAlchemy AsyncSession
    :yields: none
    """
    async with session, session.begin():
        await session.execute("TRUNCATE TABLE articles")

    yield

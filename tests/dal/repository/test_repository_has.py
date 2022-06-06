"""Tests for DAL Repository has.

Author: Dmitry Sergeev <realnexusway@gmail.com>
"""

from articles.dal import Repository

import pytest

from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio()
async def test_repository_has(session: AsyncSession) -> None:
    """Testing DAL Repository method has.

    :param session: SQLAlchemy session object.
    """

    async with session, session.begin():
        res = await session.execute(
            "INSERT INTO articles (topic, text) "
            "VALUES ('expected topic', 'expected text')"
        )

    async with session:
        assert await Repository(session).has(res.lastrowid) == True  # noqa: E712
        assert await Repository(session).has(12113242) == False  # noqa: E712

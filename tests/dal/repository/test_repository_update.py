"""Tests for DAL Repository update.

Author: Dmitry Sergeev <realnexusway@gmail.com>
"""

from articles.dal import Repository
from articles.datatypes import Article

import pytest

from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio()
async def test_repository_update(session: AsyncSession) -> None:
    """Testing DAL Repository method get.

    :param session: SQLAlchemy session object.
    """
    async with session, session.begin():
        res = await session.execute(
            "INSERT INTO articles (topic, text) VALUES ('some topic', 'some text')",
        )

    async with session, session.begin():
        await Repository(session).update(
            res.lastrowid, Article(
                topic="Marge Sympson story",
                text="Something about Marge"
            )
        )

    async with session:
        found = await session.execute(
            "SELECT topic, text, ISNULL(updated) FROM articles WHERE article_id=:id",
            {"id": res.lastrowid},
        )

    assert found.fetchall() == [("Marge Sympson story", "Something about Marge", 0)]

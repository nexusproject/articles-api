"""Tests for DAL Repository update.

Author: Dmitry Sergeev <realnexusway@gmail.com>
"""

from datetime import datetime

from articles import Article
from articles.dal.repository import Repository

import pytest

import sqlalchemy


@pytest.mark.asyncio()
async def test_repository_get(session: sqlalchemy.orm.Session) -> None:
    """Testing DAL Repository method get.

    :param session: SQLAlchemy session object.
    """
    async with session, session.begin():
        res = await session.execute(
            "INSERT INTO articles (topic, text) " "VALUES ('some topic', 'some text')",
        )

    rowid = res.lastrowid

    await Repository().update(
        rowid, Article(topic="Marge Sympson story", text="Something about Marge")
    )

    async with session:
        found = await session.execute(
            "SELECT topic, text, ISNULL(updated) FROM articles WHERE article_id=:id",
            {"id": rowid},
        )

    assert found.fetchall() == [("Marge Sympson story", "Something about Marge", 0)]

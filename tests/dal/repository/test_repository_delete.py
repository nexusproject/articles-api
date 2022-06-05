"""Tests for DAL Repository delete.

Author: Dmitry Sergeev <realnexusway@gmail.com>
"""

from articles.dal.repository import Repository

import pytest

import sqlalchemy


@pytest.mark.asyncio()
async def test_repository_delete(session: sqlalchemy.orm.Session) -> None:
    """Testing DAL Repository method delete.

    :param session: SQLAlchemy session object.
    """
    async with session, session.begin():
        res = await session.execute(
            "INSERT INTO articles (topic, text) VALUES ('some topic', 'some text')"
        )

    await Repository(session).delete(res.lastrowid)

    async with session:
        found = await session.execute(
            "SELECT count(1) FROM articles WHERE article_id=:id",
            {"id": res.lastrowid},
        )

    assert found.scalars().one() == 0

"""Tests for DAL Repository insert.

Author: Dmitry Sergeev <realnexusway@gmail.com>
"""

from datetime import datetime

from articles import Article
from articles.dal.repository import Repository

import pytest

import sqlalchemy


@pytest.mark.asyncio()
async def test_repository_get(session: sqlalchemy.orm.Session) -> None:
    """Testing DAL Repository method insert.

    :param session: SQLAlchemy session object.
    """
    article = Article(
        topic = 'Bart Sympson story',
        text = 'expected text'
    )

    await Repository().insert(article)


    async with session, session.begin():
        found = await session.execute(
            "SELECT topic, text FROM articles WHERE topic=:topic",
            {"topic": "Bart Sympson story"},
        )

    assert found.fetchall() == [('Bart Sympson story', 'expected text')]

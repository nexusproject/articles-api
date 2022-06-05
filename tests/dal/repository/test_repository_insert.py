"""Tests for DAL Repository insert.

Author: Dmitry Sergeev <realnexusway@gmail.com>
"""

from datetime import datetime

from articles.types import Article
from articles.dal.repository import Repository

import pytest

from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio()
async def test_repository_insert(session: AsyncSession) -> None:
    """Testing DAL Repository method insert.

    :param session: SQLAlchemy session object.
    """
    article = Article(
        topic = 'Bart Sympson story',
        text = 'expected text'
    )

    async with session, session.begin():
        await Repository(session).insert(article)


    async with session, session.begin():
        found = await session.execute(
            "SELECT topic, text FROM articles WHERE topic=:topic",
            {"topic": "Bart Sympson story"},
        )

    assert found.fetchall() == [('Bart Sympson story', 'expected text')]

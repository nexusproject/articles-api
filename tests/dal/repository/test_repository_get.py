"""Tests for DAL Repository get.

Author: Dmitry Sergeev <realnexusway@gmail.com>
"""

from datetime import datetime

from articles.types import ArticleEntry
from articles.dal.repository import Repository

import pytest

from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio()
async def test_repository_get(session: AsyncSession) -> None:
    """Testing DAL Repository method get.

    :param session: SQLAlchemy session object.
    """
    dt_created = datetime(2021, 6, 4, 14, 58, 58)
    dt_updated = datetime(2022, 6, 4, 14, 58, 58)

    async with session, session.begin():
        res = await session.execute(
            "INSERT INTO articles (topic, text, created, updated) "
            "VALUES ('expected topic', 'expected text', :dt_cr, :dt_up)",
            {"dt_cr": dt_created, "dt_up": dt_updated},
        )


    async with session:
        assert await Repository(session).get(res.lastrowid) == ArticleEntry(
            topic="expected topic",
            text="expected text",
            article_id=res.lastrowid,
            created=dt_created,
            updated=dt_updated,
        )

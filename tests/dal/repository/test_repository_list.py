"""Tests for DAL Repository list.

Author: Dmitry Sergeev <realnexusway@gmail.com>
"""

from articles.dal.repository import Repository

import pytest

import sqlalchemy


@pytest.fixture(autouse=True)
async def _prepare_data(session: sqlalchemy.orm.Session) -> None:
    """Prepare data for test.

    :param session: SQLAlchemy session object.
    """
    entries = [
        {
            "topic": "topic c",
            "text": "text c",
            "created": "2022-06-04 01:01:01",
            "updated": "2022-06-05 03:03:03",
        },
        {
            "topic": "topic b",
            "text": "text b",
            "created": "2022-06-04 03:03:03",
            "updated": "2022-06-05 02:02:02",
        },
        {
            "topic": "topic a",
            "text": "text a",
            "created": "2022-06-04 02:02:02",
            "updated": "2022-06-05 01:01:01",
        },
    ]

    async with session, session.begin():
        for entry in entries:
            await session.execute(
                "INSERT INTO articles (topic, text, created, updated) "
                "VALUES (:topic, :text, :created, :updated)",
                entry,
            )


@pytest.mark.asyncio()
async def test_repository_list_sort(session: sqlalchemy.orm.Session) -> None:
    """Testing DAL Repository sort options in method list.

    :param session: SQLAlchemy session object.
    """
    found = await Repository().list()
    assert [entry.topic for entry in found] == ["topic c", "topic b", "topic a"]

    found = await Repository().list(sort_by="created", sort_order="asc")
    assert [entry.topic for entry in found] == ["topic c", "topic a", "topic b"]

    found = await Repository().list(sort_by="created", sort_order="desc")
    assert [entry.topic for entry in found] == ["topic b", "topic a", "topic c"]

    found = await Repository().list(sort_by="updated")
    assert [entry.topic for entry in found] == ["topic a", "topic b", "topic c"]

    found = await Repository().list(sort_by="topic")
    assert [entry.topic for entry in found] == ["topic a", "topic b", "topic c"]

    found = await Repository().list(sort_by="topic", sort_order="desc")
    assert [entry.topic for entry in found] == ["topic c", "topic b", "topic a"]


@pytest.mark.asyncio()
async def test_repository_list_from(session: sqlalchemy.orm.Session) -> None:
    """Testing DAL Repository date_from option in method list.

    :param session: SQLAlchemy session object.
    """
    found = await Repository().list(from_date="2022-06-04 02:02:02")
    assert [entry.topic for entry in found] == ["topic a", "topic b"]

    found = await Repository().list(from_date="2022-06-04 03:03:03")
    assert [entry.topic for entry in found] == ["topic b"]


@pytest.mark.asyncio()
async def test_repository_list_page(session: sqlalchemy.orm.Session) -> None:
    """Testing DAL Repository page options in method list.

    :param session: SQLAlchemy session object.
    """
    found = await Repository().list(sort_by="updated", page_size=2)
    assert [entry.topic for entry in found] == ["topic a", "topic b"]

    found = await Repository().list(sort_by="updated", page=1, page_size=2)
    assert [entry.topic for entry in found] == ["topic c"]

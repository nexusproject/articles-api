"""Tests for the list request.

Author: Dmitry Sergeev <realnexusway@gmail.com>
"""

from datetime import datetime
from unittest.mock import AsyncMock

import articles
from articles import ArticleEntry
from articles.api.schema import ReplyList

from httpx import AsyncClient

import pytest


@pytest.mark.asyncio()
async def test_list_success() -> None:
    """Tests that the repository is calls properly and the response."""
    from_date = datetime.now()

    article = ArticleEntry(
        article_id=123,
        topic="expected topic",
        text="expected text",
        updated=None,
        created=from_date,
    )

    articles.api.Repository.list = AsyncMock(return_value=[article, article])

    async with AsyncClient(app=articles.api.app, base_url="http://localhost") as ac:
        response = await ac.get(
            f"/articles/v1/list?from_date={from_date.isoformat()}&"
            "sort_order=desc&sort_by=created&page=1&page_size=33"
        )

    articles.api.Repository.list.assert_called_with(
        from_date=from_date,
        sort_by='created',
        sort_order='desc',
        page=1,
        page_size=33
    )
    assert response.status_code == 200

    expected = ReplyList(success=True, payload=[article, article]).dict()
    # We need to patch datetime object to string representaion
    for article in expected['payload']:
        article['created'] = article['created'].isoformat()

    assert response.json() == expected

"""Tests for the update request hook.

Author: Dmitry Sergeev <realnexusway@gmail.com>
"""

from unittest.mock import AsyncMock, patch

import articles
from articles import Article
from articles.api.schema import Reply

from httpx import AsyncClient

import pytest


@pytest.mark.asyncio()
async def test_update_success() -> None:
    """Tests that the repository is calls properly and the response."""
    article = Article(
        topic="expected topic",
        text="expected text",
    )

    with patch(
        "articles.dal.repository.Repository.update",
        new_callable=AsyncMock,
    ):
        async with AsyncClient(app=articles.api.app, base_url="http://localhost") as ac:
            response = await ac.patch("/articles/v1/update/123", content=article.json())

        articles.api.Repository.update.assert_called_with(123, article)
        assert response.status_code == 200
        assert response.json() == Reply(success=True).dict()

        articles.api.Repository.update.reset_mock()


@pytest.mark.asyncio()
async def test_update_failed() -> None:
    """Tests answer for wrong request."""
    with patch(
        "articles.dal.repository.Repository.update",
        new_callable=AsyncMock,
    ):
        async with AsyncClient(app=articles.api.app, base_url="http://localhost") as ac:
            response = await ac.patch(
                "/articles/v1/update/123", data={"wrong": "request"}
            )

        assert response.status_code == 422
        assert response.reason_phrase == "Unprocessable Entity"

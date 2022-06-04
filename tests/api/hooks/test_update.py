"""Tests for the create request hook.

Author: Dmitry Sergeev <realnexusway@gmail.com>
"""

from unittest.mock import AsyncMock

import articles
from articles import Article
from articles.api.schema import Reply

from httpx import AsyncClient

import pytest


@pytest.mark.asyncio()
async def test_create_success() -> None:
    """Tests that the repository is calls properly and the response."""
    article = Article(
        topic="expected topic",
        text="expected text",
    )

    articles.api.Repository.update = AsyncMock()

    async with AsyncClient(app=articles.api.app, base_url="http://localhost") as ac:
        response = await ac.patch("/articles/v1/update/123", content=article.json())

    articles.api.Repository.update.assert_called_with(123, article)
    assert response.status_code == 200
    assert response.json() == Reply(success=True).dict()


@pytest.mark.asyncio()
async def test_create_failed() -> None:
    """Tests answer for wrong request."""
    articles.api.Repository.insert = AsyncMock()

    async with AsyncClient(app=articles.api.app, base_url="http://localhost") as ac:
        response = await ac.patch("/articles/v1/update/123", data={"wrong": "request"})

    assert response.status_code == 422
    assert response.reason_phrase == "Unprocessable Entity"

"""Tests for the update request hook.

Author: Dmitry Sergeev <realnexusway@gmail.com>
"""

from unittest.mock import AsyncMock, patch

import articles
from articles.datatypes import Article
from articles.api.schema import Reply

from httpx import AsyncClient

import pytest


@pytest.mark.asyncio()
async def test_update_success(auth_header) -> None:
    """Tests that the repository is calls properly and the response."""
    article = Article(
        topic="expected topic",
        text="expected text",
    )

    with patch(
        "articles.dal.Repository.update",
        new_callable=AsyncMock,
    ):
        async with AsyncClient(
            app=articles.api.app, base_url="http://localhost", headers=auth_header
        ) as ac:
            response = await ac.patch("/api/v1/article/123", content=article.json())

        articles.dal.Repository.update.assert_called_with(123, article)
        assert response.status_code == 200
        assert response.json() == Reply(success=True).dict()


@pytest.mark.asyncio()
async def test_update_failed(auth_header) -> None:
    """Tests answer for wrong request."""
    with patch(
        "articles.dal.Repository.update",
        new_callable=AsyncMock,
    ):
        async with AsyncClient(
            app=articles.api.app, base_url="http://localhost", headers=auth_header
        ) as ac:
            response = await ac.patch("/api/v1/article/123", data={"wrong": "request"})

        assert response.status_code == 422
        assert response.reason_phrase == "Unprocessable Entity"


@pytest.mark.asyncio()
async def test_update_unauthorized() -> None:
    """Tests answer on unauthorized request."""
    wrong_h = {"Authorization": "wrong_key"}

    with patch(
        "articles.dal.Repository.update",
        new_callable=AsyncMock,
    ):
        async with AsyncClient(
            app=articles.api.app, base_url="http://localhost", headers=wrong_h
        ) as ac:
            response = await ac.patch("/api/v1/article/123")

        assert response.status_code == 401
        assert response.reason_phrase == "Unauthorized"

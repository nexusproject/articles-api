"""Tests for the create request hook.

Author: Dmitry Sergeev <realnexusway@gmail.com>
"""

from unittest.mock import AsyncMock, patch

import articles
import articles.api.auth
from articles.api.schema import Reply
from articles.datatypes import Article

from httpx import AsyncClient

import pytest


@pytest.mark.asyncio()
async def test_create_success(auth_header: dict) -> None:
    """Tests that the repository is calls properly and the response.

    :param auth_header: Patched auth header from fixture
    """
    article = Article(
        topic="expected topic",
        text="expected text",
    )

    with patch("articles.dal.Repository.insert", new_callable=AsyncMock):
        async with AsyncClient(
            app=articles.api.app, base_url="http://localhost", headers=auth_header
        ) as ac:
            response = await ac.post("/api/v1/create", content=article.json())

        articles.dal.Repository.insert.assert_called_with(article)
        assert response.status_code == 200
        assert response.json() == Reply(success=True).dict()


@pytest.mark.asyncio()
async def test_create_failed(auth_header: dict) -> None:
    """Tests answer for wrong request.

    :param auth_header: Patched auth header from fixture
    """
    with patch("articles.dal.repository.Repository.insert", new_callable=AsyncMock):
        async with AsyncClient(
            app=articles.api.app, base_url="http://localhost", headers=auth_header
        ) as ac:
            response = await ac.post("/api/v1/create", data={"wrong": "request"})

        assert response.status_code == 422
        assert response.reason_phrase == "Unprocessable Entity"


@pytest.mark.asyncio()
async def test_create_unauthorized() -> None:
    """Tests answer for unauthorized request."""
    wrong_h = {"Authorization": "wrong_key"}

    with patch("articles.dal.repository.Repository.insert", new_callable=AsyncMock):
        async with AsyncClient(
            app=articles.api.app, base_url="http://localhost", headers=wrong_h
        ) as ac:
            response = await ac.post("/api/v1/create")

        assert response.status_code == 401
        assert response.reason_phrase == "Unauthorized"

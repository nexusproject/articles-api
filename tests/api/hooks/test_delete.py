"""Tests for the delete request.

Author: Dmitry Sergeev <realnexusway@gmail.com>
"""

from unittest.mock import AsyncMock, patch

import articles
from articles.api.schema import Reply, ReplyFailed
from articles.dal.repository import RepositoryException

from httpx import AsyncClient

import pytest


@pytest.mark.asyncio()
async def test_delete_success(auth_header) -> None:
    """Tests that the repository is calls properly and the response."""
    with patch("articles.dal.Repository.delete", new_callable=AsyncMock):
        async with AsyncClient(
            app=articles.api.app, base_url="http://localhost", headers=auth_header
        ) as ac:
            response = await ac.delete("/api/v1/article/123")

        articles.dal.Repository.delete.assert_called_with(123)

        assert response.status_code == 200

        assert response.json() == Reply(success=True).dict()


@pytest.mark.asyncio()
async def test_delete_failed(auth_header) -> None:
    """Tests the response if the reposithory raises an exception."""
    with patch(
        "articles.dal.Repository.delete",
        new_callable=AsyncMock,
        side_effect=RepositoryException("expected message"),
    ):
        async with AsyncClient(
            app=articles.api.app, base_url="http://localhost", headers=auth_header
        ) as ac:
            response = await ac.delete("/api/v1/article/123")

        assert response.status_code == 418

        assert (
            response.json()
            == ReplyFailed(success=False, error="expected message").dict()
        )

@pytest.mark.asyncio()
async def test_delete_unauthorized() -> None:
    """Tests the response on unauthorized request."""
    wrong_h = {"Authorization": "wrong_key"}

    with patch(
        "articles.dal.Repository.delete",
        new_callable=AsyncMock,
        side_effect=RepositoryException("expected message"),
    ):
        async with AsyncClient(
            app=articles.api.app, base_url="http://localhost", headers=wrong_h
        ) as ac:
            response = await ac.delete("/api/v1/article/123")

        assert response.status_code == 401
        assert response.reason_phrase == "Unauthorized"

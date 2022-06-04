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
async def test_delete_success() -> None:
    """Tests that the repository is calls properly and the response."""
    with patch("articles.dal.repository.Repository.delete", new_callable=AsyncMock):
        async with AsyncClient(app=articles.api.app, base_url="http://localhost") as ac:
            response = await ac.delete("/articles/v1/delete/123")

        articles.api.Repository.delete.assert_called_with(123)
        assert response.status_code == 200

        assert response.json() == Reply(success=True).dict()

        articles.api.Repository.delete.reset_mock()


@pytest.mark.asyncio()
async def test_delete_failed() -> None:
    """Tests the response if the reposithory raises an exception."""
    with patch(
        "articles.dal.repository.Repository.delete",
        new_callable=AsyncMock,
        side_effect=RepositoryException("expected message"),
    ):
        async with AsyncClient(app=articles.api.app, base_url="http://localhost") as ac:
            response = await ac.delete("/articles/v1/delete/123")

        assert response.status_code == 418

        assert response.json() == ReplyFailed(
            success=False,
            error="expected message"
        ).dict()

        articles.api.Repository.delete.reset_mock()

"""Conftest file for API hooks tests.

Author: Dmitry Sergeev <realnexusway@gmail.com>
"""

import articles.api.auth

import pytest


@pytest.fixture(autouse=True, scope="session")
def auth_header() -> dict:
    """Pytest fixture for auth.

    Patching defined auth key and returns headers.

    :returns: Auth header for testing
    """
    articles.api.auth.KEY = "expected_key"

    return {"Authorization": "expected_key"}

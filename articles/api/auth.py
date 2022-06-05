"""Very simple authenication.

Author: Dmitry Sergeev <realnexusway@gmail.com>
"""

from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader

KEY = "some_hardcoded_token"
api_key_header = APIKeyHeader(name="Authorization", auto_error=True)


async def get_api_key(api_key: str = Security(api_key_header)) -> str:
    """Very simple authenication.

    :param api_key: Permanent token string
    :raises HTTPException: HTTPException
    :returns: Token string
    """
    if not api_key == KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden"
        )

    return api_key

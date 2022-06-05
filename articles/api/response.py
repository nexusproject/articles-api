"""API response object.

Author: Dmitry Sergeev <realnexusway@gmail.com>
"""

from starlette.responses import JSONResponse


class MyResponse(JSONResponse):
    """Here we can easely change response."""

    pass

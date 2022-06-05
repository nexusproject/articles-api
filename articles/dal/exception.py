"""DAL Exception.

Author: Dmitry Sergeev <realnexusway@gmail.com>
"""


class DALException(Exception):
    """Dal exception."""

    def __init__(self, message: str):  # noqa: D107, ANN101, ANN204
        self.message = message

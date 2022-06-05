"""API replies schema.

Author: Dmitry Sergeev <realnexusway@gmail.com>
"""

from typing import Optional

from articles.datatypes import ArticleEntry

from pydantic import BaseModel


class Reply(BaseModel):
    """Base reply."""

    success: bool


class ReplyFailed(Reply):
    """Failed reply."""

    success: bool = False
    error: Optional[str] = None


class ReplyList(Reply):
    """Reply with list of articles."""

    payload: list[ArticleEntry]


class ReplyOne(Reply):
    """Reply with single article."""

    article: ArticleEntry

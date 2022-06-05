"""Main domain objects.

Author: Dmitry Sergeev <realnexusway@gmail.com>
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Article(BaseModel):
    """Common article object."""

    topic: str
    text: str

    class Config:  # noqa: D106
        orm_mode = True


class ArticleEntry(Article):
    """Article entry object."""

    article_id: int
    updated: Optional[datetime]
    created: datetime

    class Config:  # noqa: D106
        orm_mode = True

from datetime import datetime

from typing import Union, Optional

from pydantic import BaseModel

class Article(BaseModel):
    """Common article object."""
    topic: str
    text: str

    class Config:
        orm_mode = True

class ArticleEntry(Article):
    """Article entry object."""
    article_id: int
    updated: Optional[datetime]
    created: datetime

    class Config:
        orm_mode = True

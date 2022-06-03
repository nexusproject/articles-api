#
#
from datetime import datetime
from typing import Union, Optional, Literal
from pydantic import BaseModel
from articles import ArticleEntry


class Reply(BaseModel):
    success: bool

class ReplyFailed(Reply):
    success: bool = False
    error: Optional[str] = None

class ReplyList(Reply):
    payload: list[ArticleEntry]

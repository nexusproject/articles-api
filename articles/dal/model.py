"""DAL models.

Author: Dmitry Sergeev <realnexusway@gmail.com>
"""

from sqlalchemy import BigInteger, Column, DateTime, String, func
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Article(Base):  # type: ignore
    """Article ORM model."""

    __tablename__ = "articles"

    article_id = Column(BigInteger, primary_key=True)
    topic = Column(String)
    text = Column(String)
    created = Column(DateTime, server_default=func.now())
    updated = Column(DateTime)

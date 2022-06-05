"""DAL Repository object.

Author: Dmitry Sergeev <realnexusway@gmail.com>
"""

from datetime import datetime
from typing import Optional

from articles.datatypes import ArticleEntry

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .exception import DALException
from .model import Article


class RepositoryException(DALException):
    """Repository exception."""

    pass


class Repository:
    """Articles repository.

    XXX: Definitely using ORM and Sessions here is unnecessarily.
    Simple tablemodule pattern is enough in this task, but
    i do this because this is a demo project.
    """

    def __init__(self, session: AsyncSession):
        """Repository init.

        :param session: SQLAlchemy AsyncSession
        """
        self.session = session

    async def has(self, article_id: int) -> bool:
        """Check for article presence.

        :param article_id: ID of article
        :returns: Bool value
        """
        has = await self.session.execute(
            select(Article.article_id)
            .where(Article.article_id == article_id)
            .with_for_update(read=True)  # LOCK IN SHARE MODE
        )

        return bool(has.first())

    async def insert(self, article: Article) -> None:
        """Insert.

        :param article: Article object
        """
        self.session.add(Article(**article.dict()))

    async def update(self, article_id: int, article: Article) -> None:
        """Update.

        :param article_id: ID of article
        :param article: Article object
        :raises RepositoryException: Raises if article absent.
        """
        if not await self.has(article_id):
            raise RepositoryException(f"No article ID {article_id}. Cant UPDATE.")

        await self.session.execute(
            update(Article)
            .where(Article.article_id == article_id)
            .values(**article.dict(), updated=datetime.now())
        )

    async def delete(self, article_id: int) -> None:
        """Delete.

        :param article_id: ID of article
        :raises RepositoryException: Raises if article absent.
        """
        if not await self.has(article_id):
            raise RepositoryException(f"No article ID {article_id}. Cant DELETE.")

        await self.session.execute(
            delete(Article).where(Article.article_id == article_id)
        )

    async def get(self, article_id: int) -> ArticleEntry:
        """Get one article by id.

        :param article_id: ID of article
        :returns: ArticleEntry object
        :raises RepositoryException: Raises if article absent.
        """
        found = await self.session.execute(
            select(Article).where(Article.article_id == article_id)
        )

        if article := found.scalars().one_or_none():  # noqa: SIM106
            return ArticleEntry.from_orm(article)
        else:
            raise RepositoryException(f"No article ID {article_id}. Cant GET.")

    async def list(
        self,
        from_date: Optional[datetime] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "asc",
        page: int = 0,
        page_size: int = 10
    ) -> list[ArticleEntry]:
        """Get list of articles by given parameters.

        :param from_date: Optional start date
        :param sort_by: Field to sort. Should be one of topic/created/updated
        :param sort_order: Sort order. Should be asc/desc
        :param page: Page number. Default 0
        :param page_size: Page size
        :returns: List of ArticleEntry objects
        """
        stmt = select(Article)

        if from_date:
            stmt = stmt.where(Article.created >= from_date)

        if sort_by:
            if sort_by == "created":
                if sort_order and sort_order == "desc":
                    stmt = stmt.order_by(Article.created.desc())
                else:
                    stmt = stmt.order_by(Article.created.asc())
            elif sort_by == "updated":
                if sort_order and sort_order == "desc":
                    stmt = stmt.order_by(Article.updated.desc())
                else:
                    stmt = stmt.order_by(Article.updated.asc())
            elif sort_by == "topic":
                if sort_order and sort_order == "desc":
                    stmt = stmt.order_by(Article.topic.desc())
                else:
                    stmt = stmt.order_by(Article.topic.asc())

        stmt = stmt.limit(page_size).offset(page * page_size)

        found = await self.session.execute(stmt)

        return [ArticleEntry.from_orm(entry) for entry in found.scalars()]

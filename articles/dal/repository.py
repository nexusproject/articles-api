#
#

from .db import async_session
from .model import Article
from articles import ArticleEntry
from sqlalchemy import update, exists, select, delete
from pprint import pprint as p
from datetime import datetime

class RepositoryException(Exception):
    def __init__(self, message: str):
        self.message = message


class Repository:
    """Articles repository.

    XXX: Definitely using ORM and Sessions here is unnecessarily.
    Simple tablemodule pattern is enough in this task, but
    i do this because this is a demo project.
    """

    def __init__(self):
        self.async_session = async_session()

    async def _has(self, session, article_id) -> bool:
        has = await session.execute(
            select(Article.article_id)
            .where(Article.article_id == article_id)
            .with_for_update(read=True)  # LOCK IN SHARE MODE
        )

        return bool(has.first())

    async def insert(self, article):
        """Insert."""
        async with self.async_session() as session, session.begin():
            session.add(Article(**article.dict()))

    async def update(self, article_id, article):
        """Update."""
        async with self.async_session() as session, session.begin():
            if not await self._has(session, article_id):
                raise RepositoryException(f"No article ID {article_id}. Cant UPDATE.")

            await session.execute(
                update(Article)
                .where(Article.article_id == article_id)
                .values(**article.dict(), updated=datetime.now())
            )

    async def delete(self, article_id):
        """Delete."""
        async with self.async_session() as session, session.begin():
            if not await self._has(session, article_id):
                raise RepositoryException(f"No article ID {article_id}. Cant DELETE.")

            await session.execute(
                delete(Article).where(Article.article_id == article_id)
            )

    async def get(self, article_id):
        """Get one article by id."""
        async with self.async_session() as session, session.begin():
            found = await session.execute(
                select(Article).where(Article.article_id == article_id)
            )

            if article:=found.scalars().one_or_none():
                return ArticleEntry.from_orm(article)
            else:
                raise RepositoryException(f"No article ID {article_id}. Cant GET.")


    async def list(self, from_date, sort_by, sort_order, page, page_size):
        async with self.async_session() as session, session.begin():
            stmt = select(Article)

            if from_date:
                stmt = stmt.where(Article.created >= from_date)

            if sort_by:
                if sort_by=='created':
                    if sort_order and sort_order=='desc':
                        stmt = stmt.order_by(Article.created.desc())
                elif sort_by=='updated':
                    if sort_order and sort_order=='desc':
                        stmt = stmt.order_by(Article.updated.desc())
                    else:
                        stmt = stmt.order_by(Article.updated.asc())
                elif sort_by=='topic':
                    if sort_order and sort_order=='desc':
                        stmt = stmt.order_by(Article.topic.desc())
                    else:
                        stmt = stmt.order_by(Article.topic.asc())

            stmt = stmt.limit(page_size).offset(page*page_size)

            found = await session.execute(stmt)

            return [ArticleEntry.from_orm(entry) for entry in found.scalars()]


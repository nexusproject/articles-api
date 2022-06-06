"""API hooks.

Author: Dmitry Sergeev <realnexusway@gmail.com>
"""

from datetime import datetime
from typing import Literal, Optional

import articles.dal as dal
from articles.datatypes import Article

from fastapi import Depends, FastAPI, Request
from fastapi.security.api_key import APIKey

from sqlalchemy.ext.asyncio.session import AsyncSession

from .auth import get_api_key
from .response import MyResponse
from .schema import Reply, ReplyFailed, ReplyList, ReplyOne


app = FastAPI()


@app.on_event("startup")
async def startup_event() -> None:
    """Startup hook."""
    await dal.check_connection()


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown hook."""
    await dal.shutdown()


@app.exception_handler(dal.DALException)
async def exception_handler(request: Request, exc: dal.DALException) -> MyResponse:
    """Exception handler.

    :param request: FastApi Request object
    :param exc: Exception
    :returns: Response object
    """
    return MyResponse(
        ReplyFailed(success=False, error=exc.message).dict(), status_code=418
    )


@app.post("/api/v1/create", response_class=MyResponse, response_model=Reply)
async def create(
    article: Article,
    _: APIKey = Depends(get_api_key),
    session: AsyncSession = Depends(dal.async_session),
) -> Reply:
    """Create article request hook.

    :param article: Article object
    :param session: SQLAlchemy AsyncSession
    :returns: Reply object
    """
    async with session, session.begin():
        await dal.Repository(session).insert(article)

        return Reply(success=True)


@app.patch(
    "/api/v1/article/{article_id}",
    response_class=MyResponse,
    response_model=Reply,
    responses={418: {"model": ReplyFailed}},
)
async def update(
    article: Article,
    article_id: int,
    _: APIKey = Depends(get_api_key),
    session: AsyncSession = Depends(dal.async_session),
) -> Reply:
    """Update article.

    :param article: Article object
    :param article_id: Article ID
    :param session: SQLAlchemy AsyncSession
    :returns: Reply object
    """
    async with session, session.begin():
        await dal.Repository(session).update(article_id, article)

        return Reply(success=True)


@app.delete(
    "/api/v1/article/{article_id}",
    response_class=MyResponse,
    response_model=Reply,
    responses={418: {"model": ReplyFailed}},
)
async def delete(
    article_id: int,
    _: APIKey = Depends(get_api_key),
    session: AsyncSession = Depends(dal.async_session),
) -> Reply:
    """Delete article.

    :param article_id: Article ID
    :param session: SQLAlchemy AsyncSession
    :returns: Reply object
    """
    async with session, session.begin():
        await dal.Repository(session).delete(article_id)

        return Reply(success=True)


@app.get(
    "/api/v1/article/{article_id}",
    response_class=MyResponse,
    response_model=ReplyOne,
    responses={418: {"model": ReplyFailed}},
)
async def get(
    article_id: int,
    session: AsyncSession = Depends(dal.async_session),
) -> ReplyOne:
    """Get single article.

    :param article_id: Article ID
    :param session: SQLAlchemy AsyncSession
    :returns: ReplyOne object
    """
    async with session:
        return ReplyOne(
            success=True,
            article=await dal.Repository(session).get(article_id),
        )


@app.get(
    "/api/v1/list",
    response_class=MyResponse,
    response_model=ReplyList,
)
async def list(
    from_date: Optional[datetime] = None,
    sort_by: Optional[Literal["created", "updated", "topic"]] = None,
    sort_order: Optional[Literal["asc", "desc"]] = None,
    page: Optional[int] = 0,
    page_size: int = 3,
    session: AsyncSession = Depends(dal.async_session),
) -> ReplyList:
    """Get list of articles for given parameters.

    :param from_date: Optional start date
    :param sort_by: Field to sort. Should be one of topic/created/updated
    :param sort_order: Sort order. Should be asc/desc
    :param page: Page number. Default 0
    :param page_size: Page size
    :param session: SQLAlchemy AsyncSession
    :returns: ReplyList object
    """
    async with session:
        return ReplyList(
            success=True,
            payload=await dal.Repository(session).list(
                from_date=from_date,
                sort_by=sort_by,
                sort_order=sort_order,
                page=page,
                page_size=page_size,
            ),
        )

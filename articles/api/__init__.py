from typing import Optional, Union, Literal
from datetime import datetime

from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse

from articles.dal.repository import Repository, RepositoryException
from .response import MyResponse

from pprint import pprint as p
from pydantic import BaseModel

from .schema import Reply, ReplyFailed, ReplyList
from articles import Article, ArticleEntry


app = FastAPI()


@app.exception_handler(RepositoryException)
async def unicorn_exception_handler(request: Request, exc: RepositoryException):
    return MyResponse(
        ReplyFailed(success=False, error=exc.message).dict(), status_code=418
    )


@app.post("/articles/v1/create", response_class=MyResponse, response_model=Reply)
async def create(article: Article, repository: Repository = Depends(Repository)):
    print("--> create")
    await repository.insert(article)

    return Reply(success=True)


@app.patch(
    "/articles/v1/update/{article_id}",
    response_class=MyResponse,
    response_model=Reply,
    responses={418: {"model": ReplyFailed}},
)
async def update(
    article: Article, article_id: int, repository: Repository = Depends(Repository)
):
    """Update article.

    :param article: Article object
    :param article_id: Article ID
    :param repository: Repository object
    """
    await repository.update(article_id, article)

    return Reply(success=True)


@app.delete(
    "/articles/v1/delete/{article_id}", response_class=MyResponse, response_model=Reply
)
async def delete(article_id: int, repository: Repository = Depends(Repository)):
    """Delete article.

    :param article_id: Article ID
    :param repository: Repository object
    """
    await repository.delete(article_id)

    return Reply(success=True)


@app.get(
    "/articles/v1/list",
    response_class=MyResponse,
    response_model=ReplyList,
    status_code=200,
)
async def list(
    from_date: Optional[datetime] = None,
    sort_by: Optional[Literal['created', 'updated', 'topic']] = None,
    sort_order: Optional[Literal['asc', 'desc']] = None,
    page: Optional[int] = 0,
    page_size: int = 3,
    repository: Repository = Depends(Repository)
):
    return ReplyList(
        success=True,
        payload=await repository.list(from_date, sort_by, sort_order, page, page_size)
    )

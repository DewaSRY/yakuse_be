from typing import Annotated

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status

from app.libs.sql_alchemy_lib import get_db
from app.libs.jwt_lib.jwt_dto import TokenPayLoad
from app.libs.jwt_lib.jwt_service import get_jwt_pyload

from . import article_dtos, article_services

router = APIRouter(
    tags=["article"],
    prefix="/article",
)


@router.post("/",
             response_model=article_dtos.ArticleResponseDto,
             status_code=status.HTTP_201_CREATED)
def create_article(
    article: article_dtos.ArticleCreateDto,
    jwt_token: Annotated[TokenPayLoad, Depends(get_jwt_pyload)],
    db: Session = Depends(get_db),
):
    return article_services \
        .create_article(db, article, jwt_token.id).unwrap()


@router.get("/all",
            response_model=list[article_dtos.ArticleResponseDto],
            status_code=status.HTTP_200_OK)
def get_all_articles(
    jwt_token: Annotated[TokenPayLoad, Depends(get_jwt_pyload)],
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10
):
    return article_services \
        .get_all_articles(db, skip, limit).unwrap()


@router.get("/search/{keyword}",
            response_model=list[article_dtos.ArticleResponseDto],
            status_code=status.HTTP_200_OK)
def search_articles(
    keyword: str,
    jwt_token: Annotated[TokenPayLoad, Depends(get_jwt_pyload)],
    db: Session = Depends(get_db)
):
    return article_services.search_articles_by_title(db, keyword).unwrap()


@router.get("/category/{category_name}",
            response_model=list[article_dtos.ArticleResponseDto],
            status_code=status.HTTP_200_OK)
def get_articles_by_category_name(
    category_name: str,
    jwt_token: Annotated[TokenPayLoad, Depends(get_jwt_pyload)],
    db: Session = Depends(get_db)
):
    return article_services \
        .get_articles_by_category_name(db, category_name).unwrap()
        


@router.get("/my-articles",
            response_model=list[article_dtos.ArticleResponseDto],
            status_code=status.HTTP_200_OK)
def get_all_my_articles(
    jwt_token: Annotated[TokenPayLoad, Depends(get_jwt_pyload)],
    db: Session = Depends(get_db)
):
    return article_services \
        .get_my_articles(db, jwt_token.id).unwrap()


@router.get("/{author_id}/articles",
            response_model=list[article_dtos.ArticleResponseDto],
            status_code=status.HTTP_200_OK)
def get_articles_by_author_id(
    author_id: str,
    jwt_token: Annotated[TokenPayLoad, Depends(get_jwt_pyload)],
    db: Session = Depends(get_db)
):
    return article_services \
        .get_articles_by_author_id(db, author_id).unwrap()


@router.get("detail/{article_id}",
            response_model=article_dtos.ArticleResponseDto,
            status_code=status.HTTP_200_OK)
def get_article_detail_by_id(
    article_id: str,
    jwt_token: Annotated[TokenPayLoad, Depends(get_jwt_pyload)],
    db: Session = Depends(get_db)
):
    return article_services \
        .get_article_by_id(db, article_id).unwrap()


@router.put("/my-article/{article_id}",
            response_model=article_dtos.ArticleResponseDto,
            status_code=status.HTTP_200_OK)
async def update_article_by_id(
    article_id: str,
    article_update: article_dtos.ArticleUpdateDto,
    jwt_token: Annotated[TokenPayLoad, Depends(get_jwt_pyload)],
    db: Session = Depends(get_db)
):
    return article_services \
        .update_article_by_id(db, jwt_token.id, article_id, article_update).unwrap()


@router.delete("/delete/my-article/{article_id}",
               status_code=status.HTTP_204_NO_CONTENT)
def delete_article_by_id(
    article_id: str,
    jwt_token: Annotated[TokenPayLoad, Depends(get_jwt_pyload)],
    db: Session = Depends(get_db)
):
    return article_services \
        .delete_article_by_id(db, jwt_token.id, article_id)
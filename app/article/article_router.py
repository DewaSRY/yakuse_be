from typing import Annotated

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status

from app.libs.sql_alchemy_lib import get_db
from app.libs.jwt_lib.jwt_dto import TokenPayLoad
from app.libs.jwt_lib.jwt_service import get_jwt_pyload

from .article_dtos import ArticleCreateDto, ArticleResponseDto
from .article_services import delete_article_by_id_service, create_article_service, get_article_by_user_id_service, get_article_service

router = APIRouter(
    tags=["article"],
    prefix="/article",
)


@router.post("/", response_model=ArticleCreateDto, status_code=status.HTTP_201_CREATED)
async def create_article(
    article: ArticleCreateDto,
    jwt_token: Annotated[TokenPayLoad, Depends(get_jwt_pyload)],
    db: Session = Depends(get_db)
):
    return create_article_service(db, article, jwt_token.id).unwrap()

@router.get("/", response_model=list[ArticleResponseDto], status_code=status.HTTP_200_OK)
async def get_all_our_articles(
    jwt_token: Annotated[TokenPayLoad, Depends(get_jwt_pyload)],
    db: Session = Depends(get_db)
):
    return get_article_by_user_id_service(db, jwt_token.id)

@router.get("/public", response_model=list[ArticleResponseDto], status_code=status.HTTP_200_OK)
async def get_all_public_articles(db: Session = Depends(get_db)):
    return get_article_service(db)

@router.delete("/delete/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article_by_id(
    article_id: str,
    jwt_token: Annotated[TokenPayLoad, Depends(get_jwt_pyload)],
    db: Session = Depends(get_db)
):
    '''still error 500'''
    return delete_article_by_id_service(db, jwt_token.id, article_id)


# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImU3MzA3NjNiLWI1OTctNDM0ZS1hODIwLWM2NDYzZTUxYzA1ZSIsImV4cCI6MTcyMzc5MTEwOX0.8uAQ7krabjyTnDGwwueLv9ezFVvyB5KDbwUrkmtoqo0
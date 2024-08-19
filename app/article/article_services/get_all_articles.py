from typing import Type

from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from app.article.article_model import Article
from app.article import article_dtos

from app.utils.optional import Optional, build


def get_all_articles(db: Session, skip: int = 0, limit: int = 10) -> Optional:
    try:
        articles: list[Type[Article]] = db.query(Article) \
            .order_by(desc(Article.created_at)) \
            .offset(skip) \
            .limit(limit).all()
        
        return build(data=articles)
    except SQLAlchemyError as e:
        return build(error=HTTPException(detail=f"{e}", status_code=status.HTTP_404_NOT_FOUND))
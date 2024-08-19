from typing import Type

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from app.article.article_model import Article
from app.article import article_dtos

from app.utils.optional import Optional, build


def get_article_by_id(db: Session, article_id: str) -> Optional:
    try:
        article = db.query(Article) \
            .filter(Article.id==article_id).first()
        
        return build(data=article)
    except SQLAlchemyError as e:
        return build(error=HTTPException(detail=f"{e}", status_code=status.HTTP_404_NOT_FOUND))
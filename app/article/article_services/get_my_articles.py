from typing import Type

from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from app.article.article_model import Article
from app.article import article_dtos

from app.utils.optional import Optional, build


def get_my_articles(db: Session, author_id: str) -> Optional:
    try:
        articles = db.query(Article) \
            .filter(Article.fk_author_id==author_id) \
            .order_by(desc(Article.created_at)).all()
        
        return build(data=articles)
    except SQLAlchemyError as e:
        return build(error=HTTPException(detail=f"{e}", status_code=status.HTTP_404_NOT_FOUND))
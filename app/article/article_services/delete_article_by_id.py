from typing import Type

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from app.article.article_model import Article
from app.article import article_dtos

from app.utils.optional import Optional, build


def delete_article_by_id(db: Session, author_id: str, article_id: str):
    try:
        article_model = db.query(Article) \
            .filter(Article.fk_author_id==author_id) \
            .filter(Article.id==article_id).first()
        if not article_model:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Article not found')
        db.query(Article) \
            .filter(Article.fk_author_id==author_id) \
            .filter(Article.id==article_id).delete()
        db.commit()
        return
    
    except SQLAlchemyError as e:
        return build(error=HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed to delete article."))
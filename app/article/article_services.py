from typing import Type

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from .article_dtos import ArticleCreateDto
from .article_model import Article

from app.utils.optional import Optional, build


def create_article_service(db: Session, article: ArticleCreateDto, user_id: str) -> Optional:
    try:
        article_model = Article(**article.model_dump())
        article_model.fk_author_id = user_id
        db.add(article_model)
        db.commit()
        return build(data=article_model)
    except SQLAlchemyError:
        return build(error=HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Failed to create article.'))
    
def get_article_by_user_id_service(db: Session, user_id: str) -> list[Type[Article]]:
    return db.query(Article).filter(Article.fk_author_id == user_id).all()

def get_article_service(db: Session, skip: int = 0, limit: int = 100) -> list[Type[Article]]:
    return db.query(Article).offset(skip).limit(limit).all()

def delete_article_by_id_service(db: Session, user_id: str, article_id: str):
    article_model = db.query(Article).filter(Article.fk_author_id == user_id).filter(Article.id == article_id).first()
    if article_model is None:
        raise HTTPException(status_code=404, detail='Article not found.')
    db.query(Article).filter(Article.fk_author_id == user_id).filter(Article.id == article_id).delete()
    db.commit()
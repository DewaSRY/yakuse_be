from typing import Type

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from app.article.article_model import Article
from app.article import article_dtos

from app.utils.optional import Optional, build


def update_article_by_id(
        db: Session, author_id: str, article_id: str,
        article_update: article_dtos.ArticleUpdateDto) -> Optional:
    try:
        article_model = db.query(Article) \
            .filter(Article.fk_author_id==author_id) \
            .filter(Article.id==article_id).first()
        if not article_model:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Article not found.')
        
        article_model.title=article_update.title,
        article_model.desciption=article_update.description,
        article_model.image_url=article_update.image_url,
        article_model.fk_business_category_id=article_update.fk_business_category_id

        db.add(article_model)
        db.commit()

        return build(data=article_model)
    except SQLAlchemyError as e:
        return build(error=HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed to update user need."))
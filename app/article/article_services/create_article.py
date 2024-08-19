from typing import Type

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from app.article.article_model import Article
from app.article import article_dtos

from app.utils.optional import Optional, build


def create_article(db: Session, article: article_dtos.ArticleCreateDto, author_id: str) -> Optional:
    try:
        article_model = Article(
            title=article.title,
            description=article.description,
            image_url=article.image_url,
            fk_business_category_id=article.fk_business_category_id,
            fk_author_id=author_id
        )

        db.add(article_model)
        db.commit()
        db.refresh(article_model)

        return build(data=article_model)
    except SQLAlchemyError as e:
        return build(
            error=HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Failed to create article. {e}"))

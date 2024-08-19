from typing import Type

from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from app.article.article_model import Article
from app.article import article_dtos

from app.utils.optional import Optional, build


def search_articles_by_title(db: Session, keyword: str) -> Optional:
    try:
        articles = db.query(Article) \
            .filter(Article.title.like(f"%{keyword}%")) \
            .order_by(desc(Article.created_at)).all()
        if len(articles) < 1:
            return build(error=HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                             detail="No articles found matching the keyword"))
        
        return build(data=articles)
    
    except SQLAlchemyError as e:
        return build(error=HTTPException(detail=f"{e}",
                                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR))
    except Exception as e:
        return build(error=HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                         detail=f"E: {e}"))

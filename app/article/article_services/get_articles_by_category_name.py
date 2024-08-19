from typing import Type

from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from app.article.article_model import Article
from app.article import article_dtos

from app.utils.optional import Optional, build


def get_articles_by_category_name(db: Session, category_name: str) -> Optional:
    from app.business_category.business_category_model import BusinessCategory

    try:
        business_category_model = db.query(BusinessCategory) \
            .filter(BusinessCategory.name.like(f"%{category_name}%")).first()   
        if not business_category_model:
             return build(error=HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                             detail=f"{category_name} is not valid category"))
        
        articles = db.query(Article) \
            .filter(Article.fk_business_category_id.like(f"%{business_category_model.id}%")) \
            .order_by(desc(Article.created_at)).all()
        if not articles:
            return build(
                error=HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No articles found for this category"
                )
            )
        
        return build(data=articles)
    except SQLAlchemyError as e:
        return build(error=HTTPException(detail=f"{e}", status_code=status.HTTP_404_NOT_FOUND))
    except Exception as e:
        return build(error=HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"E: {e}"))
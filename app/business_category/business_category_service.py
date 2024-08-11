from typing import Type

from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from . import business_category_dtos
from .business_category_model import BusinessCategory

from app.utils import optional


def create_business_category(db: Session, business_category: business_category_dtos.BusinessCategoryCreateDto) -> optional.Optional:
    try:
        business_category_model = BusinessCategory(**business_category.model_dump())
        db.add(business_category_model)
        db.commit()
        return optional.build(data=business_category_model)
    except SQLAlchemyError as e:
        return optional.build(error=HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="failed to create business category"
        ))
    
def get_business_category(db: Session, skip: int = 0, limit: int = 100) -> list[Type[BusinessCategory]]:
    return db.query(BusinessCategory) \
        .offset(skip) \
        .limit(limit) \
        .all()
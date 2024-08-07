from typing import Type

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from . import business_dtos
from .business_model import Business

from app.utils import optional


def create_business(db: Session, business: business_dtos.BusinessCreateDto, user_id) -> optional.Optional:
    try:
        business_model = Business(**business.model_dump())
        business_model.fk_owner_id = user_id
        db.add(business_model)
        db.commit()
        return optional.build(data=business_model)
    except SQLAlchemyError as e:
        return optional.build(error=HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="failed to create business"
        ))


def get_business(db: Session, skip: int = 0, limit: int = 100) -> list[Type[Business]]:
    return db.query(Business) \
        .offset(skip) \
        .limit(limit) \
        .all()


def get_business_by_user_id(db: Session, user_id: str) -> list[Type[Business]]:
    print(user_id)
    return db.query(Business) \
        .filter(Business.fk_owner_id == user_id) \
        .all()

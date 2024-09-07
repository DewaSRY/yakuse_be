from typing import List, Type
import uuid
from sqlalchemy import desc, func, or_
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, UploadFile, status

from app.business_category.business_category_model import BusinessCategory
from app.libs.images_service import create_image_service
from app.user.user_model import UserModel

from app.business import business_dtos
from app.business.business_model import Business
from app.rating.rating_model import Rating

from app.utils import optional


def get_all_business(db: Session, skip: int = 0, limit: int = 15) \
        -> optional.Optional[List[Type[Business]], Exception]:
    try:
        business_model = db.query(Business) \
            .order_by(desc(Business.created_at)) \
            .offset(skip).limit(limit).all()

        if not business_model:
            return optional.build(error=HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No businesses found"
            ))
        return optional.build(data=business_model)
    except SQLAlchemyError as e:
        db.rollback()
        raise optional.build(
            error=HTTPException(status_code=409, detail="Database conflict: " + str(e)))

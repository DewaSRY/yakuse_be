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


def get_all_business_by_user_id(db: Session, user_id: str, skip: int = 0, limit: int = 10) \
        -> optional.Optional[List[Type[Business]], HTTPException]:
    try:
        business_model = db.query(Business) \
            .order_by(desc(Business.created_at)) \
            .filter(Business.fk_owner_id.like(f"%{user_id}%")) \
            .offset(skip).limit(limit).all()

        if business_model:  # if the bisniss is not zero
            return optional.build(data=business_model)
        else:
            return optional.build(
                error=HTTPException(
                    status_code=404, detail="You don't have a business list yet, create your business first!!"))

    except SQLAlchemyError as e:
        return optional.build(error=HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="failed to fetch business"
        ))

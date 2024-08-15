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


def get_detail_business_by_business_id(db: Session, business_id: uuid.UUID) \
        -> optional.Optional[Type[Business], HTTPException]:
    business_id_str = str(business_id)
    try:
        business_model = db.query(Business) \
            .filter(Business.id == business_id_str) \
            .first()

        if business_model is None:
            return optional.build(error=HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"business with id {business_id} not found"
            ))
        return optional.build(data=business_model)

    except SQLAlchemyError as e:
        return optional.build(error=HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="failed to fetch business"
        ))

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


def get_all_business_by_category(db: Session, category_name: str) \
        -> optional.Optional[List[Type[Business]], Exception]:
    try:
        # Mencari semua bisnis berdasarkan kategori
        businesses = db.query(Business).join(Business.business_category) \
            .filter(BusinessCategory.name == category_name).all()

        if businesses is None:
            return optional.build(error=HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No businesses found for this category"
            ))
        return optional.build(data=businesses)

    except SQLAlchemyError as e:
        return optional.build(error=HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Database conflict: {str(e)}"
        ))

    except Exception as e:
        return optional.build(error=HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        ))

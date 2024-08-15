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


async def delete_business_by_id(db: Session, business_id: str, user_id: str) \
        -> optional.Optional[None, Exception]:
    try:
        # Langkah 1: Mencari bisnis yang ada
        business_model = db.query(Business).filter(Business.id == business_id, Business.fk_owner_id == user_id).first()
        if not business_model:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business not found")

        # Langkah 2: Hapus bisnis dari database
        db.delete(business_model)
        db.commit()

        return optional.build(data=None)

    except SQLAlchemyError as e:
        db.rollback()
        return optional.build(error=HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Database conflict: {str(e)}"
        ))

    except Exception as e:
        return optional.build(error=HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        ))

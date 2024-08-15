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


# create-business-with-photo
async def create_business_with_photo(db: Session, business: business_dtos.BusinessCreateDto, user_id: str,
                                     file: UploadFile) -> optional.Optional[Business, Exception]:
    try:
        # Langkah 1: Membuat bisnis
        business_model = Business(**business.model_dump())
        business_model.fk_owner_id = user_id

        # Langkah 2: Upload foto
        opt_content = await create_image_service(upload_file=file, domain="business")

        # Jika upload berhasil, update `photo_url` dalam `business_model`
        business_model.photo_url = opt_content.data

        # Simpan bisnis ke dalam database
        db.add(business_model)
        db.commit()
        db.refresh(business_model)

        return optional.build(data=business_model)

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

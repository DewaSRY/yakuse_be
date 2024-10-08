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
from app.utils.error_parser import find_errr_from_args
from app.utils import optional


# create-business-with-photo
def create_business(
        db: Session, business: business_dtos.BusinessCreateDto, user_id: str, ) \
        -> optional.Optional[Business, Exception]:
    try:
        business_model = Business(**business.model_dump())
        business_model.fk_owner_id = user_id
        db.add(business_model)
        db.commit()
        return optional.build(data=business_model)

    except SQLAlchemyError as e:
        print(e)
        db.rollback()
        return optional.build(error=HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Database conflict: {find_errr_from_args("business", str(e.args))}"
        ))

    except Exception as e:
        print(e)
        return optional.build(error=HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {find_errr_from_args("business", str(e.args))}"
        ))

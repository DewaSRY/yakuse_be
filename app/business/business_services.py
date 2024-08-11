from typing import Type
import uuid
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, UploadFile, status

from app.business_category.business_category_model import BusinessCategory
from app.libs.images_service import create_image_service
from app.user.user_model import UserModel

from . import business_dtos
from .business_model import Business
from app.rating.rating_model import Rating

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


# update-photo-profile
async def upload_photo_business(db: Session, user_id: str, file: UploadFile) -> Business:
    try:
        # Panggil fungsi async dengan await
        opt_content = await create_image_service(upload_file=file, domain="business")

        business = db.query(Business).filter(Business.fk_owner_id == user_id).first()

        if business:
            # Update photo_url di tabel business
            business.photo_url = opt_content.data
            db.commit()
            db.refresh(business)

            return business  # Mengembalikan objek Business tanpa 'await'

        else:
            raise HTTPException(status_code=404, detail="Business not found")

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=409, detail="Database conflict: " + str(e))


# business-edit
def business_edit(db: Session, business: business_dtos.BusinessEdiDto, user_id: str) -> optional.Optional[
    Business, Exception]:
    try:
        business_model = db.query(Business).filter(Business.fk_owner_id == user_id).first()

        if business_model:
            # Data user sudah diisi dari request body melalui parameter 'user'
            for field, value in business.dict().items():
                if value is not None:  # Only update if value is provided
                    setattr(business_model, field, value)

            db.commit()
            db.refresh(business_model)

            return optional.build(data=business_model)

        else:
            raise optional.build(error=HTTPException(status_code=404, detail="User not found"))

    except SQLAlchemyError as e:
        db.rollback()
        raise optional.build(error=HTTPException(status_code=409, detail="Database conflict: " + str(e)))


def get_all_business(db: Session, skip: int = 0, limit: int = 100) -> list[Type[Business]]:
    return db.query(Business) \
        .offset(skip) \
        .limit(limit) \
        .all()


def get_businesses_with_ratings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(
        Business.id,
        Business.name,
        Rating.rating_count
    ) \
        .join(Rating) \
        .offset(skip) \
        .limit(limit) \
        .all()


def get_business_by_user_id(db: Session, user_id: str) -> list[Type[Business]]:
    print(user_id)
    return db.query(Business) \
        .filter(Business.fk_owner_id == user_id) \
        .all()


def get_businesses_with_testing(db: Session, skip: int = 0, limit: int = 100):
    return db.query(
        Business.id,
        Business.name,
        Business.photo_url,
        BusinessCategory.name.label('category'),
    ) \
        .join(BusinessCategory, Business.fk_business_category_id == BusinessCategory.id) \
        .order_by(Business.updated_at) \
        .offset(skip) \
        .limit(limit) \
        .all()


def get_businesses_by_user_login_with_testing(db: Session, user_id: str, skip: int = 0, limit: int = 100):
    return db.query(
        Business.id,
        Business.name,
        Business.photo_url,
        Business.contact,
        Business.location,
        Business.description,
        Business.created_at,
        Business.updated_at,
        BusinessCategory.name.label('category'),
        UserModel.fullname.label('owner'),
        func.avg(Rating.rating_count).label('rating')
    ) \
        .join(BusinessCategory, Business.fk_business_category_id == BusinessCategory.id) \
        .join(UserModel, Business.fk_owner_id == UserModel.id) \
        .join(Rating, Rating.fk_business_id == Business.id) \
        .filter(Business.fk_owner_id == user_id).order_by(Business.updated_at) \
        .offset(skip) \
        .limit(limit) \
        .all()


# detail-business-by-uuid


# detail-business-by-uuid
def get_detail_business_by_id(db: Session, business_id: uuid.UUID) -> optional.Optional:
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
        print(business_model.owner)
        print("hallo there")
        return optional.build(data=business_model)

    except Exception as e:
        print(e)
        return optional.build(error=HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="failed to fetch business"
        ))

# def get_businesses_with_category_and_rating(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(
#             Business.id, 
#             Business.name, 
#             BusinessCategory.name.label('category'), 
#             func.avg(Rating.rating_count).label('rating')
#         ) \
#         .join(Rating, Rating.fk_business_id == Business.id) \
#         .join(BusinessCategory, Business.fk_business_category_id == BusinessCategory.id) \
#         .group_by(Business.id, Business.name, BusinessCategory.name, Business.updated_at) \
#         .order_by(Business.updated_at) \
#         .offset(skip) \
#         .limit(limit) \
#         .all()

# def get_businesses_with_category_and_rating_by_user_id(db: Session, user_id:str, skip: int = 0, limit: int = 100)-> list[Type[Business]]:
#     print(user_id)
#     return db.query(
#             Business.id, 
#             Business.name,
#             Business.photo_url, 
#             BusinessCategory.name.label('category'), 
#             func.avg(Rating.rating_count).label('rating')
#         ) \
#         .join(Rating, Rating.fk_business_id == Business.id) \
#         .join(BusinessCategory, Business.fk_business_category_id == BusinessCategory.id) \
#         .group_by(Business.id) \
#         .filter(Business.fk_owner_id == user_id) \
#         .order_by(Business.updated_at) \
#         .offset(skip) \
#         .limit(limit) \
#         .all()

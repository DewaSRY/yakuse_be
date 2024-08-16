from typing import Type

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, UploadFile, status

#
from app.user.user_model import UserModel

from . import rating_dtos
from .rating_model import Rating
from app.rating.rating_model import Rating

from app.utils import optional


# def create_rating_business(db: Session, rating: rating_dtos.BusinessRatingCreateDto, user_id) -> optional.Optional:
#     try:
#         rating_model = Rating(**rating.model_dump())
#         rating_model.fk_rater_id = user_id
#         db.add(rating_model)
#         db.commit()
#         return optional.build(data=rating_model)
#     except SQLAlchemyError as e:
#         return optional.build(error=HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="failed to create rating business"
#         ))

def create_rating_business(db: Session, business_id: str, rating: rating_dtos.BusinessRatingCreateDto, user_id: str) -> optional.Optional:
    try:
        # Pastikan rating adalah instance dari DTO yang benar
        rating_model = Rating(**rating.dict())  # Gunakan .dict() untuk mengubah Pydantic model ke dict
        rating_model.fk_rater_id = user_id
        rating_model.fk_business_id = business_id

        db.add(rating_model)
        db.commit()
        db.refresh(rating_model)
        return optional.build(data=rating_model)
    except SQLAlchemyError as e:
        return optional.build(error=HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Failed to create rating for the business"
        ))


def get_rating_business(db: Session, skip: int = 0, limit: int = 100) -> list[Type[Rating]]:
    return db.query(Rating) \
        .offset(skip) \
        .limit(limit) \
        .all()


# detail-rating-business
def get_businesses_by_user_id(db: Session, user_id: str, skip: int = 0, limit: int = 100):
    from app.business.business_model import Business
    return db.query(
        Rating.id,
        Rating.rating_count,
        Rating.review_description,
        Rating.created_at,
        Rating.updated_at,
        Business.name.label('business_name'),
        UserModel.fullname.label('rater_name')
    ) \
        .join(Business, Rating.fk_business_id == Business.id) \
        .join(UserModel, Rating.fk_rater_id == UserModel.id) \
        .filter(Rating.fk_rater_id == user_id) \
        .offset(skip) \
        .limit(limit) \
        .all()

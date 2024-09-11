
from typing import Annotated
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, File, UploadFile

from app.libs.sql_alchemy_lib import get_db
from app.libs.jwt_lib import jwt_dto, jwt_service

from . import rating_dtos
from . import rating_service

router = APIRouter(
    tags=["rating"],
    prefix="/rating",
)


# create-bisnis
# @router.post("/", response_model=rating_dtos.BusinessRatingCreateDto)
# def create_rating_business(
#         rating_business: rating_dtos.BusinessRatingCreateDto,
#         jwt_token: Annotated[jwt_dto.TokenPayLoad, Depends(jwt_service.get_jwt_pyload)],
#         db: Session = Depends(get_db),
# ):
#     return rating_service.create_rating_business(db, rating_business, jwt_token.id).unwrap()

@router.post("/{busines_id}", response_model=rating_dtos.BusinessRatingCreateResponseDto)
def create_rating_business(
        busines_id: str,
        rating_business: rating_dtos.BusinessRatingCreateDto,  # Pastikan ini adalah Pydantic model
        jwt_token: Annotated[jwt_dto.TokenPayLoad, Depends(jwt_service.get_jwt_pyload)],
        db: Session = Depends(get_db),
):
    return rating_service.create_rating_business(db, busines_id, rating_business, jwt_token.id).unwrap()


# get-all-business-by-login-user-id
@router.get("/all", response_model=list[rating_dtos.RatingDto])
def get_all_rating_business(
        jwt_token: Annotated[jwt_dto.TokenPayLoad, Depends(jwt_service.get_jwt_pyload)],
        db: Session = Depends(get_db)):
    """
    Get all ratings for business
    """
    # Call the service to get the ratings
    return rating_service.get_rating_business(db)

# get-my rate-business
@router.get("/mybusiness_rate", response_model=list[rating_dtos.BusinessRatingAllResponseDto])
def get_my_rating_business(
        jwt_token: Annotated[jwt_dto.TokenPayLoad, Depends(jwt_service.get_jwt_pyload)],
        db: Session = Depends(get_db)):
    """Get ratings for a business by business_id"""
    ratings = rating_service.get_rating_by_user_id(db, jwt_token.id)  # Assuming this gets the business_id
    return ratings.unwrap()

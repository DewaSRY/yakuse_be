from typing import Annotated

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, File, UploadFile

from app.libs.sql_alchemy_lib import get_db
from app.libs.jwt_lib import jwt_dto, jwt_service

from . import business_category_dtos
from . import business_category_service

router = APIRouter(
    tags=["business_category"],
    prefix="/business_category",
)

# create-bisnis-category
@router.post("/", response_model=business_category_dtos.BusinessCategoryCreateDto)
def create_business_category(
        business_category: business_category_dtos.BusinessCategoryCreateDto,
        jwt_token: Annotated[jwt_dto.TokenPayLoad, Depends(jwt_service.get_jwt_pyload)],
        db: Session = Depends(get_db),
):
    return business_category_service.create_business_category(db, business_category).unwrap()


# get-all-business-category-public
@router.get("/", response_model=list[business_category_dtos.BusinessCategoryAllPostResponseDto])
def get_all_public_business_category(
        jwt_token: Annotated[jwt_dto.TokenPayLoad, Depends(jwt_service.get_jwt_pyload)],
        db: Session = Depends(get_db)):
    return business_category_service.get_business_category(db)

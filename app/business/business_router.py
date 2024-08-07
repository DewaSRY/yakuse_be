from typing import Annotated

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, File, UploadFile

from app.libs.sql_alchemy_lib import get_db
from app.libs.jwt_lib import jwt_dto, jwt_service
from app.libs.images_service import create_image_service

from . import business_dtos
from . import business_services

router = APIRouter(
    tags=["business"],
    prefix="/business",
)


@router.post("/", response_model=business_dtos.BusinessCreateDto)
def create_business(
        business: business_dtos.BusinessCreateDto,
        jwt_toke: Annotated[jwt_dto.TokenPayLoad, Depends(jwt_service.get_jwt_pyload)],
        db: Session = Depends(get_db),
):
    return business_services.create_business(db, business, jwt_toke.id).unwrap()


@router.get("/", response_model=list[business_dtos.BusinessResponse])
def get_all_business(
        jwt_toke: Annotated[jwt_dto.TokenPayLoad, Depends(jwt_service.get_jwt_pyload)],
        db: Session = Depends(get_db)):
    return business_services.get_business_by_user_id(db, jwt_toke.id)


@router.get("/public", response_model=list[business_dtos.BusinessResponse])
def get_all_public_business(
        jwt_toke: Annotated[jwt_dto.TokenPayLoad, Depends(jwt_service.get_jwt_pyload)],
        db: Session = Depends(get_db)):
    return business_services.get_business(db)

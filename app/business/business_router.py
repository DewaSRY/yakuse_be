from typing import Annotated, Type
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from app.business.business_model import Business
from app.libs.sql_alchemy_lib import get_db
from app.libs.jwt_lib import jwt_dto, jwt_service

from . import business_dtos
from . import business_services

router = APIRouter(
    tags=["business"],
    prefix="/business",
)


# create-business-with-photo
@router.post("/create", response_model=business_dtos.BusinessCreateWithPhotoDto)
async def create_my_profile_business(
        file: UploadFile,
        business: business_dtos.BusinessCreateDto = Depends(),
        jwt_token: jwt_service.TokenPayLoad = Depends(jwt_service.get_jwt_pyload),
        db: Session = Depends(get_db)
):
    result = await business_services \
        .create_business_with_photo(db, business, jwt_token.id, file)
    if result.error:
        raise result.error
    return result.data


# edit-my-business
@router.put("/edit/{business_id}", response_model=business_dtos.BusinessEditWithPhotoDto)
async def update_my_profile_business(
        business_id: str,
        file: UploadFile,
        business: business_dtos.BusinessEditDto = Depends(),
        jwt_token: jwt_service.TokenPayLoad = Depends(jwt_service.get_jwt_pyload),
        db: Session = Depends(get_db)
):
    """This method is used to update a business profile"""
    result = await business_services \
        .edit_business_by_business_id(db, business_id, business, jwt_token.id, file)

    if result.error:
        raise result.error

    return result.data


# get-all-business-by-login-user-id
@router.get("/my-business", response_model=list[business_dtos.BusinessResponse])
def get_all_my_business(
        jwt_token: Annotated[jwt_dto.TokenPayLoad, Depends(jwt_service.get_jwt_pyload)],
        db: Session = Depends(get_db)):
    return business_services \
        .get_all_business_by_user_id(db, jwt_token.id).unwrap()


# get-all-business-user-by-user-id
@router.get("/user/{user_id}", response_model=list[business_dtos.BusinessResponse])
def get_list_business_user_by_user_id(
        user_id: str,
        jwt_token: Annotated[jwt_dto.TokenPayLoad, Depends(jwt_service.get_jwt_pyload)],
        db: Session = Depends(get_db)
):
    return business_services.get_all_business_by_user_id(db, user_id).unwrap()


# delete-my-business
@router.delete("/delete/{business_id}")
async def delete_my_business(
        business_id: str,
        jwt_token: jwt_service.TokenPayLoad = Depends(jwt_service.get_jwt_pyload),
        db: Session = Depends(get_db)
):
    """This method is used to delete a business profile"""
    result = await business_services.delete_business_by_id(db, business_id, jwt_token.id)

    if result.error:
        raise result.error

    return {"detail": "Business deleted successfully"}


# get-all-business-public
# @router.get("/all", response_model=list[business_dtos.BusinessAllPost])
# def get_all_public_business_latest(
#         jwt_token: Annotated[jwt_dto.TokenPayLoad, Depends(jwt_service.get_jwt_pyload)],
#         db: Session = Depends(get_db)):
#     return business_services.get_all_business(db).unwrap()

@router.get("/all", response_model=list[business_dtos.BusinessAllPost])
def get_all_public_business_latest(
        jwt_token: Annotated[jwt_dto.TokenPayLoad, Depends(jwt_service.get_jwt_pyload)],
        skip: int = Query(0, description="Number of items to skip"),
        limit: int = Query(10, description="Max number of items to return"),
        db: Session = Depends(get_db)):
    
    # Mengambil hasil dari service dengan skip dan limit
    result = business_services.get_all_business(db, skip=skip, limit=limit)

    # Cek apakah hasil berupa error
    # if result.is_error():
    #     raise result.error

    # Jika tidak ada error, unwrap dan kembalikan datanya
    return result.unwrap()


# get-detail-business-by-business_id
@router.get("/{business_id}", response_model=business_dtos.BusinessResponse)
def get_detail_business_by_business_id(
        business_id: UUID,
        jwt_token: Annotated[jwt_dto.TokenPayLoad, Depends(jwt_service.get_jwt_pyload)],
        db: Session = Depends(get_db)):
    return business_services.get_detail_business_by_business_id(db, business_id).unwrap()


# get-list-business-by-category
@router.get("/category/{category_name}", response_model=list[business_dtos.BusinessAllPost])
def get_list_business_by_category_name(
        category_name: str,
        jwt_token: Annotated[jwt_dto.TokenPayLoad, Depends(jwt_service.get_jwt_pyload)],
        db: Session = Depends(get_db)
):
    return business_services \
        .get_all_business_by_category(db, category_name).unwrap()


# get-list-business-by-keyword-search
@router.get("/search/{keyword}", response_model=list[business_dtos.BusinessAllPost])
def search_business(
        keyword: str,
        jwt_token: Annotated[jwt_dto.TokenPayLoad, Depends(jwt_service.get_jwt_pyload)],
        db: Session = Depends(get_db)
):
    """Search businesses by keyword"""
    return business_services.search_business_by_keyword(db, keyword).unwrap()

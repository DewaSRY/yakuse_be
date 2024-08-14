from typing import Annotated, Type
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.business.business_model import Business
from app.libs.sql_alchemy_lib import get_db
from app.libs.jwt_lib import jwt_dto, jwt_service
from app.libs.images_service import create_image_service

from . import business_dtos
from . import business_services

router = APIRouter(
    tags=["business"],
    prefix="/business",
)

# create-business-with-photo
@router.post("/create-business", response_model=business_dtos.BusinessCreateWithPhotoDto)
async def create_my_profile_business(
    business: business_dtos.BusinessCreateDto = Depends(),
    file: UploadFile = File(...), 
    jwt_token: jwt_service.TokenPayLoad = Depends(jwt_service.get_jwt_pyload),
    db: Session = Depends(get_db)
):
    result= await business_services.create_business_with_photo(db, business, jwt_token.id, file)

    # Jika optional berisi error, raise HTTPException
    if result.error:
        raise result.error

    # Return data yang valid sesuai dengan DTO
    return result.data


# edit-profile-business
@router.put("/edit", response_model=business_dtos.BusinessEdiDto)
async def update_my_profile_business(
        business: business_dtos.BusinessEdiDto,
        jwt_token: Annotated[jwt_dto.TokenPayLoad, Depends(jwt_service.get_jwt_pyload)],
        db: Session = Depends(get_db)):
    """This method use to update user profile"""
    return business_services.business_edit(db, business, jwt_token.id).unwrap()


# get-all-business-by-login-user-id
@router.get("/my-business", response_model=list[business_dtos.BusinessResponse])
def get_all_my_business(
        jwt_token: Annotated[jwt_dto.TokenPayLoad, Depends(jwt_service.get_jwt_pyload)],
        db: Session = Depends(get_db)):
    return business_services.get_business_by_user_id(db, jwt_token.id).unwrap()

# @router.get("/{user_id}", response_model=list[business_dtos.BusinessResponse])
# def get_profile_business_by_use_id(
#         user_id:str,
#         jwt_token: Annotated[jwt_dto.TokenPayLoad, Depends(jwt_service.get_jwt_pyload)],
#         db: Session = Depends(get_db)):
#     return business_services.get_business_by_user_id(db, user_id).unwrap()


# get-all-business-public
@router.get("/all", response_model=list[business_dtos.BusinessAllPost])
def get_all_public_business_latest(
        jwt_token: Annotated[jwt_dto.TokenPayLoad, Depends(jwt_service.get_jwt_pyload)],
        db: Session = Depends(get_db)):
    return business_services.get_all_business(db).unwrap()


@router.get("/detail/{business_id}", response_model=business_dtos.BusinessResponse)
def get_detail_business_by_business_id(
        business_id: UUID,
        jwt_token: Annotated[jwt_dto.TokenPayLoad, Depends(jwt_service.get_jwt_pyload)],
        db: Session = Depends(get_db)):
    return business_services.get_detail_business_by_business_id(db, business_id).unwrap()



# create-bisnis
# @router.post("/", response_model=business_dtos.BusinessResponse)
# def create_business(
#         business: business_dtos.BusinessCreateDto,
#         jwt_token: Annotated[jwt_dto.TokenPayLoad, Depends(jwt_service.get_jwt_pyload)],
#         db: Session = Depends(get_db),
# ):
#     return business_services.create_business(db, business, jwt_token.id).unwrap()

# @router.post("/post_photo/{business_id}", response_model=business_dtos.BusinessPhotoProfileDto)
# async def upload_photo_my_business_by_id_business(
#         business_id: UUID,
#         file: UploadFile = File(...),  # Untuk menerima file upload
#         jwt_token: jwt_dto.TokenPayLoad = Depends(jwt_service.get_jwt_pyload),
#         db: Session = Depends(get_db)
# ):
#     """This Method use to upload and update the photo profile of a business (file in png or jpg)"""
#     print(f"Received business_id: {business_id}, user_id: {jwt_token.id}")  # Debug print
#     return await business_services.upload_photo_business_by_business_id(db, business_id, jwt_token.id, file)

# # upload-photo-business
# @router.post("/post_photo", response_model=business_dtos.BusinessPhotoProfileDto)
# async def upload_photo_business(
#         file: UploadFile = File(...),  # Untuk menerima file upload
#         jwt_token: jwt_dto.TokenPayLoad = Depends(jwt_service.get_jwt_pyload),
#         db: Session = Depends(get_db)
# ):
#     """This Method use to upload and update the photo profile of a business (file in png or jpg)"""
#     business = await business_services.upload_photo_business(db, jwt_token.id, file)
#     return business_dtos.BusinessPhotoProfileDto(photo_url=business.photo_url)

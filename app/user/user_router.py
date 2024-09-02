from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.libs.sql_alchemy_lib import get_db
from app.libs.jwt_lib import jwt_service, jwt_dto

from . import user_services, user_dtos, user_firebase_services


router = APIRouter(
    prefix="/user",
    tags=["user"]
)


# user--register
@router.post("/register", response_model=user_dtos.UserCreateResponseDto)
def create_user(user: user_dtos.UserCreateDto, db: Session = Depends(get_db)):
    """This method use to create user"""
    return user_services.create_user(db, user).unwrap()


# user-login
@router.post("/login", response_model=jwt_dto.AccessTokenDto)
async def user_login(user: user_dtos.UserLoginPayloadDto, db: Session = Depends(get_db)):
    """use to get all users"""
    user_optional = user_services.user_login(db=db, user=user)
    if user_optional.error:
        raise user_optional.error
    return user_services.service_access_token(user_optional.data.id)


# get-user-profile
@router.get("/profile", response_model=user_dtos.UserCreateResponseDto)
async def get_user_profile_by_id(
        jwt_token: Annotated[jwt_dto.TokenPayLoad, Depends(jwt_service.get_jwt_pyload)],
        db: Session = Depends(get_db)):
    """get user profile by id"""
    return user_services.get_user_profile(db, jwt_token.id).unwrap()


# get-other-user-profile-by-id
@router.get("/profile/{user_id}", response_model=user_dtos.UserCreateResponseDto)
async def get_other_profile_by_user_id(
        user_id: str,
        jwt_token: Annotated[jwt_dto.TokenPayLoad, Depends(jwt_service.get_jwt_pyload)],
        db: Session = Depends(get_db)):
    """get other user profile by user_id"""
    return user_services.get_user_profile_by_id(db, user_id).unwrap()


# # edit-profile-user
# @router.put("/edit", response_model=user_dtos.UserCreateResponseDto)
# async def update_user_profile(
#         user: user_dtos.UserEditProfileDto,
#         jwt_token: Annotated[jwt_dto.TokenPayLoad, Depends(jwt_service.get_jwt_pyload)],
#         db: Session = Depends(get_db)):
#     """This method use to update user profile"""
#     return user_services.user_edit(db, user, jwt_token.id).unwrap()


# edit-post-user-photo-profile
@router.put("/edit/photo-profile", response_model=user_dtos.UserCreateResponseDto)
async def update_user_photo_profile(
        file: UploadFile = File(...),  # Untuk menerima file upload
        jwt_token: jwt_dto.TokenPayLoad = Depends(jwt_service.get_jwt_pyload),
        db: Session = Depends(get_db)
):
    """This Method use to Update Photo Profile of User"""
    user_optional = await user_services.update_user_photo(db, jwt_token.id, file)
    if user_optional.error:
        raise user_optional.error
    return user_optional.data

# edit-user-with-photo
# @router.put("/edit-profile", response_model=user_dtos.UserCreateResponseDto)
# async def edit_profile(
#         user: user_dtos.UserEditProfileDto = Depends(),
#         jwt_token: jwt_service.TokenPayLoad = Depends(jwt_service.get_jwt_pyload),
#         file: UploadFile = None,  # Mark file as optional if not always required
#         db: Session = Depends(get_db)
# ):
#     result = await user_services.edit_user_by_user_id_login(db, jwt_token.id, user, file)
    
#     if result.error:
#         raise result.error
    
#     return result.data

# --
# == memanfaatkan storage yg disediakan supabase== #
# == memanfaatkan storage yg disediakan supabase== #
@router.put("/edit-profile", response_model=user_dtos.UserCreateResponseDto)
async def create_my_profile_user(
        file: UploadFile = None,  # Jika opsional, tetap `None`; jika wajib, gunakan `File(...)`
        user: user_dtos.UserEditProfileDto = Depends(),
        jwt_token: jwt_service.TokenPayLoad = Depends(jwt_service.get_jwt_pyload),
        db: Session = Depends(get_db)
):
    # Pastikan untuk menangani kasus di mana `file` adalah None di dalam layanan Anda
    result = await user_services.edit_user_by_user_id_login(db, jwt_token.id, user, file)
    
    if result.error:
        raise result.error
    
    return result.data




# @router.post("/login/firebase", response_model=jwt_dto.AccessTokenDto)
# async def firebase_login(data: user_dtos.FirebaseLoginDto, db: Session = Depends(get_db)):
#     """Authenticate user with Firebase ID token"""
#     user_optional = await user_firebase_services.firebase_login(db=db, data=data)
#     if user_optional.error:
#         raise user_optional.error
#     return user_services.service_access_token(user_optional.data.id)

from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

from app.libs.images_service import create_image_service
from app.libs.sql_alchemy_lib import get_db
from app.libs.jwt_lib import jwt_service, jwt_dto
from firebase_admin import auth, initialize_app, credentials

from . import user_services, user_dtos

load_dotenv()

cred = credentials.Certificate(os.getenv('JSON_CONFIG'))
initialize_app(cred)

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

# user--register
@router.post("/", response_model=user_dtos.UserCreateResponseDto)
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
@router.get("/profile", response_model=user_dtos.UserGetProfilTestDto)
async def get_user_profile_by_id(
        jwt_token: Annotated[jwt_dto.TokenPayLoad, Depends(jwt_service.get_jwt_pyload)],
        db: Session = Depends(get_db)):
    """get user profile by id"""
    return user_services.get_user_profile(db, jwt_token.id).unwrap()
    # return {"message":"hello world"}

# edit-profile-user
@router.put("/edit", response_model=user_dtos.UserEditResponseDto)
async def update_user_profile(
        user: user_dtos.UserEditProfileDto,
        jwt_token: Annotated[jwt_dto.TokenPayLoad, Depends(jwt_service.get_jwt_pyload)],
        db: Session = Depends(get_db)):
    """This method use to update user profile"""
    return user_services.user_edit(db, user, jwt_token.id).unwrap()


@router.put("/edit/photo", response_model=user_dtos.UserEditPhotoProfileDto)
async def update_user_photo_profile(
    file: UploadFile = File(...),  # Untuk menerima file upload
    jwt_token: jwt_dto.TokenPayLoad = Depends(jwt_service.get_jwt_pyload),
    db: Session = Depends(get_db)
):
    """Method ini digunakan untuk memperbarui foto profil pengguna"""
    user = await user_services.update_user_photo(db, jwt_token.id, file)
    return user_dtos.UserEditPhotoProfileDto(photo_url=user.photo_url)




@router.post("/login/firebase", response_model=jwt_dto.AccessTokenDto)
async def firebase_login(data: user_dtos.FirebaseLoginDto, db: Session = Depends(get_db)):
    """Authenticate user with Firebase ID token"""
    print("Received ID token:", data.id_token)

    try:
        """ verifying firebase id token"""
        decoded_token = auth.verify_id_token(data.id_token)
        print("Decoded token:", decoded_token)
        uid = decoded_token['uid']
        user_email = decoded_token.get('email')

        """ database checking find existing user"""
        user_optional = user_services.get_user_by_email(db, email=user_email)
        if user_optional.error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        """token creation"""
        return user_services.service_access_token(user_optional.data.id)
    except auth.AuthError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

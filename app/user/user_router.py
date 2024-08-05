from fastapi import APIRouter, Depends , HTTPException, status
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

from app.libs.sql_alchemy_lib import get_db
from app.libs.jwt_lib import jwt_service, jwt_dto
from firebase_admin import auth,initialize_app,credentials


from . import user_services, user_dtos

load_dotenv()

# login firebase admin

cred = credentials.Certificate(os.getenv('JSON_CONFIG'))
initialize_app(cred)

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.post("/", response_model=user_dtos.UserCreateResponseDto)
def create_user(user: user_dtos.UserCreateDto, db: Session = Depends(get_db)):
    """This method use to create user"""
    optional = user_services.create_user(db, user)
    if optional.error:
        raise optional.error
    return optional.data


@router.post("/login", response_model=jwt_dto.AccessTokenDto)
async def user_login(user: user_dtos.UserLoginPayloadDto, db: Session = Depends(get_db)):
    """use to get all users"""
    user_optional = user_services.user_login(db=db, user=user)
    if user_optional.error:
        raise user_optional.error
    user_ditch = dict([
        ("user_id", user_optional.data.id)
    ])
    return jwt_service.create_access_token(user_ditch)

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
        user_ditch = dict([
            ("user_id", user_optional.data.id)
        ])
        return jwt_service.create_access_token(user_ditch)
    except auth.AuthError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
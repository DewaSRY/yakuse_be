from typing import Annotated

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.libs.sql_alchemy_lib import get_db
from app.libs.jwt_lib.jwt_dto import TokenPayLoad
from app.libs.jwt_lib.jwt_service import get_jwt_pyload

from .user_need_dtos import UserNeedCreateDto, UserNeedResponseDto
from .user_need_services import create_user_need_service, get_user_need_by_user_id_service, get_user_need_service

router = APIRouter(
    tags=["user-need"],
    prefix="/user-need",
)


@router.post("/", response_model=UserNeedCreateDto)
def create_user_need(
    user_need: UserNeedCreateDto,
    jwt_token: Annotated[TokenPayLoad, Depends(get_jwt_pyload)],
    db: Session = Depends(get_db),
):
    return create_user_need_service(db, user_need, jwt_token.id).unwrap()
    
@router.get("/", response_model=list[UserNeedResponseDto])
def get_all_user_need(
    jwt_token: Annotated[TokenPayLoad, Depends(get_jwt_pyload)],
    db: Session = Depends(get_db)
):
    return get_user_need_by_user_id_service(db, jwt_token.id)

@router.get("/public", response_model=list[UserNeedResponseDto])
def get_all_public_user_need(
    db: Session = Depends(get_db)
):
    return get_user_need_service(db)
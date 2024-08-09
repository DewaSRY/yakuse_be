from typing import Annotated

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status

from app.libs.sql_alchemy_lib import get_db
from app.libs.jwt_lib.jwt_dto import TokenPayLoad
from app.libs.jwt_lib.jwt_service import get_jwt_pyload

from .user_need_dtos import UserNeedUpdateDto, UserNeedCreateDto, UserNeedResponseDto
from .user_need_services import get_user_need_by_id_service, delete_user_need_by_id_service, create_user_need_service, get_user_need_by_user_id_service, get_user_need_service, update_user_need_by_id_service

router = APIRouter(
    tags=["user-need"],
    prefix="/user-need",
)


@router.post("/", response_model=UserNeedResponseDto, status_code=status.HTTP_201_CREATED)
def create_user_need(
    user_need: UserNeedCreateDto,
    jwt_token: Annotated[TokenPayLoad, Depends(get_jwt_pyload)],
    db: Session = Depends(get_db),
):
    return create_user_need_service(db, user_need, jwt_token.id).unwrap()
    
@router.get("/", response_model=list[UserNeedResponseDto], status_code=status.HTTP_200_OK)
def get_all_our_user_need(
    jwt_token: Annotated[TokenPayLoad, Depends(get_jwt_pyload)],
    db: Session = Depends(get_db)
):
    return get_user_need_by_user_id_service(db, jwt_token.id)

@router.get("/public", response_model=list[UserNeedResponseDto], status_code=status.HTTP_200_OK)
def get_all_public_user_need(
    db: Session = Depends(get_db)
):
    return get_user_need_service(db)

@router.get("/{user_need_id}", response_model=UserNeedResponseDto, status_code=status.HTTP_200_OK)
def get_user_need_by_id(
    user_need_id: str,
    db: Session = Depends(get_db)
):
    return get_user_need_by_id_service(db, user_need_id)

@router.put("/{user_need_id}", response_model=UserNeedResponseDto)
async def update_user_need_by_id(
    user_need_id: str,
    user_need_update: UserNeedUpdateDto,
    jwt_token: Annotated[TokenPayLoad, Depends(get_jwt_pyload)],
    db: Session = Depends(get_db)
):
    return update_user_need_by_id_service(db, jwt_token.id, user_need_id, user_need_update).unwrap()

@router.delete("/hide/{user_need_id}")
def delete_to_hide_user_need(user_need_id: str):
    '''as a user, user can make their needs to be hide in public'''


@router.delete("/delete/{user_need_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_need_by_id(
    user_need_id: str,
    jwt_token: Annotated[TokenPayLoad, Depends(get_jwt_pyload)],
    db: Session = Depends(get_db)
):
    return delete_user_need_by_id_service(db, jwt_token.id, user_need_id)
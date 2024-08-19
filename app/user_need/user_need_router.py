from typing import Annotated

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status

from app.libs.sql_alchemy_lib import get_db
from app.libs.jwt_lib.jwt_dto import TokenPayLoad
from app.libs.jwt_lib.jwt_service import get_jwt_pyload

from . import user_need_dtos, user_need_services

router = APIRouter(
    tags=["user-need"],
    prefix="/user-need",
)


@router.post("/",
             response_model=user_need_dtos.UserNeedResponseDto,
             status_code=status.HTTP_201_CREATED)
def create_user_need(
        user_need: user_need_dtos.UserNeedCreateDto,
        jwt_token: Annotated[TokenPayLoad, Depends(get_jwt_pyload)],
        db: Session = Depends(get_db),
):
    return user_need_services \
        .create_user_need(db, user_need, jwt_token.id).unwrap()


@router.get("/all",
            response_model=list[user_need_dtos.UserNeedResponseDto],
            status_code=status.HTTP_200_OK)
def get_all_public_user_needs(
        jwt_token: Annotated[TokenPayLoad, Depends(get_jwt_pyload)],
        db: Session = Depends(get_db)
):
    return user_need_services \
        .get_all_user_needs(db).unwrap()


@router.get("/search/{keyword}",
            response_model=list[user_need_dtos.UserNeedResponseDto],
            status_code=status.HTTP_200_OK)
def search_user_needs(
        keyword: str,
        jwt_token: Annotated[TokenPayLoad, Depends(get_jwt_pyload)],
        db: Session = Depends(get_db)
):
    return user_need_services \
        .search_user_needs_by_keyword(db, keyword).unwrap()


@router.get("/category/{category_name}",
            response_model=list[user_need_dtos.UserNeedResponseDto],
            status_code=status.HTTP_200_OK)
def get_user_needs_by_category_name(
        category_name: str,
        jwt_token: Annotated[TokenPayLoad, Depends(get_jwt_pyload)],
        db: Session = Depends(get_db)
):
    return user_need_services \
        .get_user_needs_by_category_name(db, category_name).unwrap()


@router.get("/my-needs",
            response_model=list[user_need_dtos.UserNeedResponseDto],
            status_code=status.HTTP_200_OK)
def get_all_my_user_needs(
        jwt_token: Annotated[TokenPayLoad, Depends(get_jwt_pyload)],
        db: Session = Depends(get_db)
):
    return user_need_services \
        .get_my_user_needs(db, jwt_token.id).unwrap()


@router.get("/{user_id}/needs",
            response_model=list[user_need_dtos.UserNeedResponseDto],
            status_code=status.HTTP_200_OK)
def get_user_needs_by_user_id(
        user_id: str,
        jwt_token: Annotated[TokenPayLoad, Depends(get_jwt_pyload)],
        db: Session = Depends(get_db)
):
    return user_need_services \
        .get_user_needs_by_user_id(db, user_id).unwrap()


@router.get("/detail/{user_need_id}",
            response_model=user_need_dtos.UserNeedResponseDto,
            status_code=status.HTTP_200_OK)
def get_user_need_detail_by_id(
        user_need_id: int,
        jwt_token: Annotated[TokenPayLoad, Depends(get_jwt_pyload)],
        db: Session = Depends(get_db)
):
    return user_need_services \
        .get_user_need_by_id(db, user_need_id).unwrap()


@router.put("/my-need/{user_need_id}",
            response_model=user_need_dtos.UserNeedResponseDto,
            status_code=status.HTTP_200_OK)
async def update_user_need_by_id(
        user_need_id: int,
        user_need_update: user_need_dtos.UserNeedUpdateDto,
        jwt_token: Annotated[TokenPayLoad, Depends(get_jwt_pyload)],
        db: Session = Depends(get_db)
):
    return user_need_services \
        .update_user_need_by_id(db, jwt_token.id, user_need_id, user_need_update).unwrap()


@router.delete("/hide/my-need/{user_need_id}",
               status_code=status.HTTP_204_NO_CONTENT)
def delete_to_hide_user_need_by_id(
        user_need_id: int,
        jwt_token: Annotated[TokenPayLoad, Depends(get_jwt_pyload)],
        db: Session = Depends(get_db)
):
    return user_need_services \
        .hide_user_need_by_id(db, jwt_token.id, user_need_id)

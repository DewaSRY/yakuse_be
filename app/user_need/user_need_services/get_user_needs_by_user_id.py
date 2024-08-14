from typing import Type

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from app.user_need.user_need_dtos import UserNeedCreateDto, UserNeedUpdateDto
from app.user_need.user_need_model import UserNeeds

from app.utils.optional import Optional, build


def get_user_need_by_user_id_service(db: Session, user_id: str) -> list[Type[UserNeeds]]:
    try:
        user_need = db.query(UserNeeds).filter(UserNeeds.fk_user_id == user_id).all()
        return build(data=user_need)
    except SQLAlchemyError as e:
        return build(error=HTTPException(detail=f"{e}"))
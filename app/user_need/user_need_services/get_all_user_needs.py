from typing import Type

from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from app.user_need import user_need_dtos
from app.user_need.user_need_model import UserNeeds

from app.utils.optional import Optional, build


def get_all_user_needs(db: Session, skip: int = 0, limit: int = 100) -> Optional:
    try:
        user_needs: list[Type[UserNeeds]] = db.query(UserNeeds).order_by(desc(UserNeeds.created_at)).offset(skip).limit(
            limit).all()

        user_need_dtos = [user_need.to_response_dto() for user_need in user_needs]

        return build(data=user_need_dtos)
    except SQLAlchemyError as e:
        return build(error=HTTPException(detail=f"{e}"))

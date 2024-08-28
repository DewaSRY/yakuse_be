from typing import Type

from sqlalchemy import desc, or_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from app.business_category.business_category_model import BusinessCategory
from app.user_need.user_need_dtos import UserNeedCreateDto, UserNeedUpdateDto
from app.user_need.user_need_model import UserNeeds

from app.utils.optional import Optional, build


def search_user_needs_by_keyword(db: Session, keyword: str) -> Optional:
    try:
        user_needs = db.query(UserNeeds) \
            .filter(
                or_(
                    UserNeeds.title.like(f"%{keyword}%"),
                    UserNeeds.description.like(f"%{keyword}%")
                )
            ) \
            .order_by(desc(UserNeeds.created_at)).all()

        if len(user_needs) == 0:
            return build(error=HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                             detail="No user-needs found matching the keyword"))

        return build(data=user_needs)
    except SQLAlchemyError as e:
        return build(error=HTTPException(detail=f"{e}",
                                         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR))
    except Exception as e:
        return build(error=HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                         detail=f"E: {e}"))

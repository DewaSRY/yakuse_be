from typing import Type

from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from app.business_category.business_category_model import BusinessCategory
from app.user_need.user_need_dtos import UserNeedCreateDto, UserNeedUpdateDto
from app.user_need.user_need_model import UserNeeds

from app.utils.optional import Optional, build


def search_user_needs_by_keyword(db: Session, keyword: str) -> Optional:
    try:
        search_query = f"%{keyword}%"
        user_needs = db.query(UserNeeds).filter(UserNeeds.name.ilike(search_query)).order_by(desc(UserNeeds.created_at)).all()

        if not user_needs:
            return build(
                error=HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No user-needs found matching the keyword"
                )
            )

        user_need_dtos = [user_need.to_response_dto() for user_need in user_needs]

        return build(data=user_need_dtos)
    except SQLAlchemyError as e:
        return build(error=HTTPException(detail=f"{e}"))
    except Exception as e:
        return build(error=HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"E: {e}"))
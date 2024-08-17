from typing import Type

from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from app.user_need.user_need_dtos import UserNeedCreateDto, UserNeedUpdateDto
from app.user_need.user_need_model import UserNeeds

from app.utils.optional import Optional, build

"""
        businesses = db.query(Business) \
            .join(Business.business_category) \
            .filter(BusinessCategory.name == category_name).all()


"""


def get_user_needs_by_category_name(db: Session, category_name: str) -> Optional:
    from app.business_category.business_category_model import BusinessCategory

    try:
        business_category_model = db.query(BusinessCategory) \
            .filter(BusinessCategory.name.like(f"%{category_name}%")).first()

        if business_category_model is None:
            return build(error=HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                             detail=f"{category_name} is not valid category"))
        user_needs = db.query(UserNeeds) \
            .filter(UserNeeds.fk_business_category_id.like(f"{business_category_model.id}")) \
            .order_by(desc(UserNeeds.created_at)).all()

        if not user_needs:
            return build(
                error=HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No user-needs found for this category"
                )
            )

        # user_need_dtos = [user_need.to_response_dto() for user_need in user_needs]

        return build(data=user_needs)
    except SQLAlchemyError as e:
        return build(error=HTTPException(detail=f"{e}", status_code=status.HTTP_404_NOT_FOUND))
    except Exception as e:
        return build(error=HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"E: {e}"))

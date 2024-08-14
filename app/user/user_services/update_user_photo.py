from typing import Type, Optional, Callable
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, UploadFile, status

from app.libs.images_service import create_image_service

from app.user.user_model import UserModel

from app.utils import optional, find_errr_from_args


async def update_user_photo(db: Session, user_id: str, file: UploadFile) \
        -> optional.Optional[Type[UserModel], HTTPException]:
    try:
        opt_content = await create_image_service(upload_file=file, domain="user")
        user_mode = db.query(UserModel).filter(UserModel.id == user_id).first()
        if user_mode:
            # Update photo_url
            user_mode.photo_url = opt_content.data
            db.commit()
            db.refresh(user_mode)
            return optional.build(data=user_mode)
        else:
            return optional.build(error=HTTPException(status_code=404, detail="User not found"))
    except SQLAlchemyError as e:
        db.rollback()
        return optional.build(error=HTTPException(status_code=409, detail="Database conflict: " + str(e)))

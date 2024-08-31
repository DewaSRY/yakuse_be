from typing import List, Type
import uuid
from sqlalchemy import desc, func, or_
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, UploadFile, status

from app.business_category.business_category_model import BusinessCategory
from app.libs.images_service import create_image_service
from app.user.user_model import UserModel
from app.user import user_dtos

from app.business import business_dtos
from app.business.business_model import Business
from app.rating.rating_model import Rating

from app.utils import optional


# edit-user-document-with-photo

# user-edit-with-photo
async def edit_user_by_user_id_login(
        db: Session, user_id: str, user: user_dtos.UserEditProfileDto, file: UploadFile
) -> optional.Optional[Type[UserModel], Exception]:
    try:
        # Langkah 1: Mencari user yang ada
        user_model = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user_model:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        # Langkah 2: Upload foto
        opt_content = await create_image_service(upload_file=file, domain="user")

        # Jika upload berhasil, update `photo_url` dalam `user_model`
        if opt_content.data:
            user_model.photo_url = opt_content.data

        # Langkah 3: Update atribut user
        user_data = user.model_dump()  # Convert DTO to dictionary
        for attr, value in user_data.items():
            if value is not None:  # Update hanya jika value ada (bukan None)
                setattr(user_model, attr, value)

        # Simpan perubahan ke dalam database
        db.add(user_model)
        db.commit()
        db.refresh(user_model)

        return optional.build(data=user_model)

    except SQLAlchemyError as e:
        db.rollback()
        return optional.build(error=HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Database conflict: {str(e)}"
        ))

    except Exception as e:
        return optional.build(error=HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        ))


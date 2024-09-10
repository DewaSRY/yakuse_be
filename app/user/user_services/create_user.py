from typing import Type, Optional, Callable
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, UploadFile, status

from app.user.user_model import UserModel
from app.user import user_dtos
from app.libs import password_lib
from app.utils import optional, error_parser


def create_user(db: Session, user: user_dtos.UserCreateDto) -> optional.Optional[UserModel, Exception]:
    try:
        # Membuat instance user baru
        user_model = UserModel()
        user_model.email = user.email
        user_model.fullname = user.fullname
        user_model.username = user.username
        # Hash password sebelum menyimpan
        user_model.hash_password = password_lib.get_password_hash(password=user.password)

        # Menambahkan user ke dalam database
        db.add(user_model)
        db.commit()
        db.refresh(user_model)  # Memastikan data yang baru ditambahkan ter-refresh
        
        return optional.build(data=user_model)

    except IntegrityError as ie:
        db.rollback()  # Rollback jika ada kesalahan integritas data (misal, duplikasi email atau username)

        # Menentukan apakah kesalahan berasal dari email atau username yang sudah ada
        if 'email' in str(ie.orig):
            message = "Email already exists. Please use a different email."
        elif 'username' in str(ie.orig):
            message = "Username already exists. Please choose a different username."
        else:
            message = "Duplicate data found."

        # Mengembalikan kesalahan dengan pesan yang jelas
        return optional.build(error=HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=message
        ))

    except SQLAlchemyError as e:
        db.rollback()  # Rollback untuk semua error SQLAlchemy umum lainnya
        return optional.build(error=HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the user. Please try again later."
        ))

    except Exception as e:
        db.rollback()  # Rollback untuk error tak terduga
        return optional.build(error=HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        ))


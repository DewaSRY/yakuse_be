from typing import Type, Optional, Callable
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, UploadFile, status

from app.libs.images_service import create_image_service

from app.user.user_model import UserModel

from app.libs.upload_image_to_supabase import upload_image_to_supabase, validate_file
from app.utils import optional, find_errr_from_args


# async def update_user_photo(db: Session, user_id: str, file: UploadFile) \
#         -> optional.Optional[Type[UserModel], HTTPException]:
#     try:
#         opt_content = await create_image_service(upload_file=file, domain="user")
#         user_mode = db.query(UserModel).filter(UserModel.id == user_id).first()
#         if user_mode:
#             # Update photo_url
#             user_mode.photo_url = opt_content.data
#             db.commit()
#             db.refresh(user_mode)
#             return optional.build(data=user_mode)
#         else:
#             return optional.build(error=HTTPException(status_code=404, detail="User not found"))
#     except SQLAlchemyError as e:
#         db.rollback()
#         return optional.build(error=HTTPException(status_code=409, detail="Database conflict: " + str(e)))


# Daftar format file yang diizinkan dan batas ukuran file dalam byte (contoh 500KB)
# ALLOWED_EXTENSIONS = ['png', 'jpeg', 'jpg', 'webp']
# MAX_FILE_SIZE = 500 * 1024  # Maksimum ukuran file 500KB

# def validate_file(file: UploadFile):
#     # Langkah 1: Periksa format file
#     filename = file.filename
#     file_extension = filename.split('.')[-1].lower()

#     if file_extension not in ALLOWED_EXTENSIONS:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, 
#             detail=f"File format not allowed. Please upload one of the following formats: {', '.join(ALLOWED_EXTENSIONS)}"
#         )

#     # Langkah 2: Periksa ukuran file
#     file.file.seek(0, 2)  # Pindahkan pointer ke akhir file untuk mendapatkan ukuran
#     file_size = file.file.tell()  # Dapatkan ukuran file
#     file.file.seek(0)  # Kembalikan pointer ke awal agar file bisa dibaca kembali setelah validasi

#     if file_size > MAX_FILE_SIZE:
#         raise HTTPException(
#             status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
#             detail=f"File too large. Maximum allowed size is {MAX_FILE_SIZE / 1024} KB"
#         )


async def update_my_photo(db: Session, user_id: str, file: UploadFile) -> optional.Optional[UserModel, HTTPException]:
    try:
        # Langkah 1: Mencari user yang ada
        user_model = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user_model:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        # Langkah 2: Validasi file jika ada
        if file:
            validate_file(file)  # Panggil fungsi validasi

            # Debugging: Cek apakah file diterima
            print(f"File diterima untuk upload: {file.filename}")

            # Upload gambar ke Supabase atau storage lain
            public_url = await upload_image_to_supabase(
                file, 
                "YakuseProject-storage", 
                user_id, 
                folder_name="images/only_photo_profile", 
                old_file_url=user_model.photo_url
                )
            
            print(f"Public URL dari file yang diupload: {public_url}")
            
            if public_url is None:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to upload image.")
            
            # Update photo_url pada user
            user_model.photo_url = public_url           

        # Simpan perubahan ke dalam database
        db.add(user_model)
        db.commit()
        db.refresh(user_model)

        return optional.build(data=user_model)

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Database conflict: {str(e)}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )



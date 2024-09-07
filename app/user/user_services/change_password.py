from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from app.libs import password_lib

from app.user import user_dtos
from app.user.user_model import UserModel

from app.utils import optional

# async def change_password(db: Session, user_id: str, old_password: str, new_password: str) -> optional.Optional[None, Exception]:
#     try:
#         # Langkah 1: Cari user berdasarkan user_id
#         user = db.query(UserModel).filter(UserModel.id == user_id).first()
#         if not user:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

#         # Langkah 2: Validasi password lama
#         if not password_lib.verify_password(old_password, user.hash_password):
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Old password is incorrect")

#         # Langkah 3: Update password baru
#         user.hash_password = password_lib.get_password_hash(new_password)
#         db.commit()

#         return optional.build(data=None)

#     except Exception as e:
#         db.rollback()
#         return optional.build(error=HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"An error occurred: {str(e)}"
#         ))

async def change_password(
        db: Session, user_id: str, old_password: str, new_password: str
) -> optional.Optional[None, Exception]:
    try:
        # Langkah 1: Cari user berdasarkan ID
        user_model = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user_model:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        # Langkah 2: Verifikasi password lama
        if not password_lib.verify_password(old_password, user_model.hash_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Old password is incorrect")

        # Langkah 3: Update password baru
        user_model.hash_password = password_lib.get_password_hash(new_password)
        db.commit()

        return optional.build(data=None)

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


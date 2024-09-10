
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status


from app.user.user_model import UserModel

from app.utils import optional

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from app.user.user_model import UserModel
from app.utils import optional

async def delete_user_by_user_id(db: Session, user_id: str) \
        -> optional.Optional[None, Exception]:
    try:
        # Langkah 1: Mencari user yang ada
        user_model = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user_model:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User account not found")

        # Simpan informasi pengguna sebelum dihapus
        user_info = {
            "user_id": user_model.id,
            "username": user_model.username,
            "email": user_model.email
        }

        # Langkah 2: Hapus user dari database
        db.delete(user_model)
        db.commit()

        return optional.build(data=user_info) # Mengembalikan ID pengguna yang dihapus
        # return optional.build(data=None)

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

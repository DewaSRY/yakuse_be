from typing import List, Type
import uuid
from sqlalchemy import desc, func, or_
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, UploadFile, status

from app.business_category.business_category_model import BusinessCategory
from app.libs.images_service import create_image_service
from app.user.user_model import UserModel

from . import business_dtos
from .business_model import Business
from app.rating.rating_model import Rating

from app.utils import optional


# create-business-with-photo 
async def create_business_with_photo(db: Session, business: business_dtos.BusinessCreateDto, user_id: str,
                                     file: UploadFile) -> optional.Optional[Business, Exception]:
    try:
        # Langkah 1: Membuat bisnis
        business_model = Business(**business.model_dump())
        business_model.fk_owner_id = user_id

        # Langkah 2: Upload foto
        opt_content = await create_image_service(upload_file=file, domain="business")

        # Jika upload berhasil, update `photo_url` dalam `business_model`
        business_model.photo_url = opt_content.data

        # Simpan bisnis ke dalam database
        db.add(business_model)
        db.commit()
        db.refresh(business_model)

        return optional.build(data=business_model)

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


# business-edit-with-photo
async def edit_business_by_business_id(
        db: Session, business_id: str, business: business_dtos.BusinessEditDto, user_id: str, file: UploadFile
) -> optional.Optional[Business, Exception]:
    try:
        # Langkah 1: Mencari bisnis yang ada
        business_model = db.query(Business).filter(Business.id == business_id, Business.fk_owner_id == user_id).first()
        if not business_model:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business not found")

        # Langkah 2: Upload foto
        opt_content = await create_image_service(upload_file=file, domain="business")

        # Jika upload berhasil, update `photo_url` dalam `business_model`
        if opt_content.data:
            business_model.photo_url = opt_content.data

        # Update atribut bisnis
        for attr, value in business.model_dump().items():
            setattr(business_model, attr, value)

        # Simpan perubahan ke dalam database
        db.add(business_model)
        db.commit()
        db.refresh(business_model)

        return optional.build(data=business_model)

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


# get_all_my-business
def get_business_by_user_id(db: Session, user_id: str, skip: int = 0, limit: int = 100) \
        -> optional.Optional[Type[Business], Exception]:
    print(user_id)
    try:
        business_model = db.query(Business) \
            .order_by(desc(Business.created_at)).filter(Business.fk_owner_id == user_id).offset(skip).limit(limit).all()

        if business_model:  # if the bisniss is not zero
            return optional.build(data=business_model)
        else:
            return optional.build(error=HTTPException(status_code=404, detail="you not to access all data busines"))

    except SQLAlchemyError as e:
        db.rollback()
        raise optional.build(error=HTTPException(status_code=409, detail="Database conflict: " + str(e)))


# delete-my-business
async def delete_business_by_id(db: Session, business_id: str, user_id: str) -> optional.Optional[None, Exception]:
    try:
        # Langkah 1: Mencari bisnis yang ada
        business_model = db.query(Business).filter(Business.id == business_id, Business.fk_owner_id == user_id).first()
        if not business_model:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business not found")

        # Langkah 2: Hapus bisnis dari database
        db.delete(business_model)
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


# all-list-business-by-userid
def get_all_business_by_user_id(db: Session, user_id: str, skip: int = 0, limit: int = 100) \
        -> optional.Optional[List[Type[Business]], Exception]:
    try:
        business_model = db.query(Business) \
            .order_by(desc(Business.created_at)) \
            .filter(Business.fk_owner_id == user_id) \
            .offset(skip).limit(limit).all()

        if business_model:  # if the bisniss is not zero
            return optional.build(data=business_model)
        else:
            return optional.build(
                error=HTTPException(status_code=404, detail="you not to access all data busines from this user_id"))

    except Exception as e:
        print(e)
        return optional.build(error=HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="failed to fetch business"
        ))


# detail-business-by-business-uuid
def get_detail_business_by_business_id(db: Session, business_id: uuid.UUID) \
        -> optional.Optional[Type[Business], Exception]:
    business_id_str = str(business_id)
    try:
        business_model = db.query(Business) \
            .filter(Business.id == business_id_str) \
            .first()

        if business_model is None:
            return optional.build(error=HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"business with id {business_id} not found"
            ))
        return optional.build(data=business_model)

    except Exception as e:
        return optional.build(error=HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="failed to fetch business"
        ))


# get-all-list-business-public
def get_all_business(db: Session, skip: int = 0, limit: int = 100) \
        -> optional.Optional[List[Type[Business]], Exception]:
    try:
        business_model = db.query(Business) \
            .order_by(desc(Business.created_at)).offset(skip).limit(limit).all()

        if business_model is None:
            return optional.build(error=HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"all business not access"
            ))
        return optional.build(data=business_model)
    except SQLAlchemyError as e:
        db.rollback()
        raise optional.build(
            error=HTTPException(status_code=409, detail="Database conflict: " + str(e)))


# get-all-business-by-business-category
def get_all_business_by_category(db: Session, category_name: str) \
        -> optional.Optional[List[Type[Business]], Exception]:
    try:
        # Mencari semua bisnis berdasarkan kategori
        businesses = db.query(Business).join(Business.business_category) \
            .filter(BusinessCategory.name == category_name).all()

        if businesses is None:
            return optional.build(error=HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No businesses found for this category"
            ))
        return optional.build(data=businesses)

    except SQLAlchemyError as e:
        return optional.build(error=HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Database conflict: {str(e)}"
        ))

    except Exception as e:
        return optional.build(error=HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        ))


# get-list-businees-by-search-keyword
def search_business_by_keyword(db: Session, keyword: str) \
        -> optional.Optional[List[Type[Business]], Exception]:
    try:
        search_query = f"%{keyword}%"
        businesses = db.query(Business) \
            .filter((Business.name.ilike(search_query))).all()

        if not businesses:
            return optional.build(error=HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No businesses found matching the keyword"
            ))

        return optional.build(data=businesses)

    except SQLAlchemyError as e:
        return optional.build(error=HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Database conflict: {str(e)}"
        ))

    except Exception as e:
        return optional.build(error=HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        ))

from typing import List, Type
import uuid
from sqlalchemy import desc, func, or_
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, UploadFile, status

from app.business_category.business_category_model import BusinessCategory
from app.libs.images_service import create_image_service
from app.user.user_model import UserModel

from app.business import business_dtos
from app.business.business_model import Business
from app.rating.rating_model import Rating

from app.utils import optional


def get_all_business_pagination(db: Session, skip: int = 0, limit: int = 10, page: int = 1) -> business_dtos.PaginatedResponseDto:
    try:
        # Hitung total records
        total_records = db.query(func.count(Business.id)).scalar()

        # Ambil data bisnis
        business_models = db.query(Business) \
            .order_by(desc(Business.created_at)) \
            .offset(skip).limit(limit).all()

        if not business_models:
            return business_dtos.PaginatedResponseDto(
                data=[],
                pagination=business_dtos.PaginationDto(
                    total_records=total_records,
                    current_page=page,
                    total_pages=1,
                    next_page=None,
                    prev_page=None
                )
            )

        # Konversi objek Business ke DTO BusinessAllPost
        data = [
            business_dtos.BusinessAllPost(
                id=str(business.id),
                name=business.name,
                photo_url=business.photo_url,
                category=business.category,
                avg_rating=business.avg_rating,
                created_at=business.created_at,
                rating_list=business.rating_list  # Mengambil daftar rating
            )
            for business in business_models
        ]

        total_pages = (total_records + limit - 1) // limit
        next_page = page + 1 if page < total_pages else None
        prev_page = page - 1 if page > 1 else None

        pagination = business_dtos.PaginationDto(
            total_records=total_records,
            current_page=page,
            total_pages=total_pages,
            next_page=next_page,
            prev_page=prev_page
        )

        return business_dtos.PaginatedResponseDto(data=data, pagination=pagination)
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=409, detail="Database conflict: " + str(e))
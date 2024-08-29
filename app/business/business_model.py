import uuid
from typing import Type
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship, backref, Mapped

from app.business_category.business_category_model import BusinessCategory
from app.libs import sql_alchemy_lib
from app.business import business_dtos
import re


class Business(sql_alchemy_lib.Base):
    __tablename__ = "business"
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    name = Column(String(50), unique=True, index=True)
    omset = Column(Float)
    description: str = Column(Text)
    photo_url = Column(String(255))
    location = Column(Text)
    contact = Column(CHAR(36))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    fk_business_category_id = Column(Integer, ForeignKey('business_category.id'))
    fk_owner_id = Column(CHAR(36), ForeignKey('users.id'))

    ratings: Mapped[list["Rating"]] = relationship(back_populates="business")

    user: Mapped["UserModel"] = relationship(viewonly=True)
    business_category: Mapped["BusinessCategory"] = relationship(viewonly=True)

    def __repr__(self):
        return f"{self.name} {self.id}"

    @property
    def description_list(self):
        if self.description is None:
            return []
        d_list = re.split("\\s{4,}", self.description)
        return [d for d in d_list if len(d) != 0]

    @property
    def category(self):
        return self.business_category.name if self.business_category else ""

    @property
    def owner(self):
        from app.user.user_model import UserModel
        user_models: UserModel = self.user
        return user_models.username if user_models else ""

    @property
    def owner_id(self):
        from app.user.user_model import UserModel
        user_models: UserModel = self.user
        return user_models.id if user_models else ""

    @property
    def owner_info(self):
        from app.user.user_model import UserModel
        user_model: UserModel = self.user
        return business_dtos.OwnerBusinessInfoDto(
            user_id=user_model.id,
            fullname=user_model.fullname,
            photo_url=user_model.photo_url
        ).model_dump()

    # @property
    # def avg_rating(self):
    #     rating_list = self.ratings
    #     if len(rating_list) == 0:  # Menggunakan relasi ratings langsung
    #         return 0
    #     total_rating = sum(rating.rating_count for rating in rating_list)
    #     average_rating = total_rating / len(rating_list)
    #     return round(average_rating, 1)  # Membulatkan ke 1 angka di belakang koma

    @property
    def avg_rating(self):
        if not self.ratings:  # Menggunakan relasi ratings langsung
            return 0
        total_rating = sum(rating.rating_count for rating in self.ratings)
        average_rating = total_rating / len(self.ratings)
        return round(average_rating, 1)

    @property
    def total_rater(self):
        return len(self.ratings)

    @property
    def rating_list(self):
        from app.rating.rating_model import Rating
        ratting_dtos = []
        ratting_list: list[Rating] = self.ratings
        for ratting in ratting_list:
            ratting_dto = business_dtos.BusinessRatingDto(
                id=ratting.id,
                rating_count=ratting.rating_count,
                review_description=ratting.review_description,
                rater_name=ratting.rater_name).model_dump()
            ratting_dtos.append(ratting_dto)
        return ratting_dtos

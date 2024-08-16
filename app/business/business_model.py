import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship, backref

from app.rating.rating_dtos import BusinessRatingDto

from app.libs import sql_alchemy_lib
from app.business import business_dtos
import re


class Business(sql_alchemy_lib.Base):
    __tablename__ = "business"
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    name = Column(String(50), unique=True, index=True)
    price = Column(String(50))
    description: str = Column(Text)
    photo_url = Column(String(255))
    location = Column(Text)
    contact = Column(CHAR(36))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    fk_business_category_id = Column(Integer, ForeignKey('business_category.id'))
    fk_owner_id = Column(CHAR(36), ForeignKey('users.id'))

    # Relationship to Rating
    ratings = relationship("Rating", back_populates="business")

    # New relationship to BusinessCategory
    business_category = relationship("BusinessCategory", backref=backref("business", lazy=True))

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
        session = next(sql_alchemy_lib.get_db())
        user_models: UserModel = session.query(UserModel) \
            .filter(UserModel.id.like(f"%{self.fk_owner_id}%")) \
            .first()
        return user_models.username if user_models else ""

    @property
    def owner_id(self):
        from app.user.user_model import UserModel
        session = next(sql_alchemy_lib.get_db())
        user_models: UserModel = session.query(UserModel) \
            .filter(UserModel.id.like(f"%{self.fk_owner_id}%")) \
            .first()
        return user_models.id if user_models else ""

    @property
    def owner_info(self):
        from app.user.user_model import UserModel
        session = next(sql_alchemy_lib.get_db())

        user_model: UserModel = session.query(UserModel) \
            .filter(UserModel.id == self.fk_owner_id).first()

        return business_dtos.OwnerBusinessInfoDto(
            user_id=user_model.id,
            fullname=user_model.fullname,
            photo_url=user_model.photo_url
        ).model_dump()

    @property
    def rating(self):
        if not self.ratings:  # Menggunakan relasi ratings langsung
            return 0.0

        total_rating = sum(rating.rating_count for rating in self.ratings)
        average_rating = total_rating / len(self.ratings)
        return round(average_rating, 1)  # Membulatkan ke 1 angka di belakang koma


    @property
    def total_rater(self):
        if not self.ratings:
            return 0

        # Hitung jumlah unik user_id dari ratings
        unique_raters = {rating.fk_rater_id for rating in self.ratings}
        return len(unique_raters)

    @property
    def rating_list(self):
        # Menggunakan relasi ratings langsung
        return [BusinessRatingDto.from_orm(rating) for rating in self.ratings]

import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship, backref

from app.rating.rating_dtos import BusinessRatingDto

from app.libs import sql_alchemy_lib


class Business(sql_alchemy_lib.Base):
    __tablename__ = "business"
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    name = Column(String(50), unique=True, index=True)
    description = Column(Text)
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
    def rating(self):
        if not self.ratings:  # Menggunakan relasi ratings langsung
            return 0

        total_rating = sum(rating.rating_count for rating in self.ratings)
        return total_rating / len(self.ratings)
    
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


    # @property
    # def rating(self):
    #     session = next(sql_alchemy_lib.get_db())
        
    #     average_rating = session.query(func.avg(Rating.rating_count)).filter(Rating.fk_business_id == self.id).scalar()
        
    #     return average_rating if average_rating is not None else 0

    # @property
    # def rating(self):
    #     from app.rating.rating_model import Rating
    #     session = next(sql_alchemy_lib.get_db())
    #     ratting_list: list[Rating] = session.query(Rating) \
    #         .filter(Rating.fk_business_id.like(f"%{self.id}%")) \
    #         .all()
    #     if len(ratting_list) == 0:
    #         return 0

    #     total_ratting = 0
    #     for ratting in ratting_list:
    #         total_ratting += ratting.rating_count

    #     return total_ratting / len(ratting_list)

    # @property
    # def rating_list(self):
    #     from app.rating.rating_model import Rating
    #     session = next(sql_alchemy_lib.get_db())
        
    #     rating_list: list[Rating] = session.query(Rating) \
    #         .filter(Rating.fk_business_id == self.id) \
    #         .all()

    #     # Konversi setiap Rating ke dalam RatingDto
    #     return [BusinessRatingDto.from_orm(rating) for rating in rating_list]
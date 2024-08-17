import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship

from app.libs import sql_alchemy_lib


class Rating(sql_alchemy_lib.Base):
    __tablename__ = "rating"
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    rating_count = Column(Integer, index=True)
    review_description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    fk_business_id = Column(CHAR(36), ForeignKey('business.id'))
    fk_rater_id = Column(CHAR(36), ForeignKey('users.id'))

    # Relationship to Business
    # business = relationship("Business", back_populates="ratings")

    @property
    def business_name(self) -> str:
        from app.business.business_model import Business
        session = next(sql_alchemy_lib.get_db())
        business_model: Business = session.query(Business) \
            .filter(Business.id.like(f"%{self.fk_business_id}%")) \
            .first()

        return business_model.name if business_model else ""

    @property
    def rater_name(self) -> str:
        from app.user.user_model import UserModel
        session = next(sql_alchemy_lib.get_db())
        user_models: UserModel = session.query(UserModel) \
            .filter(UserModel.id.like(f"%{self.fk_rater_id}%")) \
            .first()

        return user_models.username if user_models else ""

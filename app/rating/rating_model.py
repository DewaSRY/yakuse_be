import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship, Mapped

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

    business: Mapped["Business"] = relationship(back_populates="ratings")
    user: Mapped["UserModel"] = relationship(back_populates="")

    @property
    def business_name(self) -> str:
        from app.business.business_model import Business
        business_model: Business = self.business
        return business_model.name if business_model else ""

    @property
    def rater_name(self) -> str:
        from app.user.user_model import UserModel
        user_models: UserModel = self.user
        return user_models.username if user_models else ""

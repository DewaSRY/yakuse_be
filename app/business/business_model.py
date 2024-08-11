import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship, backref

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

    @property
    def owner(self) -> str:
        from app.user.user_model import UserModel
        session = next(sql_alchemy_lib.get_db())
        user_models: UserModel = session.query(UserModel) \
            .filter(UserModel.id.like(f"%{self.fk_owner_id}%")) \
            .first()

        return user_models.username if user_models else ""

    @property
    def rating(self):
        from app.rating.rating_model import Rating
        session = next(sql_alchemy_lib.get_db())
        ratting_list: list[Rating] = session.query(Rating) \
            .filter(Rating.fk_business_id.like(f"%{self.id}%")) \
            .all()
        if len(ratting_list) == 0:
            return 0
        
        total_ratting = 0
        for ratting in ratting_list:
            total_ratting += ratting.rating_count

        return total_ratting / len(ratting_list)

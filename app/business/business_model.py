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

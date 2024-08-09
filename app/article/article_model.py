import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.mysql import CHAR

from app.libs import sql_alchemy_lib


class Article(sql_alchemy_lib.Base):
    __tablename__ = "article"
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    title = Column(Text)
    description = Column(Text)
    image_url = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    fk_business_category_id = Column(Integer, ForeignKey('business_category.id'))
    fk_author_id = Column(CHAR(36), ForeignKey('users.id'))
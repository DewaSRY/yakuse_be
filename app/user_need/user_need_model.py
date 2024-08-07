import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.mysql import CHAR

from app.libs import sql_alchemy_lib


class UserNeeds(sql_alchemy_lib.Base):
    __tablename__ = "user_needs"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String(100), unique=True, index=True)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_visible = Column(Boolean, default=True)
    fk_business_category_id = Column(Integer, ForeignKey('business_category.id'))
    fk_user_id = Column(CHAR(36), ForeignKey('users.id'))
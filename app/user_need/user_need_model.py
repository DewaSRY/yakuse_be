import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import CHAR

from .user_need_dtos import UserNeedUserInfoDto, UserNeedBusinessCategoryDto

from app.libs import sql_alchemy_lib
from app.user.user_model import UserModel
from app.business_category.business_category_model import BusinessCategory

"""
    owner_username: str
    user_profile_url: str
"""


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

    user_info = relationship("UserModel", backref="user_needs")
    business_category = relationship("BusinessCategory", backref="user_needs")

    @property
    def user_info(self) -> dict[str, str]:
        from app.user.user_model import UserModel
        session = next(sql_alchemy_lib.get_db())

        user_model: UserModel = session.query(UserModel) \
            .filter(UserModel.id == self.fk_user_id).first()

        return UserNeedUserInfoDto(
            user_id=user_model.id,
            owner_username=user_model.username,
            user_profile_url=user_model.photo_url
        ).model_dump()
    
    @property
    def category(self):
        from app.business_category.business_category_model import BusinessCategory
        session = next(sql_alchemy_lib.get_db())

        business_category_model: BusinessCategory = session.query(BusinessCategory) \
            .filter(BusinessCategory.id == self.fk_business_category_id).first()
        
        return UserNeedBusinessCategoryDto(
            id=business_category_model.id,
            name=business_category_model.name
        ).model_dump()

    def __repr__(self):
        return f"{self.title} {self.id} {self.fk_user_id}"

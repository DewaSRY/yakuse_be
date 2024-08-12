import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.mysql import CHAR

from app.libs import sql_alchemy_lib
from .user_need_dtos import UserNeedsUserInfoDto

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

    @property
    def user_info(self) -> dict[str, str]:
        from app.user.user_model import UserModel
        session = next(sql_alchemy_lib.get_db())

        user_model: UserModel = session.query(UserModel) \
            .filter(UserModel.id == self.fk_user_id).first()

        return UserNeedsUserInfoDto(
            user_id=user_model.id,
            owner_username=user_model.username,
            user_profile_url=user_model.photo_url
        ).model_dump()

    def __repr__(self):
        return f"{self.title} {self.id} {self.fk_user_id}"

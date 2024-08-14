import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.mysql import CHAR

from app.libs import sql_alchemy_lib
from app.user_need import user_need_dtos

"""
    owner_username: str
    user_profile_url: str
"""


class UserNeeds(sql_alchemy_lib.Base):
    __tablename__ = "user_needs"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String(100))
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

        return user_need_dtos.UserNeedUserInfoDto(
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
        
        return user_need_dtos.UserNeedBusinessCategoryDto(
            id=business_category_model.id,
            name=business_category_model.name
        ).model_dump()
    
    def to_dto(self) -> user_need_dtos.UserNeedResponseDto:
        return user_need_dtos.UserNeedResponseDto(
            id=self.id,
            title=self.title,
            user_info=self.user_info,
            description=self.description,
            is_visible=self.is_visible,
            category=self.category,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    def __repr__(self):
        return f"<UserNeed: id({self.id}) title({self.title}) user_id({self.fk_user_id}) "

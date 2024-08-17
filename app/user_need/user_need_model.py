import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship, backref, Mapped

from app.libs import sql_alchemy_lib
from app.user_need import user_need_dtos


class UserNeeds(sql_alchemy_lib.Base):
    __tablename__ = "user_needs"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String(100), index=True)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_visible = Column(Boolean, default=True)

    fk_business_category_id = Column(Integer, ForeignKey('business_category.id'))
    fk_user_id = Column(CHAR(36), ForeignKey('users.id'))

    business_category: Mapped["BusinessCategory"] = relationship(viewonly=True)
    user: Mapped["UserModel"] = relationship(viewonly=True)

    @property
    def user_info(self) -> dict[str, str]:
        from app.user.user_model import UserModel
        user_model: UserModel = self.user
        return user_need_dtos.UserNeedUserInfoDto(
            user_id=user_model.id,
            fullname=user_model.fullname,
            username=user_model.username,
            user_profile_url=user_model.photo_url
        ).model_dump()

    @property
    def category(self):
        from app.business_category.business_category_model import BusinessCategory
        business_category_model: BusinessCategory = self.business_category
        return user_need_dtos.UserNeedBusinessCategoryDto(
            id=business_category_model.id,
            name=business_category_model.name
        ).model_dump()

    def __repr__(self):
        return f"<UserNeed: id({self.id}) title({self.title}) user_id({self.fk_user_id}) "

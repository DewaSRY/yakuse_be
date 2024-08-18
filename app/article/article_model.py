import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import Mapped, relationship

from app.libs import sql_alchemy_lib
from app.article import article_dtos


class Article(sql_alchemy_lib.Base):
    __tablename__ = "article"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    title = Column(String(255))
    description = Column(Text)
    image_url = Column(String(255))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    fk_business_category_id = Column(Integer, ForeignKey('business_category.id'))
    fk_author_id = Column(CHAR(36), ForeignKey('users.id'))

    business_category: Mapped["BusinessCategory"] = relationship(viewonly=True)
    author: Mapped["UserModel"] = relationship(viewonly=True)

    @property
    def author_info(self) -> dict[str, str]:
        from app.user.user_model import UserModel
        author_model: UserModel = self.author
        return article_dtos.ArticleAuthorInfoDto(
            author_id=author_model.id,
            fullname=author_model.fullname,
            username=author_model.username,
            author_photo_url=author_model.photo_url
        ).model_dump()
    
    @property
    def category(self):
        from app.business_category.business_category_model import BusinessCategory
        business_category_model: BusinessCategory= self.business_category
        return article_dtos.ArticleBusinessCategoryDto(
            id=business_category_model.id,
            name=business_category_model.name
        ).model_dump()
    
    def __repr__(self):
        return f"<Article: id({self.id}) title({self.title}) author_id({self.fk_author_id} category({self.fk_business_category_id}))>"
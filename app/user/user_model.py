import uuid
import re
from sqlalchemy import Column, DateTime, String, Text, func
from sqlalchemy.dialects.mysql import CHAR

from app.libs import sql_alchemy_lib


class UserModel(sql_alchemy_lib.Base):
    __tablename__ = "users"
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    fullname = Column(String(50))
    username = Column(String(50), unique=True)
    email = Column(String(50), unique=True, index=True)
    hash_password = Column(String(100))
    phone = Column(String(50))
    address = Column(Text)
    about_me = Column(Text)
    photo_url = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    @property
    def about_me_list(self):
        if self.about_me is None:
            return []
        d_list = re.split("\\s{4,}", self.about_me)

        return [d for d in d_list if len(d) != 0]

    def __repr__(self):
        return f"{self.id} {self.username}"

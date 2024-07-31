import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import CHAR

from app.libs import sql_alchemy_lib


class UserModel(sql_alchemy_lib.Base):
    __tablename__ = "users"
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(50), unique=True, index=True)
    password = Column(String(100))

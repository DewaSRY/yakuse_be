import uuid

from sqlalchemy import ARRAY, Column, DateTime, Integer, String, Text, func
from sqlalchemy.dialects.mysql import CHAR

from app.libs import sql_alchemy_lib


class BusinessCategory(sql_alchemy_lib.Base):
    __tablename__ = "business_category"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(50), unique=True, index=True)
    describe = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, name: str, description: str):
        self.name = name
        self.describe = description

    def __repr__(self):
        return f"name:{self.name}, description:{self.describe}"

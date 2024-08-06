import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import CHAR

from app.libs import sql_alchemy_lib


class HealthCheckModel(sql_alchemy_lib.Base):
    __tablename__ = "healthcheck"
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    name = Column(String(50), unique=True, index=True)

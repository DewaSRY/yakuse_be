import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.libs import sql_alchemy_lib

engine = create_engine(
    "sqlite:///test_app.db", connect_args={"check_same_thread": False}
)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_all_table():
    sql_alchemy_lib.Base \
        .metadata.create_all(bind=engine)


def drop_all_table():
    sql_alchemy_lib.Base \
        .metadata.drop_all(bind=engine)


@pytest.fixture
def get_db():
    create_all_table()
    database = session_local()
    try:
        yield database
    finally:
        database.close()

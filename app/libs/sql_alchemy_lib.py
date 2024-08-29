from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy import Engine
import os
from dotenv import load_dotenv

load_dotenv()
"""
#######################This use to create connection with database###########################################
"""
APP_DEVELOPMENT = os.getenv("APP_DEVELOPMENT", True)
engine: Engine

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# #     connect_args={"check_same_thread": False},

# # Konfigurasi basis data dari variabel lingkungan
# DB_TYPE = os.getenv("DB_TYPE")
# DB_NAME = os.getenv("DB_NAME")
# DB_USER = os.getenv("DB_USER")
# DB_PASSWORD = os.getenv("DB_PASSWORD")
# DB_HOST = os.getenv("DB_HOST")
# DB_PORT = os.getenv("DB_PORT")

# # Update the SQLALCHEMY_DATABASE_URL to use PostgreSQL
SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URI')

# Pastikan DATABASE_URL diatur
if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DATABASE_URI is not set in the environment variables")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# # Membuat engine SQLAlchemy
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL,
#     pool_size=10,  # Increase the pool size
#     max_overflow=20,  # Adjust overflow size
#     pool_timeout=30,
# )

# letter we will use postgrest for easier service
# MYSQL_CONNECTOR = os.getenv("SQLALCHEMY_DATABASE_URL", "mysql+pymysql://root:password@localhost/MYDB")
# engine = create_engine(MYSQL_CONNECTOR)

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
"""
######################Tis code use to make interact with database object###################################
######################Mostly to do manipulation to define entity of database###############################
"""
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""
#########################Base is abstract object use to define table on database############################
#########################Developer will use it as abstract object to inherit################################
"""
Base = declarative_base()
"""
############################This code use to get the session, use to manipulation data######################
############################How to use the code,should by fastapi way#######################################
############################How to use it have something to do with dependency injection####################
############################To understand more about the code please read de fastapi document###############
############################Read this [https://fastapi.tiangolo.com/tutorial/sql-databases/]################
"""


# Dependency to get the database session
def get_db():
    database = session_local()
    try:
        yield database
    finally:
        database.close()

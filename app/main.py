from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import business_category, rating

from . import user, health_check, business, user_need, article
from .libs import sql_alchemy_lib

from .business_category import business_category_seed
from .business import business_seed

from fastapi.staticfiles import StaticFiles

import os

"""
This user to auto create all table
Dewa Wont to change database to use SQLite along development
"""

"""
INIT ALL Database Here
"""
from app.user.user_model import UserModel
from app.health_check.health_check_model import HealthCheckModel
from app.business_category.business_category_model import BusinessCategory
from app.business.business_model import Business
from app.rating.rating_model import Rating
from app.user_need.user_need_model import UserNeeds
from app.article.article_model import Article

sql_alchemy_lib.Base.metadata.create_all(bind=sql_alchemy_lib.engine)

app = FastAPI()

app.include_router(health_check.router)
app.include_router(user.user_router.router)
app.include_router(business.business_router.router)
app.include_router(business_category.business_category_router.router)
app.include_router(rating.rating_router.router)
app.include_router(user_need.user_need_router.router)
app.include_router(article.article_router.router)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://tools.slingacademy.com",
    "https://www.slingacademy.com",
    "https://yakuse.vercel.app"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=['*'],
)

if business_category_seed.get_business_category_length() == 0:
    business_category_seed.init_business_category()

if business_seed.get_business_length() == 0:
    business_seed.init_business()

root_directory = os.getcwd()  # Gets the current working directory
images_directory = os.path.join(root_directory, "images")
app.mount("/images", StaticFiles(directory=images_directory), name="images")

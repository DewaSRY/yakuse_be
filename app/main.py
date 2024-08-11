from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import business_category, rating

from . import user, health_check, business, user_need, article
from .libs import sql_alchemy_lib

from .business_category import business_category_service, business_category_dtos

from fastapi.staticfiles import StaticFiles

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

sql_alchemy_lib.Base \
    .metadata.create_all(bind=sql_alchemy_lib.engine)

app = FastAPI()

app.include_router(health_check.router)
app.include_router(user.user_router.router)
app.include_router(business.business_router.router)
app.include_router(business_category.business_category_router.router)
app.include_router(rating.rating_router.router)
app.include_router(user_need.user_need_router.router)
app.include_router(article.article_router.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# if len(business_category_service.get_business_category(sql_alchemy_lib.get_db())) == 0:
#     business_category_service.create_business_category(
#         sql_alchemy_lib.get_db(),
#         business_category_dtos.BusinessCategoryCreateDto()
#     )

app.mount("/images", StaticFiles(directory="images"), name="images")

"""
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijg0NzdiZWJhLWM4ZjQtNGVkZi1iN2NlLTUzZTQ3NGFlMmFlMiIsImV4cCI6MTcyMzY0Njk4Nn0.y973u9V7QBjqmL7tbakHYPHPMSEllCOjFKlsL4ghSVs
"""

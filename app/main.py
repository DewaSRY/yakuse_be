from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import user, health_check, business, user_need, article
from .libs import sql_alchemy_lib

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
app.include_router(user_need.user_need_router.router)
app.include_router(article.article_router.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/images", StaticFiles(directory="images"), name="images")

"""
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijg0NzdiZWJhLWM4ZjQtNGVkZi1iN2NlLTUzZTQ3NGFlMmFlMiIsImV4cCI6MTcyMzY0Njk4Nn0.y973u9V7QBjqmL7tbakHYPHPMSEllCOjFKlsL4ghSVs
"""

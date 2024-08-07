from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import user, health_check
from .libs import sql_alchemy_lib

from fastapi.staticfiles import StaticFiles

"""
This user to auto create all table
Dewa Wont to change database to use SQLite along development
"""
sql_alchemy_lib.Base \
    .metadata.create_all(bind=sql_alchemy_lib.engine)

app = FastAPI()

app.include_router(health_check.router)
app.include_router(user.user_router.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/images", StaticFiles(directory="images"), name="images")

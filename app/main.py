from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import user, health_check

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

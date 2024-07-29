from fastapi import FastAPI
from . import user, health_check

app = FastAPI()
app.include_router(health_check.router)
app.include_router(user.router)

# @app.get("/")
# def health_check():
#     return {
#         "message": "hello world"
#     }

from typing import Annotated
from datetime import timedelta
from fastapi import APIRouter, Depends

from app.libs import jwt_lib

description = """
# Health check 
this rout purpose is to check the health of the api
"""

router = APIRouter(
    tags=["health_check"],
    prefix="",
)


@router.get("/")
def api_health_check():
    """
    #api_health_check
    this function use to check the api is running
    :return:
    """
    return {"message": "hello world"}


@router.get("/protect")
def protection_health_check(jwt_token: Annotated[jwt_lib.TokenData, Depends(jwt_lib.get_jwt_pyload)]):
    """
    # protection_health_check

    """
    return {"jwt_payload": jwt_token}


@router.get("/token")
def protection_health_check():
    data = dict([
        ("user_id", "this is some id")
    ])
    return {
        "jwt_token": jwt_lib.create_access_token(data=data, expires_delta=timedelta(weeks=1))
    }

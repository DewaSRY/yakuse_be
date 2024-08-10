from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile
from pydantic import BaseModel, fields

from app.libs.jwt_lib import jwt_dto, jwt_service
from app.libs.images_service import create_image_service

router = APIRouter(
    tags=["health_check"],
    prefix="",
)


class MessageDto(BaseModel):
    message: str


@router.get("/", response_model=MessageDto)
def api_health_check():
    """
    # api_health_check
    this function use to check the api is running
    """
    return {"message": "hello world"}


@router.get("/protect", response_model=jwt_dto.TokenPayLoad)
def protection_health_check(jwt_token: Annotated[jwt_dto.TokenPayLoad, Depends(jwt_service.get_jwt_pyload)]):
    """
    # protection_health_check
    This end pint use to parse token payload
    """
    return jwt_token


@router.get("/token", response_model=jwt_dto.AccessTokenDto)
def fake_access_token():
    """
    # protection_health_check
    this endpoint use to generate fake jwt token. the fake jwt will contain fake user id,
    because almost every end point need valid endpoint this jwt will useless
    """
    data = dict([
        ("user_id", "this is some id")
    ])
    return jwt_service.create_access_token(data=data)


@router.put("/files")
async def create_upload_file(file: UploadFile):
    opt_content = await create_image_service(upload_file=file, domain="health_check")

    if opt_content.error:
        raise opt_content.error

    return {"filename": opt_content.data}

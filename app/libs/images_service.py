from fastapi import UploadFile, HTTPException, status
from app.utils import optional
import re
from dotenv import load_dotenv
import os

load_dotenv()
IMAGES_DIRECTORY = "images"
ALLOWED_EXTENSION = [".png", ".jpg", ".webp"]


async def create_image_service(upload_file: UploadFile, domain: str) -> optional.Optional:
    content = await upload_file.read()

    if not _is_extension_valid(file_name=upload_file.filename):
        return _raise_exception()

    image_dir = f"{IMAGES_DIRECTORY}/{domain}/{upload_file.filename}"

    with open(image_dir, "wb") as f:
        f.write(content)

    host_url = os.getenv("HOST_URL", "http://127.0.0.1:8000/")
    image_url = f"{host_url}/{image_dir}"

    return optional.build(data=image_url)


def _is_extension_valid(file_name: str):
    result = re.findall(r"\.[a-zA-Z]{3,}", file_name)[0]
    return result in ALLOWED_EXTENSION


def _raise_exception() -> optional.Optional:
    return optional.build(error=HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="not allowed extension"
    ))

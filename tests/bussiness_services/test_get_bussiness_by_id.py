from app.user import user_services, user_dtos
from unittest import TestCase

MOCK_USER_DTO = user_dtos.UserCreateDto(
    username="some username", email="some@Example.com", fullname="some full name", password="some password")

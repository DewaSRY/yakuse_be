import pytest

from app.user import user_services, user_dtos


@pytest.fixture(scope="module")
def get_user_dto(get_db):
    return user_services.create_user(get_db, user_dtos.UserCreateDto()).data


def test_user_can_create_access_token(get_user_dto):
    access_token = user_services.service_access_token(get_user_dto.id)
    assert access_token.access_token is not None

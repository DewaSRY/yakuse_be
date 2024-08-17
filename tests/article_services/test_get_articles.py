import pytest

from app.user import user_services, user_dtos


@pytest.fixture()
def get_user_model(get_db):
    return user_services.create_user(get_db, user_dtos.UserCreateDto()).data

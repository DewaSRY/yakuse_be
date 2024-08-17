import pytest

from app.user import user_services, user_dtos


@pytest.fixture(scope="module")
def get_create_user_dto():
    return user_dtos.UserCreateDto()


def test_create_user(get_db, get_create_user_dto):
    user_opt = user_services.create_user(get_db, get_create_user_dto)
    assert user_opt.data is not None


def test_create_duplicate_user_will_create_error(get_db, get_create_user_dto):
    user_opt_1 = user_services.create_user(get_db, get_create_user_dto)
    user_opt_2 = user_services.create_user(get_db, get_create_user_dto)
    assert user_opt_1.data is not None
    assert user_opt_2.error is not None


def test_create_duplicate_username_will_create_error(get_db, get_create_user_dto):
    user_opt_1 = user_services.create_user(get_db, get_create_user_dto)
    user_dto_2 = get_create_user_dto
    user_dto_2.email = "Example2@Example.com"
    user_opt_2 = user_services.create_user(get_db, user_dto_2)
    assert user_opt_1.data is not None
    assert user_opt_2.error is not None

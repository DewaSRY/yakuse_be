import pytest

from app.user import user_services, user_dtos


@pytest.fixture()
def get_user_model(get_db):
    return user_services.create_user(get_db, user_dtos.UserCreateDto()).data


def test_user_can_login_if_account_already_create(get_db, get_user_model):
    user_opt = user_services.user_login(get_db, user=user_dtos.UserLoginPayloadDto())
    assert user_opt.data is not None
    assert user_opt.error is None


def test_user_failed_to_login_if_password_wash_wrong(get_db, get_user_model):
    user_opt = user_services.user_login(get_db, user=user_dtos.UserLoginPayloadDto(
        password="wrongPassword"
    ))
    assert user_opt.error is not None
    assert user_opt.data is None


def test_user_failed_to_login_if_email_not_found(get_db, get_user_model):
    user_opt = user_services.user_login(get_db, user=user_dtos.UserLoginPayloadDto(
        password="wrongPassword",
        email="EmailNotFound@example.com"
    ))
    assert user_opt.error is not None
    assert user_opt.data is None

import pytest
from typing import Callable

from app.user import user_services, user_dtos
from app.user.user_model import UserModel
from sqlalchemy import BinaryExpression


@pytest.fixture()
def get_user_model(get_db):
    return user_services.create_user(get_db, user_dtos.UserCreateDto()).data


def test_get_user_by_email(get_db, get_user_model):
    def user_filter(user_model: UserModel):
        return user_model.email.like(f"{get_user_model.email}")

    actual = user_services.get_user_by_property(get_db, user_filter)
    assert actual.data is not None
    assert actual.error is None


def test_get_user_by_user_name(get_db, get_user_model):
    def user_filter(user_model: UserModel):
        return user_model.username.like(f"{get_user_model.username}")

    actual = user_services.get_user_by_property(get_db, user_filter)
    assert actual.data is not None
    assert actual.error is None


def test_get_user_by_user_full_name(get_db, get_user_model):
    def user_filter(user_model: UserModel):
        return user_model.fullname.like(f"{get_user_model.fullname}")

    actual = user_services.get_user_by_property(get_db, user_filter)
    assert actual.data is not None
    assert actual.error is None

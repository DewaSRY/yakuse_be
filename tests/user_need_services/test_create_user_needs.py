import pytest

from app.user import user_services, user_dtos
from app.user_need import user_need_services, user_need_dtos


@pytest.fixture()
def get_user_model(get_db):
    return user_services.create_user(get_db, user_dtos.UserCreateDto()).data


def test_create_user_needs(get_db, get_user_model):
    actual = user_need_services.create_user_need_service(
        db=get_db, user_need=user_need_dtos.UserNeedCreateDto(), user_id=get_user_model.id)

    assert actual.data is not None
    assert actual.error is None
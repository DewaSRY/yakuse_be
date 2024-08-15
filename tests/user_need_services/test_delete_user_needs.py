import pytest

from app.user import user_services, user_dtos
from app.user_need import user_need_services, user_need_dtos


@pytest.fixture()
def get_user_model(get_db):
    return user_services.create_user(get_db, user_dtos.UserCreateDto()).data


def test_delete_user_need_by_id(get_db, get_user_model):
    user_need_create = user_need_services.create_user_need(
        db=get_db,
        user_need=user_need_dtos.UserNeedCreateDto(),
        user_id=get_user_model.id
    ).data

    actual = user_need_services.delete_user_need_by_id(
        db=get_db,
        user_need_id=user_need_create.id,
        user_id=get_user_model.id
    )

    assert actual is None

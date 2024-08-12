import pytest

from app.user import user_services, user_dtos
from app.user_need import user_need_services, user_need_dtos


def test_get_user_need_by_id(get_db):
    user_model = user_services.create_user(
        get_db, user_dtos.UserCreateDto()).data

    user_need_create = user_need_services.create_user_need_service(
        db=get_db, user_need=user_need_dtos.UserNeedCreateDto(), user_id=user_model.id).data
    actual = user_need_services.get_user_need_by_id_service(
        db=get_db, user_need_id=user_need_create.id
    )
    assert actual is not None

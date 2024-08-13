import pytest

from app.user import user_services, user_dtos
from app.user_need import user_need_services, user_need_dtos
from app.libs import sql_alchemy_lib


@pytest.fixture()
def get_user_model(get_db):
    return user_services.create_user(
        get_db, user_dtos.UserCreateDto()).data


@pytest.fixture()
def get_user_needs_model(get_db, get_user_model):
    return user_need_services.create_user_need_service(
        db=get_db, user_need=user_need_dtos.UserNeedCreateDto(), user_id=get_user_model.id).data


def test_get_user_need_by_id(get_db, get_user_needs_model, monkeypatch):
    def mock_get_db():
        yield get_db

    monkeypatch.setattr(sql_alchemy_lib, "get_db", mock_get_db)

    actual = user_need_services.get_user_need_by_id_service(
        db=get_db, user_need_id=get_user_needs_model.id
    )
    assert actual is not None
    assert actual.user_info is not None

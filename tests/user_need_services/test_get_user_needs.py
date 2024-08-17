import pytest

from app.user import user_services, user_dtos
from app.user_need import user_need_services, user_need_dtos
from app.libs import sql_alchemy_lib


@pytest.fixture()
def get_user_model(get_db):
    return user_services.create_user(get_db, user_dtos.UserCreateDto()).data


@pytest.fixture()
def get_user_model_2(get_db):
    return user_services.create_user(
        get_db,
        user_dtos.UserCreateDto(username="a", email="a@a.a", password="a", fullname="a")
    ).data


@pytest.fixture()
def get_user_needs_model(get_db, get_user_model):
    return user_need_services.create_user_need(
        db=get_db, user_need=user_need_dtos.UserNeedCreateDto(), user_id=get_user_model.id).data


def test_get_user_need_by_id(get_db, get_user_needs_model, monkeypatch):
    def mock_get_db():
        yield get_db

    monkeypatch.setattr(sql_alchemy_lib, "get_db", mock_get_db)

    actual = user_need_services.get_user_need_by_id(
        db=get_db, user_need_id=get_user_needs_model.id
    )
    assert actual.data is not None
    assert actual.error is None


def test_get_all_our_user_needs_should_return_10(get_db, get_user_model):
    list_user_need = []
    total_user_need = 10
    for n in range(total_user_need):
        create_user_need = user_need_dtos.UserNeedCreateDto(
            title=f"title {n}",
            description=f"description {n}"
        )
        list_user_need.append(create_user_need)

    for user_need in list_user_need:
        user_need_services.create_user_need(
            db=get_db, user_need=user_need, user_id=get_user_model.id
        )

    assert len(user_need_services.get_all_user_needs(get_db).data) == total_user_need


def test_get_all_public_user_needs(get_db, get_user_model, get_user_model_2):
    list_user_need_1 = []
    list_user_need_2 = []
    total_user_need_1 = 4
    total_user_need_2 = 3
    for n in range(total_user_need_1):
        create_user_need = user_need_dtos.UserNeedCreateDto(
            title=f"title {n}",
            description=f"description {n}"
        )
        list_user_need_1.append(create_user_need)
    for n in range(total_user_need_2):
        create_user_need = user_need_dtos.UserNeedCreateDto(
            title=f"title {total_user_need_1 + n}",
            description=f"description {total_user_need_1 + n}"
        )
        list_user_need_2.append(create_user_need)
    for user_need in list_user_need_1:
        user_need_services.create_user_need(
            db=get_db, user_need=user_need, user_id=get_user_model.id
        )
    for user_need in list_user_need_2:
        user_need_services.create_user_need(
            db=get_db, user_need=user_need, user_id=get_user_model_2.id
        )

    assert len(user_need_services.get_all_user_needs(get_db).data) == total_user_need_1 + total_user_need_2


def test_get_user_needs_by_user_id(get_db, get_user_model, get_user_model_2):
    list_user_need_1 = []
    list_user_need_2 = []
    total_user_need_1 = 4
    total_user_need_2 = 3
    for n in range(total_user_need_1):
        create_user_need = user_need_dtos.UserNeedCreateDto(
            title=f"title {n}",
            description=f"description {n}"
        )
        list_user_need_1.append(create_user_need)
    for n in range(total_user_need_2):
        create_user_need = user_need_dtos.UserNeedCreateDto(
            title=f"title {total_user_need_1 + n}",
            description=f"description {total_user_need_1 + n}"
        )
        list_user_need_2.append(create_user_need)
    for user_need in list_user_need_1:
        user_need_services.create_user_need(
            db=get_db, user_need=user_need, user_id=get_user_model.id
        )
    for user_need in list_user_need_2:
        user_need_services.create_user_need(
            db=get_db, user_need=user_need, user_id=get_user_model_2.id
        )

    assert len(user_need_services.get_user_needs_by_user_id(get_db, get_user_model.id).data) == total_user_need_1
    assert len(
        user_need_services.get_user_needs_by_user_id(get_db, get_user_model_2.id).data) == total_user_need_2

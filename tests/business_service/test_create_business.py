import pytest

from app.user import user_services, user_dtos
from app.business import business_services, business_dtos


@pytest.fixture()
def get_user_model(get_db):
    return user_services.create_user(get_db, user_dtos.UserCreateDto()).data


def test_create_business(get_db, get_user_model):
    actual = business_services.create_business(
        db=get_db, business=business_dtos.BusinessCreateDto(), user_id=get_user_model.id
    )
    assert actual.data is not None
    assert actual.error is None


def test_create_business_with_duplicate_name_will_failed(get_db, get_user_model):
    business_services.create_business(
        db=get_db, business=business_dtos.BusinessCreateDto(), user_id=get_user_model.id
    )
    actual_2 = business_services.create_business(
        db=get_db, business=business_dtos.BusinessCreateDto(), user_id=get_user_model.id
    )
    assert actual_2.data is None
    assert actual_2.error is not None

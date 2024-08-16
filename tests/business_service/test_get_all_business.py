import pytest

from app.user import user_services, user_dtos
from app.business import business_services, business_dtos


@pytest.fixture()
def get_user_model(get_db):
    return user_services.create_user(get_db, user_dtos.UserCreateDto()).data


def test_get_all_business(get_db, get_user_model):
    business = business_services.create_business(
        db=get_db, business=business_dtos.BusinessCreateDto(), user_id=get_user_model.id
    )
    # business_services.get_all_business(get_db)
    all_business = business_services.get_all_business(get_db)
    assert len(all_business.data) == 1


def test_get_all_business_should_return_10(get_db, get_user_model):
    list_business = []
    for n in range(10):
        create_business = business_dtos.BusinessCreateDto(
            name=f"name {n} ",
            description=f"description {n}",
            location=f"some thing in earth {n}",
            contact=f"some contact {n}",
        )
        list_business.append(create_business)

    for business in list_business:
        business_services.create_business(
            db=get_db, business=business, user_id=get_user_model.id
        )

    assert len(business_services.get_all_business(get_db).data) == 10

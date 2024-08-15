import pytest

from app.user import user_services, user_dtos
from app.business import business_services, business_dtos


@pytest.fixture()
def get_user_model(get_db):
    return user_services.create_user(get_db, user_dtos.UserCreateDto()).data


def test_create_business(get_db, get_user_model):
    business_dto = business_dtos.BusinessCreateDto()
    business_dto.description = """
    hallo
     apa
     kabar
      kalian
       semua
    """
    business = business_services.create_business(
        db=get_db, business=business_dto, user_id=get_user_model.id
    )
    # print(len(business.data.description_list))
    # business_services.get_all_business(get_db)
    all_business = business_services.get_all_business(get_db)
    assert len(all_business.data) == 1
    assert len(business.data.description_list) > 0

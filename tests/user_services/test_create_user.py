from app.user import user_services, user_dtos

MOCK_USER_DTO = user_dtos.UserCreateDto(
    username="some username", email="some@Example.com", fullname="some full name", password="some password")


def test_first_create_user(get_db):
    user_opt = user_services.create_user(get_db, MOCK_USER_DTO)

    assert user_opt.data is not None
    assert user_opt.data.username == MOCK_USER_DTO.username
    assert user_opt.data.email == MOCK_USER_DTO.email
    assert user_opt.data.fullname == MOCK_USER_DTO.fullname
    assert user_opt.data.hash_password != MOCK_USER_DTO.password
    assert user_opt.data.photo_url is None
    assert user_opt.data.address is None
    assert user_opt.data.phone is None
    assert user_opt.data.created_at is not None
    assert user_opt.data.updated_at is not None

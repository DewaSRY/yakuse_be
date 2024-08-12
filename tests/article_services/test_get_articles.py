import pytest

from app.user import user_services, user_dtos
from app.article import article_services, article_dtos


@pytest.fixture()
def get_user_model(get_db):
    return user_services.create_user(get_db, user_dtos.UserCreateDto()).data


# def test_get_article


# def test_get_user_need_by_id(get_db, get_user_model):
#     user_need_create = user_need_services.create_user_need_service(
#         db=get_db, user_need=user_need_dtos.UserNeedCreateDto(), user_id=get_user_model.id).data
    
#     actual = user_need_services.get_user_need_by_id_service(
#         db=get_db, user_need_id=user_need_create.id
#     )
#     print(actual.data)
#     assert actual.data is not None
#     assert actual.error is None

# def test_get_all_user_needs_should_return_10(get_db, get_user_model):
#     list_user_need = []
#     total = 10
#     for n in range(total):
#         create_user_need = user_need_dtos.UserNeedCreateDto(
#             title=f"title {n}",
#             description=f"description {n}"
#         )
#         list_user_need.append(create_user_need)

#     for user_need in list_user_need:
#         user_need_services.create_user_need_service(
#             db=get_db, user_need=user_need, user_id=get_user_model.id
#         )

#     assert len(user_need_services.get_user_need_service(get_db).data) == total
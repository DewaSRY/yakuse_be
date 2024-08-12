import pytest

from app.user import user_services, user_dtos
from app.article import article_services, article_dtos


@pytest.fixture()
def get_user_model(get_db):
    return user_services.create_user(get_db, user_dtos.UserCreateDto()).data


def test_create_articles(get_db, get_user_model):
    actual = article_services.create_article_service(
        db=get_db, article=article_dtos.ArticleCreateDto(), user_id=get_user_model.id)

    assert actual.data is not None
    assert actual.error is None

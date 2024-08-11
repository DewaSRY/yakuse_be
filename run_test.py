import os

from app.user.user_model import UserModel
from app.health_check.health_check_model import HealthCheckModel
from app.business_category.business_category_model import BusinessCategory
from app.business.business_model import Business
from app.rating.rating_model import Rating
from app.user_need.user_need_model import UserNeeds
from app.article.article_model import Article

from conftest import engine


def drop_all_table():
    """Drop all table needed so there is no duplicat data while testing"""
    UserModel.__table__.drop(engine)
    HealthCheckModel.__table__.drop(engine)
    BusinessCategory.__table__.drop(engine)
    Business.__table__.drop(engine)
    Rating.__table__.drop(engine)
    UserNeeds.__table__.drop(engine)
    Article.__table__.drop(engine)


def main():
    drop_all_table()
    os.system("pytest -s")


if __name__ == "__main__":
    main()

import pytest

from app.business_category import business_category_seed


def test_business_category_will_be_zero_on_first_place(get_db):
    assert business_category_seed.get_business_category_length(get_db) == 0


def test_business_category_will_be_ten_after_get_init(get_db):
    business_category_seed.init_business_category(get_db)
    assert business_category_seed.get_business_category_length(get_db) == 10

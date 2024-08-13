import pytest

from app.utils import find_errr_from_args


def test_find_error():
    actual_text = "('(sqlite3.IntegrityError) UNIQUE constraint failed: users.email',)"
    assert find_errr_from_args("users", actual_text) == "email"

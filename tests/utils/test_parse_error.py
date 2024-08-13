import pytest

from app.utils import find_errr_from_args

TEXT_ERROR = """
(sqlite3.IntegrityError) UNIQUE constraint failed: users.email
[SQL: INSERT INTO users (id, fullname, username, email, hash_password, phone, address, about_me, photo_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) RETURNING created_at, updated_at]
[parameters: ('4e5ab87b-4243-45f7-a0dd-f6c1eb92beaf', 'SomeFullName', 'username', 'Example@example.com', '$pbkdf2-sha256$29000$y3kvRch5732P8f7fm1PqPQ$.ACox09Ii6T91.IRKSQZpTxxoQKOeIYw66AXVS4/NIQ', None, None, None, None)]
(Background on this error at: https://sqlalche.me/e/20/gkpj)
('(sqlite3.IntegrityError) UNIQUE constraint failed: users.email',)
"""


def test_find_error():
    actual_text = "('(sqlite3.IntegrityError) UNIQUE constraint failed: users.email',)"
    assert find_errr_from_args("users", actual_text) == "email"


def test_find_error_from_bigger_test():
    actual = find_errr_from_args("users", TEXT_ERROR)
    print(f"actual i s{actual}")
    assert actual == "email"

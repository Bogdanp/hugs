import pytest

from hugs.errors import ParseError
from hugs.parser import Expression, parse


def test_can_parse_simple_expressions():
    # Given that I have a valid query
    data = """\
---
-- name: select_42
SELECT 42;
"""

    # If I attempt to parse it
    expressions = list(parse(data))

    # I expect to get back a valid expression
    assert expressions == [Expression("select_42", body="-- name: select_42\nSELECT 42;")]


def test_can_parse_multiple_expressions():
    # Given that I have a set of expressions
    list_users_query = """\
-- name: list_users
-- args: offset, limit
SELECT * FROM users LIMIT :offset, :limit;\
"""
    find_user_by_email_query = """\
-- name: find_user_by_email
-- args: email
-- doc: Find a user by email.
SELECT * FROM users WHERE email = :email;\
"""

    data = f"""\
---
{list_users_query}

---
{find_user_by_email_query}
"""

    # If I parse them
    expressions = list(parse(data))

    # I expect to get back both expressions
    assert expressions == [
        Expression("list_users", args=("offset", "limit"), body=list_users_query),
        Expression("find_user_by_email", args=("email",), doc="Find a user by email.", body=find_user_by_email_query),
    ]


def test_can_parse_multiline_expressions():
    # Given that I have a valid multiline query
    data = """
---
-- name: select_42_and_43
SELECT
    42,
    43
"""

    # If I parse it
    expressions = list(parse(data))

    # I expect to get back the full query
    assert expressions == [
        Expression("select_42_and_43", body="-- name: select_42_and_43\nSELECT\n    42,\n    43"),
    ]


def test_fails_to_parse_nameless_expressions():
    # Given that I have an invalid query
    data = """
---
SELECT 42
"""

    # If I parse it
    # I expect ParseError to be raised
    with pytest.raises(ParseError):
        list(parse(data))

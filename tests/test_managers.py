import pytest

from dataclasses import dataclass
from hugs import Manager, Repository
from psycopg2.extras import DictCursor, RealDictCursor
from typing import Optional


@dataclass
class User:
    id: Optional[int]
    username: str
    password: str


def test_managers_raise_attribute_error_when_an_attr_doesnt_exist():
    # Given that I have a manager with no queries
    manager = Manager()

    # When I try to access an attr that doesn't exist
    # Then an AttributeError should be raised
    with pytest.raises(AttributeError):
        manager.find_all()


def test_managers_return_iterators_over_abstract_data_types(sqlite3_conn):
    # Given that I have a user manager based on a user repo
    users_manager = Manager(User)
    users_manager.load_queries("tests/fixtures/users.sql")

    # And my users table has a few users
    cursor = sqlite3_conn.cursor()
    users_manager.create_users_table(cursor)
    for i in range(10):
        users_manager.add_user(cursor, username=f"example_{i}", password="password")

    sqlite3_conn.commit()

    # When I run a query through the user manager
    users = users_manager.find_all(sqlite3_conn.cursor())
    for i, user in enumerate(users):
        # Then I should get back a list of User objects
        assert isinstance(user, User)
        assert f"example_{i}" == user.username


@pytest.mark.parametrize("cursor_factory", [
    None,
    DictCursor,
    RealDictCursor,
])
def test_managers_return_command_results_under_postgres(cursor_factory, postgres_conn):
    # Given that I have a user manager based on a user repo
    users_manager = Manager(User)
    users_manager.load_queries("tests/fixtures/users_postgres.sql")

    # And I have a Postgres cursor
    cursor = postgres_conn.cursor(cursor_factory=cursor_factory)
    try:
        # When I run a command that doesn't return any results
        # Then I should get back None
        assert users_manager.create_users_table(cursor) is None

        for i in range(10):
            # When I run a command that returns a result
            res = users_manager.add_user(cursor, username=f"example_{i}", password="password")
            # Then I should get back that result
            assert "id" in res

        # When I run a query through the user manager
        users = users_manager.find_all(cursor)
        for i, user in enumerate(users):
            # Then I should get back a list of User objects
            assert isinstance(user, User)
    finally:
        assert users_manager.drop_users_table(cursor) is None

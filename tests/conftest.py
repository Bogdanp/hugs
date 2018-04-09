import psycopg2
import pytest
import sqlite3

from hugs import Repository


@pytest.fixture
def sqlite3_conn():
    return sqlite3.connect(":memory:")


@pytest.fixture
def postgres_conn():
    conn = psycopg2.connect("postgres://127.0.0.1/postgres")
    conn.autocommit = True
    return conn


@pytest.fixture
def users_repo():
    repo = Repository()
    repo.load_queries("tests/fixtures/users.sql")
    return repo

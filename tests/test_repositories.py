from hugs import Repository


def test_can_load_queries_to_a_repo():
    # Given that I have a Repository
    users_repo = Repository()

    # If I attempt to add queries from a file to it
    users_repo.load_queries("tests/fixtures/users.sql")

    # I expect each method to have been defined
    assert users_repo.create_users_table
    assert users_repo.drop_users_table
    assert users_repo.find_user_by_username
    assert users_repo.select_42


def test_can_perform_queries(sqlite3_conn, users_repo):
    # Given that I have a Repository and a sqlite3 cursor
    cursor = sqlite3_conn.cursor()

    # If I attempt to execute one of the queries in the repo
    users_repo.select_42(cursor)

    # I expect to get back a valid result
    assert cursor.fetchone() == (42,)


def test_can_execute_commands_and_queries(sqlite3_conn, users_repo):
    # Given that I have a Repository and a sqlite3 cursor
    cursor = sqlite3_conn.cursor()

    # If I attempt create a table and add a user
    users_repo.create_users_table(cursor)
    users_repo.add_user(cursor, username="bogdan", password="12345")
    sqlite3_conn.commit()

    # Then query for that user
    users_repo.find_user_by_username(cursor, "bogdan")

    # I expect to get him back
    assert cursor.fetchone() == (1, "bogdan", "12345")

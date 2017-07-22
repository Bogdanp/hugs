# hugs

[![Build Status](https://travis-ci.org/Bogdanp/hugs.svg?branch=master)](https://travis-ci.org/Bogdanp/hugs)
[![Test Coverage](https://codeclimate.com/github/Bogdanp/hugs/badges/coverage.svg)](https://codeclimate.com/github/Bogdanp/hugs/coverage)
[![Code Climate](https://codeclimate.com/github/Bogdanp/hugs/badges/gpa.svg)](https://codeclimate.com/github/Bogdanp/hugs)
[![PyPI version](https://badge.fury.io/py/hugs.svg)](https://badge.fury.io/py/hugs)
[![Documentation](https://img.shields.io/badge/doc-latest-brightgreen.svg)](http://hugs.io)

**hugs** lets you map SQL expressions to Python functions.

## Installation

    pip install -U hugs

## Examples

### SQLite

`queries.sql`:

``` sql
---
-- name: add_user
-- args: username, password
-- doc: Adds a user.
INSERT INTO users (username, password) VALUES (:username, :password);

---
-- name: get_users
SELECT * FROM users;
```

`example.py`:

``` python
import sqlite3

from hugs import Repository

connection = sqlite3.Connection(":memory:")
users_repo = Repository()
users_repo.load_queries("queries.sql")

cursor = connection.cursor()
users_repo.add_user(cursor, "bogdan", "123")
connection.commit()

users_repo.get_users(cursor)
print(cursor.fetchone())
```

### PostgreSQL

`queries.sql`:

``` sql
---
-- name: add_user
-- args: username, password
-- doc: Adds a user.
INSERT INTO users (username, password) VALUES (%(username)s, %(password)s);

---
-- name: get_users
SELECT * FROM users;
```

```python
import psycopg2

from hugs import Repository

connection = psycopg2.connect(database="postgres", user="bogdan")
connection.autocommit = True

users_repo = Repository()
users_repo.load_queries("queries.sql")

with connection.cursor() as cursor:
    users_repo.add_user(cursor, "bogdan", "123")
    users_repo.find_user_by_username(cursor, "bogdan")
    print(cursor.fetchone())

connection.close()
```

## License

hugs is licensed under the 3-clause BSD license.

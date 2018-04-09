# hugs

[![Build Status](https://travis-ci.org/Bogdanp/hugs.svg?branch=master)](https://travis-ci.org/Bogdanp/hugs)
[![Test Coverage](https://codeclimate.com/github/Bogdanp/hugs/badges/coverage.svg)](https://codeclimate.com/github/Bogdanp/hugs/coverage)
[![Code Climate](https://codeclimate.com/github/Bogdanp/hugs/badges/gpa.svg)](https://codeclimate.com/github/Bogdanp/hugs)
[![PyPI version](https://badge.fury.io/py/hugs.svg)](https://badge.fury.io/py/hugs)

**hugs** lets you map SQL expressions to Python functions.


## Installation

    pipenv install hugs


## Examples

### PostgreSQL

Write all your queries and commands in a plain `.sql` file.  Command
names should end with a `!` character.

`queries.sql`:

``` sql
---
-- name: add_user!
-- args: username, password
-- doc: Adds a user.
INSERT INTO users (username, password) VALUES (%(username)s, %(password)s) RETURNING id;

---
-- name: get_users
SELECT * FROM users;
```

You can then point a `Repository` to that file to load it into memory:

`example.py`:

```python
import psycopg2

from hugs import Repository

connection = psycopg2.connect(database="postgres", user="bogdan")
connection.autocommit = True

users_repo = Repository()
users_repo.load_queries("queries.sql")

with connection.cursor() as cursor:
  users_repo.add_user(cursor, "bogdan", "123")
  users_repo.get_users(cursor)
  print(cursor.fetchone())

connection.close()
```

You can use a `Manager` instead of (or in addition to) a `Repository`
to make iterating over query results less tedious.

```python
import psycopg2

from hugs import Manager

connection = psycopg2.connect(database="postgres", user="bogdan")
connection.autocommit = True

users_manager = Manager()
users_manager.load_queries("queries.sql")

with connection.cursor() as cursor:
  users_manager.add_user(cursor, "bogdan", "123")
  for user in users_manager.get_users(cursor):
    print(user)

connection.close()
```

`Managers` optionally take a `value_factory` parameter that can be
used to convert rows to concrete data types.

```python
import psycopg2

from dataclasses import dataclass

@dataclass
class User:
  id: Optional[int]
  username: str
  password: str

connection = psycopg2.connect(database="postgres", user="bogdan")
connection.autocommit = True

users_manager = Manager(User)
users_manager.load_queries("queries.sql")

with connection.cursor() as cursor:
  for user in users_manager.get_users(cursor):
    assert isinstance(user, User)

connection.close()
```


## License

hugs is licensed under the 3-clause BSD license.

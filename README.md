# hugs

Hugs lets you map SQL expressions to Python functions.

## Example

``` sql
---
-- name: add_user
-- args: username
-- doc: Adds a user.
INSERT INTO users (username) VALUES (:username);

---
-- name: get_users
SELECT * FROM users;
```

``` python
from hugs import Repository

connection = sqlite3.Connection(":memory:")
users_repo = Repository()
users_repo.load_queries("queries.sql")

cursor = connection.cursor()
users_repo.add_user(cursor, "bogdan")
connection.commit()

users_repo.get_users(cursor)
print(cursor.fetchone())
```

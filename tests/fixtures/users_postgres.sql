---
-- name: create_users_table!
-- doc: Creates the users table if it doesn't exist.
CREATE TABLE IF NOT EXISTS hugs_users (
       id serial primary key,
       username text,
       password text
);

---
-- name: drop_users_table!
-- doc: Drops the users table.
DROP TABLE hugs_users;

---
-- name: add_user!
-- kwargs: username, password
-- doc: Adds a user.
INSERT INTO hugs_users (username, password) VALUES (%(username)s, %(password)s) RETURNING id;

---
-- name: find_user_by_username
-- args: username
-- doc: Finds a user by username.
SELECT * FROM hugs_users WHERE username = %(username)s LIMIT 1;

---
-- name: find_all
-- doc: Finds all users.
SELECT * FROM hugs_users ORDER BY username ASC;

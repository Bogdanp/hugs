---
-- name: select_42
-- doc: Returns the number 42.
SELECT 42;

---
-- name: create_users_table
-- doc: Creates the users table if it doesn't exist.
CREATE TABLE IF NOT EXISTS users (
       id integer primary key autoincrement,
       username text,
       password text
);

---
-- name: drop_users_table
-- doc: Drops the users table.
DROP TABLE users;

---
-- name: add_user
-- kwargs: username, password
-- doc: Adds a user.
INSERT INTO users (username, password) VALUES (:username, :password);

---
-- name: find_user_by_username
-- args: username
-- doc: Finds a user by username.
SELECT * FROM users WHERE username = :username LIMIT 1;

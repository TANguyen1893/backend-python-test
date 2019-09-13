BEGIN TRANSACTION;

ALTER TABLE todos RENAME TO todos_backup;

CREATE TABLE todos (
  id INTEGER PRIMARY KEY,
  user_id INT(11) NOT NULL,
  description VARCHAR(255),
  FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO todos (id, user_id, description)
  SELECT id, user_id, description
  FROM todos_backup;

COMMIT;
-- SQLite
CREATE TABLE users (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'username' varchar(255),
    'password' varchar(255),
    'email' varchar(255),
    'iban' varchar(27)
);

CREATE TABLE groups (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'name' varchar(255)
);

CREATE TABLE expenses (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'name' varchar(255),
    'value' REAL,
    'data' DATE,
    'fk_user' INTEGER,
    FOREIGN KEY (fk_user) REFERENCES users(id)
);

CREATE TABLE members (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'fk_user' INTEGER,
    'fk_group' INTEGER,
    FOREIGN KEY (fk_user) REFERENCES users(id),
    FOREIGN KEY (fk_group) REFERENCES groups(id)
);

CREATE TABLE debts(
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'fk_member' INTEGER,
    'payed' boolean,
    FOREIGN KEY (fk_member) REFERENCES members(id)
);

SELECT * FROM user
DROP TABLE user
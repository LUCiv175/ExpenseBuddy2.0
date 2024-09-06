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
    'date' DATE,
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
    'fk_expense' INTEGER,
    'payed' boolean,
    FOREIGN KEY (fk_member) REFERENCES members(id)
    FOREIGN KEY (fk_expense) REFERENCES expenses(id)
);

DROP TABLE debts


SELECT * FROM debts



INSERT INTO users (username, password, email, iban)
VALUES ('fro', 'securepassword123', 'fro@example.com', 'IT60X0542811101000000123456');

INSERT INTO expenses (name, value, date, fk_user) 
VALUES ('Groceries', 150.75, '2023-09-05', 1);


INSERT INTO groups (name) 
VALUES 
('Group A'),
('Group B'),
('Group C');

INSERT INTO members (fk_user, fk_group) 
VALUES 
(3, 1)  -- User con id 1 in Group A
(1, 2),
(2, 1),  -- User con id 1 in Group A
(2, 2);


INSERT INTO debts (fk_member, fk_expense, payed) 
VALUES 
(5, 1, false)  -- Member con id 1, debito non pagato
(4, 2, false);  -- Member con id 4, debito pagato

DELETE FROM debts




SELECT groups.id, groups.name, ROUND(SUM(value), 2),  FROM debts inner join member on members.id=debts.fk_member inner join groups on groups.id=members.fk_group WHERE fk_user=2 and payed=false group by groups.id;


SELECT expenses.id, ROUND(expenses.value/(COUNT(*)+1), 2) as value FROM debts join expenses on expenses.id=debts.fk_expense GROUP by expenses.id

SELECT groups.id, groups.name, B.value FROM groups join (SELECT members.fk_group, ROUND(SUM(value), 2) as value FROM debts join (SELECT expenses.id, ROUND(expenses.value/(COUNT(*)+1), 2) as value FROM debts join expenses on expenses.id=debts.fk_expense GROUP by expenses.id) as A on A.id=debts.fk_expense join members on members.id=debts.fk_member WHERE debts.payed=false and members.fk_user=1 group by members.fk_group) as B on B.fk_group=groups.id
SELECT * FROM debts;
SELECT * FROM members;
SELECT * FROM expenses;
SELECT * FROM groups;


SELECT ROUND(SUM(value), 2) FROM debts join members on members.id=debts.fk_member join where members.fk_user=2 and payed=false GROUP BY fk_user

SELECT COALESCE(ROUND(SUM(value), 2),0) - (SELECT COALESCE(SUM(value),0) as value FROM debts join (SELECT expenses.id, ROUND(value/(COUNT(*)+1), 2) as value FROM expenses join debts on debts.fk_expense=expenses.id where expenses.fk_user=2 GROUP BY expenses.id) as A on A.id=debts.fk_expense WHERE payed=false)as value FROM debts join (SELECT expenses.id, ROUND(expenses.value/(COUNT(*)+1), 2) as value FROM debts join expenses on expenses.id=debts.fk_expense GROUP by expenses.id) as A on A.id=debts.fk_expense join members on members.id=debts.fk_member WHERE debts.payed=false and members.fk_user=2


SELECT SUM(value) as value FROM debts join (SELECT expenses.id, ROUND(value/(COUNT(*)+1), 2) as value FROM expenses join debts on debts.fk_expense=expenses.id where expenses.fk_user=2 GROUP BY expenses.id) as A on A.id=debts.fk_expense WHERE payed=false




DROP TABLE expenses

UPDATE debts SET payed=false where id=3


---da  vedere
SELECT groups.id, groups.name, B.value FROM groups join (SELECT members.fk_group, ROUND(SUM(value), 2) as value FROM debts join (SELECT expenses.id, ROUND(expenses.value/(COUNT(*)+1), 2) as value FROM debts join expenses on expenses.id=debts.fk_expense GROUP by expenses.id) as A on A.id=debts.fk_expense join members on members.id=debts.fk_member WHERE debts.payed=false and members.fk_user=2 group by members.fk_group) as B on B.fk_group=groups.id






SELECT ROUND(SUM(value), 2) FROM expenses WHERE fk_user=1 and STRFTIME('%m-%Y', CURRENT_DATE) = STRFTIME('%m-%Y', data);
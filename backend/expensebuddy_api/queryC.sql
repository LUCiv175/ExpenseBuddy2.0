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

UPDATE debts SET payed=true where id=2


SELECT expenses.id, ROUND(expenses.value/(COUNT(*)+1), 2) as value, name, date FROM debts JOIN expenses ON expenses.id=debts.fk_expense GROUP BY expenses.id
---da  vedere

SELECT groups.id, groups.name, B.value FROM groups join (SELECT members.fk_group, ROUND(SUM(value), 2) as value FROM debts join (SELECT expenses.id, COALESCE(ROUND(expenses.value/(COUNT(*)+1), 0)-COALESCE(D.value, 0), 2) as value FROM debts join expenses on expenses.id=debts.fk_expense GROUP by expenses.id) as A on A.id=debts.fk_expense join members on members.id=debts.fk_member join (SELECT expenses.id, ROUND(expenses.value/(COUNT(*)+1)*C.numero, 2) as value FROM debts join expenses on expenses.id=debts.fk_expense join (SELECT fk_expense, Count(*) as numero FROM debts where payed=false GROUP by debts.fk_expense) as C on C.fk_expense= expenses.id where expenses.fk_user=2 GROUP by expenses.id) as D on D.id=debts.fk_expense WHERE debts.payed=false and members.fk_user=2 group by members.fk_group) as B on B.fk_group=groups.id

SELECT * FROM debts join (SELECT expenses.id, COALESCE(ROUND(expenses.value/(COUNT(*)+1), 0)-COALESCE(D.value, 0), 2) as value FROM debts join expenses on expenses.id=debts.fk_expense GROUP by expenses.id) as A on A.id=debts.fk_expense join members on members.id=debts.fk_member join (SELECT expenses.id, ROUND(expenses.value/(COUNT(*)+1)*C.numero, 2) as value FROM debts join expenses on expenses.id=debts.fk_expense join ((SELECT fk_expense, Count(*) as numero FROM debts where payed=false GROUP by debts.fk_expense) as C on C.fk_expense=expenses.id where expenses.fk_user=2 GROUP by expenses.id) as D on D.id=debts.fk_expense WHERE debts.payed=false and members.fk_user=2



SELECT fk_expense, Count(*) as numero FROM debts where payed=false GROUP by debts.fk_expense
SELECT expenses.id, ROUND(expenses.value/(COUNT(*)+1)*C.numero, 2) as value FROM debts join expenses on expenses.id=debts.fk_expense join (SELECT fk_expense, Count(*) as numero FROM debts where payed=false GROUP by debts.fk_expense) as C on C.fk_expense= expenses.id where expenses.fk_user=1 GROUP by expenses.id

SELECT expenses.id, expenses.name, expenses.value, expenses.date, expenses.fk_user, a.value FROM expenses full join (SELECT expenses.id, ROUND(expenses.value/(COUNT(*)+1), 2) as value, name, date FROM debts JOIN expenses ON expenses.id=debts.fk_expense GROUP BY expenses.id) as A on A.id = expenses.id WHERE expenses.fk_user=1 or a.id in(SELECT debts.fk_expense FROM members inner join debts on debts.fk_member=members.id where fk_user=1);


SELECT ROUND(SUM(value), 2) FROM expenses WHERE fk_user=1 and STRFTIME('%m-%Y', CURRENT_DATE) = STRFTIME('%m-%Y', data);



SELECT 
    groups.id, 
    groups.name, 
    B.value 
FROM 
    groups 
JOIN (
    SELECT 
        members.fk_group, 
        ROUND(SUM(A.value), 2) AS value 
    FROM 
        debts 
    JOIN (
        SELECT 
            expenses.id, 
            ROUND(expenses.value / (COUNT(*) + 1), 2) AS value 
        FROM 
            debts 
        JOIN 
            expenses ON expenses.id = debts.fk_expense 
        GROUP BY 
            expenses.id
    ) AS A ON A.id = debts.fk_expense 
    JOIN members ON members.id = debts.fk_member 
    WHERE 
        debts.payed = false 
    AND 
        members.fk_user = 1
    GROUP BY 
        members.fk_group
) AS B ON B.fk_group = groups.id;


SELECT 
    F.id, 
    F.name, 
    COALESCE(credit, 0.0) as credit,
    COALESCE(debit, 0.0) as debit,
    COALESCE(credit-debit, 0.0) as diff
FROM 
    (SELECT groups.id, groups.name FROM groups JOIN members ON members.fk_group=groups.id WHERE members.fk_user=1) as F
left JOIN (
    SELECT fk_group, SUM(value) as credit, 0.0 as debit FROM debts 
    JOIN (
        SELECT expenses.id, ROUND(expenses.value/(COUNT(*)+1), 2) as value, fk_user FROM debts join expenses on expenses.id=debts.fk_expense join (SELECT fk_expense, Count(*) as numero FROM debts where payed=false GROUP by debts.fk_expense) as C on C.fk_expense= expenses.id where expenses.fk_user=1 GROUP by expenses.id
    ) AS E ON E.id = debts.fk_expense 
    JOIN members ON members.id = debts.fk_member 
    WHERE 
        debts.payed = false 
    AND 
        E.fk_user = 1
        GROUP BY fk_group
    

UNION
    SELECT 
        members.fk_group,
        0.0 as credit,
        ROUND(SUM(A.value), 2) AS debit
    FROM 
        debts 
    JOIN (
        SELECT 
            expenses.id, 
            ROUND(expenses.value / (COUNT(*) + 1), 2) AS value 
        FROM 
            debts 
        JOIN 
            expenses ON expenses.id = debts.fk_expense 
        GROUP BY 
            expenses.id
    ) AS A ON A.id = debts.fk_expense 
    JOIN members ON members.id = debts.fk_member 
    WHERE 
        debts.payed = false 
    AND 
        members.fk_user = 1
    GROUP BY 
        members.fk_group
) AS B ON B.fk_group = F.id







SELECT fk_group, SUM(value) FROM debts 
    JOIN (
        SELECT expenses.id, ROUND(expenses.value/(COUNT(*)+1), 2) as value, fk_user FROM debts join expenses on expenses.id=debts.fk_expense join (SELECT fk_expense, Count(*) as numero FROM debts where payed=false GROUP by debts.fk_expense) as C on C.fk_expense= expenses.id where expenses.fk_user=1 GROUP by expenses.id
    ) AS A ON A.id = debts.fk_expense 
    JOIN members ON members.id = debts.fk_member 
    WHERE 
        debts.payed = false 
    AND 
        A.fk_user = 1
        GROUP BY fk_group



SELECT groups.id, groups.name, B.value FROM groups JOIN (SELECT members.fk_group, ROUND(SUM(A.value), 2) AS value FROM debts JOIN (SELECT expenses.id, ROUND(expenses.value / (COUNT(*) + 1), 2) AS value FROM debts JOIN expenses ON expenses.id = debts.fk_expense GROUP BY expenses.id) AS A ON A.id = debts.fk_expense JOIN members ON members.id = debts.fk_member WHERE debts.payed = false AND members.fk_user = 3 GROUP BY members.fk_group) AS B ON B.fk_group = groups.id;
SELECT groups.id, groups.name, B.value FROM groups JOIN (SELECT members.fk_group, ROUND(SUM(A.value), 2) AS value FROM debts JOIN (SELECT expenses.id, ROUND(expenses.value / (COUNT(*) + 1) * C.numero, 2) AS value FROM debts JOIN expenses ON expenses.id = debts.fk_expense JOIN (SELECT fk_expense, COUNT(*) AS numero FROM debts WHERE payed = false GROUP BY debts.fk_expense) AS C ON C.fk_expense = expenses.id WHERE expenses.fk_user = 2 GROUP BY expenses.id) AS A ON A.id = debts.fk_expense JOIN members ON members.id = debts.fk_member WHERE debts.payed = false AND members.fk_user = 2 GROUP BY members.fk_group) AS B ON B.fk_group = groups.id;



SELECT groups.id, groups.name, credit, debit, credit-debit as diff FROM groups join (SELECT fk_group, SUM(value) as credit, 0.0 as debit FROM debts right JOIN (SELECT expenses.id, ROUND(expenses.value/(COUNT(*)+1), 2) as value, fk_user FROM debts JOIN expenses ON expenses.id=debts.fk_expense JOIN (SELECT fk_expense, Count(*) as numero FROM debts WHERE payed=false GROUP BY debts.fk_expense) as C ON C.fk_expense=expenses.id WHERE expenses.fk_user=2 GROUP BY expenses.id) AS E ON E.id = debts.fk_expense JOIN members ON members.id = debts.fk_member WHERE debts.payed = false AND E.fk_user = 2 GROUP BY fk_group UNION SELECT members.fk_group, 0.0 as credit, ROUND(SUM(A.value), 2) AS debit FROM debts JOIN (SELECT expenses.id, ROUND(expenses.value / (COUNT(*) + 1), 2) AS value FROM debts JOIN expenses ON expenses.id = debts.fk_expense GROUP BY expenses.id) AS A ON A.id = debts.fk_expense JOIN members ON members.id = debts.fk_member WHERE debts.payed = false AND members.fk_user = 2 GROUP BY members.fk_group) AS B ON B.fk_group = groups.id;




SELECT F.id, F.name, F.value, F.date, users.username, F.debt FROM users join (SELECT expenses.id, expenses.name, expenses.value, expenses.date, expenses.fk_user, a.value as debt FROM expenses full join (SELECT expenses.id, ROUND(expenses.value/(COUNT(*)+1), 2) as value, name, date FROM debts JOIN expenses ON expenses.id=debts.fk_expense GROUP BY expenses.id) as A on A.id = expenses.id WHERE expenses.fk_user="+str(id)+" or a.id in(SELECT debts.fk_expense FROM members inner join debts on debts.fk_member=members.id where fk_user="+str(id)+") ORDER BY expenses.date DESC) as F on F.fk_user=1
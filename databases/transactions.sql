-- INSERT + UPDATE
BEGIN;

CREATE TABLE IF NOT EXISTS accounts(
    id SERIAL PRIMARY KEY ,
    name varchar(20) NOT NULL,
    balance float DEFAULT 100
);

INSERT INTO accounts(NAME, BALANCE)
VALUES ('vova', DEFAULT), ('yura', DEFAULT);

SAVEPOINT adequate_database;

INSERT INTO accounts(NAME, BALANCE)
VALUES ('vlad', DEFAULT), ('diana', DEFAULT);

UPDATE accounts SET balance = balance*10 WHERE id in (3,4);

ROLLBACK TO SAVEPOINT adequate_database;
COMMIT;

--DELETE
BEGIN;

ALTER TABLE orders DROP COLUMN order_status_order_status_id; --cascade

DELETE FROM order_status WHERE status_name = 'Canceled';

ROLLBACK;

DELETE FROM categories WHERE category_description IS NULL;

COMMIT;


--UPDATE
BEGIN;
CREATE TABLE IF NOT EXISTS passport(
    id SERIAL PRIMARY KEY,
    name varchar(20),
    foreign_passport bool
);

INSERT INTO passport(name, foreign_passport)
VALUES
    ('diana',true), ('vlad',false);

SAVEPOINT secure;

UPDATE passport SET foreign_passport=false;

UPDATE passport SET foreign_passport= true;

ROLLBACK TO SAVEPOINT secure;

UPDATE passport SET foreign_passport=CASE
    WHEN foreign_passport=FALSE THEN TRUE
    ELSE FALSE
END;

COMMIT;
SELECT * FROM passport;

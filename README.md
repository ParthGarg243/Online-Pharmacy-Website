# DBMS_Project
मेडिकल स्टोर

pipenv shell

python manage.py runserver

http://localhost:8000/web/login/

Transcations
Non conflicting
Sign up - done
update profile - done
Adding a new product
Marking a order as approved.

Conflicting
checkout - conflicting coz of stock update
adding items to the stock.
Check embedded sql for it accordingly


Transactions are just for the sake of acid property, for concurrency can use locks
BEGIN TRANSACTION;

-- Insert a new record
INSERT INTO Customers (Name, Email) VALUES ('John Doe', 'john@example.com');

-- Update an existing record
UPDATE Orders SET Status = 'Shipped' WHERE OrderID = 123;

-- Delete a record
DELETE FROM Products WHERE ProductID = 456;

COMMIT;

-- Transaction 1
BEGIN TRANSACTION;
UPDATE Products SET Quantity = Quantity - 1 WHERE ProductID = 123;
-- Wait for a brief period

-- Transaction 2
BEGIN TRANSACTION;
UPDATE Products SET Quantity = Quantity - 1 WHERE ProductID = 123;
COMMIT; -- Succeeds because it acquired the lock first

-- Transaction 1
COMMIT; -- Fails due to conflict, potentially rollback or retry


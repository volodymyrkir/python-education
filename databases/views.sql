--VIEW ON TABLE PRODUCTS
CREATE VIEW product_10_expensive AS
SELECT *
FROM products
WHERE category_id=10
AND price>100
WITH CHECK OPTION;

INSERT INTO product_10_expensive VALUES
(5000,'Product 5000','Product description 5000',10,101,'Product-5000',10);
INSERT INTO product_10_expensive VALUES
(5001,'Product 5000','Product description 5000','10',100,'Product-5000',9);

SELECT * FROM product_10_expensive;
DROP VIEW product_10_expensive;

--VIEW ON ORDER_STATUS AND ORDERS
CREATE VIEW orders_finished AS
SELECT ORDER_ID, SHIPPING_TOTAL, TOTAL, CREATED_AT, UPLOADED_AT, ORDER_STATUS_ID, STATUS_NAME
FROM ORDERS
JOIN order_status os on os.order_status_id = orders.order_status_order_status_id
WHERE status_name = 'Finished';

SELECT * FROM orders_finished;
DROP VIEW orders_finished;

--VIEW ON PRODUCTS AND CATEGORIES
CREATE VIEW products_category_5 AS
SELECT product_id, product_title, product_description, in_stock, price, slug, c.category_id, category_title, category_description
FROM products
JOIN categories c on products.category_id = c.category_id
WHERE c.category_title = 'Category 5';

SELECT * FROM products_category_5;
DROP VIEW products_category_5;

-- MATERIALIZED VIEW
CREATE MATERIALIZED VIEW top_customers AS
SELECT SUM(orders.total) as money_spent,user_id,users.email,users.phone_number
FROM orders
JOIN carts ON orders.carts_cart_id = carts.cart_id
JOIN users ON carts.users_user_id = users.user_id
JOIN order_status os on os.order_status_id = orders.order_status_order_status_id
JOIN order_status o on o.order_status_id = orders.order_status_order_status_id
GROUP BY users.user_id,users.email,users.phone_number
ORDER BY SUM(orders.total) DESC;

REFRESH MATERIALIZED VIEW top_customers;
SELECT * FROM top_customers;
DROP MATERIALIZED VIEW top_customers;

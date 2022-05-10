/* TASK 1:
Создайте новую таблицу potential customers с полями id, email, name, surname, second_name, city
Заполните данными таблицу.
Выведите имена и электронную почту потенциальных и существующих пользователей из города city 17
*/

CREATE TABLE potential_customers(
    id SERIAL PRIMARY KEY,
    email varchar(100),
    name varchar(255),
    surname varchar(255),
    second_name varchar(255),
    city varchar(255)
);


INSERT INTO potential_customers(email, name, surname, second_name, city)
VALUES
('potential_email1','potential_name1','potential_surname1','potential_second_name1','potential_city1'),
('potential_email2','potential_name2','potential_surname2','potential_second_name2','potential_city2'),
('potential_email3','potential_name3','potential_surname3','potential_second_name3','potential_city3'),
('potential_email4','potential_name4','potential_surname4','potential_second_name4','potential_city4'),
('potential_email5','potential_name5','potential_surname5','potential_second_name5','potential_city5'),
('potential_email6','potential_name6','potential_surname6','potential_second_name6','potential_city6'),
('potential_email7','potential_name7','potential_surname7','potential_second_name7','potential_city7'),
('potential_email8','potential_name8','potential_surname8','potential_second_name8','potential_city8'),
('potential_email9','potential_name9','potential_surname9','potential_second_name9','potential_city9'),
('potential_email10','potential_name10','potential_surname10','potential_second_name10','potential_city10'),
('potential_email11','potential_name11','potential_surname11','potential_second_name11','potential_city11'),
('potential_email12','potential_name12','potential_surname12','potential_second_name12','potential_city12'),
('potential_email13','potential_name13','potential_surname13','potential_second_name13','potential_city13'),
('potential_email14','potential_name14','potential_surname14','potential_second_name14','potential_city14'),
('potential_email15','potential_name15','potential_surname15','potential_second_name15','potential_city15'),
('potential_email16','potential_name16','potential_surname16','potential_second_name16','potential_city16'),
('potential_email17','potential_name17','potential_surname17','potential_second_name17','potential_city17'),
('potential_email18','potential_name18','potential_surname18','potential_second_name18','potential_city18'),
('potential_email19','potential_name19','potential_surname19','potential_second_name19','potential_city19'),
('potential_email20','potential_name20','potential_surname20','potential_second_name20','potential_city20'),
('potential_email21','potential_name21','potential_surname21','potential_second_name21','potential_city21'),
('potential_email22','potential_name22','potential_surname22','potential_second_name22','potential_city22'),
('potential_email23','potential_name23','potential_surname23','potential_second_name23','potential_city23'),
('potential_email24','potential_name24','potential_surname24','potential_second_name24','potential_city24'),
('potential_email25','potential_name25','potential_surname25','potential_second_name25','potential_city25'),
('potential_email26','potential_name26','potential_surname26','potential_second_name26','potential_city26'),
('potential_email27','potential_name27','potential_surname27','potential_second_name27','potential_city27'),
('potential_email28','potential_name28','potential_surname28','potential_second_name28','potential_city28'),
('potential_email29','potential_name29','potential_surname29','potential_second_name29','potential_city29'),
('potential_email30','potential_name30','potential_surname30','potential_second_name30','potential_city30');


SELECT first_name,email FROM users
WHERE city = 'city 17' UNION
SELECT name,email FROM potential_customers
WHERE city = 'potential_city17';

/* TASK 2:
Вывести имена и электронные адреса всех users отсортированных по городам и по имени (по алфавиту)
*/

SELECT first_name,email,city FROM users ORDER BY city, first_name ASC;

/* TASK 3:
Вывести наименование группы товаров, общее количество по группе товаров в порядке убывания количества
*/

SELECT categories.category_title,count(products.product_id) FROM  categories
JOIN products ON products.category_id=categories.category_id GROUP BY categories.category_title
ORDER BY COUNT(products.product_id) DESC;


/* TASK 4:
   1. Вывести продукты, которые ни разу не попадали в корзину.
2. Вывести все продукты, которые так и не попали ни в 1 заказ. (но в корзину попасть могли)
3. Вывести топ 10 продуктов, которые добавляли в корзины чаще всего.
4. Вывести топ 10 продуктов, которые не только добавляли в корзины, но и оформляли заказы чаще всего.
5. Вывести топ 5 юзеров, которые потратили больше всего денег (total в заказе).
6. Вывести топ 5 юзеров, которые сделали больше всего заказов (кол-во заказов).
7. Вывести топ 5 юзеров, которые создали корзины, но так и не сделали заказы.
 */

SELECT product_id,product_title,product_description,in_stock,price,slug,category_id
FROM PRODUCTS LEFT OUTER JOIN cart_product cp ON products.product_id = cp.products_product_id
WHERE cp.products_product_id IS NULL;


SELECT DISTINCT products.product_title
FROM products
INNER JOIN cart_product AS cp ON cp.products_product_id = products.product_id
LEFT JOIN orders ON cp.carts_cart_id = orders.carts_cart_id
WHERE orders.carts_cart_id IS NULL;


SELECT products_product_id, COUNT(products_product_id)
FROM cart_product
GROUP BY products_product_id
ORDER BY COUNT(products_product_id) DESC
LIMIT 10;


SELECT products_product_id, COUNT(products_product_id)
FROM cart_product
INNER JOIN orders
ON cart_product.carts_cart_id = orders.carts_cart_id
GROUP BY products_product_id
ORDER BY COUNT(products_product_id) DESC
LIMIT 10;


SELECT user_id, email, password, first_name, last_name, middle_name,
is_staff, country, city, address, phone_number FROM users
INNER JOIN carts c ON users.user_id = c.users_user_id
INNER JOIN orders o ON c.cart_id = o.carts_cart_id ORDER BY o.total DESC LIMIT 5;


SELECT carts.users_user_id
FROM carts
INNER JOIN orders
ON carts.cart_id = orders.carts_cart_id
GROUP BY carts.users_user_id
ORDER BY COUNT(carts.cart_id) DESC
LIMIT 5;


SELECT users_user_id FROM carts c
LEFT JOIN orders ON c.cart_id = orders.carts_cart_id
WHERE orders.carts_cart_id IS NULL
GROUP BY users_user_id
ORDER BY COUNT(c.cart_id) DESC
LIMIT 5;

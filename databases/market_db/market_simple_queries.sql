/* TASK 1:
   Вывести:
1. всех юзеров,
2. все продукты,
3. все статусы заказов
*/

SELECT * FROM users;

SELECT * FROM products;

SELECT * FROM order_status;

/* TASK 2:
    Вывести заказы, которые успешно доставлены и оплачены
*/

SELECT * FROM orders WHERE order_status_order_status_id = 3 OR order_status_order_status_id = 4;

/* TASK 3:
Вывести:
(если задание можно решить несколькими способами, указывай все)
1. Продукты, цена которых больше 80.00 и меньше или равно 150.00
2. заказы совершенные после 01.10.2020 (поле created_at)
3. заказы полученные за первое полугодие 2020 года
4. подукты следующих категорий Category 7, Category 11, Category 18
5. незавершенные заказы по состоянию на 31.12.2020
6.Вывести все корзины, которые были созданы, но заказ так и не был оформлен.
 */

SELECT * FROM products WHERE price BETWEEN 80.0001 AND 150.0;
SELECT * FROM products WHERE price>80.0 AND price<=150.0;

SELECT * FROM orders WHERE created_at>'01 october 2020'::date;
SELECT * FROM orders WHERE
created_at>'10.01.2020'::date;


SELECT * FROM ORDERS WHERE created_at>='01 january 2020'::date and created_at<='30 june 2020'::date;
SELECT * FROM ORDERS WHERE created_at>='01.01.2020'::date and created_at<='06.30.2020'::date;


SELECT * FROM products WHERE category_id IN
(SELECT category_id FROM categories WHERE category_title IN ('Category 7','Category 11', 'Category 18'));
SELECT * FROM  products WHERE category_id IN (7,11,18);


SELECT * FROM ORDERS WHERE created_at = '12.31.2020'::date AND order_status_order_status_id IN
(SELECT order_status_id FROM order_status WHERE status_name NOT ILIKE 'Finished');
SELECT * FROM ORDERS WHERE created_at='31 december 2020'::date AND NOT order_status_order_status_id = 4; /*hardcode*/


SELECT * FROM ORDERS WHERE order_status_order_status_id IN
(SELECT order_status_id FROM order_status WHERE status_name = 'Canceled');
SELECT * FROM ORDERS WHERE order_status_order_status_id = 5; /*hardcode*/
/* TASK 4:
   Вывести:
1. среднюю сумму всех завершенных сделок
2. вывести максимальную сумму сделки за 3 квартал 2020
*/
SELECT AVG(total) FROM ORDERS GROUP BY order_status_order_status_id
HAVING order_status_order_status_id =
(SELECT order_status_id FROM order_status WHERE status_name='Finished');
SELECT AVG(total) FROM ORDERS GROUP BY order_status_order_status_id HAVING
order_status_order_status_id = 4; /*hardcode*/


SELECT MAX(total) FROM orders
WHERE created_at>='01 july 2020'::date and created_at<='30 september 2020'::date;

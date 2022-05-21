-- THIS FUNCTION SETS SHIPPING TOTAL TO 0 FOR PARTICULAR CITY
create or replace function cancel_shipping(city_name varchar)
returns orders.shipping_total%type
language plpgsql
as $$
declare
    sum orders.shipping_total%type=0;
    shipping_city record;
begin
    for shipping_city in (
        select shipping_total,u.city,orders.order_id from orders
        inner join carts c on c.cart_id = orders.carts_cart_id
        inner join users u on u.user_id = c.users_user_id
    )
    loop
        if shipping_city.city = city_name then
            sum = sum + shipping_city.shipping_total;
            update orders set shipping_total = 0 where order_id = shipping_city.order_id;
        end if;
    end loop;
    return sum;
end;$$;
-- INSERTING SAMPLE DATA BECAUSE DB ITSELF HAS ONLY 1 ORDER FOR 1 USER AND, THEREFORE,
-- ONLY 1 ORDER WILL BE REMOVED FOR PARTICULAR CITY WITHOUT INSERTIONS
INSERT INTO orders(order_id, carts_cart_id, order_status_order_status_id, shipping_total, total, created_at, uploaded_at)
VALUES (6666,1,4,60,1000,'2017.02.02'::timestamp,'2017.02.02'::timestamp),
       (6667,1,4,60,1000,'2017.02.02'::timestamp,'2017.02.02'::timestamp),
(6668,1,4,60,1000,'2017.02.02'::timestamp,'2017.02.02'::timestamp);
SELECT cancel_shipping('city 1');



-- This procedure applies discount to the total of an order, taking in count order`s status
-- (accepted or in progress), and value of discount (0,0.5].
create or replace procedure discount(
    discount float,
    id_order int
)
language plpgsql
as $$
declare
status int;
begin
    select order_status_order_status_id into status from orders where order_id = id_order;
    if not found then
        raise 'Order #% not found',id_order;
    end if;
    if status not in (1,2) then
        raise 'Order #% is not processed or accepted',id_order;
    elsif discount > 0.5 or discount<=0 then
        raise 'Expected discount in range (0,0.5], got %',discount;
    else
         update orders set total = total - total*discount
         where order_id = id_order;
         commit;
    end if;
end;$$;

call discount(0.5,99999);
call discount(0.5,1);
call discount(10,2);
call discount(0.5,2);



--THIS PROCEDURE ADDS PRODUCT TO CART, ADDING IT'S PRICE TO CART`S TOTAL
--IF AMOUNT IS MORE THAN PRODUCT IN STOCK - TRANSACTION RETRIEVES.
create or replace procedure add_product(
    id_product int,
    id_cart int,
    amount int
)
language plpgsql
as $$
declare
    stock int;
    product_price products.price%type;
    temp record;
begin
    select in_stock into stock from products where product_id=id_product;
    if stock<0 then
        rollback;
    end if;
for i in 1..amount loop
    if stock<1 then
        rollback;
    else
        update products set in_stock = in_stock -1 where product_id=id_product
        returning in_stock,price into stock,product_price;
        update carts set total = total + product_price where cart_id = id_cart;
    end if;
end loop;
    select * into temp from cart_product where carts_cart_id=id_cart and products_product_id = id_product;
    if not found then
        insert into cart_product values (id_cart,id_product);
    end if;
end;$$;

call add_product(8,1,3); --DOES NOTHING
call add_product(8,1,2); --APPLIES CHANGES
call add_product(777,2000,1); -- ALSO ADDS ROW FOR cart_product (2000,777)


-- this procedure retrieves potential customer and adds it to users table
create or replace procedure add_user(
potential_user_id integer,
new_password character varying,
staff_verify smallint,
new_country character varying,
new_address character varying,
new_phone character varying
)
language plpgsql
as $$
declare
    potential_row record;

    new_id integer;
begin
    select * into potential_row from potential_customers where id = potential_user_id;
    if not found then
        raise 'Not found potential user with id %',potential_user_id;
    end if;
    select max(user_id)+1 into new_id from users;
    insert into users(user_id, email, password, first_name, last_name,
                      middle_name, is_staff, country, city, address, phone_number)
    VALUES (new_id,potential_row.email,new_password,potential_row.name,
            potential_row.surname,potential_row.second_name,staff_verify,new_country,potential_row.city,
            new_address,new_phone);
    DELETE FROM potential_customers WHERE id = potential_user_id;
    commit;
end;$$;

call add_user(3,'zxczxczxc',
    0::smallint,'Zimbabwe','Kyivska','0984959291');
call add_user(3000,'zxczxczxc', --RAISES EXCEPTION
    0::smallint,'Zimbabwe','Kyivska','0984959291');

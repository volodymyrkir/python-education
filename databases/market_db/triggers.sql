--COMPARING PRICE OF EACH PRODUCT WITH AVG ON IT'S CATEGORY
select c.category_title,product_title,price,avg(price)
over w from products
join categories c on c.category_id = products.category_id
window w as (partition by category_title)
order by c.category_title;

--Establishes, that price of product can't be more than it's category`s avg * 3
create or replace function check_price()
returns trigger
language plpgsql
as $$
declare
    avg_price numeric;
begin
    select avg(price) into avg_price from products
    where products.category_id = new.category_id group by products.category_id;
    if new.price>avg_price*3 then
        raise exception 'Price of product must be less or equal % for this product',avg_price*3;
    end if;
    return new;
end;$$;

begin;
drop trigger if exists new_product_price on products;

create trigger new_product_price
    before insert or update
    on products
    for each row
    execute procedure check_price();

commit;

insert into products values
(9998,'Product 9998','Product description 9998',31,5000,'Product-9998',3);
update products set price = 10000 where product_id=1;



--This trigger logs all status changes in every order into new table changed_orders
--Old status, new status and current time are logged.
create table changed_orders(
    changed_id serial,
    order_id integer not null,
    old_status varchar not null,
    new_status varchar not null,
    timestamp timestamp(6) default now() not null
);
create or replace function log_changed_orders()
returns trigger
language plpgsql
as $$
declare
    older_status varchar;
    newer_status varchar;
begin
    select status_name into older_status from order_status where order_status_id=old.order_status_order_status_id;
    select status_name into newer_status from order_status where order_status_id=new.order_status_order_status_id;
    insert into changed_orders(order_id, old_status, new_status) values
    (old.order_id,older_status,newer_status);
    return new;
end;
$$;

begin;

drop trigger if exists status_change on orders;

create trigger status_change
    before update
    on orders
    for each row
    execute procedure log_changed_orders();

end;

update orders set order_status_order_status_id=4 where order_id=1;

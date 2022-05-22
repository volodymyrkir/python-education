--finds all car's with input pattern
create or replace function get_cars(model_name_pattern varchar)
returns table(
    car_id integer,
    car_model varchar,
    car_price numeric
    )
as $$
begin
    return query select car.car_id,m.model_name,car.car_price from car
        join model m on m.model_id = car.models_model_id
        where m.model_name ilike '%'||model_name_pattern||'%';
    IF NOT FOUND THEN
        RAISE EXCEPTION 'No car named %',model_name_pattern;
    END IF;
end;$$
language plpgsql;

select * from get_cars('audi');
select * from get_cars('zhiguli');
select * from get_cars('123');


--discounts all prices within one brand
create or replace function discount_brand(brand_name varchar,discount float)
returns car.car_price%type
language plpgsql
as $$
declare
    sum car.car_price%type=0;
    car_record record;
begin
    if discount not between 0.1 and 0.9 then
        raise exception 'Wrong discount, expected [0.1,0.9], got %',discount;
    end if;
    for car_record in (
        select car.car_id,car.car_price,b.brand_name
        from car join model m on m.model_id = car.models_model_id
        join brand b on b.brand_id = m.brands_brand_id
    )
    loop
        if car_record.brand_name ilike brand_name then
            sum = sum + car_record.car_price-car_record.car_price*discount;
            update car set car_price = car_record.car_price-car_record.car_price*discount
            where car_id = car_record.car_id;
        end if;
    end loop;
    return sum;
end;$$;

select discount_brand('zhiguli',0.1);


--sums car_price for all cars within 1 brand
create or replace function sum_cars(brand_name varchar)
returns car.car_price%type
language plpgsql
as $$
declare
curs1 cursor for select car_price from get_cars(brand_name);
value integer;
sum car.car_price%type :=0;
bound integer;
begin
    open curs1;
    select count(*) into bound from get_cars(brand_name);
    for i in 1..bound
    loop
        fetch curs1 into value;
        sum = sum + value;
    end loop;
    close curs1;
    return sum;
end;$$;

select sum_cars('audi');

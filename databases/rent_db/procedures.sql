alter table rent add column total numeric;

update rent r set total = renting_period*(select car_price from car where car_id=r.cars_car_id);

--This procedure takes rent, in which accident happened and car was broken
--Updates cost of car in rent and if it is not cheap, makes customer to pay for repair.
create or replace procedure broken_car(
broken_rent integer,
cost numeric
)
language plpgsql
as $$
declare
    price car.car_price%type;
    id_car integer;
BEGIN
    select c.car_price,car_id into price,id_car from rent
    join car c on rent.cars_car_id = c.car_id where rent.rent_id=broken_rent;
    update rent set total=total+cost where rent_id=broken_rent;
    commit;
    if price>3000 then
        update car set car_price=car_price/2 where car.car_id=id_car;
        commit;
    else rollback;
    end if;
end;$$;

call broken_car(4,5000.0);


--This procedure replaces rent order based on new car and renting period
create or replace procedure replace_rent(
    id_rent integer,
    new_car integer,
    new_period integer
)
language plpgsql
as $$
declare
    id_branch integer;
    id_customer integer;
    car_expected integer;
    price_value car.car_price%type;
begin
    select r.branches_branch_id,r.customers_customer_id
    into id_branch,id_customer
    from rent r
    where r.rent_id=id_rent;
    delete from rent where rent_id=id_rent;
    select car_id,car_price into car_expected,price_value from car where car_id=new_car;
    if car_expected is null or price_value is null then
        rollback;
    else
    insert into rent(rent_id, cars_car_id, branches_branch_id, customers_customer_id, renting_period, total)
    values(id_rent,new_car,id_branch,id_customer,new_period,price_value*new_period);
    commit;
    end if;
end;$$;

call replace_rent(1,3,3);

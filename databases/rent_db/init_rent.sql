--create database rent;
create table country(
    country_id serial primary key,
    country_name varchar not null
);

create table city(
    city_id serial primary key,
    countries_country_id integer references country(country_id) not null,
    city_name varchar not null
);

create table address(
    address_id serial primary key,
    address_name varchar not null,
    cities_city_id integer references city(city_id) not null
);

create table contact(
    contact_id serial primary key,
    addresses_address_id integer references address(address_id) not null,
    contact_phone varchar not null
);

create table customer(
    customer_id serial primary key,
    contacts_contact_id integer references contact(contact_id) not null,
    first_name varchar not null,
    last_name varchar not null
);

create table branch(
    branch_id serial primary key,
    contacts_contact_id integer references contact(contact_id) not null
);

create table brand(
    brand_id serial primary key,
    brand_name varchar not null
);

create table model(
    model_id serial primary key,
    model_name varchar not null,
    brands_brand_id integer references brand(brand_id) not null
);

create table car(
    car_id serial primary key,
    models_model_id integer references model(model_id) not null,
    car_price numeric not null
);

create table rent(
    rent_id serial primary key,
    cars_car_id integer references car(car_id) not null,
    branches_branch_id integer references branch(branch_id) not null,
    customers_customer_id integer references customer(customer_id) not null,
    renting_period integer not null,
    renting_date date default current_date
);

begin;
create or replace procedure fill_countries()
language plpgsql
as $$
begin
for i in 1..3000
loop
insert into country(country_name)
values ('Country '||i::varchar);
end loop;
end;$$;
call fill_countries();
drop procedure fill_countries();
commit;

begin;
create or replace procedure fill_cities()
language plpgsql
as $$
begin
for i in 1..3000
loop
    insert into city(countries_country_id, city_name) values
    (i,'City 1 in country '||i::varchar),
    (i,'City 2 in country '||i::varchar);
end loop;
end;$$;
call fill_cities();
drop procedure fill_cities();
commit;

begin;
create or replace procedure fill_addresses()
language plpgsql
as $$
begin
for i in 1..3000
loop
    insert into address(address_name, cities_city_id) values
    ('address 1 in city '||i::varchar,i),
    ('address 2 in city '||i::varchar,i);
end loop;
end;$$;
call fill_addresses();
drop procedure fill_addresses();
commit;

begin;
create or replace procedure fill_contacts()
language plpgsql
as $$
begin
for i in 1..6000
loop
    insert into contact(addresses_address_id, contact_phone) values
    (i,'+'||ceil(random()*10)::varchar||ceil(random()*10)::varchar||'-'||ceil(random()*10)::varchar||
    ceil(random()*10)::varchar||ceil(random()*10)::varchar||ceil(random()*10)::varchar||ceil(random()*10)::varchar||
    ceil(random()*10)::varchar||ceil(random()*10)::varchar||ceil(random()*10)::varchar||ceil(random()*10)::varchar||
    ceil(random()*10)::varchar);
end loop;
end;$$;
call fill_contacts();
drop procedure fill_contacts();
commit;

begin;
create or replace procedure fill_customers()
language plpgsql
as $$
begin
for i in 1..5000
loop
    insert into customer(contacts_contact_id, first_name, last_name)
    values(i,'Customer_name '||i::varchar,'Customer_surname'||i::varchar);
end loop;
end;$$;
call fill_customers();
drop procedure fill_customers();
commit;

insert into brand(brand_name) values
('BMW'),('Motorola'),('Audi'),('Lexus'),('Mazda'),('KAMaz'),('Lada'),('Ferrari'),('Lamborghini'),('Zhiguli'),('Tesla');


begin;
create or replace procedure fill_models()
language plpgsql
as $$
declare
    curs_brand cursor for select * from brand;
    smth record;
    bound integer;
begin
    open curs_brand;
    select count(*) into bound from brand;
    for _ in 1..bound
    loop
        fetch curs_brand into smth;
        for i in 1..10
        loop
            insert into model(model_name, brands_brand_id)
            values(smth.brand_name::varchar||'`s car_'||i::varchar,smth.brand_id);
        end loop;
    end loop;
    close curs_brand;
end;$$;
call fill_models();
drop procedure fill_models();
commit;

begin;
create or replace procedure fill_cars()
language plpgsql
as $$
declare
    bound integer;
begin
    select count(*) into bound from model;
    for i in 1..bound
    loop
        for _ in 1..100
        loop
            insert into car(models_model_id, car_price)
            values(i,round((random()*(10000.0-2000.0)+2000.0)::numeric,2));
        end loop;
    end loop;
end;$$;
call fill_cars();
drop procedure fill_cars();
commit;

insert into branch(contacts_contact_id)
values (6000),(5999),(5998),(5997),(5996),(5995),(5994),(5993),(5992),(5991);

begin;
create or replace procedure fill_rents()
language plpgsql
as $$
declare
    bound integer;
    car_counter integer :=1;
    branches integer;
begin
    select count(*)-500 into bound from customer; --some of customers have never made an order for rent
    select count(*) into branches from branch;
    for i in 1..bound
    loop
        for _ in 1..random()*2+1
        loop
            insert into rent(cars_car_id, branches_branch_id, customers_customer_id, renting_period)
            values(car_counter,random()*(branches-1)+1,i,random()*10+1);
            car_counter = car_counter +1;
        end loop;
    end loop;
end;$$;
call fill_rents();
drop procedure fill_rents();
commit;

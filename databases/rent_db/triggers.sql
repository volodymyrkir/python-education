--logs new rent
create table log_new_rent(
    id serial primary key,
    rent_id integer not null,
    cars_car_id integer not null,
    total_registrate numeric,
    time timestamp default current_date
);

create or replace function log_new_rent()
returns trigger
language plpgsql
as $$
begin
    insert into log_new_rent(rent_id, cars_car_id, total_registrate)
    values(new.rent_id,new.cars_car_id,new.total);
    return new;
end;$$;

begin;
drop trigger if exists log_new_rent on rent;

create trigger log_new_rent
    after insert or update
    on rent
    for each row
    execute procedure log_new_rent();
commit;

insert into rent(cars_car_id, branches_branch_id, customers_customer_id, renting_period,total)
values (3,2,4,2,10000);
insert into rent(cars_car_id, branches_branch_id, customers_customer_id, renting_period,total)
values (3,2,4,2,10000);

create table log_closed_rent(
    id serial primary key,
    rent_id integer not null,
    cars_car_id integer not null,
    closed_total numeric,
    time timestamp default current_date
);
--logs deletions of rent
create or replace function log_rent()
returns trigger
language plpgsql
as $$
declare
begin
    insert into log_closed_rent(rent_id, cars_car_id, closed_total) VALUES (old.rent_id,old.cars_car_id,old.total);
    return new;
end;$$;

begin;
drop trigger if exists delete_rent on rent;
create trigger delete_rent
    before delete
    on rent
    for each row
    execute procedure log_rent();
commit;

delete from rent where rent_id=505;
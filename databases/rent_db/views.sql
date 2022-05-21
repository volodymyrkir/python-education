

create view zhiguli_expensive as
select * from car
where models_model_id between 91 and 100 and car_price>5000
with check option;

insert into zhiguli_expensive(models_model_id, car_price)
values (91,5001);
select * from zhiguli_expensive;



create view inactive_users as
select c.customer_id,c.first_name,c.last_name from customer c
left join rent r on c.customer_id = r.customers_customer_id
where r.customers_customer_id is null
order by c.customer_id;

select * from inactive_users;

create materialized view top_customers as
select customer.first_name,customer.last_name,sum(car_price*r.renting_period) from customer
join rent r on customer.customer_id = r.customers_customer_id
join car ca on car_id=r.cars_car_id
join contact c on customer.contacts_contact_id = c.contact_id
group by customer.first_name, customer.last_name
order by 3 desc;

refresh materialized view top_customers;
select * from top_customers;


--query that outputs cars ranked within their brand by price of rent.
select car_id,model_name,brand_name,car_price,dense_rank()
over (partition by brand_name order by car_price desc)
from car
    join model m on m.model_id = car.models_model_id
    join brand b on b.brand_id = m.brands_brand_id;

--query that outputs customers, which have not made a rent order.
select c.customer_id,c.first_name,c.last_name from customer c
left join rent r on c.customer_id = r.customers_customer_id where r.customers_customer_id is null;

--

select rent_id,first_name,last_name,con.contact_phone as customer_phone,c.contact_phone as branch_phone,car_id,model_name,brand_name,car_price,renting_period,renting_date
from rent join branch b on b.branch_id = rent.branches_branch_id
join customer c2 on c2.customer_id = rent.customers_customer_id
join contact con on con.contact_id=c2.contacts_contact_id
join contact c on c.contact_id = b.contacts_contact_id
join address a on c.addresses_address_id = a.address_id
join city c3 on a.cities_city_id = c3.city_id
join country c4 on c3.countries_country_id = c4.country_id
join car c5 on rent.cars_car_id = c5.car_id
join model m on c5.models_model_id = m.model_id
join brand b2 on m.brands_brand_id = b2.brand_id;

explain (analyze,buffers) select * from car where models_model_id = 3 or models_model_id = 10;

--WITHOUT INDEX

--Seq Scan on car  (cost=0.00..225.00 rows=199 width=14) (actual time=0.022..0.820 rows=200 loops=1)
  --Filter: ((models_model_id = 3) OR (models_model_id = 10))
  --Rows Removed by Filter: 10800
  --Buffers: shared hit=60
--Planning:
 -- Buffers: shared hit=5
--Planning Time: 0.076 ms
--Execution Time: 0.836 ms

create index index1 on car (models_model_id);

--WITH INDEX

--Bitmap Heap Scan on car  (cost=10.17..73.17 rows=199 width=14) (actual time=0.020..0.035 rows=200 loops=1)
--  Recheck Cond: ((models_model_id = 3) OR (models_model_id = 10))
--  Heap Blocks: exact=3
--  Buffers: shared hit=5 read=2
--  ->  BitmapOr  (cost=10.17..10.17 rows=200 width=0) (actual time=0.014..0.015 rows=0 loops=1)
--        Buffers: shared hit=2 read=2
--        ->  Bitmap Index Scan on index1  (cost=0.00..5.04 rows=100 width=0) (actual time=0.010..0.010 rows=100 loops=1)
--              Index Cond: (models_model_id = 3)
--              Buffers: shared read=2
--        ->  Bitmap Index Scan on index1  (cost=0.00..5.04 rows=100 width=0) (actual time=0.004..0.004 rows=100 loops=1)
--             Index Cond: (models_model_id = 10)
--              Buffers: shared hit=2
--Planning:
--  Buffers: shared hit=15 read=1
--Planning Time: 0.143 ms
--Execution Time: 0.058 ms

ANALYZE products;
ANALYZE cart_product;
ANALYZE orders;

EXPLAIN(ANALYZE,BUFFERS) SELECT DISTINCT products.product_title
FROM products
INNER JOIN cart_product AS cp ON cp.products_product_id = products.product_id
LEFT JOIN orders ON cp.carts_cart_id = orders.carts_cart_id
WHERE orders.carts_cart_id IS NULL;

--NO INDEX
-- HashAggregate  (cost=591.13..618.62 rows=2749 width=32) (actual time=4.764..4.931 rows=1990 loops=1)
--   Group Key: products.product_title
--   Batches: 1  Memory Usage: 241kB
--   Buffers: shared hit=140
--   ->  Merge Join  (cost=429.52..584.25 rows=2749 width=32) (actual time=2.457..4.047 rows=2767 loops=1)
--         Merge Cond: (products.product_id = cp.products_product_id)
--         Buffers: shared hit=140
--         ->  Index Scan using products_product_id_key on products  (cost=0.42..56369.49 rows=989001 width=36) (actual time=0.005..0.628 rows=4000 loops=1)
--               Buffers: shared hit=78
--         ->  Sort  (cost=428.36..435.23 rows=2749 width=4) (actual time=2.448..2.617 rows=2767 loops=1)
--               Sort Key: cp.products_product_id
--               Sort Method: quicksort  Memory: 226kB
--               Buffers: shared hit=62
--               ->  Hash Anti Join  (cost=46.75..271.33 rows=2749 width=4) (actual time=1.468..1.890 rows=2767 loops=1)
--                     Hash Cond: (cp.carts_cart_id = orders.carts_cart_id)
--                     Buffers: shared hit=62
--                     ->  Seq Scan on cart_product cp  (cost=0.00..158.95 rows=10995 width=8) (actual time=0.006..0.540 rows=10995 loops=1)
--                           Buffers: shared hit=49
--                     ->  Hash  (cost=28.00..28.00 rows=1500 width=4) (actual time=0.231..0.231 rows=1500 loops=1)
--                           Buckets: 2048  Batches: 1  Memory Usage: 69kB
--                           Buffers: shared hit=13
--                           ->  Seq Scan on orders  (cost=0.00..28.00 rows=1500 width=4) (actual time=0.002..0.095 rows=1500 loops=1)
--                                 Buffers: shared hit=13
-- Planning:
--   Buffers: shared hit=259 read=1
-- Planning Time: 5.219 ms
-- Execution Time: 5.036 ms

CREATE INDEX ON cart_product(products_product_id);
CREATE INDEX ON cart_product(carts_cart_id);
CREATE INDEX ON orders(carts_cart_id);
--INDEX ON
-- HashAggregate  (cost=591.13..618.62 rows=2749 width=32) (actual time=4.095..4.298 rows=1990 loops=1)
--   Group Key: products.product_title
--   Batches: 1  Memory Usage: 241kB
--   Buffers: shared hit=140
--   ->  Merge Join  (cost=429.52..584.25 rows=2749 width=32) (actual time=2.175..3.498 rows=2767 loops=1)
--         Merge Cond: (products.product_id = cp.products_product_id)
--         Buffers: shared hit=140
--         ->  Index Scan using products_product_id_key on products  (cost=0.42..56369.49 rows=989001 width=36) (actual time=0.004..0.526 rows=4000 loops=1)
--               Buffers: shared hit=78
--         ->  Sort  (cost=428.36..435.23 rows=2749 width=4) (actual time=2.168..2.293 rows=2767 loops=1)
--               Sort Key: cp.products_product_id
--               Sort Method: quicksort  Memory: 226kB
--               Buffers: shared hit=62
--               ->  Hash Anti Join  (cost=46.75..271.33 rows=2749 width=4) (actual time=1.358..1.769 rows=2767 loops=1)
--                     Hash Cond: (cp.carts_cart_id = orders.carts_cart_id)
--                     Buffers: shared hit=62
--                     ->  Seq Scan on cart_product cp  (cost=0.00..158.95 rows=10995 width=8) (actual time=0.003..0.480 rows=10995 loops=1)
--                           Buffers: shared hit=49
--                     ->  Hash  (cost=28.00..28.00 rows=1500 width=4) (actual time=0.221..0.222 rows=1500 loops=1)
--                           Buckets: 2048  Batches: 1  Memory Usage: 69kB
--                           Buffers: shared hit=13
--                           ->  Seq Scan on orders  (cost=0.00..28.00 rows=1500 width=4) (actual time=0.002..0.097 rows=1500 loops=1)
--                                 Buffers: shared hit=13
-- Planning:
--   Buffers: shared hit=69 read=10
-- Planning Time: 0.368 ms
-- Execution Time: 4.401 ms


-- INDEX ON WITHOUT SEQSCAN
-- SET enable_seqscan to OFF;
-- HashAggregate  (cost=744.16..771.65 rows=2749 width=32) (actual time=6.217..6.388 rows=1990 loops=1)
--   Group Key: products.product_title
--   Batches: 1  Memory Usage: 241kB
--   Buffers: shared hit=133 read=18
--   ->  Merge Join  (cost=582.56..737.29 rows=2749 width=32) (actual time=4.292..5.594 rows=2767 loops=1)
--         Merge Cond: (cp.products_product_id = products.product_id)
--         Buffers: shared hit=133 read=18
--         ->  Sort  (cost=581.40..588.27 rows=2749 width=4) (actual time=4.279..4.435 rows=2767 loops=1)
--               Sort Key: cp.products_product_id
--               Sort Method: quicksort  Memory: 226kB
--               Buffers: shared hit=55 read=18
--               ->  Hash Anti Join  (cost=69.81..424.37 rows=2749 width=4) (actual time=2.544..3.593 rows=2767 loops=1)
--                     Hash Cond: (cp.carts_cart_id = orders.carts_cart_id)
--                     Buffers: shared hit=55 read=18
--                     ->  Index Scan using cart_product_carts_cart_id_idx1 on cart_product cp  (cost=0.29..289.21 rows=10995 width=8) (actual time=0.006..1.667 rows=10995 loops=1)
--                           Buffers: shared hit=51 read=15
--                     ->  Hash  (cost=50.78..50.78 rows=1500 width=4) (actual time=0.261..0.262 rows=1500 loops=1)
--                           Buckets: 2048  Batches: 1  Memory Usage: 69kB
--                           Buffers: shared hit=4 read=3
--                           ->  Index Only Scan using orders_carts_cart_id_idx1 on orders  (cost=0.28..50.78 rows=1500 width=4) (actual time=0.008..0.142 rows=1500 loops=1)
--                                 Heap Fetches: 0
--                                 Buffers: shared hit=4 read=3
--         ->  Index Scan using products_product_id_key on products  (cost=0.42..56369.49 rows=989001 width=36) (actual time=0.009..0.537 rows=3999 loops=1)
--               Buffers: shared hit=78
-- Planning:
--   Buffers: shared hit=31
-- Planning Time: 0.239 ms
-- Execution Time: 6.469 ms

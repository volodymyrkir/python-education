EXPLAIN (ANALYZE,BUFFERS ) SELECT products_product_id, COUNT(products_product_id)
FROM cart_product
INNER JOIN orders
ON cart_product.carts_cart_id = orders.carts_cart_id
GROUP BY products_product_id
ORDER BY COUNT(products_product_id) DESC
LIMIT 10;
--NO INDEX
-- Limit  (cost=488.90..488.93 rows=10 width=12) (actual time=4.135..4.139 rows=10 loops=1)
--   Buffers: shared hit=62
--   ->  Sort  (cost=488.90..498.26 rows=3742 width=12) (actual time=4.134..4.136 rows=10 loops=1)
--         Sort Key: (count(cart_product.products_product_id)) DESC
--         Sort Method: top-N heapsort  Memory: 25kB
--         Buffers: shared hit=62
--         ->  HashAggregate  (cost=370.62..408.04 rows=3742 width=12) (actual time=3.473..3.848 rows=3463 loops=1)
--               Group Key: cart_product.products_product_id
--               Batches: 1  Memory Usage: 721kB
--               Buffers: shared hit=62
--               ->  Hash Join  (cost=46.75..329.39 rows=8246 width=4) (actual time=0.259..2.111 rows=8228 loops=1)
--                     Hash Cond: (cart_product.carts_cart_id = orders.carts_cart_id)
--                     Buffers: shared hit=62
--                     ->  Seq Scan on cart_product  (cost=0.00..158.95 rows=10995 width=8) (actual time=0.004..0.475 rows=10995 loops=1)
--                           Buffers: shared hit=49
--                     ->  Hash  (cost=28.00..28.00 rows=1500 width=4) (actual time=0.251..0.252 rows=1500 loops=1)
--                           Buckets: 2048  Batches: 1  Memory Usage: 69kB
--                           Buffers: shared hit=13
--                           ->  Seq Scan on orders  (cost=0.00..28.00 rows=1500 width=4) (actual time=0.002..0.115 rows=1500 loops=1)
--                                 Buffers: shared hit=13
-- Planning:
--   Buffers: shared hit=94
-- Planning Time: 0.349 ms
-- Execution Time: 4.225 ms

CREATE INDEX ON cart_product(carts_cart_id);
CREATE INDEX ON orders(carts_cart_id);

--INDEX ON
-- Limit  (cost=488.90..488.93 rows=10 width=12) (actual time=4.538..4.542 rows=10 loops=1)
--   Buffers: shared hit=62
--   ->  Sort  (cost=488.90..498.26 rows=3742 width=12) (actual time=4.537..4.539 rows=10 loops=1)
--         Sort Key: (count(cart_product.products_product_id)) DESC
--         Sort Method: top-N heapsort  Memory: 25kB
--         Buffers: shared hit=62
--         ->  HashAggregate  (cost=370.62..408.04 rows=3742 width=12) (actual time=3.848..4.241 rows=3463 loops=1)
--               Group Key: cart_product.products_product_id
--               Batches: 1  Memory Usage: 721kB
--               Buffers: shared hit=62
--               ->  Hash Join  (cost=46.75..329.39 rows=8246 width=4) (actual time=0.238..2.325 rows=8228 loops=1)
--                     Hash Cond: (cart_product.carts_cart_id = orders.carts_cart_id)
--                     Buffers: shared hit=62
--                     ->  Seq Scan on cart_product  (cost=0.00..158.95 rows=10995 width=8) (actual time=0.003..0.531 rows=10995 loops=1)
--                           Buffers: shared hit=49
--                     ->  Hash  (cost=28.00..28.00 rows=1500 width=4) (actual time=0.230..0.231 rows=1500 loops=1)
--                           Buckets: 2048  Batches: 1  Memory Usage: 69kB
--                           Buffers: shared hit=13
--                           ->  Seq Scan on orders  (cost=0.00..28.00 rows=1500 width=4) (actual time=0.002..0.101 rows=1500 loops=1)
--                                 Buffers: shared hit=13
-- Planning:
--   Buffers: shared hit=38 read=7
-- Planning Time: 0.304 ms
-- Execution Time: 4.575 ms

SET enable_seqscan to OFF;

--WITHOUT SEQSCAN
-- Limit  (cost=533.48..533.51 rows=10 width=12) (actual time=4.199..4.202 rows=10 loops=1)
--   Buffers: shared hit=43 read=14
--   ->  Sort  (cost=533.48..542.84 rows=3742 width=12) (actual time=4.198..4.199 rows=10 loops=1)
--         Sort Key: (count(cart_product.products_product_id)) DESC
--         Sort Method: top-N heapsort  Memory: 25kB
--         Buffers: shared hit=43 read=14
--         ->  HashAggregate  (cost=415.20..452.62 rows=3742 width=12) (actual time=3.263..3.773 rows=3463 loops=1)
--               Group Key: cart_product.products_product_id
--               Batches: 1  Memory Usage: 721kB
--               Buffers: shared hit=43 read=14
--               ->  Merge Join  (cost=0.56..373.97 rows=8246 width=4) (actual time=0.017..1.941 rows=8228 loops=1)
--                     Merge Cond: (orders.carts_cart_id = cart_product.carts_cart_id)
--                     Buffers: shared hit=43 read=14
--                     ->  Index Only Scan using orders_carts_cart_id_idx2 on orders  (cost=0.28..50.78 rows=1500 width=4) (actual time=0.009..0.129 rows=1500 loops=1)
--                           Heap Fetches: 0
--                           Buffers: shared hit=4 read=3
--                     ->  Index Scan using cart_product_carts_cart_id_idx2 on cart_product  (cost=0.29..289.21 rows=10995 width=8) (actual time=0.006..0.898 rows=8229 loops=1)
--                           Buffers: shared hit=39 read=11
-- Planning:
--   Buffers: shared hit=9
-- Planning Time: 0.156 ms
-- Execution Time: 4.234 ms

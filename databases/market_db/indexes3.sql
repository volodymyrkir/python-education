EXPLAIN (ANALYZE,BUFFERS) SELECT user_id, email, password, first_name, last_name, middle_name,
is_staff, country, city, address, phone_number FROM users
INNER JOIN carts c ON users.user_id = c.users_user_id
INNER JOIN orders o ON c.cart_id = o.carts_cart_id ORDER BY o.total DESC LIMIT 5;

--NO INDEX
-- Limit  (cost=248.30..248.31 rows=5 width=199) (actual time=3.133..3.136 rows=5 loops=1)
--   Buffers: shared hit=41 read=50 dirtied=50
--   ->  Sort  (cost=248.30..252.05 rows=1500 width=199) (actual time=3.131..3.133 rows=5 loops=1)
--         Sort Key: o.total DESC
--         Sort Method: top-N heapsort  Memory: 27kB
--         Buffers: shared hit=41 read=50 dirtied=50
--         ->  Hash Join  (cost=187.50..223.39 rows=1500 width=199) (actual time=1.832..2.549 rows=1500 loops=1)
--               Hash Cond: (c.users_user_id = users.user_id)
--               Buffers: shared hit=38 read=50 dirtied=50
--               ->  Hash Join  (cost=60.00..91.95 rows=1500 width=10) (actual time=0.384..0.749 rows=1500 loops=1)
--                     Hash Cond: (o.carts_cart_id = c.cart_id)
--                     Buffers: shared hit=28
--                     ->  Seq Scan on orders o  (cost=0.00..28.00 rows=1500 width=10) (actual time=0.007..0.095 rows=1500 loops=1)
--                           Buffers: shared hit=13
--                     ->  Hash  (cost=35.00..35.00 rows=2000 width=8) (actual time=0.368..0.369 rows=2000 loops=1)
--                           Buckets: 2048  Batches: 1  Memory Usage: 95kB
--                           Buffers: shared hit=15
--                           ->  Seq Scan on carts c  (cost=0.00..35.00 rows=2000 width=8) (actual time=0.003..0.161 rows=2000 loops=1)
--                                 Buffers: shared hit=15
--               ->  Hash  (cost=90.00..90.00 rows=3000 width=193) (actual time=1.434..1.434 rows=3000 loops=1)
--                     Buckets: 4096  Batches: 1  Memory Usage: 502kB
--                     Buffers: shared hit=10 read=50 dirtied=50
--                     ->  Seq Scan on users  (cost=0.00..90.00 rows=3000 width=193) (actual time=0.003..1.021 rows=3000 loops=1)
--                           Buffers: shared hit=10 read=50 dirtied=50
-- Planning:
--   Buffers: shared hit=282 read=7 dirtied=1
-- Planning Time: 6.248 ms
-- Execution Time: 3.197 ms

CREATE INDEX ON carts(users_user_id);
CREATE INDEX ON orders(carts_cart_id);

--WITH INDEXES
-- Limit  (cost=248.30..248.31 rows=5 width=199) (actual time=3.662..3.666 rows=5 loops=1)
--   Buffers: shared hit=88
--   ->  Sort  (cost=248.30..252.05 rows=1500 width=199) (actual time=3.660..3.664 rows=5 loops=1)
--         Sort Key: o.total DESC
--         Sort Method: top-N heapsort  Memory: 27kB
--         Buffers: shared hit=88
--         ->  Hash Join  (cost=187.50..223.39 rows=1500 width=199) (actual time=1.506..2.712 rows=1500 loops=1)
--               Hash Cond: (c.users_user_id = users.user_id)
--               Buffers: shared hit=88
--               ->  Hash Join  (cost=60.00..91.95 rows=1500 width=10) (actual time=0.593..1.223 rows=1500 loops=1)
--                     Hash Cond: (o.carts_cart_id = c.cart_id)
--                     Buffers: shared hit=28
--                     ->  Seq Scan on orders o  (cost=0.00..28.00 rows=1500 width=10) (actual time=0.005..0.122 rows=1500 loops=1)
--                           Buffers: shared hit=13
--                     ->  Hash  (cost=35.00..35.00 rows=2000 width=8) (actual time=0.580..0.581 rows=2000 loops=1)
--                           Buckets: 2048  Batches: 1  Memory Usage: 95kB
--                           Buffers: shared hit=15
--                           ->  Seq Scan on carts c  (cost=0.00..35.00 rows=2000 width=8) (actual time=0.003..0.259 rows=2000 loops=1)
--                                 Buffers: shared hit=15
--               ->  Hash  (cost=90.00..90.00 rows=3000 width=193) (actual time=0.904..0.904 rows=3000 loops=1)
--                     Buckets: 4096  Batches: 1  Memory Usage: 502kB
--                     Buffers: shared hit=60
--                     ->  Seq Scan on users  (cost=0.00..90.00 rows=3000 width=193) (actual time=0.003..0.349 rows=3000 loops=1)
--                           Buffers: shared hit=60
-- Planning:
--   Buffers: shared hit=17
-- Planning Time: 0.294 ms
-- Execution Time: 3.710 ms

SET enable_seqscan to ON;
--WITHOUT SEQSCAN
-- Limit  (cost=368.19..368.20 rows=5 width=199) (actual time=9.559..9.563 rows=5 loops=1)
--   Buffers: shared hit=92 read=15
--   ->  Sort  (cost=368.19..371.94 rows=1500 width=199) (actual time=9.558..9.560 rows=5 loops=1)
--         Sort Key: o.total DESC
--         Sort Method: top-N heapsort  Memory: 27kB
--         Buffers: shared hit=92 read=15
--         ->  Hash Join  (cost=190.34..343.27 rows=1500 width=199) (actual time=6.236..8.681 rows=1500 loops=1)
--               Hash Cond: (c.users_user_id = users.user_id)
--               Buffers: shared hit=92 read=15
--               ->  Merge Join  (cost=0.56..149.56 rows=1500 width=10) (actual time=0.016..1.864 rows=1500 loops=1)
--                     Merge Cond: (c.cart_id = o.carts_cart_id)
--                     Buffers: shared hit=30 read=7
--                     ->  Index Scan using carts_cart_id_key on carts c  (cost=0.28..80.28 rows=2000 width=8) (actual time=0.007..0.575 rows=1501 loops=1)
--                           Buffers: shared hit=14 read=4
--                     ->  Index Scan using orders_carts_cart_id_idx on orders o  (cost=0.28..66.78 rows=1500 width=10) (actual time=0.006..0.797 rows=1500 loops=1)
--                           Buffers: shared hit=16 read=3
--               ->  Hash  (cost=152.28..152.28 rows=3000 width=193) (actual time=6.210..6.210 rows=3000 loops=1)
--                     Buckets: 4096  Batches: 1  Memory Usage: 502kB
--                     Buffers: shared hit=62 read=8
--                     ->  Index Scan using users_user_id_key on users  (cost=0.28..152.28 rows=3000 width=193) (actual time=0.005..5.790 rows=3000 loops=1)
--                           Buffers: shared hit=62 read=8
-- Planning:
--   Buffers: shared hit=17
-- Planning Time: 0.280 ms
-- Execution Time: 9.615 ms

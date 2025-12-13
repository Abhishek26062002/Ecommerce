insert into admin_details VALUES ('rakesh', 'salapu', 9685741230, 'salapurakesh865@gmail.com')
-- SELECT * from admin_details
-- drop table machines
-- ALTER TABLE products
-- ADD COLUMN downloadable_files VARCHAR;
-- drop table  users;
-- select * from orders
-- select * FROM products;
-- select * from cart_items;
-- drop table wishlist_items;
-- drop table cart_items;
-- drop table orders;
-- drop table products;


-- SELECT
--     tc.table_name AS child_table,
--     kcu.column_name AS child_column,
--     ccu.table_name AS parent_table,
--     ccu.column_name AS parent_column
-- FROM 
--     information_schema.table_constraints tc
-- JOIN 
--     information_schema.key_column_usage kcu
--       ON tc.constraint_name = kcu.constraint_name
-- JOIN 
--     information_schema.constraint_column_usage ccu
--       ON ccu.constraint_name = tc.constraint_name
-- WHERE 
--     tc.constraint_type = 'FOREIGN KEY'
--     AND ccu.table_name = 'products';

-- SELECT * from order_items
-- drop table order_items;
-- drop table orders;
-- select * from order_items;
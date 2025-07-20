"List all customers from Germany"
Select * From customers
where country = 'Germany'


"Show product names and their unit prices"
SELECT product_name, unit_price
FROM products

"Find all orders placed in 2017"
select *
from orders
where year(order_date) = 2017;

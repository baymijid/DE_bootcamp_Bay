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

"List-all-products-with-fewer-than-20-units-in-stock"
select *
from products
where units_in_stock < 20;

"Get all customers who have placed more than 5 orders" 
select *, COUNT(*) as customer_orders
from orders
group by customer_id
having count(*) > 5;

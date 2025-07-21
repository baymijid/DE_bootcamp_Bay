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

" List all orders along with customer company name"
select orders.order_id, customers.company_name
from orders
inner join customers
on orders.customer_id=customers.customer_id;

"Show product name, category name, and supplier name"
select products.product_name, suppliers.company_name, categories.category_name
from products
Full outer join suppliers
on products.supplier_id=suppliers.supplier_id
full outer join categories
on products.category_id=categories.category_id

"Find top 5 most expensive products"
select unit_price, product_name
from products
order by unit_price desc
limit 5

"Show total sales per employee"
select o.employee_id, sum(od.quantity * p.unit_price)
from employees as e
inner join orders  as o on o.employee_id=e.employee_id
inner join order_details as od on od.order_id=o.order_id
inner join products as p on p.product_id=od.product_id
group by e.employee_id 

"Show products that have never been ordered"
SELECT
  p.product_id,
  p.product_name
FROM products AS p
LEFT JOIN order_details AS od
  ON p.product_id = od.product_id
WHERE od.product_id IS NULL
ORDER BY p.product_name;



"Monthly Sales Report by Category and Country
Objective: Join orders, order_details, products, categories, and customers. Aggregate sales grouped by month, category, and customer country.
Generate a monthly report showing total sales amount by product category and customer country. Show only months with more than $10,000 in sales.”"

SELECT 
	month(o.order_date),
    c.category_name, 
    cs.country,
    sum(od.quantity * p.unit_price) as total_sales

FROM orders AS o 
	JOIN order_details AS od 	ON o.order_id = od.order_id
	join products as p 			on p.product_id=od.product_id
	join categories as c 		on c.category_id=p.category_id
	join customers as cs 		on cs.customer_id=o.customer_id
group by 
	month(o.order_date), 
    c.category_name, 
    cs.country
having
	sum(od.quantity * p.unit_price) > 10000
order by
	month(o.order_date),
	c.category_name,
	cs.country;

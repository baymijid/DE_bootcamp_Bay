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



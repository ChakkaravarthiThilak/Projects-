SELECT * FROM retail_orders.table1;
use retail_orders
-- 1. Find top 10 highest revenue-generating products
SELECT 
    product_id, 
    SUM(sales_price * quantity) AS total_revenue
FROM table2
GROUP BY product_id
ORDER BY total_revenue DESC
LIMIT 10;
-- 2. Find the top 5 cities with the highest profit margins
SELECT 
    t1.city, 
    SUM(t2.profit) / SUM(t2.sales_price * t2.quantity) AS profit_margin
FROM table1 t1
JOIN table2 t2 ON t1.order_id = t2.order_id
GROUP BY t1.city
ORDER BY profit_margin DESC
LIMIT 5;
-- 3. Calculate the total discount given for each category
SELECT 
    t1.category, 
    SUM((t2.discount_percent / 100.0) * t2.list_price * t2.quantity) AS total_discount
FROM table1 t1
JOIN table2 t2 ON t1.order_id = t2.order_id
GROUP BY t1.category;
-- 4. Find the average sale price per product category
SELECT 
    t1.category, 
    AVG(t2.sales_price) AS avg_sale_price
FROM table1 t1
JOIN table2 t2 ON t1.order_id = t2.order_id
GROUP BY t1.category;
-- 5. Find the region with the highest average sale price
SELECT 
    t1.region, 
    AVG(t2.sales_price) AS avg_sale_price
FROM table1 t1
JOIN table2 t2 ON t1.order_id = t2.order_id
GROUP BY t1.region
ORDER BY avg_sale_price DESC
LIMIT 1;
-- 6. Find the total profit per category
SELECT 
    t1.category, 
    SUM(t2.profit) AS total_profit
FROM table1 t1
JOIN table2 t2 ON t1.order_id = t2.order_id
GROUP BY t1.category;
-- 7. Identify the top 3 segments with the highest quantity of orders
SELECT 
    t1.segment, 
    SUM(t2.quantity) AS total_quantity
FROM table1 t1
JOIN table2 t2 ON t1.order_id = t2.order_id
GROUP BY t1.segment
ORDER BY total_quantity DESC
LIMIT 3;
-- 8. Determine the average discount percentage given per region
SELECT 
    t1.region, 
    AVG(t2.discount_percent) AS avg_discount_percent
FROM table1 t1
JOIN table2 t2 ON t1.order_id = t2.order_id
GROUP BY t1.region;
-- 9. Find the product category with the highest total profit
SELECT 
    t1.category, 
    SUM(t2.profit) AS total_profit
FROM table1 t1
JOIN table2 t2 ON t1.order_id = t2.order_id
GROUP BY t1.category
ORDER BY total_profit DESC
LIMIT 1;
-- 10. Calculate the total revenue generated per year
SELECT 
    YEAR(t1.order_date) AS year, 
    SUM(t2.sales_price * t2.quantity) AS total_revenue
FROM table1 t1
JOIN table2 t2 ON t1.order_id = t2.order_id
GROUP BY YEAR(t1.order_date)
ORDER BY year;
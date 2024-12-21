SELECT * FROM retail_orders.table2;
use retail_orders
-- 1. Top-Selling Products: Identify products that generate the highest revenue based on sale prices
SELECT 
    p.product_id, 
    p.sub_category, 
    SUM(p.sales_price * p.quantity) AS total_revenue
FROM 
    table1 o
JOIN 
    table2 p ON o.order_id = p.order_id -- Using foreign key relationship
GROUP BY 
    p.product_id, p.sub_category
ORDER BY 
    total_revenue DESC
LIMIT 10;


-- 2. Monthly Sales Analysis: Compare year-over-year sales to identify growth or decline in certain months
SELECT 
    EXTRACT(YEAR FROM o.order_date) AS year,
    EXTRACT(MONTH FROM o.order_date) AS month,
    SUM(p.sales_price * p.quantity) AS total_sales
FROM 
    table1 o
JOIN 
    table2 p ON o.order_id = p.order_id -- Using foreign key relationship
GROUP BY 
    year, month
ORDER BY 
    year, month;
-- 3.Retrieve total sales for each category:
SELECT o.category, SUM(p.sales_price) AS total_sales
FROM table1 o
JOIN table2 p ON o.order_id = p.order_id -- Foreign Key relationship
GROUP BY o.category;

-- 4. Regional Sales Analysis: Identify which areas are performing best in terms of revenue

SELECT 
    o.region, 
    SUM(p.sales_price * p.quantity) AS total_sales,
    SUM(p.profit) AS total_profit
FROM 
    table1 o
JOIN 
    table2 p ON o.order_id = p.order_id -- Using foreign key relationship
GROUP BY 
    o.region
ORDER BY 
    total_sales DESC;

-- 5.Identify products with discounts greater than 20% and their impact on sales
SELECT 
    p.product_id, 
    p.sub_category, 
    p.discount_percent,
    SUM(p.sales_price * p.quantity) AS total_sales,
    SUM((p.list_price - p.sales_price) * p.quantity) AS discount_impact
FROM 
    table1 o
JOIN 
    table2 p ON o.order_id = p.order_id -- Using foreign key relationship
WHERE 
    p.discount_percent > 20
GROUP BY 
    p.product_id, p.sub_category, p.discount_percent
ORDER BY 
    discount_impact DESC;

-- 6.Compare sales for different segments over years
SELECT 
    o.segment, 
    EXTRACT(YEAR FROM o.order_date) AS year, 
    SUM(p.sales_price * p.quantity) AS total_sales
FROM 
    table1 o
JOIN 
    table2 p ON o.order_id = p.order_id -- Using foreign key relationship
GROUP BY 
    o.segment, year
ORDER BY 
    o.segment, year;

-- 7. Identify the product with the highest total profit
SELECT 
    p.product_id, 
    p.sub_category, 
    SUM(p.profit) AS total_profit
FROM 
    table1 o
JOIN 
    table2 p ON o.order_id = p.order_id -- Using foreign key relationship
GROUP BY 
    p.product_id, p.sub_category
ORDER BY 
    total_profit DESC
LIMIT 1;

-- 8. Monthly Revenue Contribution by Region
SELECT 
    o.region, 
    EXTRACT(YEAR FROM o.order_date) AS year, 
    EXTRACT(MONTH FROM o.order_date) AS month, 
    SUM(p.sales_price * p.quantity) AS total_sales
FROM 
    table1 o
JOIN 
    table2 p ON o.order_id = p.order_id -- Using foreign key relationship
GROUP BY 
    o.region, year, month
ORDER BY 
    year, month, total_sales DESC;

-- 9. Top Cities with the Most Orders
SELECT 
    o.city, 
    COUNT(DISTINCT o.order_id) AS total_orders
FROM 
    table1 o
JOIN 
    table2 p ON o.order_id = p.order_id -- Using foreign key relationship
GROUP BY 
    o.city
ORDER BY 
    total_orders DESC
LIMIT 10;

-- 10. Profit Contribution by Category and Sub-Category
SELECT 
    o.category, 
    p.sub_category, 
    SUM(p.profit) AS total_profit
FROM 
    table1 o
JOIN 
    table2 p ON o.order_id = p.order_id -- Using foreign key relationship
GROUP BY 
    o.category, p.sub_category
ORDER BY 
    total_profit DESC;


import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Database connection
conn = sqlite3.connect("sales_data.db")

# Function to execute SQL queries and return results
def execute_query(query):
    return pd.read_sql_query(query, conn)

# Streamlit app
st.title("Sales Data Analysis")

# Sidebar for original query selection
st.sidebar.header("Original Queries")
query_options = [
    "Top 10 Highest Revenue Generating Products",
    "Top 5 Cities with Highest Profit Margins",
    "Total Discount Given per Category",
    "Average Sale Price per Product Category",
    "Region with Highest Average Sale Price",
    "Total Profit per Category",
    "Top 3 Segments with Highest Quantity of Orders",
    "Average Discount Percentage per Region",
    "Product Category with Highest Total Profit",
    "Total Revenue Generated per Year",
]
selected_query = st.sidebar.selectbox("Choose a Query", query_options)

# Sidebar for new query selection
st.sidebar.header("New Queries")
new_query_options = [
    "Top-Selling Products",
    "Monthly Sales Analysis",
    "Total Sales for Each Category",
    "Regional Sales Analysis",
    "Products with Discounts Greater than 20%",
    "Sales Comparison by Segment Over Years",
    "Product with Highest Total Profit",
    "Monthly Revenue by Region",
    "Top Cities with Most Orders",
    "Profit Contribution by Category and Sub-Category"
]
selected_new_query = st.sidebar.selectbox("Choose a New Query", new_query_options)

# SQL Queries for original queries
queries = {
    query_options[0]: '''
        SELECT product_id, SUM(sales_price * quantity) AS total_revenue
        FROM table2
        GROUP BY product_id
        ORDER BY total_revenue DESC
        LIMIT 10;
    ''',
    query_options[1]: '''
        SELECT t1.city, SUM(t2.profit) / SUM(t2.sales_price * t2.quantity) AS profit_margin
        FROM table1 t1
        JOIN table2 t2 ON t1.order_id = t2.order_id
        GROUP BY t1.city
        ORDER BY profit_margin DESC
        LIMIT 5;
    ''',
    query_options[2]: '''
        SELECT t1.category, SUM((t2.discount_percent / 100.0) * t2.list_price * t2.quantity) AS total_discount
        FROM table1 t1
        JOIN table2 t2 ON t1.order_id = t2.order_id
        GROUP BY t1.category;
    ''',
    query_options[3]: '''
        SELECT t1.category, AVG(t2.sales_price) AS avg_sale_price
        FROM table1 t1
        JOIN table2 t2 ON t1.order_id = t2.order_id
        GROUP BY t1.category;
    ''',
    query_options[4]: '''
        SELECT t1.region, AVG(t2.sales_price) AS avg_sale_price
        FROM table1 t1
        JOIN table2 t2 ON t1.order_id = t2.order_id
        GROUP BY t1.region
        ORDER BY avg_sale_price DESC
        LIMIT 1;
    ''',
    query_options[5]: '''
        SELECT t1.category, SUM(t2.profit) AS total_profit
        FROM table1 t1
        JOIN table2 t2 ON t1.order_id = t2.order_id
        GROUP BY t1.category;
    ''',
    query_options[6]: '''
        SELECT t1.segment, SUM(t2.quantity) AS total_quantity
        FROM table1 t1
        JOIN table2 t2 ON t1.order_id = t2.order_id
        GROUP BY t1.segment
        ORDER BY total_quantity DESC
        LIMIT 3;
    ''',
    query_options[7]: '''
        SELECT t1.region, AVG(t2.discount_percent) AS avg_discount_percent
        FROM table1 t1
        JOIN table2 t2 ON t1.order_id = t2.order_id
        GROUP BY t1.region;
    ''',
    query_options[8]: '''
        SELECT t1.category, SUM(t2.profit) AS total_profit
        FROM table1 t1
        JOIN table2 t2 ON t1.order_id = t2.order_id
        GROUP BY t1.category
        ORDER BY total_profit DESC
        LIMIT 1;
    ''',
    query_options[9]: '''
        SELECT strftime('%Y', t1.order_date) AS year, SUM(t2.sales_price * t2.quantity) AS total_revenue
        FROM table1 t1
        JOIN table2 t2 ON t1.order_id = t2.order_id
        GROUP BY year
        ORDER BY year;
    ''',
}

# SQL Queries for new queries
new_queries = {
    new_query_options[0]: '''
        SELECT p.product_id, p.sub_category, SUM(p.sales_price * p.quantity) AS total_revenue
        FROM table1 o
        JOIN table2 p ON o.order_id = p.order_id
        GROUP BY p.product_id, p.sub_category
        ORDER BY total_revenue DESC
        LIMIT 10;
    ''',
    new_query_options[1]: '''
        SELECT 
            strftime('%Y', o.order_date) AS year,
            strftime('%m', o.order_date) AS month,
            SUM(p.sales_price * p.quantity) AS total_sales
        FROM table1 o
        JOIN table2 p ON o.order_id = p.order_id
        GROUP BY year, month
        ORDER BY year, month;
    ''',
    new_query_options[2]: '''
        SELECT o.category, SUM(p.sales_price) AS total_sales
        FROM table1 o
        JOIN table2 p ON o.order_id = p.order_id
        GROUP BY o.category;
    ''',
    new_query_options[3]: '''
        SELECT o.region, SUM(p.sales_price * p.quantity) AS total_sales, SUM(p.profit) AS total_profit
        FROM table1 o
        JOIN table2 p ON o.order_id = p.order_id
        GROUP BY o.region
        ORDER BY total_sales DESC;
    ''',
    new_query_options[4]: '''
        SELECT p.product_id, p.sub_category, p.discount_percent, SUM(p.sales_price * p.quantity) AS total_sales,
               SUM((p.list_price - p.sales_price) * p.quantity) AS discount_impact
        FROM table1 o
        JOIN table2 p ON o.order_id = p.order_id
        WHERE p.discount_percent > 20
        GROUP BY p.product_id, p.sub_category, p.discount_percent
        ORDER BY discount_impact DESC;
    ''',
    new_query_options[5]: '''
        SELECT o.segment, strftime('%Y', o.order_date) AS year, SUM(p.sales_price * p.quantity) AS total_sales
        FROM table1 o
        JOIN table2 p ON o.order_id = p.order_id
        GROUP BY o.segment, year
        ORDER BY o.segment, year;
    ''',
    new_query_options[6]: '''
        SELECT p.product_id, p.sub_category, SUM(p.profit) AS total_profit
        FROM table1 o
        JOIN table2 p ON o.order_id = p.order_id
        GROUP BY p.product_id, p.sub_category
        ORDER BY total_profit DESC
        LIMIT 1;
    ''',
    new_query_options[7]: '''
        SELECT o.region, strftime('%Y', o.order_date) AS year, strftime('%m', o.order_date) AS month, 
               SUM(p.sales_price * p.quantity) AS total_sales
        FROM table1 o
        JOIN table2 p ON o.order_id = p.order_id
        GROUP BY o.region, year, month
        ORDER BY year, month, total_sales DESC;
    ''',
    new_query_options[8]: '''
        SELECT o.city, COUNT(DISTINCT o.order_id) AS total_orders
        FROM table1 o
        JOIN table2 p ON o.order_id = p.order_id
        GROUP BY o.city
        ORDER BY total_orders DESC
        LIMIT 10;
    ''',
    new_query_options[9]: '''
        SELECT o.category, p.sub_category, SUM(p.profit) AS total_profit
        FROM table1 o
        JOIN table2 p ON o.order_id = p.order_id
        GROUP BY o.category, p.sub_category
        ORDER BY total_profit DESC;
    '''
}

# Function to plot a bar chart from a DataFrame
def plot_bar_chart(df, x_col, y_col, title):
    if x_col in df.columns and y_col in df.columns:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(df[x_col].astype(str), df[y_col])
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(title)
        st.pyplot(fig)
    else:
        st.error("Data columns for bar chart not found or incorrect.")

# Display query results and charts
if st.button("Execute Query"):
    # Original Query Execution
    query_result = execute_query(queries[selected_query])
    if not query_result.empty:
        st.write(query_result)
        plot_bar_chart(query_result, query_result.columns[0], query_result.columns[1], selected_query)
    else:
        st.error("No data returned from the original query.")
    
    # New Query Execution
    new_query_result = execute_query(new_queries[selected_new_query])
    if not new_query_result.empty:
        st.write(new_query_result)
        plot_bar_chart(new_query_result, new_query_result.columns[0], new_query_result.columns[1], selected_new_query)
    else:
        st.error("No data returned from the new query.")

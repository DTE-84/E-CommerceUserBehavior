-- Dimension: Customers
CREATE TABLE dim_customers (
    user_id INT PRIMARY KEY,
    user_name VARCHAR(100)
);

-- Dimension: Products
CREATE TABLE dim_products (
    item_id VARCHAR(50) PRIMARY KEY,
    item_name VARCHAR(100),
    price DECIMAL(10, 2)
);

-- Fact: Transactions
CREATE TABLE fact_transactions (
    transaction_id INT PRIMARY KEY,
    user_id INT REFERENCES dim_customers(user_id),
    item_id VARCHAR(50) REFERENCES dim_products(item_id),
    purchase_date DATE,
    revenue DECIMAL(10, 2)
);
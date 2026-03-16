# E-Commerce Analytics Pipeline: Behavioral Intelligence & Data Integrity

## Project Overview
This repository contains a high-fidelity data pipeline designed to transform raw e-commerce transaction logs into actionable behavioral insights. By leveraging a **Star Schema** architecture and **Automated Validation**, this project demonstrates the transition from categorical data to sophisticated ordinal segmentation and churn metrics.

## Key Analytics Features

### 1. Customer Segmentation (VIP vs. Standard)
Using a **Relational Join** between transaction facts and customer dimensions, this query calculates **Customer Lifetime Value (CLV)** to perform a categorical-to-ordinal transformation.

```sql
-- Segments users based on total lifetime spend
SELECT 
    c.user_name,
    COUNT(f.transaction_id) as total_purchases,
    SUM(f.revenue) as lifetime_value,
    CASE 
        WHEN SUM(f.revenue) > 1000 THEN 'VIP'
        ELSE 'Standard'
    END AS customer_segment
FROM fact_transactions f
JOIN dim_customers c ON f.user_id = c.user_id
GROUP BY c.user_id, c.user_name
ORDER BY lifetime_value DESC;
```

### 2. Churn Metrics (Predictive Risk Identification)
This analysis utilizes a **Common Table Expression (CTE)** to isolate the `last_order_date`, enabling the identification of "At Risk" and "Churned" customer segments based on behavioral latency.

```sql
-- Identifies users who made a purchase over 6 months ago, but haven't purchased in the last 30 days
WITH LastPurchase AS (
    SELECT 
        user_id, 
        MAX(purchase_date) as last_order_date
    FROM fact_transactions
    GROUP BY user_id
)
SELECT 
    c.user_name,
    lp.last_order_date,
    CURRENT_DATE - lp.last_order_date AS days_since_last_order,
    CASE
        WHEN CURRENT_DATE - lp.last_order_date > 180 THEN 'Churned'
        WHEN CURRENT_DATE - lp.last_order_date > 90 THEN 'At Risk'
        ELSE 'Active'
    END as churn_status
FROM LastPurchase lp
JOIN dim_customers c ON lp.user_id = c.user_id
WHERE CURRENT_DATE - lp.last_order_date > 90;
```

## Technical Architecture
- **Data Ingestion**: Python (Pandas) for high-performance CSV processing and data wrangling.
- **Data Warehouse**: Postgres (Relational Star Schema) for optimized querying and data integrity.
- **Validation**: Jest for automated unit testing of data transformations, ensuring production-ready reliability.

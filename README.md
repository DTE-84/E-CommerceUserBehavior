readme.md


Customer Segmentation (VIP vs. Standard)
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



Churn Metrics (Identifying At-Risk Customers)

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
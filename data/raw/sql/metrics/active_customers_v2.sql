-- Metric: Active Customers
-- Version: v2
-- Status: Active

SELECT
    COUNT(DISTINCT customer_id) AS active_customers
FROM fct_orders
WHERE is_paid_order = 1
  AND order_date >= CURRENT_DATE - INTERVAL '30' DAY;

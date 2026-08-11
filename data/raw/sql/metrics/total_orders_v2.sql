-- Metric: Total Orders
-- Version: v2
-- Status: Active

SELECT
    COUNT(order_id) AS total_orders
FROM fct_orders
WHERE is_paid_order = 1;

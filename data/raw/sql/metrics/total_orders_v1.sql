-- Metric: Total Orders
-- Version: v1
-- Status: Deprecated

SELECT
    COUNT(order_id) AS total_orders
FROM fct_orders
WHERE order_status <> 'cancelled';

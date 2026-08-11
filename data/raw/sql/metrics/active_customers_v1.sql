-- Metric: Active Customers
-- Version: v1
-- Status: Deprecated

SELECT
    COUNT(DISTINCT customer_id) AS active_customers
FROM fct_web_sessions
WHERE customer_id IS NOT NULL
  AND session_date >= CURRENT_DATE - INTERVAL '30' DAY;

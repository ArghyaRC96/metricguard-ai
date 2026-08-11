-- Metric: Conversion Rate
-- Version: v1
-- Status: Deprecated

SELECT
    1.0 * COUNT(
        DISTINCT CASE
            WHEN completed_purchase = TRUE
            THEN customer_id
        END
    )
    / NULLIF(COUNT(*), 0) AS conversion_rate

FROM fct_web_sessions;

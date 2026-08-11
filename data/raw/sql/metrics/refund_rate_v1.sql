-- Metric: Refund Rate
-- Version: v1
-- Status: Deprecated

SELECT
    1.0 * COUNT(DISTINCT r.order_id)
    /
    NULLIF(
        COUNT(DISTINCT CASE
            WHEN o.is_paid_order = 1
            THEN o.order_id
        END),
        0
    ) AS refund_rate

FROM fct_orders o

LEFT JOIN stg_refunds r
    ON o.order_id = r.order_id;

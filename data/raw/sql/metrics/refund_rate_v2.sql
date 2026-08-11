-- Metric: Refund Rate
-- Version: v2
-- Status: Active

SELECT
    1.0 * COUNT(
        DISTINCT CASE
            WHEN completed_refund_amount > 0
            THEN order_id
        END
    )
    /
    NULLIF(
        COUNT(
            DISTINCT CASE
                WHEN is_paid_order = 1
                THEN order_id
            END
        ),
        0
    ) AS refund_rate

FROM fct_orders;

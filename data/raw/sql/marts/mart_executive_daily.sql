-- ============================================================
-- Northstar Commerce
-- Mart: Executive Daily KPIs
-- Owner: BI Platform
-- Revenue Definition Version: v2
-- Last Reviewed: 2026-01-15
-- ============================================================

SELECT
    order_date,

    COUNT(
        CASE
            WHEN is_paid_order = 1
            THEN order_id
        END
    ) AS total_orders,

    SUM(
        CASE
            WHEN is_paid_order = 1
            THEN gross_merchandise_amount
            ELSE 0
        END
    ) AS gross_revenue,

    SUM(
        CASE
            WHEN is_paid_order = 1
            THEN gross_merchandise_amount
                 - discount_amount
                 - completed_refund_amount
            ELSE 0
        END
    ) AS net_revenue

FROM fct_orders

GROUP BY order_date;

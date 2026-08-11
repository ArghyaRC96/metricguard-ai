-- ============================================================
-- Northstar Commerce
-- Mart: Finance Daily
-- Owner: Finance Analytics
-- Revenue Definition Version: v3
-- Last Reviewed: 2026-04-05
-- ============================================================

SELECT
    order_date,

    COUNT(
        CASE
            WHEN is_paid_order = 1
            THEN order_id
        END
    ) AS paid_orders,

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
            THEN discount_amount
            ELSE 0
        END
    ) AS discounts,

    SUM(completed_refund_amount)
        AS refunds,

    SUM(chargeback_amount)
        AS chargebacks,

    SUM(
        CASE
            WHEN is_paid_order = 1
            THEN gross_merchandise_amount
                 - discount_amount
                 - completed_refund_amount
                 - chargeback_amount
            ELSE 0
        END
    ) AS net_revenue

FROM fct_orders

GROUP BY order_date;

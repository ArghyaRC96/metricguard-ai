-- ============================================================
-- Northstar Commerce
-- Metric: Net Revenue
-- Version: v1
-- Status: Deprecated
-- ============================================================

SELECT
    order_id,
    order_date,

    gross_merchandise_amount
    - completed_refund_amount
        AS net_revenue

FROM fct_orders

WHERE is_paid_order = 1;

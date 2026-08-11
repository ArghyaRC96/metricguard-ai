-- ============================================================
-- Northstar Commerce
-- Model: fct_orders
-- Grain: One row per order
-- Purpose:
-- Combine orders with payments, refunds, and chargebacks.
-- ============================================================

WITH payment_summary AS (

    SELECT
        order_id,

        SUM(
            CASE
                WHEN transaction_type = 'payment'
                     AND transaction_status = 'successful'
                THEN transaction_amount
                ELSE 0
            END
        ) AS successful_payment_amount,

        SUM(
            CASE
                WHEN transaction_type = 'chargeback'
                     AND transaction_status = 'posted'
                THEN transaction_amount
                ELSE 0
            END
        ) AS chargeback_amount

    FROM stg_payments

    GROUP BY order_id
),

refund_summary AS (

    SELECT
        order_id,

        SUM(
            CASE
                WHEN refund_status = 'completed'
                THEN refund_amount
                ELSE 0
            END
        ) AS completed_refund_amount

    FROM stg_refunds

    GROUP BY order_id
)

SELECT
    o.order_id,
    o.customer_id,
    o.order_date,
    o.order_status,
    o.sales_channel,
    o.currency,

    o.gross_merchandise_amount,
    o.discount_amount,
    o.subtotal_amount,
    o.shipping_amount,
    o.tax_amount,
    o.order_total_amount,

    COALESCE(
        p.successful_payment_amount,
        0
    ) AS successful_payment_amount,

    COALESCE(
        r.completed_refund_amount,
        0
    ) AS completed_refund_amount,

    COALESCE(
        p.chargeback_amount,
        0
    ) AS chargeback_amount,

    CASE
        WHEN COALESCE(
            p.successful_payment_amount,
            0
        ) > 0
        THEN 1
        ELSE 0
    END AS is_paid_order

FROM stg_orders o

LEFT JOIN payment_summary p
    ON o.order_id = p.order_id

LEFT JOIN refund_summary r
    ON o.order_id = r.order_id;
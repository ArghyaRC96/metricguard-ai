-- ============================================================
-- Northstar Commerce
-- Model: stg_payments
-- Purpose: Standardize payments and chargebacks
-- ============================================================

SELECT
    payment_id,
    order_id,

    CAST(transaction_date AS DATE)
        AS transaction_date,

    LOWER(TRIM(transaction_type))
        AS transaction_type,

    LOWER(TRIM(payment_method))
        AS payment_method,

    CAST(transaction_amount AS DECIMAL(18, 2))
        AS transaction_amount,

    LOWER(TRIM(transaction_status))
        AS transaction_status

FROM raw_payments;
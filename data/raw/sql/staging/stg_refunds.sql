-- ============================================================
-- Northstar Commerce
-- Model: stg_refunds
-- Purpose: Standardize refund transactions
-- ============================================================

SELECT
    refund_id,
    order_id,

    CAST(refund_date AS DATE)
        AS refund_date,

    CAST(refund_amount AS DECIMAL(18, 2))
        AS refund_amount,

    LOWER(TRIM(refund_reason))
        AS refund_reason,

    LOWER(TRIM(refund_status))
        AS refund_status

FROM raw_refunds;
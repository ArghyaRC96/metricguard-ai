-- ============================================================
-- Northstar Commerce
-- Model: stg_orders
-- Purpose: Standardize raw order transactions
-- ============================================================

SELECT
    order_id,
    customer_id,
    CAST(order_date AS DATE) AS order_date,

    LOWER(TRIM(order_status)) AS order_status,
    LOWER(TRIM(sales_channel)) AS sales_channel,
    UPPER(TRIM(currency)) AS currency,

    CAST(gross_merchandise_amount AS DECIMAL(18, 2))
        AS gross_merchandise_amount,

    CAST(discount_amount AS DECIMAL(18, 2))
        AS discount_amount,

    CAST(subtotal_amount AS DECIMAL(18, 2))
        AS subtotal_amount,

    CAST(shipping_amount AS DECIMAL(18, 2))
        AS shipping_amount,

    CAST(tax_amount AS DECIMAL(18, 2))
        AS tax_amount,

    CAST(order_total_amount AS DECIMAL(18, 2))
        AS order_total_amount

FROM raw_orders;
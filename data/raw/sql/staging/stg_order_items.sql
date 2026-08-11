-- ============================================================
-- Northstar Commerce
-- Model: stg_order_items
-- Purpose: Standardize raw order item transactions
-- ============================================================

SELECT
    order_item_id,
    order_id,
    product_id,

    LOWER(TRIM(product_category))
        AS product_category,

    CAST(quantity AS INTEGER)
        AS quantity,

    CAST(unit_price AS DECIMAL(18, 2))
        AS unit_price,

    CAST(line_gross_amount AS DECIMAL(18, 2))
        AS line_gross_amount,

    CAST(line_discount_amount AS DECIMAL(18, 2))
        AS line_discount_amount,

    CAST(line_net_amount AS DECIMAL(18, 2))
        AS line_net_amount

FROM raw_order_items;
-- ============================================================
-- Northstar Commerce
-- Model: fct_web_sessions
-- Grain: One row per web/app session
-- ============================================================

SELECT
    session_id,
    customer_id,

    CAST(session_start AS DATE)
        AS session_date,

    session_start,
    traffic_source,
    device_type,

    started_checkout,
    completed_purchase,
    order_id,

    CASE
        WHEN customer_id IS NOT NULL
        THEN 1
        ELSE 0
    END AS is_known_customer,

    CASE
        WHEN order_id IS NOT NULL
        THEN 1
        ELSE 0
    END AS has_linked_order

FROM stg_web_sessions;
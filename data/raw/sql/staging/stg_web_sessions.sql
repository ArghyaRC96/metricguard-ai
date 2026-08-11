-- ============================================================
-- Northstar Commerce
-- Model: stg_web_sessions
-- Purpose: Standardize web and mobile session activity
-- ============================================================

SELECT
    session_id,
    customer_id,

    CAST(session_start AS TIMESTAMP)
        AS session_start,

    LOWER(TRIM(traffic_source))
        AS traffic_source,

    LOWER(TRIM(device_type))
        AS device_type,

    CAST(started_checkout AS BOOLEAN)
        AS started_checkout,

    CAST(completed_purchase AS BOOLEAN)
        AS completed_purchase,

    order_id

FROM raw_web_sessions;
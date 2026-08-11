-- ============================================================
-- Northstar Commerce
-- Model: stg_customers
-- Purpose: Standardize raw customer records
-- ============================================================

SELECT
    customer_id,
    CAST(signup_date AS DATE) AS signup_date,
    LOWER(TRIM(region)) AS region,
    LOWER(TRIM(acquisition_channel)) AS acquisition_channel,
    LOWER(TRIM(customer_segment)) AS customer_segment,
    LOWER(TRIM(customer_status)) AS customer_status

FROM raw_customers;
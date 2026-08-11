-- ============================================================
-- Northstar Commerce
-- Mart: Operations Daily
-- Owner: Operations Analytics
-- Order Definition: Valid placed orders
-- ============================================================

SELECT
    order_date,

    COUNT(
        CASE
            WHEN order_status <> 'cancelled'
            THEN order_id
        END
    ) AS total_orders,

    COUNT(
        CASE
            WHEN order_status = 'completed'
            THEN order_id
        END
    ) AS completed_orders,

    COUNT(
        CASE
            WHEN order_status = 'shipped'
            THEN order_id
        END
    ) AS shipped_orders,

    COUNT(
        CASE
            WHEN order_status = 'returned'
            THEN order_id
        END
    ) AS returned_orders,

    COUNT(
        CASE
            WHEN order_status = 'pending'
            THEN order_id
        END
    ) AS pending_orders

FROM fct_orders

GROUP BY order_date;

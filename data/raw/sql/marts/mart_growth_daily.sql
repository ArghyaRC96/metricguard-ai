-- ============================================================
-- Northstar Commerce
-- Mart: Growth Daily
-- Owner: Growth Analytics
-- ============================================================

SELECT
    session_date,

    COUNT(*) AS total_sessions,

    COUNT(
        DISTINCT customer_id
    ) AS active_customers,

    SUM(
        CASE
            WHEN started_checkout = TRUE
            THEN 1
            ELSE 0
        END
    ) AS checkout_starts,

    SUM(
        CASE
            WHEN completed_purchase = TRUE
            THEN 1
            ELSE 0
        END
    ) AS completed_checkouts,

    CASE
        WHEN SUM(
            CASE
                WHEN started_checkout = TRUE
                THEN 1
                ELSE 0
            END
        ) = 0
        THEN 0

        ELSE
            1.0 * SUM(
                CASE
                    WHEN completed_purchase = TRUE
                    THEN 1
                    ELSE 0
                END
            )
            /
            SUM(
                CASE
                    WHEN started_checkout = TRUE
                    THEN 1
                    ELSE 0
                END
            )
    END AS conversion_rate

FROM fct_web_sessions

GROUP BY session_date;

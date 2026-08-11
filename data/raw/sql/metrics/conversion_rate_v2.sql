-- Metric: Conversion Rate
-- Version: v2
-- Status: Active

SELECT
    1.0 * SUM(
        CASE
            WHEN completed_purchase = TRUE
            THEN 1
            ELSE 0
        END
    )
    /
    NULLIF(
        SUM(
            CASE
                WHEN started_checkout = TRUE
                THEN 1
                ELSE 0
            END
        ),
        0
    ) AS conversion_rate

FROM fct_web_sessions;

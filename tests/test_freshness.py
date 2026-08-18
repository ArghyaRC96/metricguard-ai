from datetime import date

from metricguard.governance import (
    assess_freshness,
)


AS_OF_DATE = date(
    2026,
    8,
    15,
)


def test_fresh_asset():

    result = assess_freshness(
        "2026-06-10",
        as_of_date=AS_OF_DATE,
        warning_after_days=120,
        stale_after_days=180,
    )

    assert result.status == "fresh"


def test_warning_asset():

    result = assess_freshness(
        "2026-04-05",
        as_of_date=AS_OF_DATE,
        warning_after_days=120,
        stale_after_days=180,
    )

    assert result.status == "warning"


def test_stale_asset():

    result = assess_freshness(
        "2026-01-15",
        as_of_date=AS_OF_DATE,
        warning_after_days=120,
        stale_after_days=180,
    )

    assert result.status == "stale"


def test_unknown_freshness():

    result = assess_freshness(
        None,
        as_of_date=AS_OF_DATE,
        warning_after_days=120,
        stale_after_days=180,
    )

    assert result.status == "unknown"
    assert (
        result.days_since_review
        is None
    )
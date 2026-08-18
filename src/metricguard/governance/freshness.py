from datetime import date, datetime
from typing import Any

from metricguard.ingestion.models import ParsedDocument
from metricguard.metadata import build_document_metadata

from .models import FreshnessAssessment


def parse_date_value(
    value: Any,
) -> date | None:
    """Convert supported date values into datetime.date."""

    if value is None:
        return None

    if isinstance(value, datetime):
        return value.date()

    if isinstance(value, date):
        return value

    text = str(value).strip()

    if not text:
        return None

    return date.fromisoformat(text)


def assess_freshness(
    last_reviewed: Any,
    *,
    as_of_date: date,
    warning_after_days: int,
    stale_after_days: int,
) -> FreshnessAssessment:
    """Classify asset freshness from its last-reviewed date."""

    if warning_after_days >= stale_after_days:
        raise ValueError(
            "warning_after_days must be smaller "
            "than stale_after_days."
        )

    review_date = parse_date_value(
        last_reviewed
    )

    if review_date is None:

        return FreshnessAssessment(
            last_reviewed=None,
            as_of_date=str(as_of_date),
            days_since_review=None,
            status="unknown",
        )

    days_since_review = (
        as_of_date - review_date
    ).days

    if days_since_review < 0:

        status = "future_review_date"

    elif days_since_review >= stale_after_days:

        status = "stale"

    elif days_since_review >= warning_after_days:

        status = "warning"

    else:

        status = "fresh"

    return FreshnessAssessment(
        last_reviewed=str(review_date),
        as_of_date=str(as_of_date),
        days_since_review=days_since_review,
        status=status,
    )


def build_freshness_report(
    documents: list[ParsedDocument],
    *,
    as_of_date: date,
    warning_after_days: int,
    stale_after_days: int,
) -> list[dict[str, Any]]:
    """Build freshness assessments for assets with review dates."""

    report: list[dict[str, Any]] = []

    for document in documents:

        metadata = build_document_metadata(
            document
        )

        last_reviewed = metadata.get(
            "last_reviewed"
        )

        if last_reviewed is None:
            continue

        assessment = assess_freshness(
            last_reviewed,
            as_of_date=as_of_date,
            warning_after_days=
                warning_after_days,
            stale_after_days=
                stale_after_days,
        )

        report.append(
            {
                "asset_name":
                    metadata.get(
                        "dashboard_name"
                    )
                    or metadata.get(
                        "file_name"
                    ),
                "asset_type":
                    metadata.get(
                        "asset_type"
                    ),
                "source_path":
                    metadata.get(
                        "source_path"
                    ),
                **assessment.to_dict(),
            }
        )

    return report
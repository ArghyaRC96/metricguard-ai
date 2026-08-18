import json
from datetime import date
from pathlib import Path

import pandas as pd
import yaml

from metricguard.ingestion import (
    parse_knowledge_base,
)

from .freshness import (
    build_freshness_report,
)
from .versions import (
    build_dashboard_version_report,
    build_version_history,
    load_authoritative_metric_registry,
)


def load_freshness_settings(
    repo_root: Path,
) -> tuple[int, int]:
    """Load freshness thresholds from settings.yaml."""

    config_path = (
        repo_root
        / "configs"
        / "settings.yaml"
    )

    with config_path.open(
        "r",
        encoding="utf-8-sig",
    ) as file:
        config = yaml.safe_load(file)

    freshness = config["freshness"]

    return (
        int(
            freshness[
                "warning_after_days"
            ]
        ),
        int(
            freshness[
                "stale_after_days"
            ]
        ),
    )


def run_governance_analysis(
    repo_root: Path,
    *,
    as_of_date: date,
) -> None:
    """Run version and freshness intelligence."""

    raw_dir = (
        repo_root
        / "data"
        / "raw"
    )

    processed_dir = (
        repo_root
        / "data"
        / "processed"
    )

    processed_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    documents, parse_errors = (
        parse_knowledge_base(
            source_root=raw_dir,
            repo_root=repo_root,
        )
    )

    if parse_errors:
        raise RuntimeError(
            "Parsing errors detected "
            "before governance analysis."
        )

    registry = (
        load_authoritative_metric_registry(
            repo_root
        )
    )

    version_history = (
        build_version_history(
            documents
        )
    )

    dashboard_report = (
        build_dashboard_version_report(
            documents,
            registry,
        )
    )

    (
        warning_after_days,
        stale_after_days,
    ) = load_freshness_settings(
        repo_root
    )

    freshness_report = (
        build_freshness_report(
            documents,
            as_of_date=as_of_date,
            warning_after_days=
                warning_after_days,
            stale_after_days=
                stale_after_days,
        )
    )

    with (
        processed_dir
        / "metric_registry.json"
    ).open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            registry,
            file,
            indent=2,
            ensure_ascii=False,
            default=str,
        )

    pd.DataFrame(
        version_history
    ).to_csv(
        processed_dir
        / "metric_version_history.csv",
        index=False,
    )

    pd.DataFrame(
        dashboard_report
    ).to_csv(
        processed_dir
        / "dashboard_version_report.csv",
        index=False,
    )

    pd.DataFrame(
        freshness_report
    ).to_csv(
        processed_dir
        / "freshness_report.csv",
        index=False,
    )

    print("=" * 65)
    print(
        "METRICGUARD GOVERNANCE REPORT"
    )
    print("=" * 65)

    print(
        f"Authoritative metrics : "
        f"{len(registry)}"
    )

    print(
        f"Historical versions   : "
        f"{len(version_history)}"
    )

    print(
        f"Dashboard assessments : "
        f"{len(dashboard_report)}"
    )

    print(
        f"Freshness assessments : "
        f"{len(freshness_report)}"
    )

    print(
        f"As-of date            : "
        f"{as_of_date}"
    )

    print(
        "Ground truth          : excluded"
    )


if __name__ == "__main__":

    repository_root = Path.cwd()

    run_governance_analysis(
        repository_root,
        as_of_date=date.today(),
    )
import json
from pathlib import Path
from typing import Any

import pandas as pd
import yaml


SOURCE_TYPE_MAP = {
    ".sql": "sql",
    ".md": "markdown",
    ".json": "json",
    ".yml": "yaml",
    ".yaml": "yaml",
    ".csv": "csv",
}


def get_source_type(path: Path) -> str:
    """Return the normalized MetricGuard source type."""

    extension = path.suffix.lower()

    if extension not in SOURCE_TYPE_MAP:
        raise ValueError(f"Unsupported file type: {extension}")

    return SOURCE_TYPE_MAP[extension]


def parse_text_file(path: Path) -> tuple[str, None]:
    """Parse UTF-8 SQL or Markdown as plain text."""

    content = path.read_text(encoding="utf-8-sig")

    return content, None


def parse_json_file(path: Path) -> tuple[str, Any]:
    """Parse JSON and return normalized text plus structured data."""

    with path.open("r", encoding="utf-8-sig") as file:
        data = json.load(file)

    content = json.dumps(
        data,
        indent=2,
        ensure_ascii=False,
    )

    return content, data


def parse_yaml_file(path: Path) -> tuple[str, Any]:
    """Safely parse YAML and return normalized text plus structure."""

    with path.open("r", encoding="utf-8-sig") as file:
        data = yaml.safe_load(file)

    content = yaml.safe_dump(
        data,
        sort_keys=False,
        allow_unicode=True,
    )

    return content, data


def parse_csv_summary(path: Path) -> tuple[str, dict[str, Any]]:
    """Create a dataset-level RAG summary instead of row-level documents."""

    dataframe = pd.read_csv(path)

    metadata = {
        "row_count": len(dataframe),
        "column_count": len(dataframe.columns),
        "columns": list(dataframe.columns),
        "dtypes": {
            column: str(dtype)
            for column, dtype in dataframe.dtypes.items()
        },
        "null_counts": {
            column: int(count)
            for column, count in dataframe.isna().sum().items()
        },
    }

    sample_rows = (
        dataframe.head(3)
        .fillna("")
        .to_dict(orient="records")
    )

    content = (
        f"Dataset: {path.stem}\n"
        f"Rows: {len(dataframe)}\n"
        f"Columns: {len(dataframe.columns)}\n"
        f"Column names: {', '.join(dataframe.columns)}\n\n"
        f"Sample rows:\n"
        f"{json.dumps(sample_rows, indent=2, default=str)}"
    )

    return content, metadata


def parse_file(path: Path) -> tuple[str, Any | None]:
    """Dispatch a file to the correct parser."""

    extension = path.suffix.lower()

    if extension in {".sql", ".md"}:
        return parse_text_file(path)

    if extension == ".json":
        return parse_json_file(path)

    if extension in {".yml", ".yaml"}:
        return parse_yaml_file(path)

    if extension == ".csv":
        return parse_csv_summary(path)

    raise ValueError(f"Unsupported file type: {extension}")

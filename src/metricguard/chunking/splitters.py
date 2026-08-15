import json
from typing import Any

from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

from metricguard.ingestion.models import ParsedDocument


def create_recursive_splitter(
    chunk_size: int,
    chunk_overlap: int,
) -> RecursiveCharacterTextSplitter:
    """Create the generic fallback text splitter."""

    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )


def create_sql_splitter(
    chunk_size: int,
    chunk_overlap: int,
) -> RecursiveCharacterTextSplitter:
    """Create a recursive splitter with SQL-friendly boundaries."""

    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",
            "\nWITH ",
            "\nSELECT ",
            "\nFROM ",
            "\nLEFT JOIN ",
            "\nINNER JOIN ",
            "\nJOIN ",
            "\nWHERE ",
            "\nGROUP BY ",
            "\nORDER BY ",
            "\nHAVING ",
            "\n",
            " ",
            "",
        ],
    )


def create_markdown_splitter() -> MarkdownHeaderTextSplitter:
    """Create the heading-aware Markdown splitter."""

    return MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "header_1"),
            ("##", "header_2"),
            ("###", "header_3"),
        ],
        strip_headers=False,
    )


def split_if_needed(
    text: str,
    *,
    chunk_size: int,
    chunk_overlap: int,
) -> list[str]:
    """Preserve compact logical sections and split oversized ones."""

    text = text.strip()

    if not text:
        return []

    if len(text) <= chunk_size:
        return [text]

    splitter = create_recursive_splitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    return splitter.split_text(text)


def chunk_markdown(
    content: str,
    *,
    chunk_size: int,
    chunk_overlap: int,
) -> list[dict[str, Any]]:
    """Split Markdown by heading before recursive fallback."""

    splitter = create_markdown_splitter()

    sections = splitter.split_text(content)

    chunks: list[dict[str, Any]] = []

    for section in sections:

        for text in split_if_needed(
            section.page_content,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        ):

            chunks.append(
                {
                    "content": text,
                    "section_metadata": dict(
                        section.metadata
                    ),
                }
            )

    return chunks


def chunk_sql(
    content: str,
    *,
    chunk_size: int,
    chunk_overlap: int,
) -> list[dict[str, Any]]:
    """Split SQL while preferring SQL clause boundaries."""

    content = content.strip()

    if not content:
        return []

    if len(content) <= chunk_size:

        return [
            {
                "content": content,
                "section_metadata": {},
            }
        ]

    splitter = create_sql_splitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    return [
        {
            "content": text,
            "section_metadata": {},
        }
        for text in splitter.split_text(content)
    ]


def chunk_structured_data(
    structured_data: Any,
    original_content: str,
    *,
    chunk_size: int,
    chunk_overlap: int,
) -> list[dict[str, Any]]:
    """Create structure-aware chunks for JSON and YAML."""

    if structured_data is None:

        return [
            {
                "content": text,
                "section_metadata": {},
            }
            for text in split_if_needed(
                original_content,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )
        ]

    chunks: list[dict[str, Any]] = []

    if isinstance(structured_data, dict):

        for key, value in structured_data.items():

            if isinstance(value, list):

                for index, item in enumerate(value):

                    serialized = json.dumps(
                        {key: item},
                        indent=2,
                        ensure_ascii=False,
                        default=str,
                    )

                    for text in split_if_needed(
                        serialized,
                        chunk_size=chunk_size,
                        chunk_overlap=chunk_overlap,
                    ):

                        chunks.append(
                            {
                                "content": text,
                                "section_metadata": {
                                    "structure_key": key,
                                    "structure_index": index,
                                },
                            }
                        )

            else:

                serialized = json.dumps(
                    {key: value},
                    indent=2,
                    ensure_ascii=False,
                    default=str,
                )

                for text in split_if_needed(
                    serialized,
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap,
                ):

                    chunks.append(
                        {
                            "content": text,
                            "section_metadata": {
                                "structure_key": key,
                            },
                        }
                    )

    else:

        for text in split_if_needed(
            original_content,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        ):

            chunks.append(
                {
                    "content": text,
                    "section_metadata": {},
                }
            )

    return chunks


def chunk_csv(
    content: str,
    *,
    chunk_size: int,
    chunk_overlap: int,
) -> list[dict[str, Any]]:
    """Split the compact dataset summary created during ingestion."""

    return [
        {
            "content": text,
            "section_metadata": {},
        }
        for text in split_if_needed(
            content,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
    ]


def chunk_document(
    document: ParsedDocument,
    *,
    chunk_size: int,
    chunk_overlap: int,
) -> list[dict[str, Any]]:
    """Dispatch a parsed document to its source-aware chunker."""

    if document.source_type == "markdown":

        return chunk_markdown(
            document.content,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    if document.source_type == "sql":

        return chunk_sql(
            document.content,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    if document.source_type in {
        "json",
        "yaml",
    }:

        return chunk_structured_data(
            document.structured_data,
            document.content,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    if document.source_type == "csv":

        return chunk_csv(
            document.content,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    raise ValueError(
        f"Unsupported source type: "
        f"{document.source_type}"
    )
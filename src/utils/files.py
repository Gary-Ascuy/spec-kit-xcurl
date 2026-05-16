"""File I/O utilities module."""

from __future__ import annotations

import json
from pathlib import Path

from src.models.config import QuerySource, VariablesSource


def read_query_file(path: str | Path) -> QuerySource:
    """Read a GraphQL query from a file.

    Args:
        path: Path to the query file

    Returns:
        QuerySource with file content
    """
    path_obj = Path(path)
    return QuerySource.from_file(path_obj)


def read_variables_file(path: str | Path) -> VariablesSource:
    """Read variables from a JSON file.

    Args:
        path: Path to the variables file

    Returns:
        VariablesSource with file content
    """
    path_obj = Path(path)
    return VariablesSource(file_path=path_obj)


def read_headers_file(path: str | Path) -> dict[str, str]:
    """Read HTTP headers from a file.

    Args:
        path: Path to the headers file (one per line, format: "Name: value")

    Returns:
        Dictionary of headers
    """
    headers: dict[str, str] = {}
    path_obj = Path(path)

    for line in path_obj.read_text().strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            name, value = line.split(":", 1)
            headers[name.strip()] = value.strip()

    return headers

"""Response processor module."""

from __future__ import annotations

import json
from typing import Any

from rich.console import Console
from rich.syntax import Syntax

from src.models.config import OutputFormat
from src.models.graphql import GraphQLResponse

console = Console()


def format_response(
    response: GraphQLResponse,
    output_format: OutputFormat = OutputFormat.PRETTY,
) -> str:
    """Format a GraphQL response for output.

    Args:
        response: GraphQL response to format
        output_format: Desired output format

    Returns:
        Formatted response as string
    """
    if output_format == OutputFormat.JSON:
        return _format_json(response)
    elif output_format == OutputFormat.PRETTY:
        return _format_pretty(response)
    elif output_format == OutputFormat.RAW:
        return _format_raw(response)
    elif output_format == OutputFormat.COLOR:
        return _format_color(response)
    else:
        return _format_pretty(response)


def _format_json(response: GraphQLResponse) -> str:
    """Format as raw JSON."""
    return response.model_dump_json()


def _format_pretty(response: GraphQLResponse) -> str:
    """Format as pretty-printed JSON."""
    return json.dumps(
        response.model_dump(),
        indent=2,
        ensure_ascii=False,
    )


def _format_raw(response: GraphQLResponse) -> str:
    """Format as raw data only (no errors/extensions)."""
    if response.data is not None:
        return json.dumps(response.data, ensure_ascii=False)
    return ""


def _format_color(response: GraphQLResponse) -> str:
    """Format with syntax highlighting."""
    json_str = _format_pretty(response)
    syntax = Syntax(json_str, "json", theme="monokai", line_numbers=False)
    with console.capture() as capture:
        console.print(syntax)
    return capture.get().strip()

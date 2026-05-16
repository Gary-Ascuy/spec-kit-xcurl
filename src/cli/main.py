"""Click CLI entry point for xcurl."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import click
from rich.console import Console

from src.models.config import (
    CLIConfig,
    HttpHeaders,
    OutputFormat,
    QuerySource,
    VariablesSource,
)
from src.core.executor import execute
from src.core.request import build_request
from src.core.response import format_response
from src.utils.files import read_headers_file, read_query_file, read_variables_file

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def main() -> None:
    """xcurl - A CLI tool for GraphQL queries."""
    pass


@main.command()
@click.argument("endpoint")
@click.option("-q", "--query", help="Inline GraphQL query")
@click.option("-f", "--file", type=click.Path(exists=True), help="Query file")
@click.option("-v", "--variables", help="Variables as JSON string")
@click.option("-V", "--variables-file", type=click.Path(exists=True), help="Variables file")
@click.option(
    "-F",
    "--format",
    type=click.Choice(["json", "pretty", "raw", "color"]),
    default="pretty",
    help="Output format",
)
@click.option("-o", "--output", type=click.Path(), help="Write output to file")
@click.option("-H", "--header", multiple=True, help="Custom header (format: 'Name: value')")
@click.option("--headers-file", type=click.Path(exists=True), help="Headers file")
@click.option("-B", "--bearer", help="Bearer token for authentication")
@click.option("-t", "--timeout", default=30, help="Request timeout in seconds")
@click.option("--verbose", is_flag=True, help="Enable verbose output")
@click.option("--debug", is_flag=True, help="Enable debug mode")
def query(
    endpoint: str,
    query: str | None,
    file: str | None,
    variables: str | None,
    variables_file: str | None,
    format: str,  # noqa: A002
    output: str | None,
    header: tuple[str, ...],
    headers_file: str | None,
    bearer: str | None,
    timeout: int,
    verbose: bool,
    debug: bool,
) -> None:
    """Execute a GraphQL query.

    Examples:

        xcurl query https://api.example.com/graphql -q "{ user { id name } }"

        xcurl query https://api.example.com/graphql -f query.gql -v '{"id": "1"}'
    """
    import asyncio

    # Validate inputs
    if query is None and file is None:
        console.print("[error]Error:[/error] No query provided. Use --query or --file.")
        sys.exit(2)

    # Get query source
    if file is not None:
        query_source = read_query_file(file)
    else:
        query_source = QuerySource.from_inline(query or "")

    # Get variables
    variables_dict: dict[str, Any] | None = None
    if variables is not None:
        variables_dict = json.loads(variables)
    elif variables_file is not None:
        var_source = read_variables_file(variables_file)
        variables_dict = var_source.get_variables()

    # Build headers
    headers_dict: dict[str, str] = {}
    for h in header:
        if ":" in h:
            name, value = h.split(":", 1)
            headers_dict[name.strip()] = value.strip()

    if headers_file is not None:
        headers_dict.update(read_headers_file(headers_file))

    http_headers = HttpHeaders(headers=headers_dict, auth_token=bearer)

    # Build request
    variables_source = (
        VariablesSource(variables=variables_dict) if variables_dict else None
    )
    request = build_request(query_source, variables_source, http_headers)

    # Execute request
    try:
        response = asyncio.run(
            execute(endpoint, request, http_headers, timeout)
        )
    except Exception as e:
        console.print(f"[error]Error:[/error] {e}")
        sys.exit(7)

    # Format output
    output_format = OutputFormat(format)
    formatted = format_response(response, output_format)

    # Write output
    if output is not None:
        Path(output).write_text(formatted)
    else:
        console.print(formatted)

    # Handle exit codes
    if response.has_errors:
        sys.exit(8)


main.add_command(query)

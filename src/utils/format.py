"""Output formatting utilities module."""

from __future__ import annotations

import json
from typing import Any

from rich.console import Console
from rich.syntax import Syntax

console = Console()


def format_json(data: dict[str, Any]) -> str:
    """Format data as JSON string.

    Args:
        data: Data to format

    Returns:
        JSON string
    """
    return json.dumps(data, ensure_ascii=False)


def format_pretty(data: dict[str, Any]) -> str:
    """Format data as pretty-printed JSON.

    Args:
        data: Data to format

    Returns:
        Pretty-printed JSON string
    """
    return json.dumps(data, indent=2, ensure_ascii=False)


def format_raw(data: dict[str, Any]) -> str:
    """Format data as raw string (no formatting).

    Args:
        data: Data to format

    Returns:
        Raw JSON string
    """
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def format_color(data: dict[str, Any]) -> str:
    """Format data with syntax highlighting.

    Args:
        data: Data to format

    Returns:
        Colorized JSON string
    """
    json_str = format_pretty(data)
    syntax = Syntax(json_str, "json", theme="monokai", line_numbers=False)
    with console.capture() as capture:
        console.print(syntax)
    return capture.get().strip()

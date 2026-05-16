"""Configuration models for xcurl."""

from __future__ import annotations

from collections.abc import Mapping
from enum import Enum
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, Field


class OutputFormat(str, Enum):
    """Output format options."""

    JSON = "json"
    PRETTY = "pretty"
    RAW = "raw"
    COLOR = "color"


class HttpHeaders(BaseModel):
    """HTTP headers for GraphQL requests."""

    headers: dict[str, str] = Field(
        default_factory=dict,
        description="HTTP headers (case-insensitive keys)"
    )
    auth_token: Optional[str] = Field(
        default=None,
        description="Bearer token for authentication"
    )

    model_config = {"frozen": True, "validate_assignment": True}

    def get_headers(self) -> dict[str, str]:
        """Get all headers including auth."""
        # Create a mutable copy since model is frozen
        result = dict(self.headers)
        if self.auth_token is not None:
            result["Authorization"] = f"Bearer {self.auth_token}"
        # Ensure content-type is set
        if "content-type" not in {k.lower() for k in result.keys()}:
            result["Content-Type"] = "application/json"
        return result


class QuerySource(BaseModel):
    """Source of a GraphQL query."""

    kind: str
    content: str
    path: Optional[Path] = Field(
        default=None,
        description="File path if kind is FILE"
    )

    @classmethod
    def from_inline(cls, query: str) -> QuerySource:
        """Create from inline query string."""
        return cls(kind="inline", content=query)

    @classmethod
    def from_file(cls, path: Path) -> QuerySource:
        """Create from file path."""
        content = path.read_text()
        return cls(kind="file", content=content, path=path)

    @classmethod
    def from_stdin(cls) -> QuerySource:
        """Create from standard input."""
        import sys

        content = sys.stdin.read()
        return cls(kind="stdin", content=content)


class VariablesSource(BaseModel):
    """Source of GraphQL variables."""

    variables: Optional[dict[str, Any]] = Field(
        default=None,
        description="Variables from inline JSON"
    )
    file_path: Optional[Path] = Field(
        default=None,
        description="Path to variables JSON file"
    )

    def get_variables(self) -> Optional[dict[str, Any]]:
        """Get variables from source."""
        if self.file_path is not None:
            import json

            content = self.file_path.read_text()
            return json.loads(content)
        return self.variables


class CLIConfig(BaseModel):
    """CLI configuration."""

    endpoint: str = Field(description="GraphQL endpoint URL")
    headers: HttpHeaders = Field(
        default_factory=HttpHeaders,
        description="HTTP headers"
    )
    output_format: OutputFormat = Field(
        default=OutputFormat.PRETTY,
        description="Output format"
    )
    timeout: int = Field(
        default=30,
        ge=1,
        le=300,
        description="Request timeout in seconds"
    )
    verbose: bool = Field(
        default=False,
        description="Enable verbose output"
    )
    validate_query: bool = Field(
        default=False,
        description="Validate query before sending"
    )

# Data Model: GraphQL CLI Tool

**Feature**: 001-001-graphql-cli
**Date**: 2026-05-16

## Overview

This document defines the core data entities for the GraphQL CLI tool. All entities use Pydantic for runtime validation and type safety.

## Core Entities

### GraphQLRequest

Represents a complete GraphQL request with query, variables, and operation name.

```python
from pydantic import BaseModel, Field
from typing import Any

class GraphQLRequest(BaseModel):
    """A GraphQL request with query, variables, and operation name."""

    query: str = Field(
        description="The GraphQL query or mutation string",
        min_length=1
    )
    variables: dict[str, Any] | None = Field(
        default=None,
        description="Variables for the GraphQL query"
    )
    operation_name: str | None = Field(
        default=None,
        description="Name of the operation (for multiple operations in one query)"
    )

    def to_http_body(self) -> dict[str, Any]:
        """Convert to HTTP request body."""
        body: dict[str, Any] = {"query": self.query}
        if self.variables:
            body["variables"] = self.variables
        if self.operation_name:
            body["operationName"] = self.operation_name
        return body
```

**Validation Rules**:
- `query` must be non-empty string
- `variables` must be a JSON object if provided
- `operation_name` must be valid GraphQL identifier if provided

### GraphQLResponse

Represents the response from a GraphQL server.

```python
class GraphQLErrorLocation(BaseModel):
    """Location of an error in the GraphQL query."""

    line: int = Field(ge=1, description="Line number (1-indexed)")
    column: int = Field(ge=1, description="Column number (1-indexed)")

class GraphQLError(BaseModel):
    """A GraphQL error returned by the server."""

    message: str = Field(description="Human-readable error message")
    locations: list[GraphQLErrorLocation] | None = Field(
        default=None,
        description="Error locations in the query"
    )
    path: list[str | int] | None = Field(
        default=None,
        description="Path to the field causing the error"
    )
    extensions: dict[str, Any] | None = Field(
        default=None,
        description="Additional error extensions"
    )

class GraphQLResponse(BaseModel):
    """Response from a GraphQL server."""

    data: dict[str, Any] | None = Field(
        default=None,
        description="Query result data"
    )
    errors: list[GraphQLError] | None = Field(
        default=None,
        description="GraphQL errors"
    )
    extensions: dict[str, Any] | None = Field(
        default=None,
        description="Response extensions"
    )

    @property
    def has_errors(self) -> bool:
        """Check if response contains errors."""
        return self.errors is not None and len(self.errors) > 0

    @property
    def is_successful(self) -> bool:
        """Check if response was successful."""
        return not self.has_errors and self.data is not None
```

**Validation Rules**:
- At least one of `data` or `errors` must be present
- `errors` list must be non-empty if present
- `locations` in errors must have positive line/column values

### HttpHeaders

Represents HTTP headers for the request.

```python
class HttpHeaders(BaseModel):
    """HTTP headers for GraphQL requests."""

    headers: dict[str, str] = Field(
        default_factory=dict,
        description="HTTP headers (case-insensitive keys)"
    )
    auth_token: str | None = Field(
        default=None,
        description="Bearer token for authentication"
    )

    def get_headers(self) -> dict[str, str]:
        """Get all headers including auth."""
        result = self.headers.copy()
        if self.auth_token:
            result["Authorization"] = f"Bearer {self.auth_token}"
        # Ensure content-type is set
        if "content-type" not in {k.lower() for k in result.keys()}:
            result["Content-Type"] = "application/json"
        return result

    class Config:
        """Pydantic config."""
        # Allow case-insensitive header access
        frozen = True
```

**Validation Rules**:
- Header names are case-insensitive (HTTP standard)
- `auth_token` is shorthand for Authorization header
- Content-Type defaults to application/json

### QuerySource

Represents where the GraphQL query comes from.

```python
from enum import Enum
from pathlib import Path

class QuerySourceKind(Enum):
    """Type of query source."""
    INLINE = "inline"
    FILE = "file"
    STDIN = "stdin"

class QuerySource(BaseModel):
    """Source of a GraphQL query."""

    kind: QuerySourceKind
    content: str
    path: Path | None = Field(
        default=None,
        description="File path if kind is FILE"
    )

    @classmethod
    def from_inline(cls, query: str) -> "QuerySource":
        """Create from inline query string."""
        return cls(kind=QuerySourceKind.INLINE, content=query)

    @classmethod
    def from_file(cls, path: Path) -> "QuerySource":
        """Create from file path."""
        content = path.read_text()
        return cls(kind=QuerySourceKind.FILE, content=content, path=path)

    @classmethod
    def from_stdin(cls) -> "QuerySource":
        """Create from standard input."""
        import sys
        content = sys.stdin.read()
        return cls(kind=QuerySourceKind.STDIN, content=content)
```

**Validation Rules**:
- `content` must be non-empty
- `path` must exist if kind is FILE
- STDIN reads until EOF

### VariablesSource

Represents where variables come from.

```python
class VariablesSource(BaseModel):
    """Source of GraphQL variables."""

    variables: dict[str, Any] | None = Field(
        default=None,
        description="Variables from inline JSON"
    )
    file_path: Path | None = Field(
        default=None,
        description="Path to variables JSON file"
    )

    def get_variables(self) -> dict[str, Any] | None:
        """Get variables from source."""
        if self.file_path:
            import json
            content = self.file_path.read_text()
            return json.loads(content)
        return self.variables
```

**Validation Rules**:
- `file_path` must exist and contain valid JSON if provided
- `variables` must be valid JSON object (dict) if provided

### CLIConfig

Configuration for CLI behavior.

```python
class OutputFormat(Enum):
    """Output format options."""
    JSON = "json"
    PRETTY = "pretty"
    RAW = "raw"
    COLOR = "color"

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
```

**Validation Rules**:
- `endpoint` must be valid HTTP/HTTPS URL
- `timeout` must be between 1 and 300 seconds
- `output_format` must be one of the enum values

## State Machine

### Request Execution State

```text
IDLE → VALIDATING → EXECUTING → COMPLETE
           ↓            ↓
         ERROR        ERROR
```

**States**:
1. **IDLE**: Initial state, before any processing
2. **VALIDATING**: Query is being validated (if enabled)
3. **EXECUTING**: HTTP request is in flight
4. **COMPLETE**: Request finished successfully
5. **ERROR**: An error occurred at any stage

**Transitions**:
- IDLE → VALIDATING: When query is provided and validate_query is True
- IDLE → EXECUTING: When query is provided and validate_query is False
- VALIDATING → EXECUTING: When query passes validation
- VALIDATING → ERROR: When query fails validation
- EXECUTING → COMPLETE: When HTTP request succeeds
- EXECUTING → ERROR: When HTTP request fails or returns errors

## Relationships

```
GraphQLRequest
    ├── QuerySource (where query comes from)
    ├── VariablesSource (where variables come from)
    └── HttpHeaders (headers for request)
        ↓ (executes via HTTP)
GraphQLResponse
    ├── data (result)
    └── errors (any errors)

CLIConfig
    ├── endpoint
    ├── HttpHeaders
    └── OutputFormat
```

## Type Aliases

```python
from typing import TypeAlias

# JSON types
JsonValue: TypeAlias = str | int | float | bool | None | dict[str, Any] | list[Any]
JsonObject: TypeAlias = dict[str, JsonValue]

# HTTP types
Headers: TypeAlias = dict[str, str]

# Result types
Result: TypeAlias = tuple[GraphQLResponse, int]  # Response + HTTP status code
```

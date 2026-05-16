# Research: GraphQL CLI Tool

**Feature**: 001-001-graphql-cli
**Date**: 2026-05-16

## Overview

This document consolidates research findings for building a GraphQL CLI tool similar to curl but specialized for GraphQL queries and mutations.

## Technology Decisions

### HTTP Client Library: httpx

**Decision**: Use `httpx` for HTTP requests

**Rationale**:
- Modern HTTP client with async/await support
- Excellent type hints for mypy --strict compliance
- HTTP/2 and WebSocket support (future-proofing)
- Active maintenance and good documentation
- Requests API compatibility (easy migration)

**Alternatives Considered**:
- `requests`: In maintenance mode, no native async support
- `aiohttp`: More complex API, focused on async only
- `urllib`: Standard library but verbose, less ergonomic

**Code Example**:
```python
import httpx

async def execute_query(url: str, query: str, variables: dict | None = None) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            json={"query": query, "variables": variables},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()
```

### CLI Framework: click + rich

**Decision**: Use `click` for CLI structure, `rich` for output formatting

**Rationale**:
- Click: Mature, composable, excellent for subcommands, strong typing
- Rich: Beautiful terminal output, syntax highlighting, progress bars
- Both have excellent mypy support
- Large ecosystem of extensions

**Alternatives Considered**:
- `typer`: Simpler but less flexible for complex CLIs
- `argparse`: Standard library but verbose, less intuitive
- `cliff`: Opinionated, more complex setup

**Code Example**:
```python
import click
from rich.console import Console
from rich.syntax import Syntax

console = Console()

@click.command()
@click.argument("endpoint")
@click.option("-q", "--query", help="GraphQL query")
@click.option("-f", "--file", type=click.Path(exists=True), help="Query file")
def graphql(endpoint: str, query: str | None, file: str | None) -> None:
    """Execute GraphQL queries like curl."""
    if file:
        query = Path(file).read_text()
    # Execute and print with rich formatting
    console.print_json(result)
```

### Validation Library: pydantic

**Decision**: Use `pydantic` v3 for request/response validation

**Rationale**:
- Runtime type checking with Python type hints
- JSON schema generation for documentation
- Excellent mypy support (strict mode compatible)
- Minimal boilerplate compared to dataclasses
- Built-in validation primitives

**Alternatives Considered**:
- `msgspec`: Faster but less mature, fewer features
- `dataclasses`: Standard library but no validation
- `attrs`: Third-party but no runtime validation

**Code Example**:
```python
from pydantic import BaseModel, Field
from typing import Any

class GraphQLRequest(BaseModel):
    query: str
    variables: dict[str, Any] | None = None
    operation_name: str | None = None

class GraphQLError(BaseModel):
    message: str
    path: list[str | int] | None = None
    extensions: dict[str, Any] | None = None

class GraphQLResponse(BaseModel):
    data: dict[str, Any] | None = None
    errors: list[GraphQLError] | None = None
```

### Mutation Testing: mutmut

**Decision**: Use `mutmut` for mutation testing

**Rationale**:
- Designed for Python pytest workflow
- Good mutation operators (arithmetic, boolean, conditional, etc.)
- Clear HTML reporting
- Easy CI integration

**Alternatives Considered**:
- `mutpy`: Older, less active development
- `cosmic-ray`: More complex setup, Python 2 legacy

**Usage**:
```bash
mutmut run --paths-to-mutate src/
mutmut results-html
```

### GraphQL Library: graphql-core

**Decision**: Use `graphql-core` v3 for query validation

**Rationale**:
- Official Python GraphQL implementation
- Full GraphQL spec compliance
- Query parsing and validation before execution
- Introspection query support
- Type schema introspection

**Alternatives Considered**:
- `libgraphqlparser`: C bindings, more complex setup
- Custom parsing: Error-prone, reinventing the wheel

**Code Example**:
```python
from graphql import parse, validate

def validate_query(query_str: str, schema: GraphQLSchema) -> list[GraphQLError]:
    """Validate a GraphQL query against a schema."""
    document = parse(query_str)
    return validate(schema, document)
```

## Architecture Patterns

### Layered Architecture

The tool will use a clean layered architecture:

1. **CLI Layer** (`src/cli/`): Click commands, argument parsing
2. **Core Layer** (`src/core/`): GraphQL request building, HTTP execution
3. **Model Layer** (`src/models/`): Pydantic models for type safety
4. **Utils Layer** (`src/utils/`): File I/O, formatting helpers

**Benefits**:
- Clear separation of concerns
- Easy testing (mock at layer boundaries)
- Dependency inversion (core doesn't depend on CLI)
- Each layer can be tested independently

### Type Safety Strategy

All functions use strict type hints:
- `str` for strings, not `str | None` unless optional
- `dict[str, Any]` for JSON objects (with specific types where possible)
- `Protocol` for interface definitions
- `TypeAlias` for complex types

```python
from typing import TypeAlias

# Type aliases for clarity
Headers: TypeAlias = dict[str, str]
JsonValue: TypeAlias = str | int | float | bool | None | dict[str, Any] | list[Any]
JsonObject: TypeAlias = dict[str, JsonValue]
```

## Performance Considerations

1. **Async HTTP**: Use httpx async for concurrent requests
2. **Lazy Parsing**: Only parse GraphQL queries if validation requested
3. **Streaming**: Stream large responses to file instead of buffering
4. **Connection Pooling**: Reuse HTTP connections for multiple requests

## Security Considerations

1. **Token Handling**: Never log authentication tokens
2. **Input Validation**: Validate queries before sending (prevent injection)
3. **Error Messages**: Sanitize error messages (don't leak sensitive data)
4. **File Access**: Only read from specified paths (no path traversal)

## References

- [GraphQL over HTTP specification](https://graphql.github.io/graphql-over-http/draft/)
- [Click documentation](https://click.palletsprojects.com/)
- [httpx documentation](https://www.python-httpx.org/)
- [pydantic documentation](https://docs.pydantic.dev/)

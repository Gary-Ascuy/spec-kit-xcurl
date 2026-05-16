"""Integration tests for query execution."""

import asyncio
from typing import Any

import pytest
from httpx import Response

from src.core.executor import execute
from src.models.config import QuerySource, VariablesSource
from src.models.graphql import GraphQLRequest


@pytest.mark.asyncio
async def test_inline_query_execution() -> None:
    """Test executing an inline query against a mock server."""
    # This test would use a mock HTTP server
    # For now, we'll test with a real public API
    pytest.skip("Requires mock server - implementation pending")


@pytest.mark.asyncio
async def test_query_with_variables() -> None:
    """Test executing a query with variables."""
    pytest.skip("Requires mock server - implementation pending")


@pytest.mark.asyncio
async def test_query_file_execution(tmp_path: Any) -> None:
    """Test executing a query from a file."""
    # Create a test query file
    query_file = tmp_path / "test_query.gql"
    query_file.write_text("{ user { id } }")

    query_source = QuerySource.from_file(query_file)
    assert query_source.content == "{ user { id } }"


@pytest.mark.asyncio
async def test_variables_from_file(tmp_path: Any) -> None:
    """Test loading variables from a file."""
    import json

    vars_file = tmp_path / "variables.json"
    vars_file.write_text('{"id": "123"}')

    var_source = VariablesSource(file_path=vars_file)
    assert var_source.get_variables() == {"id": "123"}


def test_request_builder_integration() -> None:
    """Test the request builder with query and variables."""
    from src.core.request import build_request

    query_source = QuerySource.from_inline("{ user(id: $id) { name } }")
    variables_source = VariablesSource(variables={"id": "1"})

    request = build_request(query_source, variables_source)

    assert request.query == "{ user(id: $id) { name } }"
    assert request.variables == {"id": "1"}

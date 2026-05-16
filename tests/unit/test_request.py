"""Unit tests for GraphQLRequest model."""

import pytest
from pydantic import ValidationError


def test_graphql_request_creation() -> None:
    """Test GraphQLRequest can be created with query."""
    from src.models.graphql import GraphQLRequest

    request = GraphQLRequest(query="{ user { id } }")
    assert request.query == "{ user { id } }"
    assert request.variables is None
    assert request.operation_name is None


def test_graphql_request_with_variables() -> None:
    """Test GraphQLRequest with variables."""
    from src.models.graphql import GraphQLRequest

    request = GraphQLRequest(
        query="query GetUser($id: ID!) { user(id: $id) { name } }",
        variables={"id": "1"}
    )
    assert request.variables == {"id": "1"}


def test_graphql_request_with_operation_name() -> None:
    """Test GraphQLRequest with operation name."""
    from src.models.graphql import GraphQLRequest

    request = GraphQLRequest(
        query="query GetUser { user { name } } mutation AddUser { addUser { name } }",
        operation_name="GetUser"
    )
    assert request.operation_name == "GetUser"


def test_graphql_request_query_cannot_be_empty() -> None:
    """Test GraphQLRequest requires non-empty query."""
    from src.models.graphql import GraphQLRequest

    with pytest.raises(ValidationError):
        GraphQLRequest(query="")


def test_graphql_request_to_http_body() -> None:
    """Test to_http_body() creates correct HTTP body."""
    from src.models.graphql import GraphQLRequest

    request = GraphQLRequest(query="{ user { id } }")
    body = request.to_http_body()

    assert body == {"query": "{ user { id } }"}


def test_graphql_request_to_http_body_with_variables() -> None:
    """Test to_http_body() includes variables."""
    from src.models.graphql import GraphQLRequest

    request = GraphQLRequest(
        query="query GetUser($id: ID!) { user(id: $id) { name } }",
        variables={"id": "1"}
    )
    body = request.to_http_body()

    assert body == {
        "query": "query GetUser($id: ID!) { user(id: $id) { name } }",
        "variables": {"id": "1"}
    }


def test_graphql_request_to_http_body_with_operation_name() -> None:
    """Test to_http_body() includes operation name."""
    from src.models.graphql import GraphQLRequest

    request = GraphQLRequest(
        query="query GetUser { user { name } }",
        operation_name="GetUser"
    )
    body = request.to_http_body()

    assert body == {
        "query": "query GetUser { user { name } }",
        "operationName": "GetUser"
    }


def test_graphql_request_to_http_body_complete() -> None:
    """Test to_http_body() with all fields."""
    from src.models.graphql import GraphQLRequest

    request = GraphQLRequest(
        query="query GetUser($id: ID!) { user(id: $id) { name } }",
        variables={"id": "1"},
        operation_name="GetUser"
    )
    body = request.to_http_body()

    assert body == {
        "query": "query GetUser($id: ID!) { user(id: $id) { name } }",
        "variables": {"id": "1"},
        "operationName": "GetUser"
    }

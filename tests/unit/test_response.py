"""Unit tests for GraphQLResponse model."""

import pytest
from pydantic import ValidationError


def test_graphql_response_creation() -> None:
    """Test GraphQLResponse can be created."""
    from src.models.graphql import GraphQLResponse

    response = GraphQLResponse(data={"user": {"id": "1"}})
    assert response.data == {"user": {"id": "1"}}
    assert response.errors is None


def test_graphql_response_with_errors() -> None:
    """Test GraphQLResponse with errors."""
    from src.models.graphql import GraphQLResponse, GraphQLError

    response = GraphQLResponse(
        data=None,
        errors=[GraphQLError(message="User not found")]
    )
    assert response.data is None
    assert len(response.errors) == 1
    assert response.errors[0].message == "User not found"


def test_graphql_response_has_errors_true() -> None:
    """Test has_errors returns True when errors exist."""
    from src.models.graphql import GraphQLResponse, GraphQLError

    response = GraphQLResponse(
        data=None,
        errors=[GraphQLError(message="Error")]
    )
    assert response.has_errors is True


def test_graphql_response_has_errors_false() -> None:
    """Test has_errors returns False when no errors."""
    from src.models.graphql import GraphQLResponse

    response = GraphQLResponse(data={"user": {"id": "1"}})
    assert response.has_errors is False


def test_graphql_response_is_successful_true() -> None:
    """Test is_successful returns True when data exists and no errors."""
    from src.models.graphql import GraphQLResponse

    response = GraphQLResponse(data={"user": {"id": "1"}})
    assert response.is_successful is True


def test_graphql_response_is_successful_false_with_errors() -> None:
    """Test is_successful returns False when errors exist."""
    from src.models.graphql import GraphQLResponse, GraphQLError

    response = GraphQLResponse(
        data={"user": {"id": "1"}},
        errors=[GraphQLError(message="Warning")]
    )
    assert response.is_successful is False


def test_graphql_response_is_successful_false_no_data() -> None:
    """Test is_successful returns False when no data."""
    from src.models.graphql import GraphQLResponse

    response = GraphQLResponse(data=None)
    assert response.is_successful is False


def test_graphql_error_location() -> None:
    """Test GraphQLErrorLocation validation."""
    from src.models.graphql import GraphQLErrorLocation

    location = GraphQLErrorLocation(line=1, column=5)
    assert location.line == 1
    assert location.column == 5


def test_graphql_error_location_validation() -> None:
    """Test GraphQLErrorLocation requires positive line/column."""
    from src.models.graphql import GraphQLErrorLocation

    with pytest.raises(ValidationError):
        GraphQLErrorLocation(line=0, column=5)

    with pytest.raises(ValidationError):
        GraphQLErrorLocation(line=1, column=0)

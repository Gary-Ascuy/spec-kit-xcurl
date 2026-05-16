"""GraphQL data models."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, List, Optional, Union

from pydantic import BaseModel, Field


class GraphQLErrorLocation(BaseModel):
    """Location of an error in the GraphQL query."""

    line: int = Field(ge=1, description="Line number (1-indexed)")
    column: int = Field(ge=1, description="Column number (1-indexed)")


class GraphQLError(BaseModel):
    """A GraphQL error returned by the server."""

    message: str = Field(description="Human-readable error message")
    locations: Optional[List[GraphQLErrorLocation]] = Field(
        default=None,
        description="Error locations in the query"
    )
    path: Optional[List[Union[str, int]]] = Field(
        default=None,
        description="Path to the field causing the error"
    )
    extensions: Optional[Mapping[str, Any]] = Field(
        default=None,
        description="Additional error extensions"
    )


class GraphQLRequest(BaseModel):
    """A GraphQL request with query, variables, and operation name."""

    query: str = Field(
        description="The GraphQL query or mutation string",
        min_length=1
    )
    variables: Optional[dict[str, Any]] = Field(
        default=None,
        description="Variables for the GraphQL query"
    )
    operation_name: Optional[str] = Field(
        default=None,
        description="Name of the operation (for multiple operations in one query)"
    )

    def to_http_body(self) -> dict[str, Any]:
        """Convert to HTTP request body."""
        body: dict[str, Any] = {"query": self.query}
        if self.variables is not None:
            body["variables"] = self.variables
        if self.operation_name is not None:
            body["operationName"] = self.operation_name
        return body


class GraphQLResponse(BaseModel):
    """Response from a GraphQL server."""

    data: Optional[dict[str, Any]] = Field(
        default=None,
        description="Query result data"
    )
    errors: Optional[List[GraphQLError]] = Field(
        default=None,
        description="GraphQL errors"
    )
    extensions: Optional[Mapping[str, Any]] = Field(
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

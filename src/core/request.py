"""Request builder module."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from src.models.config import HttpHeaders, QuerySource, VariablesSource
from src.models.graphql import GraphQLRequest


def build_request(
    query_source: QuerySource,
    variables_source: VariablesSource | None = None,
    headers: HttpHeaders | None = None,
) -> GraphQLRequest:
    """Build a GraphQL request from sources.

    Args:
        query_source: Source of the GraphQL query
        variables_source: Optional source of variables
        headers: Optional HTTP headers

    Returns:
        A GraphQLRequest ready to execute
    """
    variables = None
    if variables_source is not None:
        variables = variables_source.get_variables()

    return GraphQLRequest(
        query=query_source.content,
        variables=variables,
    )

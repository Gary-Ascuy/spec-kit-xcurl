"""HTTP request executor module."""

from __future__ import annotations

import asyncio
from collections.abc import Mapping
from typing import Any

import httpx

from src.models.config import HttpHeaders
from src.models.graphql import GraphQLRequest, GraphQLResponse


async def execute(
    endpoint: str,
    request: GraphQLRequest,
    headers: HttpHeaders | None = None,
    timeout: int = 30,
) -> GraphQLResponse:
    """Execute a GraphQL request via HTTP.

    Args:
        endpoint: GraphQL endpoint URL
        request: GraphQL request to execute
        headers: Optional HTTP headers
        timeout: Request timeout in seconds

    Returns:
        GraphQLResponse from the server

    Raises:
        httpx.HTTPError: On HTTP errors
    """
    http_headers = {}
    if headers is not None:
        http_headers = headers.get_headers()

    body = request.to_http_body()

    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(
            endpoint,
            json=body,
            headers=http_headers,
        )
        response.raise_for_status()
        data = response.json()

    return GraphQLResponse(**data)

"""Unit tests for HttpHeaders model."""

import pytest
from pydantic import ValidationError


def test_http_headers_creation() -> None:
    """Test HttpHeaders can be created with default values."""
    from src.models.config import HttpHeaders

    headers = HttpHeaders()
    assert headers.headers == {}
    assert headers.auth_token is None


def test_http_headers_with_custom_headers() -> None:
    """Test HttpHeaders with custom headers."""
    from src.models.config import HttpHeaders

    headers = HttpHeaders(headers={"Content-Type": "application/json", "X-Custom": "value"})
    assert headers.headers == {"Content-Type": "application/json", "X-Custom": "value"}


def test_http_headers_with_auth_token() -> None:
    """Test HttpHeaders with bearer token."""
    from src.models.config import HttpHeaders

    headers = HttpHeaders(auth_token="my-token")
    assert headers.auth_token == "my-token"


def test_http_headers_get_headers_includes_auth() -> None:
    """Test get_headers() includes Authorization header when auth_token is set."""
    from src.models.config import HttpHeaders

    headers = HttpHeaders(auth_token="my-token", headers={"X-Custom": "value"})
    result = headers.get_headers()

    assert "Authorization" in result
    assert result["Authorization"] == "Bearer my-token"
    assert result["X-Custom"] == "value"


def test_http_headers_get_headers_defaults_content_type() -> None:
    """Test get_headers() adds Content-Type if not present."""
    from src.models.config import HttpHeaders

    headers = HttpHeaders()
    result = headers.get_headers()

    assert "Content-Type" in result
    assert result["Content-Type"] == "application/json"


def test_http_headers_get_headers_preserves_content_type() -> None:
    """Test get_headers() preserves existing Content-Type."""
    from src.models.config import HttpHeaders

    headers = HttpHeaders(headers={"Content-Type": "application/graphql"})
    result = headers.get_headers()

    assert result["Content-Type"] == "application/graphql"


def test_http_headers_is_frozen() -> None:
    """Test HttpHeaders is frozen (immutable)."""
    from src.models.config import HttpHeaders

    headers = HttpHeaders()
    with pytest.raises(Exception):  # ValidationError or TypeError for frozen models
        headers.headers = {}  # type: ignore

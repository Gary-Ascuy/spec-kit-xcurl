# xcurl

A CLI tool for GraphQL queries, similar to curl but specialized for GraphQL.

## Installation

```bash
pip install xcurl
```

Or with uv:

```bash
uv pip install xcurl
```

## Usage

```bash
# Basic query
xcurl https://api.example.com/graphql -q "{ user { id name } }"

# Query from file
xcurl https://api.example.com/graphql -f query.gql

# Query with variables
xcurl https://api.example.com/graphql \
  -q "query GetUser($id: ID!) { user(id: $id) { name } }" \
  -v '{"id": "1"}'

# With authentication
xcurl https://api.example.com/graphql \
  -B "your-token" \
  -q "{ user { id } }"
```

## Development

```bash
# Install dependencies
uv pip install -e ".[dev]"

# Run tests
pytest

# Type checking
mypy --strict src/

# Linting
ruff check src/
```

## License

MIT

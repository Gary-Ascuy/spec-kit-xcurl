# Quick Start Guide: xcurl (GraphQL CLI)

**Feature**: 001-001-graphql-cli
**Date**: 2026-05-16

## Installation

### Using pip

```bash
pip install xcurl
```

### Using uv (recommended)

```bash
uv pip install xcurl
```

### From Source

```bash
git clone https://github.com/Gary-Ascuy/xcurl.git
cd xcurl
uv pip install -e .
```

## Your First Query

### The Simplest Query

```bash
xcurl https://graphql.org/swapi-graphql/ -q "{ allPeople { people { name } } }"
```

This queries the Star Wars API and returns names of all characters.

### Expected Output

```json
{
  "data": {
    "allPeople": {
      "people": [
        {"name": "Luke Skywalker"},
        {"name": "C-3PO"},
        {"name": "R2-D2"},
        ...
      ]
    }
  }
}
```

## Common Patterns

### Query from File

Create `query.gql`:
```graphql
query GetUser($id: ID!) {
  user(id: $id) {
    id
    name
    email
  }
}
```

Execute:
```bash
xcurl https://api.example.com/graphql -f query.gql -v '{"id": "1"}'
```

### Authentication

```bash
# Bearer token
xcurl https://api.example.com/graphql \
  -B "your-token-here" \
  -f query.gql

# API key in header
xcurl https://api.example.com/graphql \
  -H "X-API-Key: your-key" \
  -f query.gql
```

### Mutation

Create `mutation.gql`:
```graphql
mutation CreateUser($name: String!, $email: String!) {
  createUser(input: {name: $name, email: $email}) {
    id
    name
    email
  }
}
```

Execute:
```bash
xcurl https://api.example.com/graphql \
  -f mutation.gql \
  -v '{"name": "Alice", "email": "alice@example.com"}'
```

### Save Output to File

```bash
xcurl https://api.example.com/graphql -f query.gql -o response.json
cat response.json
```

### Pretty Output (default)

```bash
xcurl https://api.example.com/graphql -f query.gql --format pretty
```

### Raw Output (for piping)

```bash
# Extract just the data field
xcurl https://api.example.com/graphql -f query.gql --format raw | jq '.user.name'
```

## Tips and Tricks

### Use with jq for JSON Processing

```bash
xcurl https://api.example.com/graphql -q "{ users { id name } }" | jq '.data.users[] | .name'
```

### Save Credentials in Environment

```bash
export XCURL_TOKEN="your-token"
export XCURL_ENDPOINT="https://api.example.com/graphql"

# Now you can omit them
xcurl -q "{ user { id } }"
```

### Batch Queries with xargs

```bash
# Query multiple IDs
echo "1" "2" "3" | xargs -I {} xcurl https://api.example.com/graphql \
  -q "query GetUser($id: ID!) { user(id: $id) { name } }" \
  -v "{\"id\": \"{}\"}"
```

### Debugging Mode

```bash
# See full HTTP request/response
xcurl https://api.example.com/graphql --debug -f query.gql
```

## Troubleshooting

### "No query provided" Error

Make sure you're using `-q`, `-f`, or `-`:
```bash
# Wrong
xcurl https://api.example.com/graphql

# Right
xcurl https://api.example.com/graphql -q "{ user { id } }"
```

### GraphQL Errors

The tool exits with code 8 and shows GraphQL errors:
```bash
$ xcurl https://api.example.com/graphql -q "{ badField }"
GraphQL Error:
  - Cannot query field "badField" on type "Query".
Exit code: 8
```

### Timeout Errors

Increase timeout for slow endpoints:
```bash
xcurl https://api.example.com/graphql -f query.gql --timeout 60
```

## Next Steps

- Read the full [CLI Interface Contract](contracts/cli-interface.md) for all options
- Check out the [Data Model](data-model.md) for internal structure
- See [examples/](../../examples/) for more sample queries

# CLI Interface Contract

**Feature**: 001-001-graphql-cli
**Date**: 2026-05-16

## Overview

This document defines the CLI interface contract for the GraphQL CLI tool. It specifies commands, arguments, options, exit codes, and output formats.

## Command Structure

### Main Command: `xcurl`

```bash
xcurl [OPTIONS] ENDPOINT
```

### Positional Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `ENDPOINT` | string | Yes | GraphQL endpoint URL (HTTP/HTTPS) |

### Options

#### Query Options

| Option | Short | Type | Description |
|--------|-------|------|-------------|
| `--query` | `-q` | string | Inline GraphQL query or mutation |
| `--file` | `-f` | path | Path to file containing GraphQL query |
| `--stdin` | `-` | flag | Read query from standard input |

#### Variable Options

| Option | Short | Type | Description |
|--------|-------|------|-------------|
| `--variables` | `-v` | string | Variables as JSON string |
| `--variables-file` | `-V` | path | Path to JSON file with variables |

#### Header Options

| Option | Short | Type | Description |
|--------|-------|------|-------------|
| `--header` | `-H` | string | Custom header (format: "Name: value") |
| `--headers-file` | path | Path to file with headers (one per line) |
| `--bearer` | `-B` | string | Bearer token for authentication |

#### Output Options

| Option | Short | Type | Description |
|--------|-------|------|-------------|
| `--output` | `-o` | path | Write output to file instead of stdout |
| `--format` | `-F` | string | Output format: json, pretty, raw, color (default: pretty) |
| `--indent` | `-i` | int | JSON indentation spaces (default: 2, use 0 for compact) |

#### Execution Options

| Option | Short | Type | Description |
|--------|-------|------|-------------|
| `--method` | `-X` | string | HTTP method: POST (default), GET |
| `--timeout` | `-t` | int | Request timeout in seconds (default: 30, max: 300) |
| `--validate` | flag | Validate query before sending |

#### Diagnostic Options

| Option | Short | Type | Description |
|--------|-------|------|-------------|
| `--verbose` | flag | Enable verbose output (show request details) |
| `--debug` | flag | Enable debug mode (show all HTTP traffic) |
| `--version` | flag | Show version information |
| `--help` | `-h` | flag | Show help message |

## Exit Codes

| Code | Name | Description |
|------|------|-------------|
| 0 | SUCCESS | Request completed successfully |
| 1 | GENERAL_ERROR | Generic error (catch-all) |
| 2 | INVALID_ARGUMENTS | Invalid command-line arguments |
| 3 | FILE_NOT_FOUND | Specified file not found |
| 4 | INVALID_JSON | Invalid JSON in variables or response |
| 5 | QUERY_PARSE_ERROR | GraphQL query could not be parsed |
| 6 | VALIDATION_ERROR | Query validation failed |
| 7 | HTTP_ERROR | HTTP request failed (network, timeout) |
| 8 | GRAPHQL_ERRORS | GraphQL response contained errors |
| 9 | AUTH_ERROR | Authentication failed |

## Output Formats

### JSON (`json`)

Raw JSON output as received from the server. No formatting applied.

```bash
$ xcurl https://api.example.com/graphql --query "{ hello }"
{"data":{"hello":"world"}}
```

### Pretty (`pretty`) - Default

Human-readable formatted JSON with syntax highlighting (if terminal supports it).

```bash
$ xcurl https://api.example.com/graphql --query "{ hello }"
{
  "data": {
    "hello": "world"
  }
}
```

### Raw (`raw`)

Output only the `data` field from the GraphQL response, omitting `errors` and `extensions`. Useful for piping to other tools.

```bash
$ xcurl https://api.example.com/graphql --format raw --query "{ user(id:1) { name } }"
{"user":{"name":"Alice"}}
```

### Color (`color`)

Syntax-highlighted JSON with colors for better readability (requires terminal support).

```bash
$ xcurl https://api.example.com/graphql --format color --query "{ hello }"
# Output with colors (keys in blue, strings in green, etc.)
```

## Usage Examples

### Basic Query

```bash
# Inline query
xcurl https://api.example.com/graphql -q "{ user(id: 1) { name email } }"

# Query from file
xcurl https://api.example.com/graphql -f query.gql

# Query from stdin
echo "{ user(id: 1) { name } }" | xcurl https://api.example.com/graphql -
```

### Query with Variables

```bash
# Inline variables
xcurl https://api.example.com/graphql \
  -q "query GetUser($id: ID!) { user(id: $id) { name } }" \
  -v '{"id": "1"}'

# Variables from file
xcurl https://api.example.com/graphql \
  -q "query GetUser($id: ID!) { user(id: $id) { name } }" \
  -V variables.json
```

### Mutation

```bash
# Create user
xcurl https://api.example.com/graphql \
  -q "mutation CreateUser($name: String!) { createUser(name: $name) { id name } }" \
  -v '{"name": "Bob"}'
```

### With Authentication

```bash
# Bearer token
xcurl https://api.example.com/graphql \
  -B "your-token-here" \
  -q "{ user { id } }"

# Custom header
xcurl https://api.example.com/graphql \
  -H "X-API-Key: your-key-here" \
  -q "{ user { id } }"
```

### Output to File

```bash
# Save response
xcurl https://api.example.com/graphql -q "{ user { id } }" -o response.json
```

### Verbose Mode

```bash
# Show request details
xcurl https://api.example.com/graphql \
  --verbose \
  -q "{ user { id } }"
# Output:
# > POST /graphql HTTP/1.1
# > Host: api.example.com
# > Content-Type: application/json
# >
# > {"query":"{ user { id } }"}
#
# < HTTP/1.1 200 OK
# < Content-Type: application/json
# <
# {"data":{"user":{"id":"1"}}}
```

## Error Messages

### Invalid Arguments

```bash
$ xcurl https://api.example.com/graphql
Error: No query provided. Use --query, --file, or --stdin.

Usage: xcurl [OPTIONS] ENDPOINT
```

### File Not Found

```bash
$ xcurl https://api.example.com/graphql -f nonexistent.gql
Error: File not found: nonexistent.gql
Exit code: 3
```

### Invalid JSON

```bash
$ xcurl https://api.example.com/graphql -v '{invalid json}'
Error: Invalid JSON in variables: Expecting property name enclosed in double quotes
Exit code: 4
```

### GraphQL Errors

```bash
$ xcurl https://api.example.com/graphql -q "{ user { nonexistent } }"
GraphQL Error:
  - Cannot query field "nonexistent" on type "User".
    at line 1, column 10

Exit code: 8
```

## Configuration File (Optional)

The tool can optionally read configuration from `~/.xcurl/config.yml`:

```yaml
# Default endpoint (can be overridden by CLI argument)
default_endpoint: "https://api.example.com/graphql"

# Default headers
headers:
  Authorization: "Bearer default-token"
  User-Agent: "xcurl/1.0"

# Default options
timeout: 30
output_format: "pretty"
validate_query: false
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `XCURL_ENDPOINT` | Default GraphQL endpoint |
| `XCURL_TOKEN` | Default bearer token |
| `XCURL_TIMEOUT` | Default request timeout |
| `XCURL_VERBOSE` | Enable verbose mode (1=true, 0=false) |
| `NO_COLOR` | Disable colored output |

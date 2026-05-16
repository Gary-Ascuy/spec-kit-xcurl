# Feature Specification: GraphQL CLI Tool (xcurl)

**Feature Branch**: `001-001-graphql-cli`

**Created**: 2026-05-16

**Status**: Draft

**Input**: User description: "create a CLI similar to curl but that works with graphql queries, it allow get data and call mutations, queries can be in files or inline"

## User Scenarios & Testing

### User Story 1 - Query GraphQL Data (Priority: P1)

As a developer, I want to execute GraphQL queries from the command line so that I can quickly fetch data from GraphQL APIs without using a browser or GUI tool.

**Why this priority**: This is the core functionality - without query execution, the tool is useless. This delivers immediate value for API testing and debugging.

**Independent Test**: Can be fully tested by executing a simple query against a public GraphQL API (e.g., GraphQL Playground or a test endpoint) and verifying JSON output.

**Acceptance Scenarios**:

1. **Given** a GraphQL endpoint URL, **When** I run a query inline, **Then** the response is printed as formatted JSON
2. **Given** a GraphQL query file, **When** I execute it with the CLI, **Then** the query results are returned
3. **Given** a query with variables, **When** I provide variables as JSON, **Then** the query executes with those variables
4. **Given** a malformed query, **When** I execute it, **Then** a helpful error message is displayed

### User Story 2 - Execute Mutations (Priority: P2)

As a developer, I want to execute GraphQL mutations from the command line so that I can create, update, or delete data through GraphQL APIs.

**Why this priority**: Mutations are essential for complete GraphQL interaction but are secondary to read-only queries. P2 because queries (P1) provide immediate value for data inspection.

**Independent Test**: Can be fully tested by executing a mutation against a test GraphQL API and verifying the data was modified.

**Acceptance Scenarios**:

1. **Given** a GraphQL mutation, **When** I execute it with required input, **Then** the mutation succeeds and returns expected data
2. **Given** a mutation with variables, **When** I provide variables as JSON or file, **Then** the mutation executes correctly
3. **Given** a mutation that fails validation, **When** I execute it, **Then** GraphQL errors are displayed clearly

### User Story 3 - Authentication and Headers (Priority: P2)

As a developer, I want to include custom HTTP headers and authentication tokens so that I can query secured GraphQL endpoints.

**Why this priority**: Essential for real-world usage but secondary to basic query execution. P2 because P1 can be tested against public endpoints without auth.

**Independent Test**: Can be fully tested by executing a query against a secured GraphQL API with a Bearer token.

**Acceptance Scenarios**:

1. **Given** a secured endpoint, **When** I provide an Authorization header, **Then** the query executes successfully
2. **Given** multiple custom headers, **When** I provide them, **Then** all headers are included in the request
3. **Given** a header file, **When** I load headers from it, **Then** the headers are applied to the request

### User Story 4 - Introspection and Schema Discovery (Priority: P3)

As a developer, I want to introspect GraphQL schemas so that I can discover available queries, mutations, and types.

**Why this priority**: Nice-to-have feature for exploration. P3 because developers can reference documentation or schema files separately.

**Independent Test**: Can be fully tested by running introspection against a public GraphQL API and verifying schema information is displayed.

**Acceptance Scenarios**:

1. **Given** a GraphQL endpoint, **When** I run an introspection command, **Then** the schema is displayed or saved
2. **Given** an introspection result, **When** I query for specific types, **Then** only requested type information is shown
3. **Given** a schema, **When** I save it to a file, **Then** it can be used for autocomplete or validation

### Edge Cases

- What happens when the GraphQL endpoint returns errors (partial success)?
- How does the CLI handle network timeouts or connection failures?
- What happens when the query file is malformed or contains syntax errors?
- How are very large responses handled (pagination, truncation, streaming)?
- What happens when variable types don't match the schema?
- How are nested queries and fragments handled?
- What happens with different response formats (non-JSON endpoints)?

## Requirements

### Functional Requirements

- **FR-001**: CLI MUST accept GraphQL queries as inline arguments or from files
- **FR-002**: CLI MUST accept GraphQL mutations with the same interface as queries
- **FR-003**: CLI MUST support variable injection via JSON string or file
- **FR-004**: CLI MUST support custom HTTP headers via command-line arguments or file
- **FR-005**: CLI MUST output responses as formatted JSON by default
- **FR-006**: CLI MUST support alternative output formats (raw, pretty-printed, colorized)
- **FR-007**: CLI MUST display GraphQL errors clearly when they occur
- **FR-008**: CLI MUST support introspection queries for schema discovery
- **FR-009**: CLI MUST allow specifying HTTP method (POST default, GET for queries)
- **FR-010**: CLI MUST support Bearer token authentication via shorthand flag

### Key Entities

- **GraphQLRequest**: Represents a query/mutation with optional variables and headers
- **GraphQLResponse**: Contains data, errors, and extensions from the GraphQL response
- **QueryFile**: A file containing GraphQL query/mutation text
- **VariablesFile**: A JSON file containing variable values for the query
- **HeadersFile**: A file containing HTTP headers to include with requests
- **Config**: CLI configuration for defaults like endpoint URL, default headers

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users can execute a GraphQL query with a single command similar to curl
- **SC-002**: Query execution completes in under 2 seconds for typical API responses
- **SC-003**: 90% of users successfully execute their first query within 5 minutes without documentation
- **SC-004**: CLI provides helpful error messages that guide users to fix common mistakes

## Assumptions

- Target users are developers familiar with GraphQL and command-line tools
- GraphQL endpoints are accessible via HTTP/HTTPS
- Responses follow standard GraphQL response format (data, errors fields)
- Users have Python 3.13+ installed or can use a standalone binary
- Default output format is JSON (similar to curl's default output)
- Query files use .graphql or .gql extension convention

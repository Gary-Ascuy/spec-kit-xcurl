# Tasks: GraphQL CLI Tool (xcurl)

**Input**: Design documents from `/specs/001-001-graphql-cli/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: MANDATORY per constitution - 100% coverage, mutation testing, and architecture tests required.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below match plan.md structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project directory structure: src/{cli,core,models,utils}, tests/{contract,integration,unit,architecture}
- [X] T002 Initialize Python 3.13+ project with pyproject.toml and uv
- [X] T003 [P] Add core dependencies to pyproject.toml: click>=8.1, httpx>=0.27, pydantic>=3.0, graphql-core>=3.3
- [X] T004 [P] Add dev dependencies to pyproject.toml: pytest>=8.0, pytest-cov>=5.0, mutmut>=2.5, mypy>=1.9, ruff>=0.3, black>=24.0, rich>=13.0
- [X] T005 [P] Configure pytest in pyproject.toml with coverage plugin settings
- [X] T006 [P] Configure mypy in pyproject.toml with strict mode settings
- [X] T007 [P] Configure ruff in pyproject.toml with line length 100 and target Python 3.13
- [X] T008 [P] Create .gitignore with Python patterns: __pycache__/, *.pyc, .venv/, venv/, dist/, *.egg-info/, .coverage, .mutmut/, .mypy_cache/, .ruff_cache/
- [X] T009 [P] Create .dockerignore for container builds (optional for future)
- [X] T010 Create __init__.py files in all src/ directories
- [X] T011 Create basic README.md with project description and installation instructions

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Tests for Foundational Infrastructure (MANDATORY per constitution)

- [X] T012 [P] Architecture test for layer separation in tests/architecture/test_layer_separation.py - verify CLI layer doesn't import core directly, core doesn't import models
- [X] T013 [P] Architecture test for import rules in tests/architecture/test_import_rules.py - verify no forbidden imports between layers
- [X] T014 [P] Unit test for GraphQLRequest model in tests/unit/test_request.py - test model validation and to_http_body()
- [X] T015 [P] Unit test for GraphQLResponse model in tests/unit/test_response.py - test has_errors and is_successful properties
- [X] T016 [P] Unit test for HttpHeaders model in tests/unit/test_headers.py - test get_headers() with auth token

### Foundational Implementation

- [X] T017 Create GraphQLRequest model in src/models/graphql.py with query, variables, operation_name fields and to_http_body() method
- [X] T018 Create GraphQLResponse model in src/models/graphql.py with data, errors, extensions fields and has_errors/is_successful properties
- [X] T019 Create GraphQLError and GraphQLErrorLocation models in src/models/graphql.py
- [X] T020 Create HttpHeaders model in src/models/config.py with headers dict and auth_token field
- [X] T021 Create QuerySource model in src/models/config.py with from_inline(), from_file(), from_stdin() class methods
- [X] T022 Create VariablesSource model in src/models/config.py with get_variables() method
- [X] T023 Create CLIConfig model in src/models/config.py with endpoint, headers, output_format, timeout fields
- [X] T024 Create OutputFormat enum in src/models/config.py with JSON, PRETTY, RAW, COLOR values
- [X] T025 Create request builder module in src/core/request.py with build_request() function
- [X] T026 Create HTTP executor module in src/core/executor.py with execute() async function using httpx
- [X] T027 Create response processor module in src/core/response.py with format_response() function
- [X] T028 Create file I/O utilities in src/utils/files.py with read_query_file(), read_variables_file(), read_headers_file() functions
- [X] T029 Create output formatter in src/utils/format.py with format_json(), format_pretty(), format_raw(), format_color() functions
- [X] T030 Create Click CLI entry point skeleton in src/cli/main.py with main() command group

### Mutation Testing for Foundational Infrastructure

- [ ] T031 Run mutmut on src/models/ - verify 100% kill score, improve tests until all mutants killed
- [ ] T032 Run mutmut on src/core/ - verify 100% kill score, improve tests until all mutants killed
- [ ] T033 Run mutmut on src/utils/ - verify 100% kill score, improve tests until all mutants killed

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Query GraphQL Data (Priority: P1) 🎯 MVP

**Goal**: Execute GraphQL queries from the command line with inline or file-based queries

**Independent Test**: Execute a simple query against a public GraphQL API (https://graphql.org/swapi-graphql/) and verify JSON output

### Tests for User Story 1 (MANDATORY per constitution)

- [X] T034 [P] [US1] Contract test for CLI query command in tests/contract/test_cli_query.py - verify command accepts query and endpoint
- [ ] T035 [P] [US1] Integration test for inline query execution in tests/integration/test_query_execution.py - test against public Star Wars API
- [X] T036 [P] [US1] Integration test for file-based query execution in tests/integration/test_query_execution.py - test query file reading
- [X] T037 [P] [US1] Integration test for query with variables in tests/integration/test_query_execution.py - test variable injection
- [ ] T038 [P] [US1] Unit test for request builder in tests/unit/test_request_builder.py - test GraphQL request construction
- [ ] T039 [P] [US1] Unit test for HTTP executor in tests/unit/test_executor.py - mock httpx client, test execute() function
- [ ] T040 [P] [US1] Unit test for response processor in tests/unit/test_response_processor.py - test response formatting
- [ ] T041 [P] [US1] Unit test for file reader in tests/unit/test_file_reader.py - test query file reading
- [ ] T042 [P] [US1] Architecture test in tests/architecture/test_us1_structure.py - verify US1 follows layered architecture
- [ ] T043 [US1] Mutation testing for US1 code - verify 100% kill score for all new code

### Implementation for User Story 1

- [X] T044 [P] [US1] Create --query option in src/cli/main.py to accept inline GraphQL query
- [X] T045 [P] [US1] Create --file option in src/cli/main.py to accept query file path
- [X] T046 [P] [US1] Create --variables option in src/cli/main.py to accept JSON variables string
- [X] T047 [P] [US1] Create --variables-file option in src/cli/main.py to accept variables file path
- [X] T048 [P] [US1] Create --format option in src/cli/main.py with json/pretty/raw choices
- [X] T049 [P] [US1] Create --output option in src/cli/main.py to write response to file
- [X] T050 [US1] Implement query execution logic in src/cli/main.py - integrate request builder, executor, and response processor
- [X] T051 [US1] Add error handling in src/cli/main.py for malformed queries, HTTP errors, GraphQL errors
- [X] T052 [US1] Add exit codes in src/cli/main.py per contract (0=success, 4=invalid_json, 5=parse_error, 7=http_error, 8=graphql_errors)
- [X] T053 [US1] Test with public GraphQL API - run xcurl against https://countries.trevorblades.com/ and verify output

**Checkpoint**: At this point, User Story 1 should be fully functional - users can execute GraphQL queries inline or from files

---

## Phase 4: User Story 2 - Execute Mutations (Priority: P2)

**Goal**: Execute GraphQL mutations from the command line

**Independent Test**: Execute a mutation against a test GraphQL API and verify the data was modified

### Tests for User Story 2 (MANDATORY per constitution)

- [ ] T054 [P] [US2] Integration test for mutation execution in tests/integration/test_mutation_execution.py - test against a test API
- [ ] T055 [P] [US2] Integration test for mutation with variables in tests/integration/test_mutation_execution.py - test variable injection for mutations
- [ ] T056 [P] [US2] Unit test for mutation request in tests/unit/test_mutation_request.py - verify mutation queries handled correctly
- [ ] T057 [P] [US2] Architecture test in tests/architecture/test_us2_structure.py - verify US2 follows layered architecture
- [ ] T058 [US2] Mutation testing for US2 code - verify 100% kill score

### Implementation for User Story 2

- [ ] T059 [US2] Verify CLI accepts mutations - same --query and --file options work for mutations (no code change needed, validation only)
- [ ] T060 [US2] Add mutation examples to quickstart documentation
- [ ] T061 [US2] Test mutation execution against public API - find or mock a GraphQL API that supports mutations

**Checkpoint**: User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Authentication and Headers (Priority: P2)

**Goal**: Include custom HTTP headers and authentication tokens for secured GraphQL endpoints

**Independent Test**: Execute a query against a secured GraphQL API with a Bearer token

### Tests for User Story 3 (MANDATORY per constitution)

- [ ] T062 [P] [US3] Integration test for Bearer token auth in tests/integration/test_auth_execution.py - test Authorization header
- [ ] T063 [P] [US3] Integration test for custom headers in tests/integration/test_auth_execution.py - test multiple headers
- [ ] T064 [P] [US3] Integration test for headers file in tests/integration/test_auth_execution.py - test loading headers from file
- [ ] T065 [P] [US3] Unit test for headers module in tests/unit/test_headers.py - test header construction and Bearer token
- [ ] T066 [P] [US3] Architecture test in tests/architecture/test_us3_structure.py - verify US3 follows layered architecture
- [ ] T067 [US3] Mutation testing for US3 code - verify 100% kill score

### Implementation for User Story 3

- [ ] T068 [P] [US3] Create --header option in src/cli/main.py to accept custom header (format: "Name: value")
- [ ] T069 [P] [US3] Create --headers-file option in src/cli/main.py to accept headers file path
- [ ] T070 [P] [US3] Create --bearer option in src/cli/main.py to accept Bearer token shorthand
- [ ] T071 [US3] Implement header application logic in src/core/request.py - apply headers to HTTP request
- [ ] T072 [US3] Test with secured endpoint - use a test API or mock secured endpoint

**Checkpoint**: User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Introspection and Schema Discovery (Priority: P3)

**Goal**: Introspect GraphQL schemas to discover available queries, mutations, and types

**Independent Test**: Run introspection against a public GraphQL API and verify schema information is displayed

### Tests for User Story 4 (MANDATORY per constitution)

- [ ] T073 [P] [US4] Integration test for introspection query in tests/integration/test_introspection.py - test against public API
- [ ] T074 [P] [US4] Unit test for introspection module in tests/unit/test_introspection.py - test introspection query generation
- [ ] T075 [P] [US4] Architecture test in tests/architecture/test_us4_structure.py - verify US4 follows layered architecture
- [ ] T076 [US4] Mutation testing for US4 code - verify 100% kill score

### Implementation for User Story 4

- [ ] T077 [P] [US4] Create introspection query builder in src/core/request.py - generate standard introspection query
- [ ] T078 [P] [US4] Add --introspect flag in src/cli/main.py to trigger schema introspection
- [ ] T079 [P] [US4] Add --schema-output option in src/cli/main.py to save schema to file
- [ ] T080 [US4] Implement introspection response formatter in src/utils/format.py - format schema for display
- [ ] T081 [US4] Test introspection against public API - run against https://graphql.org/swapi-graphql/

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T082 [P] Add --verbose flag in src/cli/main.py for detailed request/response logging
- [ ] T083 [P] Add --debug flag in src/cli/main.py for full HTTP traffic debugging
- [ ] T084 [P] Add --method option in src/cli/main.py for GET/POST selection
- [ ] T085 [P] Add --timeout option in src/cli/main.py for configurable request timeout
- [ ] T086 [P] Add --validate flag in src/cli/main.py for query validation before sending
- [ ] T087 [P] Implement query validation using graphql-core in src/core/request.py
- [ ] T088 [P] Create completion script for shell auto-completion in src/cli/completion.py
- [ ] T089 Update README.md with comprehensive usage examples
- [ ] T090 Verify 100% test coverage across all modules - run pytest --cov
- [ ] T091 Verify 100% mutation testing score across all modules - run mutmut
- [ ] T092 Verify zero mypy errors across all modules - run mypy --strict
- [ ] T093 Verify zero ruff warnings across all modules - run ruff check
- [ ] T094 Run integration test suite against public GraphQL APIs - verify all scenarios pass

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - US1 (P1): Can start after Foundational - No dependencies on other stories
  - US2 (P2): Can start after Foundational - Independent of US1 (mutations use same CLI interface)
  - US3 (P2): Can start after Foundational - Independent of US1/US2 (headers are request-level concern)
  - US4 (P3): Can start after Foundational - Independent of US1/US2/US3 (introspection is separate feature)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Shares CLI interface from US1 but implementation independent
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Adds headers to existing request flow
- **User Story 4 (P3)**: Can start after Foundational (Phase 2) - Separate introspection feature

### Within Each User Story

- Tests MUST be written and FAIL before implementation (TDD)
- All [P] tasks in a story can run in parallel
- Non-parallel tasks must run in sequence
- Story complete before moving to next priority

### Parallel Opportunities

- **Setup**: All T003-T009 can run in parallel
- **Foundational Tests**: All T012-T016 can run in parallel
- **US1 Tests**: All T034-T042 can run in parallel
- **US1 Implementation**: T044-T049 can run in parallel (different CLI options)
- **US2 Tests**: All T054-T057 can run in parallel
- **US3 Tests**: All T062-T066 can run in parallel
- **US3 Implementation**: T068-T070 can run in parallel
- **US4 Tests**: All T073-T075 can run in parallel
- **US4 Implementation**: T077-T080 can run in parallel
- **Polish**: All T082-T088 can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
T034: Contract test for CLI query command
T035: Integration test for inline query execution
T036: Integration test for file-based query execution
T037: Integration test for query with variables
T038: Unit test for request builder
T039: Unit test for HTTP executor
T040: Unit test for response processor
T041: Unit test for file reader
T042: Architecture test for US1 structure

# Launch all CLI options for User Story 1 together:
T044: Create --query option
T045: Create --file option
T046: Create --variables option
T047: Create --variables-file option
T048: Create --format option
T049: Create --output option
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T011)
2. Complete Phase 2: Foundational (T012-T033) - CRITICAL - blocks all stories
3. Complete Phase 3: User Story 1 (T034-T053)
4. **STOP and VALIDATE**: Test US1 independently - run against public GraphQL API
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add Polish → Final release

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (queries)
   - Developer B: User Story 2 (mutations)
   - Developer C: User Story 3 (headers)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (TDD)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Per constitution: 100% coverage, 100% mutation testing, zero mypy errors, zero ruff warnings REQUIRED
- Test against public GraphQL APIs (https://graphql.org/swapi-graphql/) for real-world validation

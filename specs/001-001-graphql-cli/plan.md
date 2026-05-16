# Implementation Plan: GraphQL CLI Tool (xcurl)

**Branch**: `001-001-graphql-cli` | **Date**: 2026-05-16 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/001-001-graphql-cli/spec.md`

## Summary

Build a CLI tool similar to curl but specialized for GraphQL queries and mutations. The tool will accept queries inline or from files, support variables, headers, and authentication. It will provide formatted JSON output with helpful error messages. Target platform is CLI with Python 3.13+ following strict typing, 100% coverage, and mutation testing.

## Technical Context

**Language/Version**: Python 3.13+ (latest stable)

**Primary Dependencies**: `click` for CLI interface, `httpx` for async HTTP requests, `pydantic` for type-safe request/response validation

**Storage**: N/A (stateless CLI tool)

**Testing**: pytest with pytest-cov, mutmut for mutation testing, mypy --strict, ruff

**Target Platform**: Cross-platform CLI (Linux, macOS, Windows) via Python entry point

**Project Type**: cli

**Performance Goals**: <2s p95 for typical API responses, minimal startup overhead (<100ms)

**Constraints**: Single binary distribution optional but not required (pip install acceptable), offline mode for introspection caching

**Scale/Scope**: ~1000 LOC core, handles typical GraphQL APIs (<1MB responses), 10-15 CLI commands/flags

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Required Quality Gates

- [ ] 100% test coverage (pytest-cov)
- [ ] 100% mutation testing score (mutmut)
- [ ] Zero mypy errors (--strict mode)
- [ ] Zero ruff warnings
- [ ] Architecture tests passing (module boundaries, dependency rules)
- [ ] All type hints complete (no Any without justification)
- [ ] All dependencies justified and minimal

### Architecture Requirements

- [ ] Layered architecture enforced (no forbidden imports)
- [ ] Domain layer independent of presentation/infrastructure
- [ ] Dependency inversion respected
- [ ] Package structure matches design

## Project Structure

### Documentation (this feature)

```text
specs/001-001-graphql-cli/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── cli-interface.md # CLI command contract
└── tasks.md             # Phase 2 output (NOT created by /speckit-plan)
```

### Source Code (repository root)

```text
src/
├── __init__.py
├── cli/
│   ├── __init__.py
│   └── main.py          # Click CLI entry point
├── core/
│   ├── __init__.py
│   ├── request.py       # GraphQL request builder
│   ├── executor.py      # HTTP request executor
│   └── response.py      # Response processor
├── models/
│   ├── __init__.py
│   ├── graphql.py       # GraphQL data models
│   └── config.py        # Configuration models
└── utils/
    ├── __init__.py
    ├── format.py        # Output formatting
    └── files.py         # File I/O utilities

tests/
├── contract/
│   └── test_cli_interface.py  # CLI contract tests
├── integration/
│   ├── test_query_execution.py
│   └── test_mutation_execution.py
├── unit/
│   ├── test_request.py
│   ├── test_executor.py
│   └── test_response.py
└── architecture/
    ├── test_layer_separation.py
    └── test_import_rules.py

pyproject.toml           # Project config, dependencies
README.md                # Project documentation
```

**Structure Decision**: Single project structure (CLI tool). Layered architecture with CLI (presentation), Core (business logic), Models (domain), and Utils (infrastructure). This enforces separation of concerns: CLI parsing separate from GraphQL logic separate from HTTP transport.

## Complexity Tracking

> No violations - all constitution requirements satisfied.

---

## Phase 0: Research Findings

### Research Topics

1. **HTTP Client Library**: Chose `httpx` over `requests`
   - **Decision**: httpx with async support
   - **Rationale**: Modern, async/await support, better type hints, active maintenance, requests in maintenance mode
   - **Alternatives considered**: requests (no async), aiohttp (less intuitive API), urllib (standard library but verbose)

2. **CLI Framework**: Chose `click` for CLI interface
   - **Decision**: click with rich for output formatting
   - **Rationale**: Mature, composable, excellent for subcommands, strong typing support. Rich adds colored/formatted output
   - **Alternatives considered**: typer (simpler but less flexible), argparse (standard library but verbose)

3. **Validation Library**: Chose `pydantic` for request/response models
   - **Decision**: pydantic v3 with strict type validation
   - **Rationale**: Runtime type checking, JSON schema generation, excellent mypy support, minimal boilerplate
   - **Alternatives considered**: msgspec (faster but less mature), dataclasses (standard library but no validation)

4. **Mutation Testing Tool**: Chose `mutmut` for mutation testing
   - **Decision**: mutmut with pytest runner
   - **Rationale**: Designed for Python pytest workflow, good mutation operators, clear reporting
   - **Alternatives considered**: mutpy (older, less active)

5. **GraphQL Query Parsing**: Chose `graphql-core` for query validation
   - **Decision**: graphql-core v3 (official Python GraphQL implementation)
   - **Rationale**: Full GraphQL spec compliance, query parsing and validation, introspection support
   - **Alternatives considered**: libgraphqlparser (C bindings, complex setup), singql (deprecated)

---

## Phase 1: Design Artifacts

### Data Model

See [data-model.md](data-model.md) for complete entity definitions, validation rules, and state transitions.

### CLI Interface Contract

See [contracts/cli-interface.md](contracts/cli-interface.md) for command schema, arguments, options, and exit codes.

### Quick Start Guide

See [quickstart.md](quickstart.md) for installation, first query, and common patterns.

---

**Constitution Re-check (Post-Phase 1)**: All gates satisfied. Architecture enforces clear boundaries between CLI, core, models, and utils layers.

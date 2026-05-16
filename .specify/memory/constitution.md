<!--
Sync Impact Report:
- Version change: (initial) → 1.0.0
- Modified principles: N/A (initial creation)
- Added sections: All (Core Principles, Technology Standards, Quality Gates, Governance)
- Removed sections: None
- Templates requiring updates:
  ✅ .specify/templates/plan-template.md (Technical Context section updated)
  ✅ .specify/templates/spec-template.md (Requirements section verified)
  ✅ .specify/templates/tasks-template.md (Test task categories verified)
- Follow-up TODOs: None
-->

# xcurl Constitution

## Core Principles

### I. Test Excellence (NON-NEGOTIABLE)

100% code coverage is mandatory. Every line of production code MUST be covered by automated tests. Coverage is measured per module and MUST be maintained at 100% across the entire codebase.

**Mutation Testing**: All code MUST pass mutation testing. Mutation tests verify that tests actually catch bugs - a mutant that survives indicates a weak test that MUST be improved. Use mutmut or similar tool; target 100% mutant kill score.

**Architecture Tests**: Every architectural decision MUST be enforced by tests. Module boundaries, dependency rules, and structural invariants MUST be tested automatically. Architecture unit tests verify:
- Forbidden imports between modules
- Enforcement of layered architecture (e.g., domain layer never imports presentation)
- Adherence to dependency inversion principles
- Package structure integrity

**Rationale**: High coverage without mutation testing is false confidence. Tests that pass but don't catch defects are worse than useless. Architecture tests prevent design erosion and keep the codebase maintainable.

### II. Type Safety

Strong typing is mandatory. All functions MUST use type hints. All public APIs MUST have complete type annotations. Use `mypy` in strict mode (`--strict`). No `# type: ignore` without explicit approval and documented justification.

**Generic Types**: Use generic types (`List[T]`, `Dict[K, V]`, `Protocol`, etc.) instead of `Any`. All collections MUST specify their element types.

**Rationale**: Types are documentation that doesn't lie. They catch bugs at write time, not runtime. Strict typing enables confident refactoring.

### III. Python Best Practices

Follow PEP 8, PEP 257 (docstrings), and PEP 484 (type hints). Use `ruff` for linting and `black` for formatting. No warnings suppressed without documentation.

**Dependencies**: Minimize external dependencies. Each dependency MUST have a clear, justified purpose. Prefer standard library solutions.

**Rationale**: Consistent code is readable code. Standard library reduces attack surface and maintenance burden.

### IV. Modern Python

Use the latest stable Python version (3.13+). Leverage modern language features appropriately: pattern matching, type parameter syntax, walrus operator where it improves clarity.

**Backwards Compatibility**: Not a concern for this project. Use new features when they improve code quality.

**Rationale**: Newer Python has better performance, security, and developer experience.

### V. Simplicity

Prefer simple solutions over clever ones. Code MUST be obvious to a competent Python developer. Avoid premature optimization. Complexity MUST be justified and documented.

**Rationale**: Simple code is easier to understand, test, and modify. Clever code becomes unmaintainable.

## Technology Standards

### Language and Version

- **Python**: 3.13+ (use latest stable release)
- **Package Manager**: `uv` (preferred) or `poetry`
- **Virtual Environment**: Required for all development

### Testing Framework

- **Unit Tests**: `pytest` with `pytest-cov` for coverage
- **Mutation Testing**: `mutmut` or `mutpy`
- **Architecture Tests**: `deptry` for dependency enforcement, custom tests for structure
- **Type Checking**: `mypy --strict`
- **Linting**: `ruff` (replaces flake8, isort, pydocstyle)
- **Formatting**: `black`

### Quality Gates

No code MAY be merged without:

1. 100% test coverage (pytest-cov)
2. 100% mutation kill score (mutmut)
3. Zero mypy errors (--strict mode)
4. Zero ruff warnings
5. All architecture tests passing
6. All documentation updated

### Development Workflow

1. Write test FIRST (TDD)
2. Run tests - verify they FAIL
3. Implement code to make tests pass
4. Run mutation tests - improve until 100% kill
5. Run type checker - fix all errors
6. Run linter - fix all warnings
7. Format with black
8. Create PR only after all gates pass

## Quality Gates

All pull requests MUST:

- Pass 100% code coverage check
- Pass 100% mutation testing
- Pass strict mypy type checking
- Pass ruff linting with zero warnings
- Pass all architecture tests
- Include tests for any new functionality
- Update documentation for any API changes

Automated CI/CD MUST enforce these gates. No manual overrides.

## Governance

### Amendments

This constitution MAY be amended by:
1. Documenting the proposed change with rationale
2. Updating version number according to semantic versioning
3. Updating all dependent templates to remain consistent
4. Communicating changes to all contributors

### Versioning

- **MAJOR**: Remove or redefine principles (breaking changes)
- **MINOR**: Add new principles or sections
- **PATCH**: Clarifications, wording improvements

### Compliance

All contributors MUST adhere to these principles. Code reviews MUST verify compliance. Complexity deviations MUST be documented and justified.

### Guidance

Refer to project documentation for runtime development guidance specific to xcurl.

---

**Version**: 1.0.0 | **Ratified**: 2026-05-16 | **Last Amended**: 2026-05-16

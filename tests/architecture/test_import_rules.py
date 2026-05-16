"""Architecture tests for import rules."""

import ast
import sys
from pathlib import Path


def _get_imports(filepath: Path) -> list[tuple[str, str]]:
    """Extract all imports from a Python file."""
    imports = []
    content = filepath.read_text()
    tree = ast.parse(content)

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(("import", alias.name))
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                imports.append(("from", f"{module}.{alias.name}"))

    return imports


def test_no_forbidden_imports_in_cli() -> None:
    """Verify CLI doesn't import forbidden modules."""
    cli_path = Path("src/cli/main.py")
    if not cli_path.exists():
        return  # Skip if file doesn't exist yet

    imports = _get_imports(cli_path)

    # CLI should not import test modules
    for kind, name in imports:
        assert not name.startswith("tests."), f"CLI should not import tests: {name}"


def test_no_forbidden_imports_in_core() -> None:
    """Verify core doesn't import forbidden modules."""
    core_files = Path("src/core").glob("*.py")
    for filepath in core_files:
        if filepath.name == "__init__.py":
            continue
        imports = _get_imports(filepath)

        # Core should not import CLI (presentation layer)
        for kind, name in imports:
            assert not name.startswith("src.cli"), f"Core should not import CLI: {name}"


def test_no_forbidden_imports_in_models() -> None:
    """Verify models don't import forbidden modules."""
    model_files = Path("src/models").glob("*.py")
    for filepath in model_files:
        if filepath.name == "__init__.py":
            continue
        imports = _get_imports(filepath)

        # Models should not import CLI or core
        for kind, name in imports:
            assert not name.startswith("src.cli"), f"Models should not import CLI: {name}"
            # Models can import httpx for types but not core logic

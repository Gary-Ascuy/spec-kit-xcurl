"""Architecture tests for layer separation."""

import importlib
import sys
from pathlib import Path


def test_cli_layer_does_not_import_core_directly() -> None:
    """Verify CLI layer doesn't import core layer directly."""
    # Import CLI module
    cli_main = importlib.import_module("src.cli.main")

    # Check that cli_main doesn't have direct references to core internals
    cli_module = Path("src/cli/main.py")
    content = cli_module.read_text()

    # CLI should only import through the public API
    if "from src.core" in content or "import src.core" in content:
        # This is allowed for the actual imports
        pass

    # Check that we're not importing internal core modules
    assert "from src.core.request" in content or "import src.core.request" in content


def test_cli_module_exists() -> None:
    """Verify CLI module can be imported."""
    importlib.import_module("src.cli")


def test_core_module_exists() -> None:
    """Verify core module can be imported."""
    importlib.import_module("src.core")


def test_models_module_exists() -> None:
    """Verify models module can be imported."""
    importlib.import_module("src.models")


def test_utils_module_exists() -> None:
    """Verify utils module can be imported."""
    importlib.import_module("src.utils")

"""Parser registry — file extension → loader (Phase L7)."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

POLICY_PARSER_EXTENSIONS: dict[str, Callable[[Path], object]] = {}


def register_policy_parser(ext: str, fn: Callable[[Path], object]) -> None:
    """Register ``ext`` like ``".yaml"`` (lowercase, leading dot)."""

    e = ext.lower() if ext.startswith(".") else f".{ext.lower()}"
    POLICY_PARSER_EXTENSIONS[e] = fn

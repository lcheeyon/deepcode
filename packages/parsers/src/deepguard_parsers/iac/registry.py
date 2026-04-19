"""IaC parser registry (Laocoon; Phase L9)."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

IaC_PARSERS: dict[str, Callable[[str], list[dict[str, str]]]] = {}


def register_iac_parser(ext: str, fn: Callable[[str], list[dict[str, str]]]) -> None:
    e = ext.lower() if ext.startswith(".") else f".{ext.lower()}"
    IaC_PARSERS[e] = fn


def _stub_tf(text: str) -> list[dict[str, str]]:
    _ = text
    return [{"rule": "STUB_TF_SCAN", "resource": "terraform_stub", "severity": "LOW"}]


register_iac_parser(".tf", _stub_tf)


def parse_iac_file(path: Path) -> list[dict[str, str]]:
    fn = IaC_PARSERS.get(path.suffix.lower())
    if fn is None:
        return []
    return fn(path.read_text(encoding="utf-8", errors="replace"))

"""Pytest defaults: EPIC-DG-11 hermetic unit runs (override in integration jobs if needed)."""

from __future__ import annotations

import os

# Unit tests should not open LangSmith connections or install a global OTEL provider
# unless a test explicitly clears these.
os.environ.setdefault("LANGCHAIN_TRACING_V2", "false")
os.environ.setdefault("DEEPGUARD_OTEL_BOOTSTRAP", "0")

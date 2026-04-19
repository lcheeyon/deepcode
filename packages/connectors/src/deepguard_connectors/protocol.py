"""Cloud connector protocol (Architecture §15)."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class CloudConnector(Protocol):
    """Loads frozen resource snapshots (no live mutating APIs in L9)."""

    def load_snapshot(self, snapshot_ref: str) -> dict[str, Any]:
        """Return JSON-serialisable snapshot payload (S3-style ref resolves to fixture)."""
        ...

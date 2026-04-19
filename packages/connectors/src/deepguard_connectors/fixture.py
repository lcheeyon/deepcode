"""Load ``eval/fixtures/cloud`` JSON by reference id (Phase L9)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast


class FixtureConnector:
    """Resolve ``snapshot_ref`` to ``fixtures_root / f"{ref}.json"``."""

    def __init__(self, fixtures_root: Path) -> None:
        self._root = fixtures_root.resolve()

    def load_snapshot(self, snapshot_ref: str) -> dict[str, Any]:
        path = (self._root / f"{snapshot_ref}.json").resolve()
        path.relative_to(self._root)
        return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))

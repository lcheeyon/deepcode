"""Redis cache keys for parsed policy payloads (Architecture §9)."""

from __future__ import annotations

import hashlib


def tiresias_cache_key(*, framework: str, source_bytes: bytes) -> str:
    """Deterministic key: ``tiresias:policy:{framework}:{sha256}``."""

    digest = hashlib.sha256(source_bytes).hexdigest()
    fw = framework.strip().lower().replace(" ", "_")[:64]
    return f"tiresias:policy:{fw}:{digest}"

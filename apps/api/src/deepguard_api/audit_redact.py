"""Auditor-safe JSON views (Phase L14 — no SECRET-classified fields)."""

from __future__ import annotations

from typing import Any

_SECRET_KEYS = frozenset(
    {
        "raw_credential",
        "access_token_plain",
        "api_key_plain",
        "private_key_pem",
        "client_secret",
    }
)


def redact_for_auditor(data: Any) -> Any:
    """Recursively replace known secret keys with a fixed placeholder."""

    if isinstance(data, dict):
        out: dict[str, Any] = {}
        for k, v in data.items():
            lk = str(k).lower()
            if lk in _SECRET_KEYS or lk.endswith("_secret") or lk.endswith("_token_plain"):
                out[str(k)] = "[REDACTED]"
            else:
                out[str(k)] = redact_for_auditor(v)
        return out
    if isinstance(data, list):
        return [redact_for_auditor(x) for x in data]
    return data

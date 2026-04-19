"""Sink-safe payload shaping for LangSmith / LangFuse (Architecture §23.1 Q9, EPIC-DG-11-001)."""

from __future__ import annotations

# External observability sinks must not receive unbounded raw LLM payloads.
DEFAULT_EXCERPT_MAX_BYTES = 4096


def excerpt_for_trace_sink(text: str | None, *, max_bytes: int = DEFAULT_EXCERPT_MAX_BYTES) -> str:
    """Return a UTF-8 safe prefix of ``text`` capped at ``max_bytes`` (EPIC-DG-11-001-02)."""

    if not text:
        return ""
    raw = text.encode("utf-8")[:max_bytes]
    return raw.decode("utf-8", errors="replace")


def sanitize_trace_metadata_value(
    value: object,
    *,
    max_bytes: int = DEFAULT_EXCERPT_MAX_BYTES,
) -> object:
    """Shorten large strings before attaching to LangSmith / LangFuse metadata (§8.2)."""

    if isinstance(value, str) and len(value.encode("utf-8")) > max_bytes:
        return excerpt_for_trace_sink(value, max_bytes=max_bytes)
    if isinstance(value, dict):
        return {
            str(k): sanitize_trace_metadata_value(v, max_bytes=max_bytes)
            for k, v in value.items()
        }
    if isinstance(value, list):
        return [sanitize_trace_metadata_value(v, max_bytes=max_bytes) for v in value]
    return value


def redact_secrets(
    mapping: dict[str, object],
    *,
    banned_keys: frozenset[str] | None = None,
) -> dict[str, object]:
    """Drop ``SECRET``-class keys from dict-like metadata (EPIC-DG-11-001-03 baseline)."""

    banned = banned_keys or frozenset(
        {
            "api_key",
            "secret",
            "password",
            "token",
            "authorization",
            "x-api-key",
            "private_key",
        }
    )
    out: dict[str, object] = {}
    for k, v in mapping.items():
        lk = str(k).lower().replace("-", "_")
        if any(b in lk for b in ("secret", "password", "token", "api_key", "private_key")):
            out[str(k)] = "[REDACTED]"
            continue
        if lk in banned:
            out[str(k)] = "[REDACTED]"
            continue
        out[str(k)] = sanitize_trace_metadata_value(v) if isinstance(v, (str, dict, list)) else v
    return out

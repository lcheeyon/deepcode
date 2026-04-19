"""Helpers for pytest-html: attach sample HTTP request/response JSON to reports."""

from __future__ import annotations

import json
from collections.abc import MutableSequence
from typing import Any

from pytest_html import extras as html_extras


def attach_api_exchange(
    extras: MutableSequence[Any],
    *,
    name: str,
    method: str,
    path: str,
    request_json: dict[str, Any] | list[Any] | None = None,
    request_headers: dict[str, str] | None = None,
    response_status: int,
    response_body: Any = None,
) -> None:
    """Append a collapsible JSON block (request + response) to the HTML report."""
    summary = {
        "request": {
            "method": method,
            "path": path,
            "headers_sample": request_headers or {},
            "json_body": request_json,
        },
        "response": {"http_status": response_status, "json_body": response_body},
    }
    extras.append(
        html_extras.json(
            json.dumps(summary, indent=2, default=str),
            name=name,
        )
    )

"""ASGI entry for ``uvicorn apps.api.main:app`` (run from repo root)."""

from deepguard_api.main import app

__all__ = ["app"]

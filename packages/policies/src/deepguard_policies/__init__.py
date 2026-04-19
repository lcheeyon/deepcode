"""Policy parsers and registry (Phase L7 / EPIC DG-05)."""

from pathlib import Path

from deepguard_policies.cache_keys import tiresias_cache_key
from deepguard_policies.parse import PolicyParseResult, parse_policy_file
from deepguard_policies.registry import POLICY_PARSER_EXTENSIONS, register_policy_parser


def _yaml_loader(path: Path) -> object:
    return parse_policy_file(path)


register_policy_parser(".yaml", _yaml_loader)

__all__ = [
    "POLICY_PARSER_EXTENSIONS",
    "PolicyParseResult",
    "parse_policy_file",
    "register_policy_parser",
    "tiresias_cache_key",
]

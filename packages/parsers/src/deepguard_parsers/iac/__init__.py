"""IaC parsers (Phase L9)."""

from deepguard_parsers.iac.registry import IaC_PARSERS, parse_iac_file, register_iac_parser

__all__ = ["IaC_PARSERS", "parse_iac_file", "register_iac_parser"]

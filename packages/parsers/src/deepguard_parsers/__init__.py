"""Parsers for code / IaC (Phase L8–L9)."""

from deepguard_parsers.chunker import ASTAwareChunker, StubASTAwareChunker
from deepguard_parsers.dependency_graph import cap_dependency_graph_depth
from deepguard_parsers.iac.registry import IaC_PARSERS, parse_iac_file, register_iac_parser

__all__ = [
    "ASTAwareChunker",
    "IaC_PARSERS",
    "StubASTAwareChunker",
    "cap_dependency_graph_depth",
    "parse_iac_file",
    "register_iac_parser",
]

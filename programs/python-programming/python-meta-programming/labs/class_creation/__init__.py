"""Executable class-creation evidence for Python Metaprogramming Module 09."""

from .boundaries import DECISIONS, OwnershipDecision, boundary_evidence
from .evidence import build_evidence, render_evidence
from .lifecycle import lifecycle_evidence
from .manual import ClassRecipe, build_class, manual_creation_evidence
from .namespace import DeclarationMeta, DeclarationNamespace, namespace_evidence
from .registry import PluginRegistry, make_plugin_family, registry_evidence
from .resolution import resolution_evidence

__all__ = [
    "ClassRecipe",
    "DECISIONS",
    "DeclarationMeta",
    "DeclarationNamespace",
    "OwnershipDecision",
    "PluginRegistry",
    "boundary_evidence",
    "build_class",
    "build_evidence",
    "lifecycle_evidence",
    "make_plugin_family",
    "manual_creation_evidence",
    "namespace_evidence",
    "registry_evidence",
    "render_evidence",
    "resolution_evidence",
]

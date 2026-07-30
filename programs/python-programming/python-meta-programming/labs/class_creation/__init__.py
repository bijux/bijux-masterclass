"""Executable class-creation evidence for Python Metaprogramming Module 09."""

from .lifecycle import lifecycle_evidence
from .manual import ClassRecipe, build_class, manual_creation_evidence
from .namespace import DeclarationMeta, DeclarationNamespace, namespace_evidence
from .resolution import resolution_evidence

__all__ = [
    "ClassRecipe",
    "DeclarationMeta",
    "DeclarationNamespace",
    "build_class",
    "lifecycle_evidence",
    "manual_creation_evidence",
    "namespace_evidence",
    "resolution_evidence",
]

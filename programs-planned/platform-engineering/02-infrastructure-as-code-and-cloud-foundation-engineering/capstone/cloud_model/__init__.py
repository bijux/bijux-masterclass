"""Dependency-light semantic model for Atlas Cloud Foundation.

This package is deliberately smaller than OpenTofu and AWS. It makes selected
course invariants executable; it is not a provider, IAM simulator, or cloud
control plane.
"""

from .identity import canonical_json, digest_object

__all__ = ["canonical_json", "digest_object"]

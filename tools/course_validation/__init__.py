"""Validation support for the canonical Bijux Courses corpus."""

from .blueprint import validate_blueprint
from .chapter import validate_chapter

__all__ = ["validate_blueprint", "validate_chapter"]

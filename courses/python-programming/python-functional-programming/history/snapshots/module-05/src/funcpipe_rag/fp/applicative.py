"""Backward-compatible name for Module 05 Validation.

The module-05 cores introduce Validation as an applicative; later cores refer to
it as `fp.validation`. This module keeps the earlier import path working.
"""

from .validation import *  # noqa: F403

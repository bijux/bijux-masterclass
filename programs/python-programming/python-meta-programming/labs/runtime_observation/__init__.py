"""Safe runtime-observation evidence used by the Module 02 lab."""

from .debug_view import DebugEntry, build_debug_view
from .evidence import build_evidence, render_evidence

__all__ = ["DebugEntry", "build_debug_view", "build_evidence", "render_evidence"]

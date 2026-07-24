"""Infrastructure adapters implementing domain ports/capabilities (end-of-Module-09)."""

from .atomic_storage import AtomicFileStorage
from .clock import MonotonicTestClock, SystemClock
from .file_storage import FileStorage
from .logger import CollectingLogger, ConsoleLogger
from .memory_storage import InMemoryStorage

__all__ = [
    "AtomicFileStorage",
    "CollectingLogger",
    "ConsoleLogger",
    "FileStorage",
    "InMemoryStorage",
    "MonotonicTestClock",
    "SystemClock",
]

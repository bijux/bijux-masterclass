"""Infrastructure adapters implementing domain ports/capabilities (end-of-Module-07)."""

from .clock import MonotonicTestClock, SystemClock
from .file_storage import FileStorage
from .logger import CollectingLogger, ConsoleLogger
from .memory_storage import InMemoryStorage
from .atomic_storage import AtomicFileStorage

__all__ = [
    "FileStorage",
    "InMemoryStorage",
    "AtomicFileStorage",
    "SystemClock",
    "MonotonicTestClock",
    "ConsoleLogger",
    "CollectingLogger",
]


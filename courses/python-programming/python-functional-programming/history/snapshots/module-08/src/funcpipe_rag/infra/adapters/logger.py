"""Module 07 infra: log sinks (console + test collector)."""

from __future__ import annotations

from funcpipe_rag.domain.capabilities import Logger
from funcpipe_rag.domain.logging import LogEntry


class ConsoleLogger(Logger):
    def log(self, entry: LogEntry) -> None:
        try:
            print(f"[{entry.level}] {entry.msg}")
        except OSError:
            pass


class CollectingLogger(Logger):
    def __init__(self) -> None:
        self.entries: list[LogEntry] = []

    def log(self, entry: LogEntry) -> None:
        self.entries.append(entry)


__all__ = ["ConsoleLogger", "CollectingLogger"]


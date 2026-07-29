from __future__ import annotations

from collections.abc import Iterator

from funcpipe_rag.interop.stdlib_fp import merge_streams, running_sum


def test_stdlib_interop_defers_source_consumption() -> None:
    pulls: list[tuple[str, int]] = []

    def source(name: str, values: tuple[int, ...]) -> Iterator[int]:
        for value in values:
            pulls.append((name, value))
            yield value

    merged = merge_streams(source("left", (1, 2)), source("right", (3,)))

    assert pulls == []
    assert next(merged) == 1
    assert pulls == [("left", 1)]
    assert list(merged) == [2, 3]
    assert pulls == [("left", 1), ("left", 2), ("right", 3)]


def test_stdlib_running_fold_exposes_each_prefix() -> None:
    totals = running_sum([3, -1, 4])

    assert list(totals) == [3, 2, 6]

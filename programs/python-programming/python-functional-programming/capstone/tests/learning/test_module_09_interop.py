from __future__ import annotations

from collections.abc import Iterator

from funcpipe_rag.interop.stdlib_fp import merge_streams, running_sum
from funcpipe_rag.interop.toolz_compat import compose, curried_filter, curried_map, pipe


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


def test_optional_helper_facade_preserves_plain_python_semantics() -> None:
    normalize = compose(str.strip, str.lower)
    select_nonempty = curried_filter(bool)
    lengths = curried_map(len)

    result = pipe(
        ["  ALPHA ", " ", "Beta"],
        curried_map(normalize),
        select_nonempty,
        lengths,
        list,
    )

    assert result == [5, 4]

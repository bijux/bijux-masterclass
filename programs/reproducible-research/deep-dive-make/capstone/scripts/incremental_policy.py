"""Parse the incremental requested-work contract."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path, PurePosixPath


@dataclass(frozen=True)
class IncrementalCase:
    input_path: PurePosixPath
    must_rebuild: tuple[PurePosixPath, ...]
    must_remain: tuple[PurePosixPath, ...]

    @property
    def governed_outputs(self) -> frozenset[PurePosixPath]:
        return frozenset((*self.must_rebuild, *self.must_remain))


def _paths(raw: str, line: int) -> tuple[PurePosixPath, ...]:
    paths = tuple(PurePosixPath(value) for value in raw.split(",") if value)
    if not paths or any(path.is_absolute() or ".." in path.parts for path in paths):
        raise ValueError(f"line {line}: paths must be safe repository-relative names")
    return paths


def read_incremental_policy(path: Path) -> list[IncrementalCase]:
    cases: list[IncrementalCase] = []
    inputs: set[PurePosixPath] = set()
    for line, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw or raw.startswith("#"):
            continue
        fields = raw.split("\t")
        if len(fields) != 3:
            raise ValueError(f"line {line}: expected input, rebuild, and remain fields")
        input_path = _paths(fields[0], line)[0]
        rebuild = _paths(fields[1], line)
        remain = _paths(fields[2], line)
        if input_path in inputs:
            raise ValueError(f"line {line}: duplicate input: {input_path}")
        if set(rebuild) & set(remain):
            raise ValueError(
                f"line {line}: output cannot be both rebuilt and unchanged"
            )
        if len(set(rebuild)) != len(rebuild) or len(set(remain)) != len(remain):
            raise ValueError(f"line {line}: output names must not repeat")
        inputs.add(input_path)
        cases.append(IncrementalCase(input_path, rebuild, remain))
    if not cases:
        raise ValueError("incremental policy contains no cases")
    governed_outputs = cases[0].governed_outputs
    for case in cases[1:]:
        if case.governed_outputs != governed_outputs:
            raise ValueError(
                f"input {case.input_path}: governed output set differs from the first case"
            )
    return cases

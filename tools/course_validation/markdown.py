from __future__ import annotations

import re
from dataclasses import dataclass

FENCE = re.compile(r"^(?: {0,3})(?P<fence>`{3,}|~{3,})(?P<info>.*)$")
ATX_HEADING = re.compile(r"^(?: {0,3})(?P<marks>#{1,6})(?:[ \t]+(?P<title>.*)|[ \t]*)$")


@dataclass(frozen=True)
class Heading:
    level: int
    title: str
    start: int
    end: int


def _heading_title(raw: str) -> str:
    return re.sub(r"[ \t]+#+[ \t]*$", "", raw).strip()


def headings(text: str, level: int | None = None) -> tuple[Heading, ...]:
    found: list[Heading] = []
    open_marker: str | None = None
    open_length = 0
    offset = 0
    for line_with_ending in text.splitlines(keepends=True):
        line = line_with_ending.rstrip("\r\n")
        if open_marker is not None:
            if re.fullmatch(rf" {{0,3}}{re.escape(open_marker)}{{{open_length},}}[ \t]*", line):
                open_marker = None
                open_length = 0
            offset += len(line_with_ending)
            continue
        fence = FENCE.match(line)
        if fence:
            marker = fence.group("fence")
            open_marker = marker[0]
            open_length = len(marker)
            offset += len(line_with_ending)
            continue
        match = ATX_HEADING.match(line)
        if match:
            heading_level = len(match.group("marks"))
            if level is None or heading_level == level:
                found.append(
                    Heading(
                        level=heading_level,
                        title=_heading_title(match.group("title") or ""),
                        start=offset,
                        end=offset + len(line_with_ending),
                    )
                )
        offset += len(line_with_ending)
    return tuple(found)


def prose_only(text: str) -> str:
    output: list[str] = []
    open_marker: str | None = None
    open_length = 0
    for line_with_ending in text.splitlines(keepends=True):
        line = line_with_ending.rstrip("\r\n")
        ending = line_with_ending[len(line):]
        if open_marker is not None:
            output.append(" " * len(line) + ending)
            if re.fullmatch(rf" {{0,3}}{re.escape(open_marker)}{{{open_length},}}[ \t]*", line):
                open_marker = None
                open_length = 0
            continue
        fence = FENCE.match(line)
        if fence:
            marker = fence.group("fence")
            open_marker = marker[0]
            open_length = len(marker)
            output.append(" " * len(line) + ending)
            continue
        output.append(line_with_ending)
    return "".join(output)

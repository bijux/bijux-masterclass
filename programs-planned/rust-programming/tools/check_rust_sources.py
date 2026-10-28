#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
OPEN_TO_CLOSE = {"(": ")", "[": "]", "{": "}"}
CLOSERS = set(OPEN_TO_CLOSE.values())


def raw_string_prefix(text: str, index: int) -> tuple[int, str] | None:
    """Return (content_start, terminator) when index starts r#*\" or br#*\"."""
    cursor = index
    if text.startswith("br", cursor):
        cursor += 2
    elif text.startswith("r", cursor):
        cursor += 1
    else:
        return None
    hashes = 0
    while cursor < len(text) and text[cursor] == "#":
        hashes += 1
        cursor += 1
    if cursor >= len(text) or text[cursor] != '"':
        return None
    return cursor + 1, '"' + ("#" * hashes)


def scan(path: Path) -> list[str]:
    text = path.read_text(errors="strict")
    stack: list[tuple[str, int, int]] = []
    errors: list[str] = []
    index = 0
    line = 1
    column = 1

    def advance(count: int = 1) -> None:
        nonlocal index, line, column
        for _ in range(count):
            if index >= len(text):
                return
            if text[index] == "\n":
                line += 1
                column = 1
            else:
                column += 1
            index += 1

    while index < len(text):
        character = text[index]

        if text.startswith("//", index):
            while index < len(text) and text[index] != "\n":
                advance()
            continue

        if text.startswith("/*", index):
            start_line, start_column = line, column
            depth = 0
            while index < len(text):
                if text.startswith("/*", index):
                    depth += 1
                    advance(2)
                elif text.startswith("*/", index):
                    depth -= 1
                    advance(2)
                    if depth == 0:
                        break
                else:
                    advance()
            if depth:
                errors.append(f"unterminated block comment opened at {start_line}:{start_column}")
            continue

        raw = raw_string_prefix(text, index)
        if raw is not None:
            content_start, terminator = raw
            advance(content_start - index)
            end = text.find(terminator, index)
            if end < 0:
                errors.append(f"unterminated raw string opened at {line}:{column}")
                break
            advance(end + len(terminator) - index)
            continue

        if text.startswith('b"', index) or character == '"':
            start_line, start_column = line, column
            if text.startswith('b"', index):
                advance(2)
            else:
                advance()
            escaped = False
            while index < len(text):
                current = text[index]
                if escaped:
                    escaped = False
                    advance()
                elif current == "\\":
                    escaped = True
                    advance()
                elif current == '"':
                    advance()
                    break
                else:
                    advance()
            else:
                errors.append(f"unterminated string opened at {start_line}:{start_column}")
            continue

        # Recognize char and byte-char literals, but leave lifetimes such as 'a untouched.
        char_prefix = 2 if text.startswith("b'", index) else 1 if character == "'" else 0
        if char_prefix:
            start = index
            cursor = index + char_prefix
            if cursor < len(text):
                if text[cursor] == "\\":
                    cursor += 1
                    if cursor < len(text) and text[cursor] == "u" and cursor + 1 < len(text) and text[cursor + 1] == "{":
                        closing = text.find("}", cursor + 2)
                        cursor = len(text) if closing < 0 else closing + 1
                    else:
                        cursor += 1
                else:
                    cursor += 1
                if cursor < len(text) and text[cursor] == "'":
                    advance(cursor + 1 - start)
                    continue

        if character in OPEN_TO_CLOSE:
            stack.append((character, line, column))
            advance()
            continue

        if character in CLOSERS:
            if not stack:
                errors.append(f"unexpected `{character}` at {line}:{column}")
            else:
                opening, opening_line, opening_column = stack.pop()
                expected = OPEN_TO_CLOSE[opening]
                if character != expected:
                    errors.append(
                        f"`{opening}` at {opening_line}:{opening_column} closes as "
                        f"`{character}` at {line}:{column}; expected `{expected}`"
                    )
            advance()
            continue

        advance()

    for opening, opening_line, opening_column in reversed(stack):
        errors.append(
            f"unclosed `{opening}` from {opening_line}:{opening_column}; "
            f"expected `{OPEN_TO_CLOSE[opening]}`"
        )
    return errors


def main() -> int:
    sources = [
        path
        for path in ROOT.rglob("*.rs")
        if "compiler-labs" not in path.relative_to(ROOT).parts
    ]
    problems: list[tuple[Path, str]] = []
    for source in sorted(sources):
        for problem in scan(source):
            problems.append((source.relative_to(ROOT), problem))

    print(f"checked lexical structure of {len(sources)} non-specimen Rust sources")
    for path, problem in problems:
        print(f"BROKEN {path}: {problem}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())

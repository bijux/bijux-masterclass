from __future__ import annotations

import re
from dataclasses import dataclass

FENCE = re.compile(r"^(?: {0,3})(?P<fence>`{3,}|~{3,})(?P<info>.*)$")
ATX_HEADING = re.compile(r"^(?: {0,3})(?P<marks>#{1,6})(?:[ \t]+(?P<title>.*)|[ \t]*)$")
LEGACY_INLINE = re.compile(r"\\\(([^\n]*?)\\\)")
MATH_SPAN = re.compile(r"\$\$.*?\$\$|\$`.*?`\$|\$(?:\\.|[^$\n])+?\$", re.DOTALL)
INLINE_CODE = re.compile(r"`[^`\n]*`")
TEX_COMMAND = re.compile(r"\\[A-Za-z]+")
MATH_TEX_COMMAND = re.compile(
    r"\\(?:alpha|beta|gamma|delta|epsilon|eta|theta|lambda|mu|nu|xi|pi|rho|"
    r"sigma|tau|phi|chi|psi|omega|Gamma|Delta|Theta|Lambda|Pi|Sigma|Phi|Psi|Omega|"
    r"forall|exists|neg|land|lor|Rightarrow|Leftrightarrow|rightarrow|leftarrow|"
    r"leftrightarrow|to|mapsto|in|notin|subset|subseteq|supset|supseteq|setminus|"
    r"cup|cap|times|otimes|oplus|circ|parallel|approx|equiv|sim|simeq|ne|neq|"
    r"le|leq|ge|geq|prec|preceq|succ|succeq|vdash|models|sum|prod|int|lim|log|"
    r"ln|exp|min|max|Pr|frac|tfrac|dfrac|sqrt|binom|langle|rangle|lfloor|rfloor|"
    r"lceil|rceil|mathbb|mathcal|mathrm|mathbf|mathsf|operatorname|text|begin|end|"
    r"hat|bar|overline|underline|partial|nabla|infty|varnothing|bot|top|Downarrow|"
    r"Uparrow|rightharpoonup|ldots|cdots|quad|qquad)\b"
)
HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
BIJUX_VERIFY_COMMENT = re.compile(r"<!-- bijux-verify:.*?-->[ \t]*(?:\n|$)", re.DOTALL)
MARKDOWN_LINK = re.compile(r"!?\[[^\]\n]*\]\([^\n)]*\)")
BARE_MATH_COMMAND = re.compile(
    r"(?<![\\A-Za-z])(?:operatorname|Theta|Omega|Delta|Gamma|Lambda|Sigma|Phi|Psi|"
    r"lceil|rceil|lfloor|rfloor|log|ln|Pr|binom)(?=\b|[_({])"
)
SIMPLE_MATH_EXPRESSION = re.compile(r"[A-Za-z0-9_{}.,+*/^'\-\[\] ]+")


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


def _map_unfenced_lines(text: str, transform: callable) -> str:
    """Apply a line-local transformation while preserving fenced code verbatim."""
    output: list[str] = []
    open_marker: str | None = None
    open_length = 0
    for line_with_ending in text.splitlines(keepends=True):
        line = line_with_ending.rstrip("\r\n")
        if open_marker is not None:
            output.append(line_with_ending)
            if re.fullmatch(rf" {{0,3}}{re.escape(open_marker)}{{{open_length},}}[ \t]*", line):
                open_marker = None
                open_length = 0
            continue
        fence = FENCE.match(line)
        if fence:
            marker = fence.group("fence")
            open_marker = marker[0]
            open_length = len(marker)
            output.append(line_with_ending)
            continue
        output.append(transform(line_with_ending))
    return "".join(output)


def _normalize_broken_math_closers(line: str) -> str:
    """Repair a truncated legacy close delimiter without guessing prose spans."""
    line = re.sub(r"\$([^$\n]*)\\\$", r"$\1$", line)

    def replace_parenthesis(match: re.Match[str]) -> str:
        content = match.group(1)
        trimmed = content.rstrip()
        if trimmed.endswith("\\"):
            trimmed = trimmed[:-1]
        return "$" + trimmed + "$"

    return re.sub(r"\\?\(([^()\n]*?)\\\)", replace_parenthesis, line)


def _map_outside_inline_code_and_comments(line: str, transform: callable) -> str:
    """Transform visible prose while preserving code spans and HTML comments."""
    output: list[str] = []
    cursor = 0
    protected = sorted(
        (*INLINE_CODE.finditer(line), *HTML_COMMENT.finditer(line)),
        key=lambda match: match.start(),
    )
    for match in protected:
        if match.start() < cursor:
            continue
        output.append(transform(line[cursor : match.start()]))
        output.append(match.group(0))
        cursor = match.end()
    output.append(transform(line[cursor:]))
    return "".join(output)


def _without_inline_code_and_comments(text: str) -> str:
    """Blank protected Markdown spans without changing offsets or line numbers."""

    def blank(match: re.Match[str]) -> str:
        return "".join("\n" if character == "\n" else " " for character in match.group(0))

    return INLINE_CODE.sub(blank, HTML_COMMENT.sub(blank, text))


def _normalize_bare_math_commands(content: str) -> str:
    """Repair command names whose TeX escape was lost in legacy prose."""
    return BARE_MATH_COMMAND.sub(lambda match: "\\" + match.group(0), content)


def _looks_like_parenthetical_math(content: str) -> bool:
    candidate = content.strip()
    if not candidate or len(candidate) > 180:
        return False
    if any(token in candidate for token in ("http://", "https://", ";", "?", "!")):
        return False
    if re.fullmatch(r"[A-Za-z](?:_[A-Za-z0-9{}]+|\^[A-Za-z0-9{}+\-]+)?", candidate):
        return True
    if BARE_MATH_COMMAND.search(candidate) or MATH_TEX_COMMAND.search(candidate):
        return True
    if re.search(r"(?:=|!=|<=|>=|<|>|≤|≥|≠|≈|→|←|↔|∈|∉|⊂|⊆|∧|∨|⇒|⇔)", candidate):
        return True
    if re.search(r"(?:^|[^A-Za-z])(?:O|o)\([^()]+\)$", candidate):
        return True
    function = re.match(r"([A-Za-z][A-Za-z0-9_']*)\(", candidate)
    if function and (
        len(function.group(1)) == 1
        or function.group(1)[0].isupper()
        or "_" in function.group(1)
    ):
        return True
    if re.fullmatch(r"[A-Za-z](?:_[A-Za-z0-9{}]+)?\[[^\]\n]+[\])]", candidate):
        return True
    if SIMPLE_MATH_EXPRESSION.fullmatch(candidate) and re.search(
        r"(?:\.{2,}|\[|\]|\+|-|\*|/|\^)",
        candidate,
    ):
        words = re.findall(r"[A-Za-z]+", candidate)
        if words and all(len(word) == 1 for word in words):
            return True
    if re.fullmatch(
        r"[A-Za-z](?:_[A-Za-z0-9{}]+)?(?:\s*,\s*[A-Za-z](?:_[A-Za-z0-9{}]+)?)+",
        candidate,
    ):
        return True
    return False


def _normalize_parenthetical_math_fragment(fragment: str) -> str:
    """Convert conservative, balanced parenthetical notation to inline math."""
    if "$" in fragment:
        return fragment
    pairs: list[tuple[int, int, int]] = []
    stack: list[tuple[int, int]] = []
    square_depth = 0
    for index, character in enumerate(fragment):
        if character == "[":
            square_depth += 1
        elif character == "]" and square_depth:
            square_depth -= 1
        elif character == "(":
            stack.append((index, square_depth))
        elif character == ")" and square_depth > (stack[-1][1] if stack else 0):
            # A half-open interval such as [0,n) consumes this closer.
            square_depth -= 1
        elif character == ")" and stack:
            start, _start_square_depth = stack.pop()
            pairs.append((start, index, len(stack)))
    selected: list[tuple[int, int]] = []
    for start, end, _depth in sorted(pairs, key=lambda pair: (pair[0], -pair[1])):
        if any(parent_start <= start and end <= parent_end for parent_start, parent_end in selected):
            continue
        if any(open_start < start for open_start, _square_depth in stack):
            # The surrounding group crosses a protected Markdown span. Leave
            # the nested pair for explicit authorial repair as one unit.
            continue
        if start and (fragment[start - 1].isalnum() or fragment[start - 1] in "_}]"):
            # This pair is an argument inside a larger undelimited expression,
            # not a prose wrapper around a complete mathematical fragment.
            continue
        if _looks_like_parenthetical_math(fragment[start + 1 : end]):
            selected.append((start, end))
    for start, end in sorted(selected, reverse=True):
        content = _normalize_bare_math_commands(fragment[start + 1 : end].strip())
        content = content.replace("<=", r"\le ").replace(">=", r"\ge ").replace("!=", r"\ne ")
        content = re.sub(r"\s+in\s+", r" \\in ", content)
        content = content.replace("...", r"\ldots")
        fragment = fragment[:start] + "$" + content + "$" + fragment[end + 1 :]
    return fragment


def _normalize_parenthetical_math_line(line: str) -> str:
    """Apply parenthetical normalization outside existing math and links."""
    output: list[str] = []
    cursor = 0
    protected = sorted(
        (*MATH_SPAN.finditer(line), *MARKDOWN_LINK.finditer(line)),
        key=lambda match: match.start(),
    )
    for match in protected:
        if match.start() < cursor:
            continue
        output.append(_normalize_parenthetical_math_fragment(line[cursor : match.start()]))
        output.append(match.group(0))
        cursor = match.end()
    output.append(_normalize_parenthetical_math_fragment(line[cursor:]))
    return "".join(output)


def _normalize_existing_math_commands(line: str) -> str:
    """Restore a narrow allowlist of TeX command escapes inside inline math."""

    def replace(match: re.Match[str]) -> str:
        span = match.group(0)
        if span.startswith("$$"):
            return "$$" + _normalize_bare_math_commands(span[2:-2]) + "$$"
        return "$" + _normalize_bare_math_commands(span[1:-1]) + "$"

    return MATH_SPAN.sub(replace, line)


def normalize_parenthetical_math(text: str) -> str:
    """Normalize conservative legacy parenthetical notation without touching code."""
    in_display_math = False

    def normalize_line(line_with_ending: str) -> str:
        nonlocal in_display_math
        ending = line_with_ending[len(line_with_ending.rstrip("\r\n")) :]
        line = line_with_ending[: len(line_with_ending) - len(ending)] if ending else line_with_ending
        if line.strip() == "$$":
            in_display_math = not in_display_math
            return line_with_ending
        if in_display_math:
            return line_with_ending
        line = _map_outside_inline_code_and_comments(
            line,
            lambda fragment: _normalize_parenthetical_math_line(
                fragment.replace("\x08inom", r"\binom")
            ),
        )
        return line + ending

    return _map_unfenced_lines(text, normalize_line)


def normalize_github_math(text: str) -> str:
    """Normalize legacy TeX Markdown syntax to GitHub's supported math syntax.

    The conversion intentionally limits inference to explicit legacy delimiters
    and malformed close markers. Fenced examples, inline code, and HTML comments
    are never rewritten.
    """
    in_display_math = False

    def normalize_line(line_with_ending: str) -> str:
        nonlocal in_display_math
        ending = line_with_ending[len(line_with_ending.rstrip("\r\n")) :]
        line = line_with_ending[: len(line_with_ending) - len(ending)] if ending else line_with_ending
        stripped = line.strip()
        if stripped == r"\[":
            in_display_math = True
            return f"{line[: len(line) - len(line.lstrip())]}$$" + ending
        if stripped == r"\]":
            in_display_math = False
            return f"{line[: len(line) - len(line.lstrip())]}$$" + ending
        if stripped == "$$":
            in_display_math = not in_display_math
            return line + ending
        if in_display_math:
            return _normalize_bare_math_commands(line) + ending
        line = _map_outside_inline_code_and_comments(
            line,
            lambda fragment: LEGACY_INLINE.sub(
                lambda match: f"${match.group(1)}$",
                _normalize_broken_math_closers(fragment),
            ),
        )
        line = _map_outside_inline_code_and_comments(line, _normalize_existing_math_commands)
        return line + ending

    return _map_unfenced_lines(text, normalize_line)


def github_math_issues(text: str) -> tuple[str, ...]:
    """Return Markdown rendering defects that invalidate GitHub math rendering."""
    issues: list[str] = []
    prose = prose_only(text)
    prose = BIJUX_VERIFY_COMMENT.sub("", prose)
    code_spans = tuple(INLINE_CODE.finditer(HTML_COMMENT.sub("", prose)))
    visible = _without_inline_code_and_comments(prose)
    if r"\[" in visible or r"\]" in visible:
        issues.append("use GitHub display math delimiters ($$), not \\[...\\]")
    if r"\(" in visible or r"\)" in visible:
        issues.append("use GitHub inline math delimiters ($...$), not \\(...\\)")
    if any(MATH_TEX_COMMAND.search(match.group(0)[1:-1]) for match in code_spans):
        issues.append("mathematical TeX must use math delimiters rather than inline code")
    if "\x08inom" in visible:
        issues.append("damaged TeX binomial command must be repaired")
    math_spans = tuple(MATH_SPAN.finditer(visible))
    if any(BARE_MATH_COMMAND.search(match.group(0)) for match in math_spans):
        issues.append("TeX command inside math is missing its escape")
    inline_residual = MATH_SPAN.sub("", visible).replace(r"\$", "")
    inline_residual = re.sub(r"(?m)^\s*\$\$\s*$", "", inline_residual)
    if "$" in inline_residual:
        issues.append("inline math delimiters must be balanced or literal dollars escaped")
    display_delimiters = sum(1 for line in prose.splitlines() if line.strip() == "$$")
    if display_delimiters % 2:
        issues.append("display math delimiters must be balanced")
    return tuple(issues)


def github_math_diagnostics(text: str) -> tuple[str, ...]:
    """Report remaining TeX-like prose that requires an authorial rendering review."""
    prose = prose_only(text)
    prose = BIJUX_VERIFY_COMMENT.sub("", prose)
    visible = _without_inline_code_and_comments(prose)
    residual = MATH_SPAN.sub("", visible)
    if TEX_COMMAND.search(residual):
        return ("remaining TeX command outside recognized math delimiters",)
    return ()

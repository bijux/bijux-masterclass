#!/usr/bin/env python3
"""Insert consistent pedagogic page maps into course-book and capstone docs."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from audit_masterclass_docs import REPO_ROOT, iter_markdown


PROGRAM_TITLES = {
    "deep-dive-make": "Deep Dive Make",
    "deep-dive-snakemake": "Deep Dive Snakemake",
    "deep-dive-dvc": "Deep Dive DVC",
    "python-object-oriented-programming": "Python Object-Oriented Programming",
    "python-functional-programming": "Python Functional Programming",
    "python-meta-programming": "Python Meta-Programming",
}

FAMILY_TITLES = {
    "reproducible-research": "Reproducible Research",
    "python-programming": "Python Programming",
}

START_MARKER = "<!-- page-maps:start -->"
END_MARKER = "<!-- page-maps:end -->"


def sanitize(label: str) -> str:
    clean = re.sub(r"\s+", " ", label.strip())
    return clean.replace('"', "'")


def humanize_slug(slug: str) -> str:
    cleaned = re.sub(r"^\d+-", "", slug)
    cleaned = re.sub(r"^module-\d+-", "", cleaned)
    cleaned = re.sub(r"^module-\d+$", lambda m: m.group(0).replace("-", " ").title(), cleaned)
    cleaned = cleaned.replace(".md", "").replace("-", " ")
    return " ".join(word.capitalize() if word.islower() else word for word in cleaned.split())


def extract_title(text: str) -> str | None:
    in_fence = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence and line.startswith("# "):
            return line[2:].strip()
    return None


def derive_context(path: Path, title: str, kind: str) -> tuple[str, str, str]:
    rel = path.relative_to(REPO_ROOT)
    _, family, program, section, *rest = rel.parts
    family_title = FAMILY_TITLES[family]
    program_title = PROGRAM_TITLES[program]

    if kind == "capstone":
        section_label = "Capstone guide"
        if rest:
            section_label = humanize_slug(rest[0])
        return family_title, program_title, section_label

    if section == "course-book":
        if not rest:
            return family_title, program_title, "Course home"

        first = rest[0]
        if first == "index.md":
            return family_title, program_title, "Course home"
        if first == "capstone.md":
            return family_title, program_title, "Capstone guide"
        if first.startswith("module-") and len(rest) == 1:
            return family_title, program_title, humanize_slug(first)
        if first.startswith("module-") and len(rest) > 1:
            return family_title, program_title, humanize_slug(first)
        if len(rest) == 1:
            return family_title, program_title, humanize_slug(first)
        return family_title, program_title, humanize_slug(rest[0])

    return family_title, program_title, sanitize(title)


def build_block(path: Path, text: str, kind: str) -> str | None:
    title = extract_title(text)
    if title is None:
        return None

    family_title, program_title, section_label = derive_context(path, title, kind)
    page_title = sanitize(title)

    if kind == "capstone":
        heading = "## Guide Maps"
        diagram_a = f"""```mermaid
graph LR
  family["{sanitize(family_title)}"]
  program["{sanitize(program_title)}"]
  guide["Capstone docs"]
  section["{sanitize(section_label)}"]
  page["{page_title}"]
  proof["Proof route"]

  family --> program --> guide --> section --> page
  page -.checks against.-> proof
```"""
        diagram_b = """```mermaid
flowchart LR
  orient["Read the guide boundary"] --> inspect["Inspect the named files, targets, or artifacts"]
  inspect --> run["Run the confirm, demo, selftest, or proof command"]
  run --> compare["Compare output with the stated contract"]
  compare --> review["Return to the course claim with evidence"]
```"""
    else:
        heading = "## Page Maps"
        diagram_a = f"""```mermaid
graph LR
  family["{sanitize(family_title)}"]
  program["{sanitize(program_title)}"]
  section["{sanitize(section_label)}"]
  page["{page_title}"]
  capstone["Capstone evidence"]

  family --> program --> section --> page
  page -.applies in.-> capstone
```"""
        diagram_b = """```mermaid
flowchart LR
  orient["Orient on the page map"] --> read["Read the main claim and examples"]
  read --> inspect["Inspect the related code, proof, or capstone surface"]
  inspect --> verify["Run or review the verification path"]
  verify --> apply["Apply the idea back to the module and capstone"]
```"""

    return (
        f"{START_MARKER}\n"
        f"{heading}\n\n"
        f"{diagram_a}\n\n"
        f"{diagram_b}\n"
        f"{END_MARKER}\n"
    )


def insert_block(text: str, block: str) -> str:
    if START_MARKER in text and END_MARKER in text:
        pattern = re.compile(
            rf"{re.escape(START_MARKER)}.*?{re.escape(END_MARKER)}\n?",
            re.DOTALL,
        )
        return pattern.sub(block, text, count=1)

    lines = text.splitlines(keepends=True)
    for index, line in enumerate(lines):
        if line.startswith("# "):
            insert_at = index + 1
            while insert_at < len(lines) and lines[insert_at].strip() == "":
                insert_at += 1
            block_text = "\n" + block + "\n"
            return "".join(lines[:insert_at]) + block_text + "".join(lines[insert_at:])
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Exit non-zero if page maps are missing.")
    args = parser.parse_args()

    changed = 0
    missing = []

    for kind in ("course-book", "capstone"):
        for path in iter_markdown(kind):
            text = path.read_text(encoding="utf-8")
            block = build_block(path, text, kind)
            if block is None:
                missing.append(path.relative_to(REPO_ROOT).as_posix())
                continue
            updated = insert_block(text, block)
            if START_MARKER not in text or updated != text:
                if not args.check:
                    path.write_text(updated, encoding="utf-8")
                changed += int(updated != text)

    if missing:
        print("Missing H1 for page-map insertion:")
        for item in missing:
            print(item)

    if args.check:
        if missing:
            return 1
        return 0

    print(f"Updated {changed} files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

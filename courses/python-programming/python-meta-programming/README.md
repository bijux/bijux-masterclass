<a id="top"></a>
# Python Metaprogramming: A Correctness-First Deep Dive

[![License](https://img.shields.io/github/license/bijux/python-meta-programming?style=flat-square)](https://github.com/bijux/python-meta-programming/blob/main/LICENSE)
[![Docs](https://img.shields.io/badge/docs-live-blue?style=flat-square)](https://bijux.github.io/python-meta-programming/)
[![Pages](https://img.shields.io/github/actions/workflow/status/bijux/python-meta-programming/pages.yml?branch=main&label=pages&style=flat-square)](https://github.com/bijux/python-meta-programming/actions/workflows/pages.yml)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue?style=flat-square)](https://www.python.org/)
[![MkDocs Material](https://img.shields.io/badge/mkdocs-material-informational?style=flat-square)](https://squidfunk.github.io/mkdocs-material/)

**A rigorous, correctness-first course on Python metaprogramming** — covering introspection, decorators, descriptors, and metaclasses with a focus on traceable runtime behavior, engineering contracts, and professional responsibility.

This is not a collection of clever tricks. It is a systematic exploration of Python’s most powerful (and most dangerous) features, designed to help you reason confidently about what actually happens at runtime and avoid subtle bugs that arise from misunderstanding the language model.

- **Live documentation**: https://bijux.github.io/python-meta-programming/
- **Author hub**: https://bijux.github.io/

<span style="font-size: 1em;">[Back to top](#top)</span>

---

<a id="toc"></a>
## Table of Contents

1. [Why this course?](#why)
2. [Target audience](#audience)
3. [Course structure](#structure)
4. [Key principles](#principles)
5. [Running the docs locally](#local)
6. [Related projects](#related)
7. [Contributing](#contributing)
8. [License](#license)

<span style="font-size: 1em;">[Back to top](#top)</span>

---

<a id="why"></a>
## Why this course?

Python metaprogramming is where the language’s flexibility shines — and where reliability most often breaks down. Many resources present decorators, descriptors, and metaclasses as “magic” patterns without clearly delineating:

- What is guaranteed by the language specification,
- What is CPython-specific,
- What invariants must hold for correctness,
- What breaks under refactoring, typing tools, debugging, or concurrency.

This course treats every mechanism as an **engineering contract**. Every claim is backed by minimal, runnable examples that demonstrate the exact runtime behavior. The goal is not to teach the most advanced tricks, but to give you a mental model you can trust when building or maintaining complex systems.

<span style="font-size: 1em;">[Back to top](#top)</span>

---

<a id="audience"></a>
## Target audience

This material is intended for:

- Intermediate to advanced Python developers who already write clean, idiomatic code and now need to understand (or review) framework-level internals.
- Library authors and framework maintainers who want to make informed trade-offs when using descriptors, metaclasses, or advanced decorators.
- Engineers responsible for codebases that rely on heavy metaprogramming (ORMs, serialization libraries, plugin systems, etc.).

**Prerequisites**: Solid understanding of Python classes, functions, inheritance, and basic introspection (`dir`, `getattr`, etc.). Familiarity with type hints is helpful but not required.

<span style="font-size: 1em;">[Back to top](#top)</span>

---

<a id="structure"></a>
## Course structure

The course is divided into focused modules that build progressively:

- **00 – Overview and Introduction**
- **01 – Everything Is an Object**
- **02 – Basic Introspection**
- **03 – The `inspect` Module**
- **04 – Decorators: Fundamentals**
- **05 – Decorators: Production Patterns & Typing**
- **06 – Class Decorators, `@property`, and the Typing Bridge**
- **07 – The Descriptor Protocol (Part 1)**
- **08 – The Descriptor Protocol (Part 2 – Framework Grade)**
- **09 – Metaclasses**
- **10 – Professional Responsibility & the Outer Darkness**
- **11 – Outro**

Each module includes runnable code examples, visual diagrams, precise definitions, and a glossary of terms.

<span style="font-size: 1em;">[Back to top](#top)</span>

---

<a id="principles"></a>
## Key principles

- **Correctness over cleverness** – Prefer the simplest tool (plain code → descriptors → decorators → metaclasses) that solves the problem reliably.
- **Explicit contracts** – Every advanced feature is presented with its runtime invariants and failure modes.
- **Tooling-friendly** – Patterns preserve introspection, signatures, tracebacks, and static typing where possible.
- **Professional responsibility** – Clear red lines for production use (e.g., no monkey-patching stdlib types, no in-process eval of untrusted input).

<span style="font-size: 1em;">[Back to top](#top)</span>

---

<a id="local"></a>
## Running the documentation locally

The site is built with MkDocs Material. To preview locally:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -r requirements-docs.txt
mkdocs serve
```

To validate the build exactly as CI does:

```bash
mkdocs build --strict
```

<span style="font-size: 1em;">[Back to top](#top)</span>

---

<a id="related"></a>
## Related projects

Other correctness-focused deep dives in the same style:

- **bijux hub**: https://bijux.github.io/
- **bijux-cli**: https://bijux.github.io/bijux-cli/
- **Deep Dive Make**: https://bijux.github.io/deep-dive-make/

<span style="font-size: 1em;">[Back to top](#top)</span>

---

<a id="contributing"></a>
## Contributing

Contributions are welcome and encouraged. The bar is deliberately high to maintain rigor:

- Include a minimal, self-contained example that demonstrates the change or fixes the issue.
- Add or update verification code (runnable snippets) that proves the claim.
- Specify tested Python versions.
- Preserve or improve narrative clarity and consistency.

All contributions must adhere to the course’s tone: precise, evidence-based, and tooling-aware.

<span style="font-size: 1em;">[Back to top](#top)</span>

---

<a id="license"></a>
## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

<span style="font-size: 1em;">[Back to top](#top)</span>

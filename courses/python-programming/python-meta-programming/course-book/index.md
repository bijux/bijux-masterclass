<a id="top"></a>
# Python Metaprogramming: Course Book

**A correctness-first exploration of Python’s metaprogramming mechanisms** — introspection, decorators, descriptors, and metaclasses — grounded in traceable runtime behavior, explicit invariants, and professional engineering discipline.

This repository contains the source material for the course, rendered as a static site using MkDocs Material.

- **Live documentation**: https://bijux.github.io/python-meta-programming/
- **Repository root**: https://github.com/bijux/python-meta-programming

<span style="font-size: 1em;">[Back to top](#top)</span>

---

<a id="toc"></a>
## Table of Contents

1. [Purpose and scope](#purpose)
2. [Target audience](#audience)
3. [Course structure](#structure)
4. [Methodology and standards](#methodology)
5. [Prerequisites](#prerequisites)
6. [Verification protocol](#verification)
7. [Related projects](#related)
8. [Contributing](#contributing)
9. [License](#license)

<span style="font-size: 1em;">[Back to top](#top)</span>

---

<a id="purpose"></a>
## Purpose and scope

Python’s metaprogramming facilities enable extraordinary flexibility but also introduce significant risks to reliability, debuggability, and maintainability. Many existing resources either focus on superficial patterns or dive directly into advanced constructs without establishing a solid foundation in runtime semantics.

This course addresses that gap by providing a systematic, evidence-based treatment of the core mechanisms:

- Precise delineation of language-guaranteed behavior versus implementation-specific details,
- Clear identification of invariants required for correctness,
- Explicit discussion of failure modes and their observable signatures,
- Emphasis on tooling-friendly, maintainable patterns and clear boundaries for production use.

Every claim is supported by minimal, executable examples that demonstrate the exact runtime behavior.

<span style="font-size: 1em;">[Back to top](#top)</span>

---

<a id="audience"></a>
## Target audience

This material is designed for:

- Intermediate to advanced Python developers seeking a deeper understanding of framework-level internals,
- Library and framework authors who need to make informed decisions when employing descriptors, decorators, or metaclasses,
- Engineers maintaining systems that rely on sophisticated metaprogramming (e.g., ORMs, serialization frameworks, plugin architectures).

**Prerequisites**: Proficiency with Python classes, functions, inheritance, and basic introspection (`dir`, `getattr`, etc.). Familiarity with type hints is beneficial but not required.

<span style="font-size: 1em;">[Back to top](#top)</span>

---

<a id="structure"></a>
## Course structure

The course progresses incrementally through focused modules:

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

Each module includes runnable code examples, visual diagrams, precise definitions, and a dedicated glossary.

<span style="font-size: 1em;">[Back to top](#top)</span>

---

<a id="methodology"></a>
## Methodology and standards

Modules follow a consistent, rigorous structure:

- **Definition** → **Semantics** → **Failure modes** → **Minimal reproducible example** → **Recommended pattern** → **Verification probe**

No assertion is presented without an accompanying executable demonstration. Claims that cannot be verified through small, self-contained programs are considered incomplete.

<span style="font-size: 1em;">[Back to top](#top)</span>

---

<a id="prerequisites"></a>
## Prerequisites

- Python 3.11+ recommended (most content is compatible with 3.10 unless explicitly noted),
- Standard library only for core examples,
- No external dependencies required to run the provided snippets.

<span style="font-size: 1em;">[Back to top](#top)</span>

---

<a id="verification"></a>
## Verification protocol

Readers are encouraged to validate claims immediately:

- Copy provided snippets into a temporary file,
- Execute under the target Python version,
- Treat any discrepancy as a potential issue until resolved.

Discrepancies, ambiguities, or non-runnable examples should be reported via issues or pull requests.

<span style="font-size: 1em;">[Back to top](#top)</span>

---

<a id="related"></a>
## Related projects

This course aligns with other correctness-focused resources in the same style:

- **bijux hub**: https://bijux.github.io/
- **bijux-cli**: https://bijux.github.io/bijux-cli/
- **Deep Dive Make**: https://bijux.github.io/deep-dive-make/

<span style="font-size: 1em;">[Back to top](#top)</span>

---

<a id="contributing"></a>
## Contributing

Contributions that enhance clarity, correctness, or completeness are welcome. Requirements include:

- A minimal, self-contained reproduction or demonstration,
- An updated or new verification probe,
- Specification of tested Python versions,
- Preservation of the course’s precise, evidence-based tone.

<span style="font-size: 1em;">[Back to top](#top)</span>

---

<a id="license"></a>
## License

This project is licensed under the **MIT License**. See the repository root [LICENSE](https://github.com/bijux/python-meta-programming/blob/main/LICENSE) file for details.

<span style="font-size: 1em;">[Back to top](#top)</span>

# Rust Programming — Courses 1–6

This repository is one **sixty-module learning path**, not six unrelated introductions. Each course changes the level of reasoning while preserving the vocabulary built before it:

```text
values and control
        ↓
resources and memory
        ↓
contracts and architecture
        ↓
dataflow and effects
        ↓
syntax and compile-time authority
        ↓
external boundaries and systems proofs
```

The course book is the primary product. Labs isolate one mechanism. Compiler specimens train prediction. Capstones force cross-module transfer. None of those supporting surfaces replaces the chapter explanation.

## Begin

1. Read [How to study this program](START_HERE.md).
2. Learn the shared [Rust reasoning model](REASONING_MODEL.md).
3. Inspect the [sixty-module course map](COURSE_MAP.md).
4. Use the [skill map](SKILL_MAP.md) to understand what each course adds.
5. Track real completion in [PROGRESS.md].

## The six-course sequence

| Course | Course book | You finish able to… | Capstone |
|---:|---|---|---|
| 1 | [Rust Foundations](01-rust-foundations/course-book/index.md) | Learn to read Rust as a typed language, make ownership visible, model valid states, handle failure explicitly, and finish a complete tested program. | **Taskboard** |
| 2 | [Ownership, Lifetimes, and Memory](02-rust-ownership-lifetimes-memory/course-book/index.md) | Deepen ownership until you can design borrowed APIs, cleanup protocols, shared graphs, interior mutability, representation claims, variance, and pinning without folklore. | **Memory Workspace** |
| 3 | [Traits, Generics, and Architectural Design](03-rust-traits-generics-architectural-design/course-book/index.md) | Turn type-level knowledge into architecture: define lawful contracts, choose static or dynamic polymorphism, compose behavior, encode protocols, and evolve public APIs. | **Review Engine** |
| 4 | [Functional Rust](04-rust-functional-programming/course-book/index.md) | Make callable capability, laziness, traversal, failure, accumulation, structural sharing, and effects explicit enough to reason about composition and cost. | **LedgerFlow** |
| 5 | [Rust Metaprogramming](05-rust-metaprogramming/course-book/index.md) | Use generation only where one checked declaration must own several Rust surfaces or validated build data, and keep the expanded program understandable as ordinary Rust. | **CommandForge** |
| 6 | [Rust Systems Programming](06-rust-systems-programming/course-book/index.md) | Cross external boundaries without losing the guarantees built in the first five courses: define representations, track resources, isolate unsafe obligations, and expose safe interfaces. | **FrameVault** |

## Study rhythm

Each course is ten dense study days across two calendar weeks. One module is one full day:

```text
chapter → predictions → repair → focused construction → lab → capstone → explanation
```

Advance only when you can explain the decisive rule and transfer it to a new problem. A passing test suite proves observed behavior, not understanding. An explanation without working code proves vocabulary, not engineering skill. The program requires both.

## Toolchain and dependencies

The program uses Rust 2024 Edition and pins Rust 1.97.1. Courses 1–4 and 6 use the standard library for their main instructional products. Course 5 introduces pinned `proc-macro2`, `quote`, and `syn` only where structural procedural macros require them.

See [Source notes](SOURCE_NOTES.md) for the primary contracts used to verify language, library, Cargo, macro, unsafe, and FFI claims.

## Repository commands

```bash
make audit          # curriculum structure, content, manifests, and source policy
make links          # local Markdown-link validation
make rust-source-audit
make progress       # show the sixty-module progress bar
make compiler-labs  # run all 460 prediction specimens; requires Rust/Cargo
make test           # test all six workspaces; requires Cargo
make starters       # check all independent starters; requires Cargo
make docs           # build the unified book; requires MkDocs
make proof          # strongest included route
```

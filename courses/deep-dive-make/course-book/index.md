<a id="top"></a>
# Deep Dive Make: The Course-Book
A five-module course-book for learning **GNU Make as a declarative build-graph engine**—with an explicit correctness contract. The focus is not “Makefile tricks,” but **semantic discipline**: truthful dependency graphs, atomic outputs, parallel safety, deterministic results, and repeatable verification.  

[![CI](https://github.com/bijux/deep-dive-make/actions/workflows/ci.yaml/badge.svg?branch=main)](https://github.com/bijux/deep-dive-make/actions/workflows/ci.yaml?query=branch%3Amain)
[![GNU Make](https://img.shields.io/badge/GNU%20Make-4.3%2B-blue?style=flat-square)](https://www.gnu.org/software/make/)
[![License](https://img.shields.io/github/license/bijux/deep-dive-make?style=flat-square)](https://github.com/bijux/deep-dive-make/blob/main/LICENSE)
[![Docs](https://img.shields.io/badge/docs-site-blue?style=flat-square)](https://bijux.github.io/deep-dive-make/)
[![Capstone](https://img.shields.io/badge/capstone-make--capstone-green?style=flat-square)](https://github.com/bijux/deep-dive-make/tree/main/make-capstone)

> **At a glance**: progressive modules • minimal, reproducible examples • exercises with verification hooks • a runnable capstone that proves the claims.  
> **Quality bar**: every core assertion is designed to be *testable* using `--trace`, `-p`, and serial/parallel equivalence checks. This course-book assumes **GNU Make 4.3+** and intentionally avoids “hand-wavy” build folklore.
---
## Table of Contents
- [Why this course-book exists](#why-this-course-book-exists)
- [How the course-book is written](#how-the-course-book-is-written)
- [What you will learn](#what-you-will-learn)
- [Prerequisites](#prerequisites)
- [How to read it](#how-to-read-it)
- [Verification via the capstone](#verification-via-the-capstone)
- [Diagnostics playbook](#diagnostics-playbook)
- [Repository links](#repository-links)
- [Contributing](#contributing)
- [License](#license)
---
## Why this course-book exists
Many Make-based systems “work” by accident: undeclared inputs, ordering-by-phony targets, stamp files used as wishful thinking, and recipes that become unsafe the moment `-j` is enabled. These failures are costly because they are **intermittent**, **non-local**, and **hard to reproduce**.
This course-book treats Make as it is: an engine for evaluating a dependency graph. It teaches a strict contract:  
- **Truthful DAG**: all real edges are declared (depfiles, manifests, or principled stamps).  
- **Atomic publication**: outputs appear only when their construction succeeds.  
- **Parallel safety**: `-j` changes throughput, not meaning.  
- **Determinism**: serial and parallel builds converge to the same results.  
- **Self-testing**: invariants are continuously verified, not assumed.  
If you maintain a legacy Makefile or design a new build, the objective is the same: **correctness that survives scale and change**.  
[Back to top](#top)

---
## How the course-book is written
Each module follows a consistent, engineering-first structure:
> **Concept** → **Semantics** → **Failure signatures** → **Minimal repro** → **Repair pattern** → **Verification method**
You are expected to distrust claims that cannot be checked. Where possible, the course-book provides direct verification via:
- `make --trace` (why something rebuilt)
- `make -p` (expanded database: targets/vars/rules)
- serial vs parallel equivalence checks (hashes, manifests, outputs)  
[Back to top](#top)

---
## What you will learn
### Module map

| Module | Title | What it gives you |
|---:|---|---|
| 01 | Foundations | Make semantics, correct rebuild triggers, depfiles, atomicity primitives. |
| 02 | Scaling | Parallelism without races, discovery patterns, repository structure for growth. |
| 03 | Production Practice | Determinism, CI discipline, selftests, constraints that prevent drift. |
| 04 | Semantics Under Pressure | Edge cases that matter in real incidents: precedence, includes, multi-output modeling, rule subtleties. |
| 05 | Hardening | Portability, jobserver correctness, “hermetic-ish” techniques, performance, failure isolation. |

Syllabus: [`module-00.md`](module-00)  
[Back to top](#top)

---
## Prerequisites
You do not need prior Make mastery. You do need the ability to work comfortably in a shell.
Required:
- **GNU Make 4.3+**
- **POSIX shell** (`/bin/sh`)
- **C toolchain** (for the capstone exercises)
**macOS note**: `/usr/bin/make` is BSD Make. Install GNU Make and use `gmake`:
```sh
brew install make
```  
### Required GNU Make Features (Minimum 4.3+)
This course-book and capstone rely on GNU Make 4.3+ for full pattern fidelity:

| Feature               | Introduced | Justification                                      |
|-----------------------|------------|----------------------------------------------------|
| Grouped targets `&:`  | 4.3        | Safe multi-output generators (single invocation)   |
| Improved diagnostics  | 4.0+       | `--trace` and forensics (used extensively)         |
| Parallel safety       | Ongoing    | Jobserver and ordering primitives                  |

Older versions may work for basic modules but lack key parallel-safe primitives. Fallbacks are discussed where relevant.  
[Back to top](#top)

---
## How to read it
Recommended path (best learning outcomes):
1. Start at the syllabus: [`module-00.md`](module-00)
2. Read modules in order (01 → 05)
3. After each module, apply at least one pattern in the capstone and re-run selftests
If you are here for incident response or reference:
* jump to Module 04 and Module 05
* use the diagnostics playbook below  
[Back to top](#top)
---
## Verification via the capstone
The course is paired with an executable reference build: [`make-capstone/`](https://github.com/bijux/deep-dive-make/tree/main/make-capstone). It exists for one reason: **proof**.

From the repository root:
```sh
# Linux (GNU Make)
make -C make-capstone selftest

# macOS (GNU Make)
gmake -C make-capstone selftest
```
A passing run means the core invariants hold on your machine: convergence, serial/parallel equivalence, and negative tests that detect common lies (missing edges, unsafe stamps, non-atomic writes).    
[Back to top](#top)
---
## Diagnostics playbook
When builds misbehave, start here:
* **Unexpected rebuilds**: `make --trace <target>` (find the triggering edge)
* **“It works on my machine” variables**: `make -p` and inspect `origin` / `flavor`
* **Parallel-only failures**: suspect missing edges or non-atomic producers; compare serial/parallel outputs
* **Generated headers / multi-output rules**: model producers explicitly; don’t rely on incidental order
* **Portability / recursion / jobserver**: treat as correctness topics, not convenience features
This course-book is designed to be both a curriculum and an operational reference.  
[Back to top](#top)
---
## Repository links
* Project overview: [`README.md`](https://github.com/bijux/deep-dive-make/blob/main/README.md)
* Capstone: [`make-capstone/`](https://github.com/bijux/deep-dive-make/tree/main/make-capstone)
* CI workflow: [`.github/workflows/ci.yaml`](https://github.com/bijux/deep-dive-make/blob/main/.github/workflows/ci.yaml)  
[Back to top](#top)
---
## Contributing
Contributions are welcome when they improve **correctness**, **clarity**, or **reproducibility** (tight repros, sharper diagnostics, better exercises).
Process:
1. Fork and clone
2. Make a focused change
3. From the repository root, verify:
   ```sh
   make -C make-capstone selftest
   ```
   (or `gmake -C make-capstone selftest` on macOS)
4. Open a PR against `main`, with a short “claim → proof” note  
[Back to top](#top)
---
## License
MIT — see [`LICENSE`](https://github.com/bijux/deep-dive-make/blob/main/LICENSE). © 2025 Bijan Mousavi.  

[Back to top](#top)

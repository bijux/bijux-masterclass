<a id="top"></a>
# Deep Dive Make: The Program Guide

<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive Make"]
  section["Course home"]
  page["Deep Dive Make: The Program Guide"]
  capstone["Capstone evidence"]

  family --> program --> section --> page
  page -.applies in.-> capstone
```

```mermaid
flowchart LR
  orient["Orient on the page map"] --> read["Read the main claim and examples"]
  read --> inspect["Inspect the related code, proof, or capstone surface"]
  inspect --> verify["Run or review the verification path"]
  verify --> apply["Apply the idea back to the module and capstone"]
```
<!-- page-maps:end -->

A ten-module program for learning **GNU Make as a declarative build-graph engine**. The
course is organized around one idea: Make is valuable only when the build graph stays
truthful under change, pressure, and review.

The top-level course-book has three durable surfaces:

- [`guides/`](guides/index.md) for learner routes, module promises, checkpoints, and capstone entry
- [`reference/`](reference/index.md) for durable definitions, anti-pattern maps, and review aids
- Modules `00` to `10` for the teaching arc itself

[![Series Validation](https://github.com/bijux/bijux-masterclass/actions/workflows/program-validation.yml/badge.svg?branch=master)](https://github.com/bijux/bijux-masterclass/actions/workflows/program-validation.yml?query=branch%3Amaster)
[![GNU Make](https://img.shields.io/badge/GNU%20Make-4.3%2B-blue?style=flat-square)](https://www.gnu.org/software/make/)
[![License](https://img.shields.io/github/license/bijux/bijux-masterclass?style=flat-square)](https://github.com/bijux/bijux-masterclass/blob/master/LICENSE)
[![Docs](https://img.shields.io/badge/docs-series-blue?style=flat-square)](https://bijux.io/bijux-masterclass/reproducible-research/deep-dive-make/)
[![Capstone](https://img.shields.io/badge/capstone-reference-green?style=flat-square)](https://github.com/bijux/bijux-masterclass/tree/master/programs/reproducible-research/deep-dive-make/capstone)

> **At a glance**: beginner-to-mastery progression • minimal reproducible examples •
> bounded proof routes • a runnable capstone that corroborates the claims.
> **Quality bar**: every core assertion should be checkable with `--trace`, `-p`,
> serial versus parallel equivalence, or one of the saved review bundles.

---
## Why this program exists

Many Make-based systems “work” by accident: undeclared inputs, phony ordering,
wishful-thinking stamps, and parallel runs that silently change behavior. Deep Dive Make
exists to replace folklore with a stricter contract:

- **truthful DAG**: all semantically real edges are declared
- **atomic outputs**: artifacts appear only when valid
- **parallel safety**: `-j` changes throughput, not meaning
- **determinism**: repeated runs converge to the same state
- **reviewable proof**: build claims can be corroborated with commands and bundles

If the course is doing its job, learners leave with better judgment, not just more syntax.
[Back to top](#top)

---
## Start here
If you are not sure where to begin, use [`start-here.md`](guides/start-here.md) before diving
into the modules. It routes beginners, working maintainers, and build stewards to the
right entry point so the capstone does not become an accidental first lesson.

If your route is shaped by urgency rather than calm study, use
[`pressure-routes.md`](guides/pressure-routes.md).

[Back to top](#top)

---
## Course guide
Use [`course-guide.md`](guides/course-guide.md) when you need one page that groups the course
surfaces by learner need: first entry, stable reference, capstone use, and review use.

[Back to top](#top)

---
## Learning contract
Use [`learning-contract.md`](guides/learning-contract.md) as the stable reference for how this
course teaches: concept, failure mode, repair, and proof. It makes the pedagogical bar
explicit instead of leaving it scattered across modules.

[Back to top](#top)

---
## Use these support pages first

These are the pages that make the course easier to trust and easier to finish:

| Need | Best page |
| --- | --- |
| first learner route | [`start-here.md`](guides/start-here.md) |
| route under repair, stewardship, or incident pressure | [`pressure-routes.md`](guides/pressure-routes.md) |
| stable support hub | [`course-guide.md`](guides/course-guide.md) |
| what each module title actually promises | [`module-promise-map.md`](guides/module-promise-map.md) |
| whether you are ready to move on | [`module-checkpoints.md`](guides/module-checkpoints.md) |
| smallest honest proof route | [`proof-ladder.md`](guides/proof-ladder.md) |
| capstone entry by module | [`capstone-map.md`](guides/capstone-map.md) |

[Back to top](#top)

---
## Course shape at a glance

Use this snapshot when you want the fastest sense of how the arc is organized:

- [Module 00](module-00-orientation/index.md) explains the study strategy, the support surfaces, and the capstone timing.
- [Modules 01-03](module-01-foundations-build-graph-and-truth/index.md) establish graph truth, parallel safety, and production proof habits.
- [Modules 04-06](module-04-cli-precedence-includes-and-rule-edge-cases/index.md) deal with pressure: semantics, hardening, and generated-file boundaries.
- [Modules 07-08](module-07-reusable-build-architecture-and-build-apis/index.md) turn the build into a reusable architecture with trustworthy release surfaces.
- [Modules 09-10](module-09-performance-observability-and-build-incident-response/index.md) finish with incidents, migration, governance, and tool-boundary judgment.
- [Guides](guides/index.md) hold learner routes and capstone entry.
- [Reference](reference/index.md) holds the durable maps, glossaries, anti-patterns, and review standards.

---
## How the guide is written
Each module follows a consistent, engineering-first structure:
> **Concept** → **Semantics** → **Failure signatures** → **Minimal repro** → **Repair pattern** → **Verification method**
You are expected to distrust claims that cannot be checked. Where possible, the guide provides direct verification via:
- `make --trace` (why something rebuilt)
- `make -p` (expanded database: targets/vars/rules)
- serial vs parallel equivalence checks (hashes, manifests, outputs)  
[Back to top](#top)

---
## What you will learn
### Module map

| Module | Title | What it gives you |
|---:|---|---|
| 01 | Foundations: The Build Graph and Truth | The graph model, rebuild truth, and the first dependable Makefiles. |
| 02 | Scaling: Parallelism, Safety, and Large-Project Structure | Parallel safety, discovery patterns, and structure for growth. |
| 03 | Production Practice: Determinism, Debugging, CI Contracts, Selftests, and Disciplined DSL | Determinism, CI discipline, selftests, and forensics that explain rebuilds. |
| 04 | Make Semantics Under Pressure: CLI, Precedence, Includes, and Rule Edge-Cases | CLI semantics, precedence, includes, and rule edge cases you need in incidents. |
| 05 | Hardening: Portability, Jobserver, Hermeticity, Performance, and Failure Modes | Portability, jobserver correctness, modeled inputs, and failure isolation. |
| 06 | Generated Files, Multi-Output Rules, and Pipeline Boundaries | Correct generators, multi-output producers, manifests, and publication boundaries. |
| 07 | Reusable Build Architecture, Layered Includes, and Build APIs | Layered includes, build APIs, macros, and repository-scale structure. |
| 08 | Release Engineering, Packaging, and Artifact Publication Contracts | Packaging, artifact publication, install contracts, and release manifests. |
| 09 | Performance, Observability, and Build Incident Response | Measurement, observability, build triage, and operational runbooks. |
| 10 | Migration, Governance, and Knowing Make's Boundaries | Migration strategy, governance, anti-pattern recognition, and tool-boundary judgment. |

Syllabus: [`module-00-orientation/index.md`](module-00-orientation/index.md)  
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
This program guide and capstone rely on GNU Make 4.3+ for full pattern fidelity:

| Feature               | Introduced | Justification                                      |
|-----------------------|------------|----------------------------------------------------|
| Grouped targets `&:`  | 4.3        | Safe multi-output generators (single invocation)   |
| Improved diagnostics  | 4.0+       | `--trace` and forensics (used extensively)         |
| Parallel safety       | Ongoing    | Jobserver and ordering primitives                  |

Older versions may work for basic modules but lack key parallel-safe primitives. Fallbacks are discussed where relevant.  
[Back to top](#top)

---
## Verification via the capstone

The course is paired with an executable reference build in [`capstone/`](https://github.com/bijux/bijux-masterclass/tree/master/programs/reproducible-research/deep-dive-make/capstone). The capstone is not the first lesson. It is the corroboration surface once the module idea is already legible.

Use these routes in order:

1. [`proof-ladder.md`](guides/proof-ladder.md) to size the proof correctly
2. [`capstone-map.md`](guides/capstone-map.md) to enter by module arc
3. [`command-guide.md`](guides/command-guide.md) when you need the exact command layer

From the repository root, the most useful first commands are:

```sh
make PROGRAM=reproducible-research/deep-dive-make capstone-walkthrough
make PROGRAM=reproducible-research/deep-dive-make inspect
make PROGRAM=reproducible-research/deep-dive-make test
```

Use `gmake` inside `capstone/` on macOS.

[Back to top](#top)
---
## Diagnostics playbook
When builds misbehave, start here:
* **Unexpected rebuilds**: `make --trace <target>` (find the triggering edge)
* **“It works on my machine” variables**: `make -p` and inspect `origin` / `flavor`
* **Parallel-only failures**: suspect missing edges or non-atomic producers; compare serial/parallel outputs
* **Generated headers / multi-output rules**: model producers explicitly; don’t rely on incidental order
* **Portability / recursion / jobserver**: treat as correctness topics, not convenience features
This program guide is designed to be both a curriculum and an operational reference.  
[Back to top](#top)
---
## Review surfaces

When you are reviewing whether the course and capstone are actually coherent, use:

* [`topic-boundaries.md`](reference/topic-boundaries.md)
* [`anti-pattern-atlas.md`](reference/anti-pattern-atlas.md)
* [`module-promise-map.md`](guides/module-promise-map.md)
* [`module-checkpoints.md`](guides/module-checkpoints.md)
* [`completion-rubric.md`](reference/completion-rubric.md)

[Back to top](#top)
---
## Repository links
* Project overview: [`README.md`](https://github.com/bijux/bijux-masterclass/blob/master/programs/reproducible-research/deep-dive-make/README.md)
* Capstone: [`capstone/`](https://github.com/bijux/bijux-masterclass/tree/master/programs/reproducible-research/deep-dive-make/capstone)
* Validation workflow: [`.github/workflows/program-validation.yml`](https://github.com/bijux/bijux-masterclass/blob/master/.github/workflows/program-validation.yml)  
[Back to top](#top)
---
## Contributing
Contributions are welcome when they improve **correctness**, **clarity**, or **reproducibility** (tight repros, sharper diagnostics, better exercises).
Process:
1. Fork and clone
2. Make a focused change
3. From the repository root, verify:
   ```sh
   make -C capstone selftest
   ```
   (or `gmake -C capstone selftest` on macOS)
4. Open a PR against `main`, with a short “claim → proof” note  
[Back to top](#top)
---
## License
MIT — see the repository root [`LICENSE`](https://github.com/bijux/bijux-masterclass/blob/master/LICENSE). © 2025 Bijan Mousavi <bijan@bijux.io>.  

[Back to top](#top)

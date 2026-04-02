<a id="top"></a>
# Deep Dive Make: Program Capstone
The capstone is the executable reference build for **Deep Dive Make**: a compact C project whose Makefiles are written to **prove**, not merely claim, production-grade properties—**truthful DAGs, atomic publication, parallel safety, determinism, and self-testing invariants**. It is the practical companion to the program guide in [`course-book/`](https://github.com/bijux/bijux-masterclass/tree/master/programs/reproducible-research/deep-dive-make/course-book): every major pattern in the text has a living implementation here, with repros for common failure modes and CI-enforced verification.

[![Series Validation](https://github.com/bijux/bijux-masterclass/actions/workflows/program-validation.yml/badge.svg?branch=master)](https://github.com/bijux/bijux-masterclass/actions/workflows/program-validation.yml?query=branch%3Amaster)
[![GNU Make](https://img.shields.io/badge/GNU%20Make-4.3%2B-blue?style=flat-square)](https://www.gnu.org/software/make/)
[![License](https://img.shields.io/github/license/bijux/bijux-masterclass?style=flat-square)](https://github.com/bijux/bijux-masterclass/blob/master/LICENSE)
[![Docs](https://img.shields.io/badge/docs-series-blue?style=flat-square)](https://bijux.io/bijux-masterclass/reproducible-research/deep-dive-make/)
[![Capstone](https://img.shields.io/badge/capstone-reference-green?style=flat-square)](https://github.com/bijux/bijux-masterclass/tree/master/programs/reproducible-research/deep-dive-make/capstone)

> **In one line:** a small build that behaves like a serious build—correct under change, correct under `-j`, and instrumented to catch its own lies.

---
## Table of Contents
- [Who should start here](#who-should-start-here)
- [Purpose](#purpose)
- [Quick start](#quick-start)
- [What selftest proves](#what-selftest-proves)
- [Recommended first walkthrough](#recommended-first-walkthrough)
- [Public targets](#public-targets)
- [What it builds](#what-it-builds)
- [Where it fits in the program](#where-it-fits-in-the-program)
- [Architecture](#architecture)
- [Platform notes](#platform-notes)
- [Repro pack](#repro-pack)
- [Links into the program guide](#links-into-the-program-guide)
- [Contributing](#contributing)
- [License](#license)
---
## Who should start here
Start here if you already understand the course concept you are studying and now want to
see the same idea in a realistic reference build.

Do **not** start here if you still need first exposure to the concept itself. In that
case, use the smaller module exercises first and come back when you want confirmation and
inspection.

[Back to top](#top)

---
## Purpose
This capstone exists to eliminate ambiguity. “Correct Makefiles” should not be a matter of taste; they should be a matter of **verifiable properties**.
This build is designed to enforce:  
- **Truthful DAG**: edges are explicit (depfiles, manifests/stamps where required), with deterministic discovery.  
- **Atomic publication**: outputs are not visible until they are valid.  
- **Parallel safety**: `-j` accelerates execution but does not alter meaning.  
- **Determinism**: serial and parallel runs converge to identical outputs.  
- **Self-tests**: the build system is treated as code—tested, gated, and regression-resistant.    
[Back to top](#top)

---
## Quick start
From this directory (`capstone/`):
```sh
# Linux (GNU Make)
make selftest
```
```sh
# macOS (install GNU Make first, then use gmake)
brew install make
gmake selftest
```
A passing `selftest` is the signal that the contract holds: convergence, serial/parallel equivalence, and negative tests designed to detect common defects.
[Back to top](#top)

---
## What selftest proves
`selftest` is the most important target in this capstone because it verifies build-system
behavior, not just program behavior.

It checks three things:

| Check | What it proves | Why it matters |
| --- | --- | --- |
| convergence | `make all` reaches an up-to-date state | the graph does not keep asking for more work after success |
| serial/parallel equivalence | `-j1` and `-j2` produce the same artifact set | scheduling changes throughput, not meaning |
| negative hidden-input case | an intentionally hidden input breaks convergence | the proof harness can detect lies instead of only happy paths |

The selftest also includes a lightweight trace-volume guardrail so observability costs do
not silently drift upward. The output is grouped into named steps so the learner can see
which proof is running and why it matters.

[Back to top](#top)

---
## Recommended first walkthrough
Use this order the first time you enter the capstone:

1. `make walkthrough`
2. `make help`
3. read `Makefile`
4. read `tests/run.sh`
5. run `make selftest`
6. inspect one file under `repro/`

That route keeps the learner focused on public contract first, proof harness second, and
failure teaching material third.

The walkthrough bundle is written to `artifacts/walkthrough/reproducible-research/deep-dive-make/`.

[Back to top](#top)

---
## Public targets
These are the stable entrypoints you can rely on and extend:

| Target | Meaning | Why you care |
| ------------------- | --------------------------------------------------------------------- | ------------------------------------ |
| `help` | Print available targets and key knobs. | Discoverability. |
| `tour` | Print the recommended walkthrough order. | Faster onboarding into the capstone. |
| `walkthrough` | Write the learner-facing walkthrough bundle. | Durable first-pass reading route. |
| `all` | Build primary artifacts. | Normal build. |
| `test` | Run runtime checks on outputs. | Functional validation. |
| `selftest` | Verify build-system invariants (convergence, equivalence, negatives). | Integrity gate. |
| `discovery-audit` | Confirm discovery is rooted and stable. | Prevent “works on my machine” edges. |
| `attest` | Record toolchain/flag/env facts (non-contaminating by default). | Reproducibility audit. |
| `portability-audit` | Check version/tool assumptions and feature availability. | Cross-platform discipline. |
| `repro` | List available failure repros. | Training + debugging. |
| `clean` | Remove build outputs and stamps. | Reset. |

Optional (explicit opt-in): `USE_EVAL=yes eval-demo` demonstrates quarantined `$(eval)` patterns.  
[Back to top](#top)

---
## What it builds
A deliberately small C project with real build-system pressure points:
* **`app`**: main executable built from a small set of sources.
* **Dynamic binaries**: `src/dynamic/*.c` discovered deterministically and built into `build/bin/dyn*`.
* **Generated header**: `build/include/dynamic.h` generated by `scripts/` and used across translation units.
Core mechanics:
* depfiles (`*.d`) are treated as true edges
* publication is atomic (temp → rename)
* tests assert behavior (not just “it compiled”)  

### Why this capstone is small on purpose

The capstone is intentionally compact so learners can still audit it end to end. The
point is not repository size. The point is exposing real build-system failure classes in a
surface area a human can still reason about.

[Back to top](#top)

---
## Where it fits in the program
The capstone is intentionally strongest after the beginner modules have already taught the
core semantics on smaller local projects.

| Program area | What the capstone lets you verify |
| --- | --- |
| Modules 01-02 | The difference between a truthful graph and a graph that only appears to work. |
| Modules 03-05 | Deterministic discovery, selftests, portability boundaries, and failure-mode evidence. |
| Modules 06-07 | Generated headers, layered `mk/*.mk` architecture, and reusable build helpers. |
| Modules 08-09 | Dist packaging, attestations, performance guardrails, and incident-oriented diagnostics. |
| Module 10 | A compact system you can review for migration boundaries, governance rules, and anti-patterns. |

If you are new to Make, use this repository as corroboration after the early local
exercises, not as your first exposure to syntax.
[Back to top](#top)

---
## Architecture
The Makefiles are intentionally layered so the design stays readable under growth:
```mermaid
graph TD
  capstone["capstone/"]
  capstone --> makefile["Makefile"]
  capstone --> mk["mk/"]
  capstone --> src["src/"]
  capstone --> include["include/"]
  capstone --> scripts["scripts/"]
  capstone --> tests["tests/"]
  capstone --> repro["repro/"]
  capstone --> thirdparty["thirdparty/"]
  mk --> common["common.mk"]
  mk --> macros["macros.mk"]
  mk --> objects["objects.mk"]
  mk --> stamps["stamps.mk"]
  mk --> contract["contract.mk"]
  mk --> rulesEval["rules_eval.mk"]
```
The intent is to model a “real” build in miniature: the same failure modes show up, but the surface area stays small enough to audit.  
[Back to top](#top)

---
## Platform notes
* **macOS**: `/usr/bin/make` is BSD Make—use GNU Make (`gmake`).
* **Toolchains differ**: determinism is verified via stamps/equivalence checks rather than assumed.
* **Portability**: the build declares its boundary (GNU Make floor, shell assumptions) and audits it with `portability-audit`.  
[Back to top](#top)

---
## Repro pack
`repro/` contains small Makefiles that intentionally demonstrate failure modes (often only visible under `-j`), along with the repair patterns taught in the program guide.
Examples include:
* shared append/log races
* temp file collisions and partial writes
* incorrect stamp usage that hides inputs
* incorrect modeling of generated headers
* directory creation hazards
* ambiguous rule-selection and ordering mistakes
Run a repro directly:
```sh
make -f repro/01-shared-append.mk -j4
```  

List the available repro entrypoints:

```sh
make repro
```

Best first route:

1. `repro/01-shared-log.mk`
2. `repro/05-mkdir-race.mk`
3. `repro/06-order-only-misuse.mk`

That route moves from obvious concurrency failure into subtler graph-modeling mistakes.

[Back to top](#top)

---
## Links into the program guide
* Program site: [https://bijux.io/bijux-masterclass/reproducible-research/deep-dive-make/](https://bijux.io/bijux-masterclass/reproducible-research/deep-dive-make/)
* Source chapters: [`course-book/`](https://github.com/bijux/bijux-masterclass/tree/master/programs/reproducible-research/deep-dive-make/course-book)
* Guided route through this repository: [`capstone-map.md`](https://github.com/bijux/bijux-masterclass/blob/master/programs/reproducible-research/deep-dive-make/course-book/capstone-map.md)
The capstone is referenced throughout the modules via “tie-ins.” The expectation is a tight loop:
**read → reproduce → repair → verify**  
[Back to top](#top)

---
## Contributing
Contributions are welcome when they improve **correctness**, **clarity**, or **reproducibility** (new repros, sharper invariants, better diagnostics).
Minimum bar for changes that touch the build (from repository root):
```sh
make PROGRAM=reproducible-research/deep-dive-make test
```
(or `gmake PROGRAM=reproducible-research/deep-dive-make test` on macOS)
Open a PR against `main` with a short “claim → proof” note (what you changed, why it’s correct, and how it’s verified).  
[Back to top](#top)

---
## License
MIT — see the repository root [`LICENSE`](https://github.com/bijux/bijux-masterclass/blob/master/LICENSE). © 2025 Bijan Mousavi <bijan@bijux.io>.  
[Back to top](#top)

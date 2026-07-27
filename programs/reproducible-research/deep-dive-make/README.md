# Deep Dive Make

A standalone course and executable capstone that teaches **GNU Make as a build-graph
engine**, not a scripting language. It starts with a three-line Makefile and grows toward
parallel-safe, deterministic, reviewable builds that other people can trust.

This is a ten-session course for self-study as much as for classroom follow-up. Each
session is designed to stand on its own for a learner who missed the live explanation:

- a plain-language overview
- a small demonstration you can run in minutes
- a worked example that expands the idea
- ten exercises that move from warm-up to design and repair
- explicit exit criteria so you know whether to continue

Orientation, ten full-day modules, and 100 exercises take you from first contact to
long-lived build-system stewardship.
---

## What this is

Most Makefiles “work” until they don’t: hidden inputs, phony ordering, stamp hacks, and parallel builds that silently change behavior.

**Deep Dive Make** is a structured path out of that mess. It teaches Make through a strict contract:

- **Truthful DAG**: every dependency edge is explicit (depfiles, manifests, or principled stamps).
- **Safe publication**: validate before publishing and use set-level atomicity where the
  consumer contract requires it.
- **Parallel safety**: `-j` speeds up builds without changing semantics.
- **Determinism**: serial and parallel builds converge to identical results.
- **Self-testing**: the build validates itself (convergence, equivalence, and failure modes).

This is a practical step toward *real* understanding of Make: what it guarantees, what it does not, and how to design Makefiles that remain correct as projects grow.

The course book has four learning surfaces:

- `course-book/guides/` for learner routes, module promises, checkpoints, and capstone entry
- `course-book/capstone/` for repository entry, command routing, review worksheets, and proof reading
- `course-book/reference/` for durable review maps, glossaries, standards, and anti-patterns
- `course-book/module-00-orientation/` plus Modules `01` to `10` for the core teaching arc

Use the course in this order:

1. `course-book/guides/start-here.md`
2. `course-book/guides/pressure-routes.md`
3. `course-book/guides/course-guide.md`
4. `course-book/guides/module-promise-map.md`
5. `course-book/guides/module-checkpoints.md`
6. `course-book/module-00-orientation/index.md`
7. Modules `01` to `10` in order
8. `course-book/guides/proof-ladder.md`, `course-book/capstone/index.md`, and `course-book/capstone/capstone-map.md` once the local model is clear

## Module map

| Module | Title | Main focus |
| --- | --- | --- |
| `00` | Orientation and Study Practice | establish the learner route, proof ladder, and capstone timing |
| `01` | Build Graph Truth and Rebuild Semantics | make dependency edges and rebuild meaning explicit |
| `02` | Parallel Safety and Project Structure | scale the graph without introducing race-prone structure |
| `03` | Determinism, Debugging, and CI Proof | make builds explainable, repeatable, and self-testing |
| `04` | CLI Semantics, Precedence, and Rule Edge Cases | survive pressure with a correct mental model of Make behavior |
| `05` | Portability, Jobserver, and Failure Modes | harden builds across environments and concurrency settings |
| `06` | Generated Files, Multi-Output Rules, and Pipeline Boundaries | model generators and publication boundaries truthfully |
| `07` | Reusable Build Architecture and Public Build APIs | turn Make into a governable repository architecture |
| `08` | Release Engineering and Artifact Publication Contracts | publish artifacts with explicit install and integrity rules |
| `09` | Performance, Observability, and Incident Response | diagnose build incidents with evidence rather than folklore |
| `10` | Migration, Governance, and Make Boundaries | finish with stewardship, migration, and tool-boundary judgment |

---

## What you get

### 1) Orientation and ten teaching modules

A beginner-to-advanced handbook with explanations, runnable demonstrations, worked
examples, and ten exercises per teaching module. The 100 exercises move from reading a
small graph to diagnosing concurrency, generation, release, performance, and governance
problems in real repositories.

Read on the website: https://bijux.io/bijux-masterclass/reproducible-research/deep-dive-make/

### 2) The executable capstone

`capstone/` is a working build that embodies the rules above and provides a concrete reference for “what correct looks like” under pressure (including parallel builds).

### 3) Review surfaces that keep the course honest

The course now includes dedicated support pages for:

- topic boundaries and blind spots
- module promise tracking
- module-end checkpoints
- anti-pattern routing
- proof sizing and capstone escalation

### 4) A repro pack of failure modes

Small, isolated examples of common pitfalls (races, stamp lies, mkdir hazards, generated header modeling) meant to be *reproduced*, not merely described.

## How one study day works

Every module is written to fill a serious day of independent study.

| Study block | What you do | What you keep |
| --- | --- | --- |
| First contact | run the smallest demonstration | one prediction and one observed result |
| Core lesson | read the concept pages slowly | short notes on what changed in your mental model |
| Guided practice | rebuild the worked example yourself | a working artifact you can explain |
| Exercises 1-5 | establish the rule, vocabulary, and evidence loop | traces, diagrams, and short explanations |
| Exercises 6-10 | repair, extend, and defend the design | a small portfolio of commands and outcomes |
| Exit check | test yourself before moving on | a clear yes-or-no answer about readiness |

If the course ever feels like a pile of pages, return to this table. The goal is to
learn by predicting, running, observing, and explaining, not by browsing.

---

## Begin with the smallest build

If Make is new to you, do not begin by running the capstone. Start with
[Module 00](course-book/module-00-orientation/index.md), where you create one file target,
run it twice, change its input, and watch Make decide whether work is needed. Then complete
Module 01 before using the repository-sized example.

The progression is deliberate:

```mermaid
flowchart LR
  first["One input and one output"] --> trace["Predict and trace a rebuild"]
  trace --> module["Complete the module demonstration"]
  module --> capstone["Inspect the same idea in the capstone"]
  capstone --> proof["Run the proportionate proof route"]
```

From the monorepo root, use these commands after the module-sized example is clear:

### Linux (GNU Make)

```sh
make PROGRAM=reproducible-research/deep-dive-make capstone-walkthrough
make PROGRAM=reproducible-research/deep-dive-make inspect
make PROGRAM=reproducible-research/deep-dive-make test
make PROGRAM=reproducible-research/deep-dive-make proof
```

### macOS (GNU Make via Homebrew)

```sh
brew install make
gmake PROGRAM=reproducible-research/deep-dive-make capstone-walkthrough
gmake PROGRAM=reproducible-research/deep-dive-make inspect
gmake PROGRAM=reproducible-research/deep-dive-make test
gmake PROGRAM=reproducible-research/deep-dive-make proof
```

Use `capstone-walkthrough` to connect the lessons to the repository, `inspect` when you
need the public boundary, `test` for routine proof, and `proof` only when the narrower
routes are no longer enough.

---

## Repository layout

```mermaid
graph TD
  root["bijux-masterclass/programs/reproducible-research/deep-dive-make/"]
  root --> book["course-book/"]
  root --> capstone["capstone/"]
  root --> workflows["../../../../.github/workflows/"]
  root --> license["LICENSE"]
  root --> readme["README.md"]
  book --> m00["module-00-orientation/index.md"]
  book --> m01["module-01-build-graph-foundations-truth/index.md"]
  book --> m02["module-02-parallel-safety-project-structure/index.md"]
  book --> m03["module-03-determinism-debugging-self-testing/index.md"]
  book --> m04["module-04-rule-semantics-precedence-edge-cases/index.md"]
  book --> m05["module-05-portability-hermeticity-failure-modes/index.md"]
  book --> m06["module-06-generated-files-multi-output-pipeline-boundaries/index.md"]
  book --> m07["module-07-build-architecture-layered-includes-apis/index.md"]
  book --> m08["module-08-release-engineering-artifact-contracts/index.md"]
  book --> m09["module-09-performance-observability-incident-response/index.md"]
  book --> m10["module-10-migration-governance-tool-boundaries/index.md"]
  capstone --> capMakefile["Makefile"]
  capstone --> mk["mk/"]
  capstone --> src["src/"]
  capstone --> include["include/"]
  capstone --> scripts["scripts/"]
  capstone --> tests["tests/"]
  capstone --> repro["repro/"]
  workflows --> ci["program-validation.yml"]
```

---

## Who this is for

* Engineers learning Make for the first time and wanting a correctness-first path.
* Engineers inheriting brittle Makefiles and needing a safe migration path.
* People who “know Make” but still get surprised by rebuild behavior or `-j` races.
* Teams that want a build system they can trust in CI and at scale.

This is not “Make syntax tutorials.” It is **build semantics and correctness engineering** with Make as the tool.

---

## Contributing

Contributions that improve correctness, clarity, or reproducibility are welcome (typos, exercises, minimal repros, capstone hardening).

1. Fork & clone `bijux-masterclass`
2. Make a focused change (docs or capstone)
3. From the monorepo root, verify:
   ```sh
   make PROGRAM=reproducible-research/deep-dive-make test
   ```
4. Open a PR against `main`

---

## License

MIT — see the repository root [LICENSE](https://github.com/bijux/bijux-masterclass/blob/main/LICENSE). © 2025-2026 Bijan Mousavi <bijan@bijux.io>.

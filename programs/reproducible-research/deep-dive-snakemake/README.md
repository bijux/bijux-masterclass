# Deep Dive Snakemake

A program guide and executable capstone that teaches **Snakemake as a workflow engine**—not merely a collection of rules and scripts. The objective is to enable the creation of workflows that feature **explicit contracts, safe dynamic behavior, atomic outputs, reproducible execution, and built-in validation**, from first-contact workflow design to long-lived workflow stewardship.

[![Series Validation](https://github.com/bijux/bijux-masterclass/actions/workflows/program-validation.yml/badge.svg?branch=master)](https://github.com/bijux/bijux-masterclass/actions/workflows/program-validation.yml?query=branch%3Amaster)
[![Snakemake](https://img.shields.io/badge/Snakemake-8.0%2B-blue?style=flat-square)](https://snakemake.readthedocs.io/en/stable/)
[![License](https://img.shields.io/github/license/bijux/bijux-masterclass?style=flat-square)](https://github.com/bijux/bijux-masterclass/blob/master/LICENSE)
[![Docs](https://img.shields.io/badge/docs-series-blue?style=flat-square)](https://bijux.io/bijux-masterclass/reproducible-research/deep-dive-snakemake/)
[![Capstone](https://img.shields.io/badge/capstone-reference-green?style=flat-square)](https://github.com/bijux/bijux-masterclass/tree/master/programs/reproducible-research/deep-dive-snakemake/capstone)

> CI executes full confirmation runs including workflow execution and artifact validation.

---

## Who this program is for

- Engineers who already know basic Snakemake syntax and now need stronger workflow design judgment
- Engineers and researchers who want a beginner-to-mastery path instead of scattered Snakemake snippets
- Researchers and platform teams maintaining pipelines that must survive CI, shared filesystems, and long-lived change
- Reviewers who want concrete criteria for deciding whether a workflow is robust or merely convenient

## Who this program is not for

- Readers who only want isolated snippets without understanding workflow contracts
- Teams trying to debug executor behavior before they understand their workflow semantics

## What this is

Many Snakemake workflows function adequately in simple cases but encounter issues under scale: implicit dependencies, checkpoint misuse, non-atomic outputs, configuration drift, or reproducibility failures across environments.

**Deep Dive Snakemake** provides a structured approach to robust design. It emphasizes a strict contract:

- **Explicit inputs/outputs**: every dependency and product is declared and enforced.
- **Atomic publication**: outputs are written safely with no partial artifacts.
- **Dynamic safety**: checkpoints and re-evaluation used correctly without races or surprises.
- **Configuration discipline**: validated schemas and modular composition.
- **Reproducibility**: profiles, manifests, and integrity checks for verifiable runs.
- **Self-validation**: wrapper-driven checks confirm correctness end-to-end.

This repository offers a structured beginner-to-mastery path through Snakemake semantics: understanding its guarantees, limitations, and patterns that ensure workflows remain reliable as complexity increases.

The repository now separates three surfaces clearly:

- `course-book/guides/` for learner entry, study routes, and capstone reading routes
- `course-book/reference/` for stable maps, glossary pages, and review checklists
- `course-book/module-00-orientation/` through `course-book/module-10-*/` for the actual learning arc

[Back to top](#top)

---

## What you should be able to do after this program

- explain why a workflow re-runs using evidence instead of intuition
- distinguish a truthful dynamic DAG from a workflow that only appears to work
- separate workflow logic, profile policy, and published artifact contracts cleanly
- extend a pipeline without weakening its publish boundary or provenance story
- review a Snakemake repository for hidden coupling, poison artifacts, and reproducibility gaps

[Back to top](#top)

---

## What you get

### 1) The program guide

A compact, focused handbook with a full 10-module progression:

- **01 — First Principles**: file contracts, targets, dry-runs, and the basic Snakemake mental model
- **02 — Dynamic DAGs**: checkpoints, deterministic discovery, integrity, and dynamic safety
- **03 — Production Operation**: profiles, retries, staging, and governance
- **04 — Scaling Patterns**: modularity, interfaces, CI gates, and executor-proof semantics
- **05 — Rule Boundaries**: scripts, wrappers, environments, and helper-code discipline
- **06 — Publish Contracts**: versioned outputs, manifests, reports, and downstream trust
- **07 — Workflow Architecture**: modules, file APIs, repository structure, and reuse
- **08 — Operating Contexts**: profiles, executors, storage, and staging policy
- **09 — Incident Response**: performance, observability, and workflow debugging under pressure
- **10 — Mastery**: governance, migration, anti-patterns, and tool-boundary judgment

Read on the website: https://bijux.io/bijux-masterclass/reproducible-research/deep-dive-snakemake/

### 2) The executable capstone

`capstone/` is a complete end-to-end pipeline on toy FASTQ data that embodies the principles above, demonstrating:

- checkpoint-driven sample discovery
- per-sample processing stages
- summary and report generation
- versioned `publish/v1/` outputs
- checksummed manifest and artifact sanity checks
- a Make-driven verification flow

[Back to top](#top)

---

## Recommended background

- Comfortable shell usage and basic Python workflow tooling
- Basic Snakemake familiarity: rules, wildcards, `snakemake -n`, and dry-run interpretation
- Willingness to treat workflow design as an engineering contract rather than as glue code

[Back to top](#top)

---

## Quick start

Prerequisites:
- Python 3.11+
- `make`

From the repository root:

### Preview the course book locally

```bash
make PROGRAM=reproducible-research/deep-dive-snakemake docs-serve
```

Open the local URL displayed by MkDocs.

### Run the capstone reference workflow

```bash
make PROGRAM=reproducible-research/deep-dive-snakemake test
```

This executes formatting/linting/tests, a dry-run, full workflow execution, and artifact validation.

Successful completion confirms the workflow's contract on your system.

[Back to top](#top)

---

## How to study this program well

1. Start with `course-book/guides/start-here.md`, then `course-book/module-00-orientation/index.md`.
2. Work through Modules 01 to 10 in order because later workflow patterns depend on earlier file-contract discipline.
3. Treat each module as a design checkpoint: read the overview, then the detailed module body, then inspect the capstone for the same idea.
4. Use `course-book/guides/capstone-map.md` and `course-book/guides/proof-matrix.md` when you need to enter the reference workflow deliberately instead of browsing randomly.
5. Re-run the capstone proof targets regularly so the workflow stays executable in your head, not only in prose.
6. Use dry-runs, summaries, and proof artifacts as learning tools, not only as debugging tools.

[Back to top](#top)

---

## How to know you are succeeding

- You can explain every published artifact and why it belongs at the publish boundary.
- You can describe what a checkpoint is allowed to discover and what it must never hide.
- You can distinguish executor policy from workflow semantics.
- You can review a workflow and identify hidden coupling, poison artifacts, or provenance gaps quickly.

[Back to top](#top)

---

## Module map

- `00` Orientation and study strategy
- `01` First principles and the file-DAG contract
- `02` Dynamic DAGs, integrity, and deterministic discovery
- `03` Production operations and policy boundaries
- `04` Scaling workflows and interface boundaries
- `05` Software boundaries and reproducible rules
- `06` Publishing and downstream contracts
- `07` Workflow architecture and file APIs
- `08` Operating contexts and execution policy
- `09` Observability, performance, and incident response
- `10` Governance, migration, and tool boundaries

[Back to top](#top)

---

## Repository layout

```mermaid
graph TD
  root["bijux-masterclass/programs/reproducible-research/deep-dive-snakemake/"]
  root --> book["course-book/"]
  root --> mkdocs["mkdocs.yml"]
  root --> capstone["capstone/"]
  root --> workflows["../../../../.github/workflows/"]
  root --> makefile["Makefile"]
  root --> license["LICENSE"]
  root --> readme["README.md"]
  capstone --> snakefile["Snakefile"]
  capstone --> config["config/"]
  capstone --> workflow["workflow/"]
  capstone --> more["..."]
```

[Back to top](#top)

---

## Capstone promise

The capstone is the course’s executable proof. It is not decorative. It exists so that
the big claims in the course can always be located in runnable workflow behavior:

- explicit discovery instead of hidden sample state
- versioned publishing instead of informal results directories
- profiles as policy instead of tribal command lines
- verification gates instead of “it ran once” confidence

[Back to top](#top)

---

## Contributing

Contributions that enhance correctness, clarity, or reproducibility are welcome (improvements to documentation, exercises, or capstone hardening).

1. Fork and clone `bijux-masterclass`.
2. Implement a focused change (documentation or capstone).
3. From the monorepo root, verify:
   ```bash
   make PROGRAM=reproducible-research/deep-dive-snakemake test
   ```
4. Open a pull request against `master` or `main`.

[Back to top](#top)

---

## License

MIT — see the repository root [LICENSE](https://github.com/bijux/bijux-masterclass/blob/master/LICENSE). © 2025 Bijan Mousavi <bijan@bijux.io>.

[Back to top](#top)

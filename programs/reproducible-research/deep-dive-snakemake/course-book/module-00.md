<a id="top"></a>

# Deep Dive Snakemake: Program Outline

Deep Dive Snakemake is now a ten-module program that starts from first-contact workflow
thinking and ends with long-lived workflow judgment. The through-line does not change:

- **Truthful file contracts**: every real input and output is declared.
- **Safe publication**: trusted outputs appear only at a deliberate boundary.
- **Dynamic discipline**: checkpoints and discovery stay explicit and reviewable.
- **Operational clarity**: profiles, staging, and retries change policy, not meaning.
- **Executable proof**: manifests, reports, tests, and verification surfaces back the claims.

This repository contains both the program guide in `course-book/` and the executable
reference workflow in `capstone/`.

---

## Program Arc

### Module 01 — First Principles: The File-DAG Contract

Start from the essential Snakemake mental model: rules declare file contracts, targets
drive the DAG, and dry-runs explain planned work before execution.

**Deliverable:** a tiny workflow whose outputs, reruns, and publish boundary can be explained with evidence.

### Module 02 — Dynamic DAGs, Integrity, and Deterministic Discovery

Learn how a workflow can discover work in stages without turning the plan into a moving
target. This module introduces disciplined checkpoints, explicit discovery artifacts, and
integrity evidence.

**Deliverable:** a dynamic workflow whose discovered set is explicit and reproducible across runs.

### Module 03 — Production Operation: Profiles, Retries, Staging, and Governance

Move from local workflow semantics to operational policy. Profiles, retries, incomplete
handling, staging, and governance become deliberate contracts instead of tribal commands.

**Deliverable:** a workflow that can be run in different operating contexts without changing its meaning.

### Module 04 — Scaling Patterns: Modularity, Interfaces, CI Gates, and Executor-Proof Semantics

Learn how to grow a repository without losing its shape. Interfaces, file APIs, CI gates,
and executor-proof semantics keep larger workflows reviewable.

**Deliverable:** a modular workflow whose repository layout and review gates make change safer instead of harder.

### Module 05 — Software Stacks, Scripts, Wrappers, and Reproducible Rule Boundaries

Define the boundary between Snakemake logic and the software it drives. Scripts,
packages, wrappers, and environment files become explicit parts of the workflow contract.

**Deliverable:** a workflow whose helper code and software stack can be reviewed without relying on local shell magic.

### Module 06 — Versioned Publishing, Reports, and Downstream Workflow Contracts

Separate internal execution state from stable published outputs. Versioned publish
surfaces, manifests, checksums, and reports become deliberate downstream interfaces.

**Deliverable:** a workflow that publishes a stable bundle another consumer can trust and validate.

### Module 07 — Workflow Architecture, Modules, File APIs, and Reuse Without Confusion

Scale the repository itself: reusable rule families, helper code boundaries, and file APIs
that stay understandable as more people and more workflows touch the codebase.

**Deliverable:** a repository layout that a newcomer can inspect without guessing where the real contract lives.

### Module 08 — Operating Contexts: Profiles, Executors, Storage, and Staging Boundaries

Go deeper on the difference between workflow semantics and execution context. Profiles,
executors, storage, and staging become policy surfaces that can change without corrupting
the workflow contract.

**Deliverable:** a workflow whose local, CI, and scheduler-oriented runs share one stable meaning.

### Module 09 — Performance, Observability, and Workflow Incident Response

Learn how to measure workflow cost, inspect drift, read operational artifacts, and
respond to slow or flaky behavior without hiding the truth.

**Deliverable:** an evidence-first incident ladder for real workflow runs under pressure.

### Module 10 — Mastery: Governance, Migration, Anti-Patterns, and Tool Boundaries

Finish with workflow judgment: reviewing real repositories, planning migrations, setting
governance rules, and deciding when Snakemake should remain the orchestrator or hand a
concern to another tool.

**Deliverable:** an evidence-based workflow review and a migration or stewardship plan for a real repository.

---

## Recommended Reading Path

1. Read Modules 01 to 10 in order.
2. Use the capstone as corroboration after every module, but rely on it most heavily from Modules 02 to 09.
3. Re-run proof commands as you go instead of trusting prose summaries.
4. Treat Module 10 as the finish of the program, not as optional reference material.

If you are completely new to Snakemake, spend extra time in Module 01 before moving on.
If you already run Snakemake in production, Modules 03, 04, 08, 09, and 10 are the
fastest route to operational value.

---

## Capstone Relationship

The capstone is strongest as the executable companion to Modules 02 to 09, where dynamic
behavior, publish boundaries, profiles, modularity, and operational review become
concrete. Module 01 still benefits from smaller local exercises first so the learner sees
Snakemake semantics before the repository becomes larger.

**Proof command:**

```bash
make PROGRAM=reproducible-research/deep-dive-snakemake test
```

Use the capstone to answer this question repeatedly: if a workflow behavior changed
tomorrow, which file or boundary should absorb that change, and why?

[Back to top](#top)

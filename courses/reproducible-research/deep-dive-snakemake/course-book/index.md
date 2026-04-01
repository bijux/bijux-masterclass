# Deep Dive Snakemake

Deep Dive Snakemake teaches workflow design as a discipline of explicit file contracts,
deterministic planning, safe dynamic behavior, and durable operational boundaries. It is
not about collecting more rules. It is about making workflows explainable, reproducible,
and survivable.

## Why this course exists

Many Snakemake resources stop too early. They explain rules, wildcards, and dry-runs,
but they do not prepare readers for the pressure that appears later:

- checkpoints that quietly hide nondeterminism
- profiles that mutate behavior without a clear policy boundary
- outputs that exist but are not trustworthy
- workflows that pass once locally and then drift in CI or on shared infrastructure

This course exists to close that gap.

## Reading contract

This is not a browse-at-random reference. The learner path is deliberate:

1. Start with orientation and the study map.
2. Learn truthful file contracts before dynamic DAG behavior.
3. Learn dynamic DAG behavior before production execution and governance.
4. Learn production execution before scaling boundaries and CI gates.

If you skip that order, later material will still be readable, but the trade-offs will
feel arbitrary instead of principled.

## What each module contributes

- [Module 00](module-00.md) establishes the learner contract, study strategy, and capstone map.
- [Module 01](module-01.md) defines the semantic floor: file contracts, rebuild truth, wildcards, and publishing discipline.
- [Module 02](module-02.md) explains dynamic DAGs, integrity, environments, and performance patterns.
- [Module 03](module-03.md) turns profiles, retries, staging, and governance into operational contracts.
- [Module 04](module-04.md) explains modularity, interface boundaries, CI gates, and executor-proof semantics.
- [Capstone](readme-capstone.md) provides the executable reference workflow that keeps the course honest.

## How to use the capstone while reading

- After Module 01, inspect its explicit file contracts and stable publish boundary.
- After Module 02, inspect the checkpoint and the way discovery is stabilized.
- After Module 03, inspect profiles, retries, artifact verification, and proof targets.
- After Module 04, inspect module boundaries, file APIs, and CI-style gates.

The capstone should function as your executable answer to “what does this rule look like in a real workflow?”

## Common failure modes this course is trying to prevent

- treating a workflow as a script rather than as a file-driven DAG
- allowing dynamic discovery to hide moving targets or unstable plans
- mixing workflow semantics with site policy or executor quirks
- publishing artifacts without a stable versioned interface
- trusting a workflow because it ran once rather than because its proofs are explicit

## Expected learner rhythm

- Read one module overview before reading the detailed module body.
- Pause at every major diagram or proof hook and explain what invariant it is protecting.
- Keep the capstone open while reading so the abstractions stay attached to a concrete workflow.
- Re-run verification commands regularly instead of waiting until the end.

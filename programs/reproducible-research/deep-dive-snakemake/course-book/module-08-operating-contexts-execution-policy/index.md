# Module 08: Operating Contexts and Execution Policy

A workflow that only works under one command on one machine is not yet operationally
serious.

But a workflow that changes meaning every time the operating context changes is not
reproducible either.

This module is about keeping those two truths separate.

You will learn how to:

- treat profiles as policy rather than hidden workflow logic
- compare local, CI, and scheduler contexts without semantic drift
- decide which retries and latency settings are operational help versus correctness crutches
- reason about storage, staging, and scratch boundaries honestly
- review operating-context changes before “works here, fails there” becomes normal

The capstone corroboration surface for this module is the set of operating-policy files and
audit routes around them: `profiles/local/config.yaml`, `profiles/ci/config.yaml`,
`profiles/slurm/config.yaml`, the `profile-audit` bundle in the Makefile, and the guides
that explain profile review and execution evidence.

## Why this module exists

Many workflow teams eventually hit the same confusion:

- a profile changes and nobody knows whether the workflow meaning changed too
- retries are raised because failures are unexplained
- CI, local, and cluster runs all feel slightly different, but the difference is not named
- storage or latency assumptions live in folklore instead of in reviewable policy

This module repairs those problems by teaching operating context as a boundary, not as a
grab bag of flags.

## Study route

```mermaid
flowchart LR
  overview["Overview"] --> core1["Core 1: profiles as policy"]
  core1 --> core2["Core 2: executors and semantic stability"]
  core2 --> core3["Core 3: retries, latency, and failure discipline"]
  core3 --> core4["Core 4: staging, storage, and scratch boundaries"]
  core4 --> core5["Core 5: operating-context review"]
  core5 --> example["Worked example"]
  example --> practice["Exercises and answers"]
  practice --> glossary["Glossary"]
```

Read the module in that order if profiles and execution contexts still feel like one
undifferentiated topic.

If the basic problem is already clear, use this shortcut:

- open Core 1 if your question is mostly about profile boundaries
- open Core 3 if your question is mostly about retries, incomplete outputs, and failure policy
- open Core 5 if your question is mostly about review and drift across contexts

## Module map

| Page | Purpose |
| --- | --- |
| `index.md` | explains the module promise and study route |
| `profiles-as-policy-and-semantic-boundaries.md` | teaches what profiles may and may not own |
| `executors-queues-and-context-invariant-workflow-meaning.md` | teaches how execution surfaces can vary without changing the workflow contract |
| `retries-latency-and-failure-discipline.md` | teaches operational help versus hidden correctness debt |
| `staging-storage-and-filesystem-assumptions.md` | teaches where operating contexts touch data locality and visibility |
| `reviewing-operating-context-drift-and-policy-leaks.md` | teaches how to review profile and executor changes honestly |
| `worked-example-auditing-local-ci-and-slurm-without-semantic-drift.md` | walks through a concrete policy audit route |
| `exercises.md` | gives five mastery exercises |
| `exercise-answers.md` | explains model answers and review logic |
| `glossary.md` | keeps the module vocabulary stable |

## What should be clear by the end

By the end of this module, you should be able to explain:

- which settings belong in profiles and which do not
- why executor changes should alter operations rather than workflow meaning
- how retries and latency waits can help or hide problems
- why staging and storage assumptions need explicit review
- how to tell whether an operating-context change is policy drift or semantic drift

## Capstone route

Use the capstone only after the local module ideas are already legible.

Best corroboration surfaces for this module:

- `capstone/profiles/local/config.yaml`
- `capstone/profiles/ci/config.yaml`
- `capstone/profiles/slurm/config.yaml`
- `capstone/Makefile`
- [Profile Audit Guide](../capstone-docs/profile-audit-guide.md)
- [Capstone File Guide](../capstone/capstone-file-guide.md)

Useful proof route:

```bash
snakemake --profile profiles/local -n
snakemake --profile profiles/ci -n
snakemake --profile profiles/slurm -n
make profile-audit
```

The point of that route is not only to compare flags. It is to inspect whether the
workflow promise stays stable while the operating policy changes.

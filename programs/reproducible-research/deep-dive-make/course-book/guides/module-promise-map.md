# Module Promise Map

Use this page when a module title sounds plausible but still too compressed. A good module
title should tell you what kind of judgment you will leave with, not just which topic
area the chapter occupies.

## How to read the map

Each row answers four practical questions:

1. what the module is trying to change in your mental model
2. what it is not trying to cover yet
3. what kind of evidence should corroborate the lesson
4. what you should be able to do afterward

If a module page drifts from that contract, the drift should be visible here.

## Module contracts

| Module | The promise | The boundary | You should leave able to... | First corroboration route |
| --- | --- | --- | --- | --- |
| [01 Foundations](../module-01-build-graph-foundations-truth/index.md) | Make the build graph legible instead of mystical | targets, prerequisites, rebuild causes, atomic publication | explain one rebuild in terms of declared inputs and outputs | [Capstone Walkthrough](../capstone/capstone-walkthrough.md) |
| [02 Parallel Safety](../module-02-parallel-safety-project-structure/index.md) | show that concurrency is a truth test, not a speed hack | runnable targets, one-writer rules, order-only edges, race classes | explain why one concurrent shape is safe and another is dishonest | [Repro Catalog](../capstone/repro-catalog.md) |
| [03 Determinism](../module-03-determinism-debugging-self-testing/index.md) | turn correctness into a repeatable operating habit | stable discovery, CI-facing targets, selftests, Make-native debugging | distinguish product tests from build-system proof | [Capstone Proof Checklist](../capstone/capstone-proof-checklist.md) |
| [04 Semantics](../module-04-rule-semantics-precedence-edge-cases/index.md) | replace folklore with named GNU Make rules | precedence, expansion, includes, remakes, rule semantics | explain a surprising result by naming the governing rule | [Command Guide](../capstone/command-guide.md) |
| [05 Hardening](../module-05-portability-hermeticity-failure-modes/index.md) | surface the assumptions a build must declare to stay trustworthy | tools, shell behavior, hidden inputs, failure containment | say which assumptions belong in policy instead of custom or lore | [Capstone Map](../capstone/capstone-map.md) |
| [06 Generated Files](../module-06-generated-files-multi-output-pipeline-boundaries/index.md) | treat generators as ordinary graph owners instead of side effects | generated headers, manifests, multi-output rules, publish points | trace a generated artifact back to its semantic inputs | [Capstone File Guide](../capstone/capstone-file-guide.md) |
| [07 Build Architecture](../module-07-build-architecture-layered-includes-apis/index.md) | scale the build without turning it into a private language | public targets, layered `mk/` files, macros, naming | point to the right file when a structural change is needed | [Capstone File Guide](../capstone/capstone-file-guide.md) |
| [08 Release Engineering](../module-08-release-engineering-artifact-contracts/index.md) | define what a publishable artifact actually promises | bundle layout, manifests, attestations, install behavior | explain why a file belongs inside or outside a released surface | [Capstone Proof Checklist](../capstone/capstone-proof-checklist.md) |
| [09 Incident Response](../module-09-performance-observability-incident-response/index.md) | make build incidents diagnosable under pressure | measurement, observability, triage ladders, runbooks | choose the next evidence surface before editing anything | [Capstone Review Worksheet](../capstone/capstone-review-worksheet.md) |
| [10 Governance](../module-10-migration-governance-tool-boundaries/index.md) | teach stewardship, migration order, and honest tool boundaries | review method, migration sequencing, governance rules, handoff decisions | improve a build while preserving proof and public trust | [Capstone Extension Guide](../capstone/capstone-extension-guide.md) |

## What this page prevents

This map exists to prevent four common course failures:

- a module promises judgment but only delivers syntax
- a module promises operations but never reaches executable proof
- a module promises architecture but leaves ownership blurry
- a module promises stewardship but never turns into review behavior

If you notice one of those failures while reading a module, come back here and name the
missing piece directly.

## Best companion pages

- [Module Checkpoints](module-checkpoints.md) when you need the exit bar after the promise
- [Proof Ladder](proof-ladder.md) when the corroboration route feels too heavy
- [Capstone Map](../capstone/capstone-map.md) when the promise is clear but the repository route is not


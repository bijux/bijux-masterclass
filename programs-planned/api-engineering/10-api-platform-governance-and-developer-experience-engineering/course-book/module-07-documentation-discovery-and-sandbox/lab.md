# Lab — Onboard a consumer without private help

> **Module 07:** Documentation, Discovery, Sandboxes, and Consumer Onboarding

## Objective

Publish the task-oriented portal source, search index, sandbox profile, and first-success evidence.

## Why this lab matters

This lab turns the module’s governing question—**Can a new consumer find the right interface, trust it, and complete a useful workflow safely without private organizational knowledge?**—into a falsifiable experiment. The portal core builds a deterministic search index from Markdown and contract metadata. The sandbox core derives stable fixture identity, enforces synthetic-only data, and records expiry. These small mechanisms make discovery and isolation testable without pretending to be a complete commercial portal.

It advances the cumulative Analysis Runs Platform by requiring this result: **Publish the task-oriented portal source, search index, sandbox profile, and first-success evidence**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Run `make docs-proof` and `make sandbox-proof`. Use a fresh sandbox session and
the checked-in documentation source.

## Hypothesis

The clean implementation should satisfy this claim: **The normal path reaches a defined first success. The stale example fails quality checks. Production data import is rejected. The owner and support path remain discoverable at every step.** When the lab introduces this fault—**the lab introduces its declared planted defect**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

Act as a consumer who knows only the goal “submit an analysis and retrieve its
artifact.” Use search, interface-selection guidance, the quickstart, sandbox, and
support route. Then break one example version and attempt to import production
data into the sandbox.

### Investigation notes

Before editing code, predict the first observable divergence caused by **the lab introduces its declared planted defect**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Publish the task-oriented portal source, search index, sandbox profile, and first-success evidence**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

The normal path reaches a defined first success. The stale example fails quality
checks. Production data import is rejected. The owner and support path remain
discoverable at every step.

## Required evidence

Write `reports/module-07-onboarding.json` with timestamps, selected interface,
contract version, failure points, first-success duration, search results, and
support handoff.

## Interpretation and defense

1. Which state or effect is authoritative for **Documentation, Discovery, Sandboxes, and Consumer Onboarding**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **the lab introduces its declared planted defect** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Destroy the sandbox session, revoke credentials, restore the example, and rerun
proofs.

## Completion gate

A new consumer can complete the task without undocumented credentials, private
contacts, or production data.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Documentation, Discovery, Sandboxes, and Consumer Onboarding**. A green command without the negative case and causal explanation does not satisfy this gate.

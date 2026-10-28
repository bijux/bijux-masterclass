# Lab — Evolve a schema and rebuild a projection safely

> **Module 05:** Schema Evolution, Compatibility, Replay, and Historical Truth

## Objective

Accept one genuinely additive event change, reject structural and replay hazards, and rebuild analytics in an isolated effect version.

## Why this lab matters

This lab turns the module’s governing question—**How do event schemas evolve while retained historical events remain immutable and replay remains intelligible?**—into a falsifiable experiment. A replay selects a source range, event types, tenant scope, consumer/effect version, target store, maximum event count, concurrency, start mode, and side-effect policy. It has an owner, approval, dry run, abort conditions, progress checkpoints, and reconciliation oracle.

It advances the cumulative Analysis Runs Platform by requiring this result: **Classify compatibility, add upcasters, preserve source bytes, define retention, and run bounded dry-run replay**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

1. Freeze the baseline schemas and examples under `capstone/releases/baseline/`.
2. Select the completed-run and artifact-published event types.
3. Create `analytics-completion:v2` with a separate target.
4. Prepare a retained fixture stream containing old events, duplicates, and one correction.
5. Set outbound notification and webhook capabilities to denied.

## Hypothesis

The clean implementation should satisfy this claim: **The additive candidate preserves old records; breaking and replay-unsafe candidates are rejected with exact reasons. Upcasting is deterministic. Dry run creates no durable effect. Apply mode updates only the v2 target, processes each event once, applies correction policy, and emits no external side effects.** When the lab introduces this fault—**Inject one current-time dependency and one notification side effect; confirm the replay proof rejects them**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

Evaluate the accepted-additive, rejected-breaking, and rejected-replay-unsafe candidates. Add one deterministic
upcaster for a representation-only change. Run a dry replay with an event bound, inspect would-apply counts,
then apply into the isolated projection.

Inject one current-time dependency and one notification side effect; confirm the replay proof rejects them.
Catch up from a recorded high-water position and compare the rebuilt projection with authoritative fixture
totals.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Inject one current-time dependency and one notification side effect; confirm the replay proof rejects them**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Accept one genuinely additive event change, reject structural and replay hazards, and rebuild analytics in an isolated effect version**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

The additive candidate preserves old records; breaking and replay-unsafe candidates are rejected with exact
reasons. Upcasting is deterministic. Dry run creates no durable effect. Apply mode updates only the v2
target, processes each event once, applies correction policy, and emits no external side effects.

## Required evidence

- `work/module-05/compatibility-report.json`
- `work/module-05/semantic-review.md`
- `work/module-05/replay-plan.yaml`
- dry-run and apply reports
- v1/v2 projection comparison
- side-effect denial evidence
- output from `make evolution-proof` and `make replay-proof`

## Interpretation and defense

1. Which state or effect is authoritative for **Schema Evolution, Compatibility, Replay, and Historical Truth**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Inject one current-time dependency and one notification side effect; confirm the replay proof rejects them** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Remove nondeterministic and side-effect defects, reset the v2 target, restore fixture checkpoints, and retain
the accepted schema/replay artifacts. Do not modify baseline events.

## Completion gate

The lab passes only when historical records remain byte-identical, every release decision is explained,
replay is bounded and side-effect-free, and the v2 projection can be rebuilt reproducibly without deleting
v1 inbox evidence.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Schema Evolution, Compatibility, Replay, and Historical Truth**. A green command without the negative case and causal explanation does not satisfy this gate.

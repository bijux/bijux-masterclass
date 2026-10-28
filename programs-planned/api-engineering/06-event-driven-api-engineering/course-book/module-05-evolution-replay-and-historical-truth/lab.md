# Lab — Evolve a schema and rebuild a projection safely

## Objective

Accept one genuinely additive event change, reject structural and replay hazards, and rebuild analytics in an isolated effect version.

## Setup conditions


1. Freeze the baseline schemas and examples under `capstone/releases/baseline/`.
2. Select the completed-run and artifact-published event types.
3. Create `analytics-completion:v2` with a separate target.
4. Prepare a retained fixture stream containing old events, duplicates, and one correction.
5. Set outbound notification and webhook capabilities to denied.


## Failure action and investigation


Evaluate the accepted-additive, rejected-breaking, and rejected-replay-unsafe candidates. Add one deterministic
upcaster for a representation-only change. Run a dry replay with an event bound, inspect would-apply counts,
then apply into the isolated projection.

Inject one current-time dependency and one notification side effect; confirm the replay proof rejects them.
Catch up from a recorded high-water position and compare the rebuilt projection with authoritative fixture
totals.



### Investigation notes

Before editing, write a one-sentence hypothesis answering: **How do event schemas evolve while retained historical events remain immutable and replay remains intelligible?** Record the first observation that contradicts the expected model. After the repair, explain why the capstone can now claim: Classify compatibility, add upcasters, preserve source bytes, define retention, and run bounded dry-run replay. A passing command without this causal explanation is insufficient.

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


## Cleanup and reset


Remove nondeterministic and side-effect defects, reset the v2 target, restore fixture checkpoints, and retain
the accepted schema/replay artifacts. Do not modify baseline events.


## Completion gate


The lab passes only when historical records remain byte-identical, every release decision is explained,
replay is bounded and side-effect-free, and the v2 projection can be rebuilt reproducibly without deleting
v1 inbox evidence.

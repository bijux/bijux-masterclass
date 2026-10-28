# Lab — Prove duplicate publication with one committed effect

> **Module 04:** Transactional Publication, Inbox Deduplication, and Exactly-Once Effects

## Objective

Reproduce the producer and consumer uncertainty windows, then show how outbox and inbox transactions preserve the Analysis Events contract.

## Why this lab matters

This lab turns the module’s governing question—**How do producers avoid dual writes and consumers obtain exactly-once effects on top of at-least-once delivery?**—into a falsifiable experiment. Draw two timelines—producer and consumer—and mark each durable commit. For every arrow crossing systems, ask whether a retry can repeat it and which stable identity makes repetition safe. Then inspect the transaction boundaries in code and SQL; folder names do not prove atomicity.

It advances the cumulative Analysis Runs Platform by requiring this result: **Implement transactional outbox publication, inbox deduplication, effect-version identity, and atomic consumer effects**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

1. Complete the deterministic broker lab.
2. Create one completed-run event with fixed ID and canonical bytes.
3. Initialize the domain/outbox store, relay, broker, and two independent projections.
4. Configure the relay to raise after its first successful publish.
5. Configure one consumer to lose acknowledgement after commit.

## Hypothesis

The clean implementation should satisfy this claim: **The authoritative state and outbox are atomic, relay recovery may duplicate publication, each logical consumer/effect commits exactly one projection update, and independent effects each run once. The planted non-atomic consumer must demonstrate a missing or duplicated effect.** When the lab introduces this fault—**Plant an inbox-before-effect defect and require its proof to fail**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

Commit the domain fact and outbox row. Run the relay; capture the injected crash. Recover and run it again.
Confirm two broker records share one event ID and body.

Deliver both records to `analytics:v1`. Apply the first effect and simulate acknowledgement loss. Process the
duplicate and verify the inbox classifies it as already applied. Process the same event with
`notification:v1` and verify that independent effect is not suppressed. Plant an inbox-before-effect defect
and require its proof to fail.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Plant an inbox-before-effect defect and require its proof to fail**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Reproduce the producer and consumer uncertainty windows, then show how outbox and inbox transactions preserve the Analysis Events contract**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

The authoritative state and outbox are atomic, relay recovery may duplicate publication, each logical
consumer/effect commits exactly one projection update, and independent effects each run once. The planted
non-atomic consumer must demonstrate a missing or duplicated effect.

## Required evidence

- `work/module-04/producer-timeline.json`
- `work/module-04/consumer-timeline.json`
- event-body digests for both broker records
- inbox and projection snapshots
- one external-side-effect boundary design
- output from `make outbox-inbox-proof`
- optional PostgreSQL evidence marked executed or not executed

## Interpretation and defense

1. Which state or effect is authoritative for **Transactional Publication, Inbox Deduplication, and Exactly-Once Effects**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Plant an inbox-before-effect defect and require its proof to fail** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Remove the injected crash hooks and planted non-atomic code. Clear deterministic stores and test broker
channels. If a live database was used, roll back test rows without deleting migration history.

## Completion gate

The lab passes only when duplicate publication and duplicate delivery are visible in evidence while each
declared business effect remains one. A test that calls the handler once does not satisfy the gate.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Transactional Publication, Inbox Deduplication, and Exactly-Once Effects**. A green command without the negative case and causal explanation does not satisfy this gate.

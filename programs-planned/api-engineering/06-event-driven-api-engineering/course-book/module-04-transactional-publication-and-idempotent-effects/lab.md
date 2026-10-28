# Lab — Prove duplicate publication with one committed effect

## Objective

Reproduce the producer and consumer uncertainty windows, then show how outbox and inbox transactions preserve the Analysis Events contract.

## Setup conditions


1. Complete the deterministic broker lab.
2. Create one completed-run event with fixed ID and canonical bytes.
3. Initialize the domain/outbox store, relay, broker, and two independent projections.
4. Configure the relay to raise after its first successful publish.
5. Configure one consumer to lose acknowledgement after commit.


## Failure action and investigation


Commit the domain fact and outbox row. Run the relay; capture the injected crash. Recover and run it again.
Confirm two broker records share one event ID and body.

Deliver both records to `analytics:v1`. Apply the first effect and simulate acknowledgement loss. Process the
duplicate and verify the inbox classifies it as already applied. Process the same event with
`notification:v1` and verify that independent effect is not suppressed. Plant an inbox-before-effect defect
and require its proof to fail.



### Investigation notes

Before editing, write a one-sentence hypothesis answering: **How do producers avoid dual writes and consumers obtain exactly-once effects on top of at-least-once delivery?** Record the first observation that contradicts the expected model. After the repair, explain why the capstone can now claim: Implement transactional outbox publication, inbox deduplication, effect-version identity, and atomic consumer effects. A passing command without this causal explanation is insufficient.

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


## Cleanup and reset


Remove the injected crash hooks and planted non-atomic code. Clear deterministic stores and test broker
channels. If a live database was used, roll back test rows without deleting migration history.


## Completion gate


The lab passes only when duplicate publication and duplicate delivery are visible in evidence while each
declared business effect remains one. A test that calls the handler once does not satisfy the gate.

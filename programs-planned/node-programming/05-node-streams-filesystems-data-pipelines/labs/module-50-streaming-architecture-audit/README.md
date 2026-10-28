# Laboratory 10 — Streaming Architecture Audit

**Module 50: Integrated Streaming Architecture, Testing, and Independent Change**

## Product

Audit and repair an independent NDJSON export system. Produce the representation graph, queue budget, resource ledger, commit matrix, chunk-boundary test set, and an implementation that survives injected failures.

This is an independent mechanism study. It deliberately excludes FlowLedger’s other stages so failures can be attributed to one contract.

## Governing question

> Can you review and evolve a complete Node.js dataflow system without losing byte semantics, pressure, parser bounds, resource ownership, commit rules, or deterministic evidence?

## Public surface

- `auditPipeline(source, options)` decodes bounded NDJSON, validates records, filters them, and returns a deterministic report under separate `maxLineBytes` and `maxOutputBytes` limits.

- `StageContract` names input, output, owner, bound, and completion for architecture review.

- `missingFields(stage)` identifies incomplete stage specifications in the starter.

## Required invariants

- Input chunking does not change accepted records or canonical output.

- Every inspected record becomes emitted or filtered exactly once.

- Source SHA-256 identifies the exact incoming bytes.

- Malformed input and over-limit lines fail before a final product is published.

- The architecture report names every resource owner and capacity bound.

- Canonical output is rejected before its retained byte budget is exceeded.

## Implementation sequence

1. Draw the full stage and representation graph.

2. Implement bounded incremental decode and validation.

3. Add deterministic canonical rendering and filtering.

4. Add source hashing and conservation accounting.

5. Generate chunk-boundary and exact fault-position tests.

6. Write the independent architecture review and change proposal.

Do not begin by reading the reference. The starter defines the vocabulary and a baseline, not the final design.

## Adversarial cases

- one-byte chunks and one complete chunk;

- multibyte text split at every byte;

- line exactly at and beyond the limit;

- JSON and domain failures after earlier valid records;

- filter predicate failure;

- abort during each blocking edge in the extended design;

- destination or child failure after apparent upstream completion;

- different schedule and chunk orders producing one canonical report;

Add cases in the smallest order that falsifies an incorrect model. Avoid arbitrary sleeps; use exact chunks, counters, injected callbacks, or explicit state transitions.

## Prohibited shortcuts

- calling a diagram complete without queues and terminal states;

- using live counters as authoritative final accounting;

- collecting all input merely to simplify integration;

- publishing before every required stage agrees on success;

- adding a feature only to code without updating errors, limits, tests, and docs;

A shortcut is prohibited because it removes the mechanism the laboratory exists to teach, not because one implementation style is preferred.

## Completion evidence

1. a representation graph, capacity map, resource tree, and commit matrix;

2. chunk-partition and fault-position tests;

3. conservation assertions;

4. a list of deliberate non-guarantees;

5. an independently implemented rejects-bundle design or equivalent cross-layer extension;

## Independent transfer

Add a resumable import checkpoint to a streaming system. Define what state can be replayed safely, what byte position means after decoding and filtering, and how the checkpoint is committed with the data.

Your transfer design must reconstruct the module ledger for the new domain. Renaming the laboratory types is not transfer.

## Architecture defense

Present the system to a second reader using five artifacts: a representation graph, queue-and-capacity map, resource ownership tree, terminal-state table, and publication matrix. The reader should be able to choose any accepted record and trace its bytes from source chunk through decoding, validation, filtering, canonical rendering, hashing, and final visibility. They should also be able to choose any failure edge and identify the owner responsible for cancellation and cleanup.

Perform one counterfactual review: double the maximum line length, add a required rejects output, or insert a child-process filter. Enumerate every limit, error type, test, command option, report field, and publication decision that must change. Reject the feature proposal if it modifies only the happy-path code. The final architecture audit is successful when the design's guarantees and non-guarantees are both explicit, when live instrumentation is not confused with authoritative terminal accounting, and when schedule or chunk variation cannot change the canonical product.

## Comparing with the reference

After your tests pass, inspect `reference/` and locate the first meaningful difference. Adopt it only when it proves an invariant your design misses; otherwise retain the simpler design.

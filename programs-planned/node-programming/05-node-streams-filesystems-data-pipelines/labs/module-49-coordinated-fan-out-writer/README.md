# Laboratory 9 — Coordinated Fan-Out Writer

**Module 49: Multi-Stage Dataflow, Fan-Out, and Commit Coordination**

## Product

Build a required two-sink writer that respects both destinations’ pressure, propagates one branch failure to the complete operation, tracks visible-byte conservation, and demonstrates a versioned-bundle commit protocol.

This is an independent mechanism study. It deliberately excludes FlowLedger’s other stages so failures can be attributed to one contract.

## Governing question

> How do you coordinate branches, side outputs, metadata, and multiple candidate files when a linear pipeline is no longer enough?

## Public surface

- `fanOut(source, destinations, signal?)` writes every chunk to every required destination and returns counts.

- `CollectingSink` simulates independently pressured branches.

- `assertConservation` verifies mutually exclusive terminal record categories.

## Required invariants

- Every required destination receives identical bytes in identical order.

- The source advances only after all branches accept the current chunk.

- One branch failure destroys sibling branches and rejects the owner.

- All destinations reach terminal completion before success is returned.

- Chunk and byte accounting is independent of branch completion order.

## Implementation sequence

1. Implement a cancellable single-destination write helper.

2. Coordinate one chunk across all destinations.

3. Add source exhaustion, destination end, and complete finish waiting.

4. Add shared failure teardown.

5. Assert identical branch output under different delays.

6. Design the versioned bundle commit note.

Do not begin by reading the reference. The starter defines the vocabulary and a baseline, not the final design.

## Adversarial cases

- zero destinations;

- one fast and one slow branch;

- a branch returning false on the first write;

- a branch error after earlier chunks;

- abort during a branch drain wait;

- source failure;

- destination finish failure;

- different branch completion orders;

Add cases in the smallest order that falsifies an incorrect model. Avoid arbitrary sleeps; use exact chunks, counters, injected callbacks, or explicit state transitions.

## Prohibited shortcuts

- using EventEmitter for required async delivery;

- advancing when only one branch accepts capacity;

- copying every chunk without a mutation or lifetime reason;

- returning after calling `end()` without awaiting all branches;

- calling sequential renames an atomic multi-file transaction;

A shortcut is prohibited because it removes the mechanism the laboratory exists to teach, not because one implementation style is preferred.

## Completion evidence

1. byte-exact equality across branches;

2. pressure tests with differently delayed sinks;

3. failure propagation and cleanup tests;

4. a conservation equation with adversarial categories;

5. a multi-file publication state diagram;

## Independent transfer

Design an export that produces data.ndjson, rejects.ndjson, and manifest.json. Choose a publication protocol and give the visible-artifact state after each possible failure.

Your transfer design must reconstruct the module ledger for the new domain. Renaming the laboratory types is not transfer.

## Bundle publication exercise

Extend the design note from two byte sinks to a logical bundle containing `data.ndjson`, `rejects.ndjson`, and `manifest.json`. Define a version directory or indirection record that prevents readers from observing a mixed generation. List every candidate file, who owns it, and the single publication step that makes the bundle current. Sequentially replacing three final filenames is not one atomic bundle commit.

For the streaming fan-out itself, trace one chunk when branch A accepts immediately and branch B returns `false`. The source must not advance until B regains capacity, yet A must not receive the chunk again. Inject a failure in each branch after different accepted-byte counts and show how sibling destruction and final rejection are coordinated. Conclude with a conservation statement for source bytes, per-branch accepted bytes, and terminal branch states. This statement should remain valid regardless of which branch emits its completion event first.

## Comparing with the reference

After your tests pass, inspect `reference/` and locate the first meaningful difference. Adopt it only when it proves an invariant your design misses; otherwise retain the simpler design.

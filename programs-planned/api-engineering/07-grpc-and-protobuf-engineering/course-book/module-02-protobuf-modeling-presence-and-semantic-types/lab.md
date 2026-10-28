# Lab — Prove presence and 64-bit meaning across Python and TypeScript

**Module:** Protobuf Modeling, Presence, and Semantic Types

## Objective

Complete the Analysis RPC 1.0 message model, publish cross-language presence and integer vectors, and document every field whose absence changes behavior.

## Setup

Use the checked-in proto source, generated-equivalent Python descriptors, and dependency-light TypeScript semantic adapters. Do not alter generator options during the experiment without recording them.

## Controlled actions

1. Construct absent and present-empty terminal-detail cases and compare `HasField` or equivalent semantic projections.
2. Serialize revisions at 2^53−1, 2^53, 2^63−1, and invalid overflow boundaries.
3. Round-trip the binary bytes and canonical ProtoJSON evidence through both language adapters.
4. Inject an unknown enum number and record whether each runtime preserves, exposes, or rejects it.
5. Send invalid upload frames with no `oneof` member and with semantically repeated metadata.
6. Run the model proof twice and confirm identical binary digests and reports.

## Correctness oracle

Both tracks produce the same declared semantic projection and exact binary digest for supported cases. Unsafe numeric coercion, collapsed presence, invalid oneof sequences, or undocumented unknown-enum behavior fails the lab.

## Required evidence

- `capstone/shared/vectors/presence.json`
- `capstone/shared/vectors/int64.json`
- `reports/module-02-model-proof.json`

## Cleanup

Remove generated scratch bytes outside the golden-fixture directory and restore the checked-in vector files. Re-run the model proof from a clean process.

## Completion gate

No field whose absence changes behavior may lack explicit presence semantics, and no supported TypeScript path may coerce a 64-bit contract value to an unsafe number.

A successful command without this evidence does not complete the lab.

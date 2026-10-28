# Lab — Prove presence and 64-bit meaning across Python and TypeScript

> **Module 02:** Protobuf Modeling, Presence, and Semantic Types

## Objective

Complete the Analysis RPC 1.0 message model, publish cross-language presence and integer vectors, and document every field whose absence changes behavior.

## Why this lab matters

This lab turns the module’s governing question—**How do we encode domain meaning in Protobuf without allowing language defaults, JSON conventions, or storage models to erase important distinctions?**—into a falsifiable experiment. The review ends with two artifacts: a field-semantics table and cross-language vectors. Every field records creator, presence, unit, range, sensitivity, identity scope, and evolution rule. The vectors exercise absence, empty values, unknown enum numbers, oneof alternatives, and the complete int64 boundary. That evidence is more valuable than a screenshot of generated classes.

It advances the cumulative Analysis Runs Platform by requiring this result: **Complete the Analysis RPC 1.0 message model, publish cross-language presence and integer vectors, and document every field whose absence changes behavior**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Use the checked-in proto source, generated-equivalent Python descriptors, and dependency-light TypeScript semantic adapters. Do not alter generator options during the experiment without recording them.

## Hypothesis

The clean implementation should satisfy this claim: **Both tracks produce the same declared semantic projection and exact binary digest for supported cases. Unsafe numeric coercion, collapsed presence, invalid oneof sequences, or undocumented unknown-enum behavior fails the lab.** When the lab introduces this fault—**Inject an unknown enum number and record whether each runtime preserves, exposes, or rejects it**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Construct absent and present-empty terminal-detail cases and compare `HasField` or equivalent semantic projections.
2. Serialize revisions at 2^53−1, 2^53, 2^63−1, and invalid overflow boundaries.
3. Round-trip the binary bytes and canonical ProtoJSON evidence through both language adapters.
4. Inject an unknown enum number and record whether each runtime preserves, exposes, or rejects it.
5. Send invalid upload frames with no `oneof` member and with semantically repeated metadata.
6. Run the model proof twice and confirm identical binary digests and reports.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Inject an unknown enum number and record whether each runtime preserves, exposes, or rejects it**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Complete the Analysis RPC 1.0 message model, publish cross-language presence and integer vectors, and document every field whose absence changes behavior**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

Both tracks produce the same declared semantic projection and exact binary digest for supported cases. Unsafe numeric coercion, collapsed presence, invalid oneof sequences, or undocumented unknown-enum behavior fails the lab.

## Required evidence

- `capstone/shared/vectors/presence.json`
- `capstone/shared/vectors/int64.json`
- `reports/module-02-model-proof.json`

## Interpretation and defense

1. Which state or effect is authoritative for **Protobuf Modeling, Presence, and Semantic Types**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Inject an unknown enum number and record whether each runtime preserves, exposes, or rejects it** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Remove generated scratch bytes outside the golden-fixture directory and restore the checked-in vector files. Re-run the model proof from a clean process.

## Completion gate

No field whose absence changes behavior may lack explicit presence semantics, and no supported TypeScript path may coerce a 64-bit contract value to an unsafe number.

A successful command without this evidence does not complete the lab.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Protobuf Modeling, Presence, and Semantic Types**. A green command without the negative case and causal explanation does not satisfy this gate.

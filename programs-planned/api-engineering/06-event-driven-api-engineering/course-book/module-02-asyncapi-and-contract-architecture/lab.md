# Lab — Publish the Analysis Events 1.0 AsyncAPI contract

> **Module 02:** AsyncAPI, CloudEvents, and Contract Architecture

## Objective

Turn the approved taxonomy into a machine-readable, offline-resolvable asynchronous API and prove every packaged example against the envelope and payload layers.

## Why this lab matters

This lab turns the module’s governing question—**How do AsyncAPI, CloudEvents, schemas, channels, operations, bindings, and examples form one governed event contract?**—into a falsifiable experiment. The checkpoint from Event Thinking, Ownership, and Message Taxonomy established this result: Create the minimal message taxonomy, publication decision record, owner catalogue, and synchronous/asynchronous boundary. This module builds on that evidence rather than reopening the predecessor. Its result becomes the prerequisite for Delivery Semantics, Ordering, Partitioning, and Acknowledgement .

It advances the cumulative Analysis Runs Platform by requiring this result: **Publish Analysis Events API 1.0 with canonical envelopes, message schemas, examples, operation ownership, and deterministic bundles**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

1. Complete Module 01 and freeze its event catalogue diff.
2. Run `make data-proof` to establish duplicate-key-aware parsing.
3. Inspect `capstone/contracts/asyncapi.yaml`, message fragments, JSON Schemas, and examples.
4. Create `work/module-02/contract-review.md` with four sections: operations, channels, messages, and schemas.
5. Keep the live broker stopped; this lab is contract-first.

## Hypothesis

The clean implementation should satisfy this claim: **The source document parses with duplicate-key detection, every local reference resolves offline, each operation points to an allowed message, all examples satisfy event profile 1.0 and their payload schemas, and the catalogue covers every public message. The validation report states its scope without claiming complete protocol conformance.** When the lab introduces this fault—**Plant one reversed operation, one invalid example, and one unresolved reference**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

Add or repair one command operation and at least three event operations. For each, verify the application
perspective, allowed channel messages, stable operation ID, event type, schema URI, partition field, and
example.

Plant one reversed operation, one invalid example, and one unresolved reference. Confirm that the local
proof fails for each distinct reason, then repair the document. Run the optional independent AsyncAPI
validator only if the pinned CLI is available, recording it separately.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Plant one reversed operation, one invalid example, and one unresolved reference**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Turn the approved taxonomy into a machine-readable, offline-resolvable asynchronous API and prove every packaged example against the envelope and payload layers**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

The source document parses with duplicate-key detection, every local reference resolves offline, each
operation points to an allowed message, all examples satisfy event profile 1.0 and their payload schemas,
and the catalogue covers every public message. The validation report states its scope without claiming
complete protocol conformance.

## Required evidence

- `work/module-02/contract-review.md`
- `work/module-02/reference-map.json`
- `work/module-02/example-results.json`
- failure outputs for reversed direction, bad example, and missing reference
- repaired contract diff
- `make contract-proof` output
- optional independent-validator output marked executed or not executed

## Interpretation and defense

1. Which state or effect is authoritative for **AsyncAPI, CloudEvents, and Contract Architecture**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Plant one reversed operation, one invalid example, and one unresolved reference** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Remove planted defects and generated bundles, restore deterministic source ordering, and confirm no remote
cache or downloaded schema remains in the repository. Rerun the proof from a clean checkout path.

## Completion gate

The lab passes only if a reviewer can start from one operation, resolve its channel, message, envelope,
payload schema, example, owner, and retention policy without guessing. Every deliberately planted defect
must be detected by a named proof.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **AsyncAPI, CloudEvents, and Contract Architecture**. A green command without the negative case and causal explanation does not satisfy this gate.

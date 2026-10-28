# Lab — Publish the Analysis Events 1.0 AsyncAPI contract

## Objective

Turn the approved taxonomy into a machine-readable, offline-resolvable asynchronous API and prove every packaged example against the envelope and payload layers.

## Setup conditions


1. Complete Module 01 and freeze its event catalogue diff.
2. Run `make data-proof` to establish duplicate-key-aware parsing.
3. Inspect `capstone/contracts/asyncapi.yaml`, message fragments, JSON Schemas, and examples.
4. Create `work/module-02/contract-review.md` with four sections: operations, channels, messages, and schemas.
5. Keep the live broker stopped; this lab is contract-first.


## Failure action and investigation


Add or repair one command operation and at least three event operations. For each, verify the application
perspective, allowed channel messages, stable operation ID, event type, schema URI, partition field, and
example.

Plant one reversed operation, one invalid example, and one unresolved reference. Confirm that the local
proof fails for each distinct reason, then repair the document. Run the optional independent AsyncAPI
validator only if the pinned CLI is available, recording it separately.



### Investigation notes

Before editing, write a one-sentence hypothesis answering: **How do AsyncAPI, CloudEvents, schemas, channels, operations, bindings, and examples form one governed event contract?** Record the first observation that contradicts the expected model. After the repair, explain why the capstone can now claim: Publish Analysis Events API 1.0 with canonical envelopes, message schemas, examples, operation ownership, and deterministic bundles. A passing command without this causal explanation is insufficient.

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


## Cleanup and reset


Remove planted defects and generated bundles, restore deterministic source ordering, and confirm no remote
cache or downloaded schema remains in the repository. Rerun the proof from a clean checkout path.


## Completion gate


The lab passes only if a reviewer can start from one operation, resolve its channel, message, envelope,
payload schema, example, owner, and retention policy without guessing. Every deliberately planted defect
must be detected by a named proof.

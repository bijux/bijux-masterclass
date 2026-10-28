# Laboratory 10 — Architecture Council

[Course 10](../../README.md) · [Common laboratory method](../../../START_HERE.md#laboratory-method)

## Product

Build and defend a bounded artifact registry that reads two format versions, stores a stable owned artifact model, applies runtime-selected policies, and supports a small operation protocol. The implementation is deliberately modest; the main product is an architecture in which every mechanism has a named requirement, proof owner, compatibility cost, and removal condition.

The starter contains one `Decision` record. Expand it into a decision ledger and a working registry. The final system should be smaller than the list of advanced mechanisms you know.

### Required system

Implement:

- V1 and V2 decoders that produce one stable `Artifact` type;
- deterministic canonical V2 encoding;
- a registry keyed by stable artifact identity;
- an open `Policy` boundary with duplicate-name rejection;
- all-or-nothing insertion after policy validation;
- a bounded batch operation or explicit runtime capacity;
- deterministic listing;
- typed errors distinguishing format, policy, duplicate identity, and capacity failure.

Keep policy erasure local. Do not add unsafe code, pinning, async execution, procedural macros, or a plugin ABI unless you can show a requirement that ordinary Rust cannot satisfy.

### Decision ledger

For each retained mechanism, record:

| Requirement | Mechanism | Invariant owner | Primary evidence | Compatibility cost | Removal condition |
|---|---|---|---|---|---|

Include at least five rejected mechanisms and explain why each is premature. A rejection is part of the design, not evidence of insufficient ambition.

### Architecture review

Trace one successful V1 load, one V2 policy failure, one duplicate insert, and one capacity failure. At every boundary, name the current representation and whether failure leaves the registry unchanged. Add a public API review from the perspective of both callers and future policy implementors.

### Transfer

Add a second artifact format with one new optional field. Preserve V1 and V2 reads, keep the public artifact model stable where possible, and create migration fixtures. Present the changed ledger to another reader and record which earlier decision changed—or why none did.

### Using the reference

Build your own system and ledger before opening `solution/`. The reference demonstrates a small typed registry but does not constitute the full council report. Compare its invariant ownership with yours and identify at least one mechanism you intentionally omitted.

### Completion standard

A reader can reconstruct the system from requirements to mechanisms to evidence, and can remove any advanced feature whose requirement disappears. The laboratory fails if it becomes a showcase of GATs, const generics, erasure, unsafe code, and macros without distinct product obligations.

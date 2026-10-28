# Laboratory 100 — Architecture Council

**Course 10 · Module 100: Architectural Synthesis: Building and Defending a Long-Lived Rust System**

[Chapter](../../course-book/module-100-architectural-synthesis-building-and-defending-a-long-lived-rust-system/index.md) · [Workbook](../../course-book/module-100-architectural-synthesis-building-and-defending-a-long-lived-rust-system/workbook.md) · [AxiomStore guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Architectural Synthesis: Building and Defending a Long-Lived Rust System**: Can you turn ten courses of mechanisms into one restrained architecture whose guarantees, unsafe core, verification evidence, compatibility policy, and operating limits can survive independent review? The product must make **Construct an invariant map connecting product claims to types, runtime validation, synchronization, unsafe proofs, tests, and operational policy** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **architecture defense record** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

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

### Mechanism-specific completion standard

A reader can reconstruct the system from requirements to mechanisms to evidence, and can remove any advanced feature whose requirement disappears. The laboratory fails if it becomes a showcase of GATs, const generics, erasure, unsafe code, and macros without distinct product obligations.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Architecture Council**.
2. Draw the smallest **architecture defense record** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to AxiomStore so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Whole-laboratory completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Construct an invariant map connecting product claims to types, runtime validation, synchronization, unsafe proofs, tests, and operational policy.
- Choose static, dynamic, enum, const-generic, borrowing, owned, generated, concurrent, async, and unsafe mechanisms only where their proof benefit exceeds complexity.
- Review dependency direction, public surface, failure taxonomy, resource bounds, and deterministic behavior as one architecture.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 100 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **architecture defense record**. Defend why your design is simpler than one plausible alternative under the new requirements.

# Laboratory 68 — Bounded SPSC Ring

**Course 7 · Module 68: Lock-Free Protocols, Reclamation, and Unsafe Send/Sync**

[Chapter](../../course-book/module-68-lock-free-protocols-reclamation-and-unsafe-send-sync/index.md) · [Workbook](../../course-book/module-68-lock-free-protocols-reclamation-and-unsafe-send-sync/workbook.md) · [BatchWeave guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Lock-Free Protocols, Reclamation, and Unsafe Send/Sync**: What proof permits shared raw storage to be accessed without a lock, and where do role confusion, ABA, destruction, or memory reclamation invalidate a locally plausible algorithm? The product must make **Distinguish obstruction-free, lock-free, and wait-free progress claims from ordinary nonblocking API behavior** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **atomic state machine** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

> What exact role, initialization, atomic-ordering, and destruction proof makes a safe one-producer/one-consumer ring possible?

By the end, the answer must be visible in the public API, protocol diagram, failure behavior, causal tests, and explanation—not merely in a successful run.

## Product

Build a fixed-capacity SPSC queue that returns one non-cloneable producer and one non-cloneable consumer. Push and pop are nonblocking. Shared storage uses `UnsafeCell<MaybeUninit<T>>` behind a private unsafe `Sync` proof.

## Product-specific design pressure

This is the only unsafe concurrency laboratory. Its purpose is to train proof review and rejection boundaries, not to provide a general queue for application use.

## Contract

Requested capacity is nonzero and uses one sentinel slot. Endpoints are `Send` when `T: Send` and not `Sync`. Producer and consumer use release/acquire index publication. Inner drop occurs after endpoints disappear and destroys exactly unread initialized values. No MPMC, fairness, blocking, or general reclamation claim is made.

## Required milestones

1. Write slot-state and role tables.
2. Construct one producer and consumer with private fields.
3. Implement push/pop kernels with local safety comments.
4. Implement unread-value destruction.
5. Test wraparound and endpoint auto-trait intent.

## Adversarial cases

- capacity zero
- capacity one
- full
- empty
- many wraparounds
- producer dropped first
- consumer dropped with unread values
- drop-counted payload
- attempted endpoint cloning

## Evidence to produce

- unsafe obligation register
- release/acquire graph
- slot initialization diagram
- drop-count test
- explicit nonclaims

## Prohibited shortcuts

- cloneable endpoints
- public raw inner access
- SeqCst as substitute for role proof
- dropping every slot
- generalizing to MPMC
- immediate reclamation of pointer nodes

## Transfer

Transfer the proof method to a fixed one-writer/one-reader telemetry mailbox. State whether overwriting unread data is allowed and how that changes slot ownership.

## Comparing with the reference

Compare each `SAFETY:` comment to the global obligation register. The reference is acceptable only if private API shape enforces the assumptions that unsafe code cites.

## Completion check

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Work from `starter/` and do not open `solution/` until the protocol, adversarial cases, and transfer are implemented or a precise blocker is written.

The laboratory is complete when the tests and documented failure paths pass, and you can answer the governing question without the chapter:

For **Laboratory 68 — Bounded SPSC Ring**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Working route

1. Read the product contract and run the starter’s baseline checks for **Bounded SPSC Ring**.
2. Draw the smallest **atomic state machine** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to BatchWeave so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Distinguish obstruction-free, lock-free, and wait-free progress claims from ordinary nonblocking API behavior.
- Explain why `UnsafeCell` is necessary for mutation through shared references and why it removes automatic `Sync`.
- Use `MaybeUninit<T>` to represent slots whose initialization state is governed by a concurrent protocol.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 68 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **atomic state machine**. Defend why your design is simpler than one plausible alternative under the new requirements.

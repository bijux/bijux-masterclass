# Laboratory 68 — Bounded SPSC Ring

This is the independent product for **Course 7, Module 68**. Read the [module chapter](../../course-book/module-68-lock-free-protocols-reclamation-and-unsafe-send-sync/index.md) and complete its [workbook](../../course-book/module-68-lock-free-protocols-reclamation-and-unsafe-send-sync/workbook.md) before consulting the reference implementation.

## Learning target

> What exact role, initialization, atomic-ordering, and destruction proof makes a safe one-producer/one-consumer ring possible?

By the end, the answer must be visible in the public API, protocol diagram, failure behavior, causal tests, and explanation—not merely in a successful run.

## Product

Build a fixed-capacity SPSC queue that returns one non-cloneable producer and one non-cloneable consumer. Push and pop are nonblocking. Shared storage uses `UnsafeCell<MaybeUninit<T>>` behind a private unsafe `Sync` proof.

## Why this laboratory exists

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

> What exact role, initialization, atomic-ordering, and destruction proof makes a safe one-producer/one-consumer ring possible?

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

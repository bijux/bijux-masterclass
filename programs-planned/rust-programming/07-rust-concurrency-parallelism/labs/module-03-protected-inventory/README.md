# Laboratory 63 — Protected Inventory

This is the independent product for **Course 7, Module 63**. Read the [module chapter](../../course-book/module-63-shared-state-locks-and-protected-invariants/index.md) and complete its [workbook](../../course-book/module-63-shared-state-locks-and-protected-invariants/workbook.md) before consulting the reference implementation.

## Learning target

> Which complete business relation belongs under one lock, and how do concurrent callers preserve it through success, rejection, snapshot, and panic?

By the end, the answer must be visible in the public API, protocol diagram, failure behavior, causal tests, and explanation—not merely in a successful run.

## Product

Build a shared reservation inventory with immutable capacity and mutex-protected available/reserved counts. Concurrent callers reserve and release units. Every public observation is an owned snapshot.

## Why this laboratory exists

The lab prevents “mutex per field” reasoning. It makes one multi-field invariant the center of API design and tests guard scope, arithmetic, poisoning policy, and contention without condition variables.

## Contract

The invariant is `available + reserved == capacity`, with neither component above capacity. Reserving or releasing zero is a successful no-op. Failed nonzero reserve/release leaves state unchanged. Public methods never return guards. The solution chooses and documents a fail-closed poison policy. Logging hooks run only after guard release.

## Required milestones

1. Write the invariant and transition table.
2. Implement private state under one mutex.
3. Implement reserve, release, and snapshot.
4. Add an optional post-transition observer called after unlock.
5. Write barrier-coordinated contention tests.

## Adversarial cases

- zero capacity
- reserve and release zero
- reserve above available
- release above reserved
- two contenders for one unit
- observer re-enters snapshot
- poisoned state

## Evidence to produce

- invariant and linearization points
- guard-scope trace
- barrier-based contention test
- reentrant observer test
- poisoning decision

## Prohibited shortcuts

- separate locks for related fields
- callback while holding the guard
- sleep-based winner assertions
- public guard return
- blind poison recovery

## Transfer

Transfer the design to adjacent-seat booking. Decide whether one coarse seating-map lock remains preferable to per-row locks when a booking may span rows.

## Comparing with the reference

Compare invariant placement and observer timing. The reference should update both fields before unlock, reject without mutation, and call unknown code only on an owned snapshot after the guard is gone.

## Completion check

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Work from `starter/` and do not open `solution/` until the protocol, adversarial cases, and transfer are implemented or a precise blocker is written.

The laboratory is complete when the tests and documented failure paths pass, and you can answer the governing question without the chapter:

> Which complete business relation belongs under one lock, and how do concurrent callers preserve it through success, rejection, snapshot, and panic?

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

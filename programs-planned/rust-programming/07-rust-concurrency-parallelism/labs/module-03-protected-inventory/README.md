# Laboratory 63 — Protected Inventory

**Course 7 · Module 63: Shared State: Locks and Protected Invariants**

[Chapter](../../course-book/module-63-shared-state-locks-and-protected-invariants/index.md) · [Workbook](../../course-book/module-63-shared-state-locks-and-protected-invariants/workbook.md) · [BatchWeave guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Shared State: Locks and Protected Invariants**: Which exact invariant does a lock protect, how small can the protected transition be, and what state remains valid after contention or panic? The product must make **Name the state invariant protected by each `Mutex` or `RwLock` rather than treating the primitive as a generic thread-safety wrapper** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **protected-invariant table** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

> Which complete business relation belongs under one lock, and how do concurrent callers preserve it through success, rejection, snapshot, and panic?

By the end, the answer must be visible in the public API, protocol diagram, failure behavior, causal tests, and explanation—not merely in a successful run.

## Product

Build a shared reservation inventory with immutable capacity and mutex-protected available/reserved counts. Concurrent callers reserve and release units. Every public observation is an owned snapshot.

## Product-specific design pressure

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

For **Laboratory 63 — Protected Inventory**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Working route

1. Read the product contract and run the starter’s baseline checks for **Protected Inventory**.
2. Draw the smallest **protected-invariant table** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to BatchWeave so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Name the state invariant protected by each `Mutex` or `RwLock` rather than treating the primitive as a generic thread-safety wrapper.
- Distinguish shared liveness supplied by `Arc` from exclusion supplied by a lock.
- Keep guard scope limited to the smallest complete state transition.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 63 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **protected-invariant table**. Defend why your design is simpler than one plausible alternative under the new requirements.

# Reasoned Solutions — Module 63: Shared State: Locks and Protected Invariants

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-03-protected-inventory/README.md) · [BatchWeave guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 63: Shared State: Locks and Protected Invariants**. Compare the reasoning against this question: *Which exact invariant does a lock protect, how small can the protected transition be, and what state remains valid after contention or panic?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Part 1 — Prediction solutions

### Prediction 1

A snapshot can observe capacity one, available zero, reserved zero between the two updates. Put both fields under one lock or encode the transition in one atomic state when the representation permits it.

### Prediction 2

The sender waits for channel capacity while holding the mutex; the receiver cannot drain or process because it waits for the mutex. Drop the guard before the blocking send or redesign ownership so the receiver does not need that lock.

### Prediction 3

`Arc` only keeps the allocation alive across owners. Mutation still requires exclusive ownership, a lock, atomics, or another synchronized interior-mutation mechanism.

### Prediction 4

Recovering the inner state is memory-safe, but the product has not proved that a panic left the relation valid. Validate, repair, rebuild, or fail closed according to an explicit policy.

### Prediction 5

Callers can extend guard duration, call unknown code, violate lock order, and couple the type’s invariant to external effects. Return an owned snapshot or expose a narrower operation.

### Prediction 6

No. Standard-library lock fairness is platform-dependent and not a portable correctness premise. Use a protocol whose safety does not require that order, or implement/test an explicit queueing policy.

### Prediction 7

Sleep does not causally establish acquisition order and can pass or fail due to load. Use barriers or channels to establish the intended precondition, then assert an invariant independent of the winner.

### Prediction 8

The protected transition is complete before logging, contention is reduced, and a reentrant logger cannot attempt to reacquire the same guard. The snapshot remains an owned consistent observation.

## Part 2 — Repair reasoning

Capacity is immutable; available and reserved belong in one `State` under one mutex. Reserve and release validate and update both fields while holding one guard. Snapshot locks the same state. Logging receives an owned snapshot after unlock. If panic can only occur outside the critical section, poison should be rare; if it occurs inside, fail closed or validate the capacity relation before recovery.

The lock-order table collapses because ordinary operations acquire one lock. This is not “less advanced”; it is a smaller and more reviewable correctness surface.

## Part 3 — Focused construction guidance

### Construction 1

One lock gives a single transfer transition and simple snapshots. Two account locks require stable account-ID order, forbid callbacks while both are held, and need a separate strategy for total-balance snapshots. Choose based on actual contention, not abstraction fashion.

### Construction 2

Read state and revision under lock, release it, run the callback on owned input, then reacquire and commit only if revision still matches. Retry or report conflict explicitly.

### Construction 3

On poison, obtain the inner state, validate metadata, discard derived entries, rebuild from immutable source, then clear poison only after the invariant holds. A rebuild error leaves the cache unavailable rather than silently trusted.

### Construction 4

The design needs measured evidence that concurrent reads are long and dominant. Correctness cannot depend on writer preference. A mutex may be simpler and faster for tiny reads.

### Construction 5

Use a barrier to release two reservers together. With capacity one, join both and assert exactly one success, one insufficiency error, and a final snapshot whose relation remains valid.

## Part 4 — Laboratory comparison

Compare invariant placement first. The reference should have one private state lock, owned snapshots, short guards, and no sleep-based tests. Inspect whether arithmetic is checked, whether error paths leave the relation unchanged, and whether the poison behavior matches the written contract.

## Part 5 — Capstone comparison

The queue state should already make impossible states difficult: capacity is nonzero and immutable, buffer length never exceeds it, and once closed no push succeeds. Waiting is intentionally absent so Module 64 can add notification without redefining truth. This separation prevents condition variables from becoming the state model.

## Part 6 — Reconstruction and defense

A strong defense names the invariant, the linearization point, and every observer that follows the protocol. It explains guard scope and poison policy, and it does not claim fairness or performance without evidence. The simplest coherent lock boundary is preferred until measured contention justifies a more complex graph.

A strong defense states what is guaranteed for every allowed schedule, what is merely likely on one machine, and what the design intentionally leaves unspecified.

## Deep reasoning and transfer

### Decisive model

> Which exact invariant does a lock protect, how small can the protected transition be, and what state remains valid after contention or panic?

Build a **protected-invariant table**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Name the state invariant protected by each `Mutex` or `RwLock` rather than treating the primitive as a generic thread-safety wrapper.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Distinguish shared liveness supplied by `Arc` from exclusion supplied by a lock.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Keep guard scope limited to the smallest complete state transition.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Avoid performing user callbacks, channel sends, file I/O, or expensive computation while holding a guard.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Choose between one coarse invariant lock and several locks with an explicit ordering protocol.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Name the state invariant protected by each `Mutex` or `RwLock` rather than treating the primitive as a generic thread-safety wrapper.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the protected-invariant table.

### Reference implementation comparison

For [Protected Inventory](../../labs/module-03-protected-inventory/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In BatchWeave, Module 63 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Shared State: Locks and Protected Invariants**, which relationship decides this question: “Which exact invariant does a lock protect, how small can the protected transition be, and what state remains valid after contention or panic?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to BatchWeave?

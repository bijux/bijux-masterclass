# Laboratory 64 — Phase Gate

**Course 7 · Module 64: Coordination: Condvars, Barriers, and Phase Protocols**

[Chapter](../../course-book/module-64-coordination-condvars-barriers-and-phase-protocols/index.md) · [Workbook](../../course-book/module-64-coordination-condvars-barriers-and-phase-protocols/workbook.md) · [BatchWeave guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Coordination: Condvars, Barriers, and Phase Protocols**: How do threads wait for a state predicate or phase transition without polling, lost wakeups, or treating notification itself as truth? The product must make **Write every condition-variable wait as a predicate loop over mutex-protected state** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **predicate and wakeup record** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

> How can a group wait for durable phase predicates, tolerate spurious wakeups, and enter a terminal state that releases every waiter?

By the end, the answer must be visible in the public API, protocol diagram, failure behavior, causal tests, and explanation—not merely in a successful run.

## Product

Build a reusable phase gate with states `Created`, `Prepared`, `Running`, `Finished`, and `Cancelled`. Threads may wait until a minimum phase or a terminal cancellation. Legal transitions are monotonic and protected by one mutex plus condition variable.

## Product-specific design pressure

The lab removes queue payloads so the only difficulty is predicate-based coordination. It also includes one fixed-cohort barrier exercise to contrast phase state with rendezvous.

## Contract

Waiters loop under the mutex. Advancing to the same phase is idempotent; backward or post-terminal transitions fail. Cancellation is terminal and notifies all. Timed waits use one monotonic deadline. The barrier helper accepts a fixed participant count, joins every participant, reports worker panic, checks sum overflow, and makes no cancellation claim.

## Required milestones

1. Define the phase order and transition errors.
2. Implement `wait_until` as a predicate loop.
3. Implement deadline-based waiting without resetting the budget.
4. Implement terminal cancellation and notify-all.
5. Add a fixed-cohort barrier demonstration.

## Adversarial cases

- spurious wake simulation through irrelevant notification
- waiter starts after phase already advanced
- backward transition
- double cancellation
- timeout near deadline
- barrier participant count one
- cohort sum overflow
- waiters released by cancellation

## Evidence to produce

- predicate definitions
- transition table
- timeout budget trace
- causal waiter-release tests
- barrier participant obligations and complete join accounting

## Prohibited shortcuts

- using `if` around wait
- treating notification as state
- sleeping before notify
- resetting timeout after wake
- using a barrier when participants can cancel

## Transfer

Transfer the gate to a media pipeline. Then allow one decoder to fail before the barrier and replace the barrier phase with cancellable state plus condition-variable waiting.

## Comparing with the reference

Compare predicate loops and terminal behavior. The reference should let late waiters proceed immediately, keep timeout against one deadline, and never require a notification history to reconstruct truth.

## Completion check

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Work from `starter/` and do not open `solution/` until the protocol, adversarial cases, and transfer are implemented or a precise blocker is written.

The laboratory is complete when the tests and documented failure paths pass, and you can answer the governing question without the chapter:

For **Laboratory 64 — Phase Gate**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Working route

1. Read the product contract and run the starter’s baseline checks for **Phase Gate**.
2. Draw the smallest **predicate and wakeup record** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to BatchWeave so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Write every condition-variable wait as a predicate loop over mutex-protected state.
- Explain the atomic unlock-and-wait transition and why it prevents the ordinary lost-wakeup window.
- Distinguish `notify_one` and `notify_all` by which state transition can enable which waiters.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 64 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **predicate and wakeup record**. Defend why your design is simpler than one plausible alternative under the new requirements.

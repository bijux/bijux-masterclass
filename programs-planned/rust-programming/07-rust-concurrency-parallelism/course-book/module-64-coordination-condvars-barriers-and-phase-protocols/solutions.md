# Reasoned solutions — Module 64: Coordination: Condvars, Barriers, and Phase Protocols

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the BatchWeave guide](../capstone.md)

The decisive correction is to place truth in protected state. Condition variables, barriers, and one-time cells coordinate observation of state transitions; they do not replace the state model. Every strong answer names the predicate and the event that can make it true.

The answers below are reasoning models, not scripts to imitate. A different implementation can be stronger when it proves the same contract more directly. Compare ownership, synchronization, progress, failure, and determinism—not only surface syntax.

## Part 1 — Prediction solutions

### Prediction 1

A spurious return can pass the `if` and pop from an empty queue or proceed with false assumptions. Use a `while` loop that rechecks empty and closed under the reacquired guard.

### Prediction 2

Yes. The item is durable state. The consumer locks, sees nonempty, and does not wait. Correctness does not depend on remembering the earlier notification.

### Prediction 3

One consumer reacquires the mutex first and pops. The other later sees empty and loops back to waiting unless the queue is closed. The predicate serializes competition.

### Prediction 4

The blocked producer may remain asleep forever because closure enables it to return an error but no producer-side notification occurs. Close should notify all waiters on both conditions.

### Prediction 5

The remaining three participants can wait forever for an arrival that will never occur. Barrier membership must be fixed and failure-compatible, or the protocol needs a cancellable phase state.

### Prediction 6

Total wait can exceed the intended budget indefinitely. Compute one deadline and pass only the remaining duration on each iteration.

### Prediction 7

The first test fixes process-global state for later tests, creating order dependence and preventing independent configuration. Inject per-test configuration instead.

### Prediction 8

The wait is not synchronized with the predicate transition and may panic because a condition variable is used with multiple mutexes. Use exactly the mutex that protects the predicate.

## Part 2 — Repair reasoning

The correct queue has one protected state containing buffer and closed flag. Consumers loop on `empty && !closed`; producers loop on `full && !closed`. Push notifies one consumer, pop notifies one producer, and close notifies all on both condition variables. This removes sentinel-count coupling and supports any fixed worker count.

Thread parking can implement coordination, but then the product must build its own durable waiter registration and wake protocol. For this course’s queue, condition variables express the invariant more directly and reduce custom proof surface.

## Part 3 — Focused construction guidance

### Construction 1

The state machine distinguishes open-empty, open-partial, open-full, closed-nonempty, and closed-empty. Push is enabled only in open states with capacity; pop is enabled when nonempty; termination occurs at closed-empty.

### Construction 2

Lock, compute one deadline, loop while empty and open, wait for remaining duration, and recheck. Return `Item`, `Closed`, or `TimedOut` based on protected state after wake.

### Construction 3

Every phase must have the same fixed cohort or a new barrier. Each participant reaches exactly once per phase. A panic before arrival makes the design unsuitable unless panic aborts the whole process.

### Construction 4

An immutable parser table is a valid process-wide one-time value. Test configuration varies by test and should be passed explicitly; a global cell would make the first initializer authoritative accidentally.

### Construction 5

Fill a capacity-one queue, start a producer that announces immediately before calling `push`, wait for that announcement, then pop and join. The assertion concerns eventual completion and value order, not an exact delay.

## Part 4 — Laboratory comparison

Inspect the predicates before code. The reference should loop, represent a terminal phase in state, and notify all on termination. A barrier test is acceptable only when all participants are controlled and guaranteed to arrive. Sleep-based “proof” should be replaced by handshake channels or barriers that establish the precondition.

## Part 5 — Capstone comparison

The queue is now a complete coordination abstraction. Its API should not expose condition variables or guards. Job execution occurs after `pop` returns, so expensive and fallible work cannot poison the queue lock. Close is idempotent and wakes every blocked operation. These facts become prerequisites for cancellation in Module 66.

## Part 6 — Reconstruction and defense

A complete defense names every wait predicate and every transition that can enable it. It explains atomic unlock-and-wait, looped rechecking, closure notification, and fixed barrier membership. It does not claim that notifications are queued messages or that timeout proves no notification occurred.

A strong defense states what is guaranteed for every allowed schedule, what is merely likely on one machine, and what the design intentionally leaves unspecified.

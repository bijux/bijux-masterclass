# Laboratory 3 — Callback Budget

## Product and purpose

The product searches an ordered source through an expensive synchronous operation. Its real contract includes invocation count, ordering, stopping, retention, and failure—facts a callable type alone cannot express.

## Entry standard

Complete a callable contract ledger for the attempt and acceptance callbacks: argument, result, invocation count, order, retention, receiver, timing, and failure. Predict the Module 3 cases before running them. The starter contains a deliberately small synchronous callback boundary; you must establish the exact stopping rule and prove it through call-sequence evidence.

## Public contract

`firstAccepted` receives source values, a nonnegative safe call budget, an attempt callback, and an acceptance predicate. It returns accepted value with source index and call count, source exhausted, or budget exhausted. Callbacks are synchronous, not retained, and never retried after a throw.

## Required construction sequence

Implement the result union and loop from the observable rules. Test empty input, zero budget, first acceptance, acceptance on the final permitted call, source exhaustion, thrown attempt, and mutable closure state. Record exact call sequences rather than testing only the result.

Keep the public surface small. Add private helpers only when they name a real step or invariant. Each exported function needs at least one success test and one boundary or failure test.

## Adversarial review

Record exact attempt and predicate calls for empty source, zero budget, acceptance on the first and last permitted call, budget exhaustion before source exhaustion, source exhaustion first, mutable closure state, and a thrown attempt. Confirm that no later callback executes after a throw and that the result’s call count matches the trace rather than a guessed loop index.

## Prohibited shortcuts

Do not precompute attempts with `map`, call the acceptance predicate after an attempt throws, exceed the budget by one, or catch and retry arbitrary callback failures. Do not document asynchronous callbacks when the implementation does not await them.

A shortcut is prohibited because it destroys the reasoning target, not because the reference implementation uses a different style.

## Completion evidence

The laboratory is complete when exact call traces prove count, order, stopping, and throw behavior for every terminal result. The implementation must never exceed the budget, retain callbacks, retry a thrown attempt, or claim async support. Explain why your loop publishes the right call count at each return point before inspecting the reference.

## Independent transfer

Add an observation callback invoked after each successful attempt. Decide whether observer failure aborts selection and state that choice in types, prose, and tests.

Add the observer to the callable contract ledger before changing the signature. State whether it runs before or after acceptance testing, whether it receives failed attempts, and whether an observer throw consumes a budget call.

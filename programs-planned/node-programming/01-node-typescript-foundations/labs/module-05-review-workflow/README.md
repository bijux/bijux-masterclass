# Laboratory 5 — Review Workflow

## Product and purpose

The review workflow turns state modeling into an executable protocol. Its closed union should remove fields and methods that do not make sense in the current state instead of relying on optional-property discipline.

## Entry standard

List the legal workflow states and transitions without using optional fields. For each state, write the fields that must exist and those that must not exist. Predict the Module 5 narrowing cases, then run the starter. Its baseline proves only that one union member can be rendered; complete validation, transitions, and exhaustiveness remain open.

## Public contract

States are draft, in-review, approved, and rejected. Draft can be submitted; in-review can be approved or rejected; terminal states cannot transition. State-specific timestamps and reason/note fields exist only where meaningful. Rendering is exhaustive.

## Required construction sequence

Define narrow transition functions first, then an aggregate operation if needed for dynamic commands. Test every legal edge and every illegal source state. Add an unknown-data validator or at least a table showing why a status string alone cannot establish the union.

Keep the public surface small. Add private helpers only when they name a real step or invariant. Each exported function needs at least one success test and one boundary or failure test.

## Adversarial review

Challenge every legal and illegal transition, repeated transition, absent reviewer, empty rationale, malformed unknown status, extra state-specific field, and stale object narrowed before an external effect. Verify that rendering is exhaustive and that impossible input is rejected at the boundary rather than forced through a cast or broad optional-field shape.

## Prohibited shortcuts

Do not create one interface with optional terminal fields, use arbitrary status strings, cast persisted objects to Review, or swallow illegal transitions as no-ops. Do not put edit behavior on terminal states merely because one class-like object is convenient.

A shortcut is prohibited because it destroys the reasoning target, not because the reference implementation uses a different style.

## Completion evidence

The laboratory is complete when the union represents every legal state without contradictory optional fields, transitions accept only valid source states, unknown values are checked at runtime, and exhaustive rendering fails statically when a new variant is omitted. Show one malformed value that a cast would admit and your decoder rejects before opening the reference.

## Independent transfer

Add withdrawn as a terminal state reachable from draft or in-review. Use the compiler to locate every exhaustive policy surface and document the difference between compiler evidence and runtime validation.

Define the exact state transition and required fields for the new revision state. Update the union, decoder, renderer, transition functions, and exhaustiveness evidence together; do not add another optional field to every member.

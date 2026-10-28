# Module 5 Solutions

## A. State design

Queued requires an ID and source. Active adds start time and perhaps worker identity. Completed requires result path, byte count, and completion time. Failed requires an error description and failure time. Do not leave completed-only fields optional on every state.

## B. Narrowing

`typeof string` leaves strings only. The object/null check leaves non-null objects including arrays unless separately rejected. An `in` check proves property presence but not the property’s value type. The completed discriminant selects `CompletedSession`. Truthiness removes null, zero, and empty string, which may be too broad for the domain.

## C. Validator

First prove a non-null non-array object. Read properties as unknown. Require `attempts` to be a positive safe integer and `mode` to equal one of the literals. Return a newly constructed object from validated values. The construction, not an assertion over the original object, is the trust boundary.

## D. Exhaustiveness

Adding `paused` makes the argument passed to `assertNever` have the paused type. Every exhaustive switch now fails type checking until a deliberate case is added.

## E–F. Design notes

Aggregate lookup may begin with the broad union, but it should narrow and delegate to state-specific transition functions. StudyLedger’s renderer and command dispatcher should use exhaustive switches so future members create visible work.

## G. Readiness answer

Structural typing compares shape. `unknown` preserves safety until narrowed; `any` disables it. Assertions alter belief, validators establish runtime evidence. A discriminant selects one union member. Exact optional properties distinguish absence from present undefined. `never` proves no statically known alternative remains after exhaustive handling.

## Extended solution

Contradictory original values include completed without `actualMinutes`, planned with `completedAt`, active with `reason`, and rejected arbitrary status text. The union assigns state-specific fields to each variant. Abandoned records `startedAt: string | null` so the terminal state preserves whether work began without optional-property ambiguity.

A predicate that checks only `status` can accept missing IDs, invalid minutes, impossible chronology, and missing terminal fields. Hostile tests need null, arrays, unknown status, completed without actual minutes, duplicate IDs at the ledger layer, and wrong field types.

When a fifth state is added, exhaustive renderers and summaries should fail until policy is supplied. Casting to never deletes that evidence. The correct repair handles the new state and updates every affected transition, decoder, and report.

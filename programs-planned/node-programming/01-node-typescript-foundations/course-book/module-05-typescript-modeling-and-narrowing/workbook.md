# Module 5 Workbook

## A. Repair the state bag

Convert this into a discriminated union:

```ts
interface Upload {
  state: string;
  path?: string;
  bytes?: number;
  error?: string;
}
```

Required states are queued, active, completed, and failed. Decide which fields each state must contain.

## B. Narrowing prediction

For each check, state the narrowed type and any runtime values still possible:

- `typeof value === 'string'`
- `value !== null && typeof value === 'object'`
- `'status' in value` after proving `value` is an object
- `session.status === 'completed'`
- `if (value)` where `value: string | 0 | null`

## C. `unknown` validator

Write a small validator for:

```ts
interface RetryPolicy {
  readonly attempts: number;
  readonly mode: 'fixed' | 'exponential';
}
```

Reject arrays, null, missing fields, extra invalid values, fractions, and nonpositive attempts. Do not use `as RetryPolicy` until every field has been established.

## D. Exhaustiveness

Add a new `paused` state to a union and show how `assertNever` identifies every switch that requires a policy decision.

## E. Independent laboratory

Complete [Review Workflow](../../labs/module-05-review-workflow/README.md). Invalid transitions should be unrepresentable in the narrow transition functions and explicitly rejected at the aggregate boundary.

## F. StudyLedger transfer

Implement the full session and command unions. Test every legal transition, representative illegal transitions, and exhaustive rendering.

## G. Reconstruction

Explain structural typing, unknown versus any, type assertion versus runtime validation, discriminant narrowing, optional-property semantics, and the exact evidence provided by `never`.

## H. State-model repair

Replace this interface with a closed union:

```ts
interface Session {
  status: string;
  topic: string;
  startedAt?: string;
  completedAt?: string;
  actualMinutes?: number;
  reason?: string;
}
```

List four contradictory values the original interface permits. Define the legal fields for planned, active, completed, and abandoned states. Decide how an abandoned session records whether it had started.

## I. Predicate audit

Review a user-defined predicate that returns `true` whenever an object has a `status` string. Explain why that does not establish `StudySession`. Write the minimum hostile cases needed to disprove it.

## J. StudyLedger checkpoint

Write exhaustive rendering and an `assertNever` helper. Temporarily add a fifth state and observe every compilation site that reveals missing policy. Do not keep casts to `never` as repairs.

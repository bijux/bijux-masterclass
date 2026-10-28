# Module 5 — TypeScript Modeling, Unions, Narrowing, `unknown`, and `never`

> **Question:** How can static types express the domain while runtime checks establish facts about external values?

## Why this comes now

You can now reason about runtime values, functions, and object identity. TypeScript becomes useful when it describes those relationships rather than hiding them. The core Course 1 technique is the discriminated union: each valid state carries exactly the fields that state requires, and control flow narrows the alternatives.

The module also establishes a strict trust rule: external data begins as `unknown`. TypeScript narrowing is driven by runtime evidence, not by assertions.

## Outcomes

You can:

- choose between type aliases and interfaces without treating the choice as ideology;
- explain structural compatibility and excess-property checks;
- model closed alternatives with literal types and discriminated unions;
- narrow using `typeof`, equality, property checks, predicates, and switch statements;
- distinguish `unknown`, `any`, and a validated domain value;
- use `never` to expose an unhandled alternative;
- model StudyLedger states without contradictory optional fields or boolean flags.

## 1. Types describe sets of possible values

```ts
interface PlannedSession {
  readonly status: 'planned';
  readonly id: number;
  readonly topic: string;
  readonly plannedMinutes: number;
  readonly createdAt: string;
}
```

The interface describes object values with at least the required structure. TypeScript is structurally typed: a value can be compatible without explicitly declaring that it implements the interface.

This is powerful for composition and testing, but it means type names do not create runtime brands. A plain object with matching members is accepted. Runtime validation remains necessary at external boundaries.

## 2. Avoid the optional-field state bag

A weak model is:

```ts
interface Session {
  status: string;
  startedAt?: string;
  completedAt?: string;
  actualMinutes?: number;
  abandonmentReason?: string;
}
```

It permits contradictory and incomplete combinations:

- `status: 'completed'` with no completion time;
- a planned session with an abandonment reason;
- an active session with an actual duration;
- an arbitrary status spelling.

A discriminated union encodes the alternatives:

```ts
interface SessionBase {
  readonly id: number;
  readonly topic: string;
  readonly plannedMinutes: number;
  readonly createdAt: string;
}

interface PlannedSession extends SessionBase {
  readonly status: 'planned';
}

interface ActiveSession extends SessionBase {
  readonly status: 'active';
  readonly startedAt: string;
}

interface CompletedSession extends SessionBase {
  readonly status: 'completed';
  readonly startedAt: string;
  readonly completedAt: string;
  readonly actualMinutes: number;
  readonly note?: string;
}

interface AbandonedSession extends SessionBase {
  readonly status: 'abandoned';
  readonly abandonedAt: string;
  readonly reason: string;
}

export type StudySession =
  | PlannedSession
  | ActiveSession
  | CompletedSession
  | AbandonedSession;
```

Now `completedAt` is available only after TypeScript has evidence that the state is completed.

## 3. Narrowing follows runtime checks

```ts
function renderSession(session: StudySession): string {
  switch (session.status) {
    case 'planned':
      return `${session.id}\tplanned\t${session.topic}`;
    case 'active':
      return `${session.id}\tactive\t${session.startedAt}\t${session.topic}`;
    case 'completed':
      return `${session.id}\tcompleted\t${session.actualMinutes}\t${session.topic}`;
    case 'abandoned':
      return `${session.id}\tabandoned\t${session.reason}\t${session.topic}`;
    default:
      return assertNever(session);
  }
}

function assertNever(value: never): never {
  throw new Error(`unhandled session: ${JSON.stringify(value)}`);
}
```

If a new union member is added, the default branch receives that member rather than `never`, causing a type error. This is static evidence for a closed model. It is not runtime validation of arbitrary objects.

## 4. `unknown` versus `any`

`any` disables meaningful checking in both directions. `unknown` accepts any value but requires evidence before use:

```ts
function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}
```

A validator can then inspect properties. The predicate itself is a proof boundary: if it returns true incorrectly, TypeScript trusts a false claim. Keep predicates small and test them adversarially.

Type assertions are appropriate only when another verified mechanism establishes the fact but TypeScript cannot express it. They are not a parsing strategy.

## 5. Optional properties need exact semantics

With `exactOptionalPropertyTypes`, this:

```ts
interface CompletedSession {
  readonly note?: string;
}
```

means the property may be absent; it does not automatically mean a present property may contain `undefined`. That distinction improves JSON and object-shape reasoning.

Choose among:

- absent property;
- `string | undefined` property always present;
- `string | null` with explicit null representation.

StudyLedger omits an absent note in canonical storage.

## 6. Structural typing and accidental compatibility

Two types with identical structure are compatible even if the domain names differ:

```ts
interface UserId { value: number }
interface SessionId { value: number }
```

Course 1 avoids overengineering brands but uses dedicated parsers and parameter names to keep roles clear. Course 3 will introduce stronger advanced type techniques. When accidental interchange would create serious harm, a branded or class-based boundary may be justified earlier.

## 7. User-defined predicates and assertion functions

A predicate narrows on true:

```ts
function isStatus(value: unknown): value is StudySession['status'] {
  return value === 'planned'
    || value === 'active'
    || value === 'completed'
    || value === 'abandoned';
}
```

An assertion function throws on failure and narrows after return:

```ts
function assertString(value: unknown, path: string): asserts value is string {
  if (typeof value !== 'string') {
    throw new Error(`${path} must be a string`);
  }
}
```

Use predicates for branchable checks and assertion functions when failure should immediately leave the current operation. Module 8 builds complete validators with structured issues.

## 8. Functions should accept the narrowest valid state

```ts
function startSession(
  session: PlannedSession,
  startedAt: string,
): ActiveSession {
  return { ...session, status: 'active', startedAt };
}
```

This signature makes an invalid transition uncallable from correctly typed code. A function accepting `StudySession` and throwing when the state is wrong is sometimes necessary at a dynamic lookup boundary, but the narrow transition should remain the domain core.

The application can narrow after finding a session:

```ts
if (session.status !== 'planned') {
  throw new Error(`session ${session.id} cannot start from ${session.status}`);
}
return startSession(session, startedAt);
```

## 9. Commands are also a discriminated union

```ts
export type Command =
  | { readonly kind: 'plan'; readonly topic: string; readonly minutes: number }
  | { readonly kind: 'start'; readonly id: number }
  | { readonly kind: 'complete'; readonly id: number; readonly minutes: number; readonly note?: string }
  | { readonly kind: 'abandon'; readonly id: number; readonly reason: string }
  | { readonly kind: 'list'; readonly status?: StudySession['status'] }
  | { readonly kind: 'summary' }
  | { readonly kind: 'help' }
  | { readonly kind: 'version' };
```

This separates raw token grammar from executable application intent. Unknown command names never enter the union.

## 10. StudyLedger increment

Replace provisional records with the complete session union. Implement:

- state-specific transition functions;
- exhaustive rendering;
- a typed command union;
- application dispatch that narrows each command;
- tests proving invalid transitions fail before a candidate ledger is returned.

Keep validation of persisted unknown objects for Module 8. Today’s trusted in-memory model still needs correct construction authority.

## Common wrong models

### “TypeScript types validate JSON”

Types are erased. A parsed object must be checked at runtime.

### “Optional fields are a flexible state model”

They often permit contradictory shapes. Use a union when alternatives have different required data.

### “`as` converts a value”

It changes static interpretation only.

### “A type predicate is automatically correct”

The implementation is a trusted proof boundary and can lie.

### “`never` makes impossible runtime input disappear”

It proves exhaustiveness over the static union. External input still requires validation.

## 11. Types are sets and operations over sets

Think of a type as a set of possible runtime values. A union broadens the set:

```ts
type Identifier = string | number;
```

An intersection requires a value to satisfy both structures:

```ts
type Timestamped = { createdAt: string };
type Named = { name: string };
type NamedRecord = Timestamped & Named;
```

This model helps explain narrowing. A runtime check removes possibilities from the current set. It does not transform the value into a different runtime category.

A discriminated union works well because checking one literal property partitions the set cleanly. Optional-field bags do not: many combinations remain representable, including contradictory ones.

## 12. Structural typing and accidental compatibility

TypeScript usually compares structure rather than declared identity:

```ts
interface UserId { value: number }
interface OrderId { value: number }

const user: UserId = { value: 1 };
const order: OrderId = user; // structurally compatible
```

This can be convenient, but domains sometimes need nominal distinction. Later courses introduce branded and opaque types. In Course 1, keep constructors and parameter names explicit and avoid reusing indistinguishable wrappers for unrelated concepts.

Excess-property checking is a limited convenience, not a general exact-object guarantee:

```ts
interface Point { x: number; y: number }
// const direct: Point = { x: 1, y: 2, label: 'A' }; // warning
const wider = { x: 1, y: 2, label: 'A' };
const assigned: Point = wider; // allowed
```

Runtime validators must check unknown keys themselves when misspellings or schema drift should be rejected.

## 13. Narrowing can become stale after effects

TypeScript tracks control flow, but an external call may change mutable data through an alias:

```ts
interface Box { value?: string }

function consume(box: Box, effect: () => void): string {
  if (box.value === undefined) throw new Error('missing');
  effect();
  return box.value.toUpperCase();
}
```

If `effect` can mutate the same box, the earlier proof may no longer match reality. Prefer copying the narrowed primitive into a local binding before unknown effects, or use immutable boundaries.

This is one reason state transitions return new values in StudyLedger. The discriminant and state-specific fields remain coherent within one value.

## 14. User-defined predicates are proof-producing code

A predicate signature such as:

```ts
function isConfig(value: unknown): value is Config
```

asks TypeScript to trust the implementation. A buggy predicate can introduce the same unsound belief as an assertion. Test predicates against hostile shapes and keep them small.

Assertion functions are even stronger:

```ts
function assertConfig(value: unknown): asserts value is Config {
  if (!isConfig(value)) throw new Error('invalid config');
}
```

Use them when failure should interrupt control flow. Use result objects when callers need to collect or render multiple issues.

## 15. Model transitions in function signatures

A narrow transition can make illegal calls unrepresentable for typed callers:

```ts
function approve(review: InReview, decidedAt: string): Approved
```

An aggregate application command may begin with `Review` and perform a runtime state check before calling the narrow transition. These layers serve different callers:

- the narrow function supports composition after state is known;
- the aggregate operation handles dynamic IDs and commands;
- the decoder establishes that persisted unknown data is some valid `Review`.

Do not force one function to perform all three jobs.

## 16. `never` is evidence of static exhaustiveness

In an exhaustive switch, the remaining value should be `never`:

```ts
function assertNever(value: never): never {
  throw new Error(`unexpected value: ${JSON.stringify(value)}`);
}
```

The runtime throw still matters because untyped JavaScript callers, stale persisted data, or incorrect assertions can violate the static model. `never` does not make impossible runtime data disappear; it makes a gap visible to typed compilation.

## Practice sequence

Complete the [workbook](workbook.md), then [Review Workflow](../../labs/module-05-review-workflow/README.md). Refactor StudyLedger until state-specific fields can be read only after narrowing.

## Ready to continue

Continue when you can explain how every domain value is constructed, which checks narrow it, and why no assertion is being used in place of evidence.

Next: [Module 6 — Collections, Iteration, Generic Relationships, and Deterministic Data](../module-06-collections-iteration-and-generics/index.md)

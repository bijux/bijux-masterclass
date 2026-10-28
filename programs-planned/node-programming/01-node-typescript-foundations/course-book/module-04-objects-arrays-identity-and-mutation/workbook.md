# Module 4 Workbook

## A. Draw alias graphs

For each snippet, draw bindings and object identities before and after execution:

```ts
const a = { nested: { value: 1 } };
const b = { ...a };
b.nested.value = 2;
```

```ts
const items = [{ id: 1 }, { id: 2 }];
const copy = items.slice();
copy[0]!.id = 9;
```

```ts
let source = { value: 1 };
function replace(input: { value: number }): void {
  input = { value: 2 };
}
replace(source);
```

## B. Mutation audit

Classify these array methods as mutating or non-mutating and state whether element objects remain shared: `push`, `map`, `filter`, `sort`, `slice`, `splice`, `concat`, `reverse`.

## C. Repair a false immutable update

```ts
function rename(state: State, id: number, name: string): State {
  const next = { ...state };
  const item = next.items.find((value) => value.id === id);
  if (item) item.name = name;
  return next;
}
```

Repair it so the original state and item remain unchanged, missing IDs fail, and unrelated item identities are preserved.

## D. Equality design

Define domain equality for a study session. Decide whether timestamps, notes, source metadata, and object identity matter. Explain why JSON text and `===` are insufficient.

## E. Independent laboratory

Complete [Inventory Transform](../../labs/module-04-inventory-transform/README.md). Its reference tests include nested aliases and identity-preservation checks.

## F. StudyLedger transfer

Implement append and replace operations. Write assertions for:

- new ledger identity;
- new sessions-array identity;
- changed-session identity;
- unchanged-session identity preservation;
- original state unchanged after a rejected operation.

## G. Reconstruction

Explain copied reference versus copied object, shallow versus deep policy, static readonly versus runtime freezing, and structural sharing versus deep cloning.

## H. Identity ledger

Given an inventory containing three items and nested suppliers, draw identity before and after a supplier email update. Mark every identity that must change and every identity that must remain equal by `===`.

Repair this function without cloning unrelated records:

```ts
function rename(items: readonly Item[], id: number, name: string): readonly Item[] {
  const item = items.find(value => value.id === id)!;
  item.name = name;
  return [...items];
}
```

The failure case for a missing ID must preserve the complete original graph.

## I. Candidate publication

Design a bulk stock adjustment that validates all IDs and final counts before exposing a result. Compare an immutable candidate approach with a mutable staged copy. State the invariant that holds after processing each requested adjustment.

## J. StudyLedger checkpoint

Make plan/start/complete/abandon return new ledgers. Retain every prior value in a test and prove its discriminant has not changed. Check both object identity and semantic fields.

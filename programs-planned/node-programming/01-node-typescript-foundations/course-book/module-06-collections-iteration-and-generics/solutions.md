# Module 6 Solutions

## A. Pipeline reasoning

`filter` retains the input item type unless its predicate is a type guard; order is preserved and cardinality is at most the input. `map` preserves cardinality and order while changing item type. `flatMap` can expand or remove items. `reduce` produces one final accumulator.

## B. Duplicates

Store both value and original index in the temporary map. On a repeated key, report the stored index and current index without replacing the first entry. This retains the first evidence and makes corruption deterministic.

## C. Grouping

Iterate source values once. Create a group array on first key occurrence, then push values in source order. JavaScript `Map` iterates keys in insertion order; decide whether that first-occurrence group order is public or sort keys during rendering.

## D. Search

Normalize once, reject empty text, and compare normalized fields. Do not use `value.note!`; narrow optional presence before normalization.

## E–F. Design notes

StudyLedger query functions accept readonly arrays and return new derived arrays or summary objects. They do not mutate retained state. Unique indexing is a validator or temporary query aid, not a second ledger authority.

## G. Readiness answer

`for...of` yields iterable elements; `for...in` yields enumerable property keys. Collection adapters have specific cardinality semantics. Generics preserve caller-selected relationships. Map is a dynamic keyed collection; object is a property container. Sorting needs a nonmutating plan and comparator. Local mutation is compatible with a pure external contract when no state escapes before completion.

## Extended solution

Array is the source of truth for stable session order and duplicates; `Map` can be a derived unique-ID index; `Set` suits tag membership. `indexUniqueBy` stores the first source position and throws with both positions before overwriting. `groupBy` appends to arrays in source traversal order.

The fold prefix invariant states that after `k` sessions, every count and minute total equals the corresponding value for exactly `sessions.slice(0, k)`. Empty input produces zeros. Planned minutes include every session’s plan; completed minutes include only actual minutes from completed sessions.

StudyLedger queries sort by ID and operate on copies or read-only traversal. Case-insensitive search normalizes the query and candidate text under one explicit locale policy. Tests retain the original array and compare order and identities after every query.

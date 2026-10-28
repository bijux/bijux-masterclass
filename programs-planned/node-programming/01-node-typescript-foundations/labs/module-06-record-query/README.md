# Laboratory 6 — Record Query

## Product and purpose

This library combines collection choice, deterministic order, state narrowing, duplicate policy, and useful generics. It is not an invitation to build an abstract query framework.

## Entry standard

Choose the collection for each required operation before coding: stable source traversal, unique ID lookup, tag membership, grouped counts, and deterministic output. Trace item type and cardinality through the planned adapters and predict the Module 6 cases. The starter demonstrates typed records but leaves duplicate policy, missing lookup, grouping, and order semantics unresolved.

## Public contract

Records preserve source order and have unique IDs. Draft and published records share common fields; published adds a timestamp. Queries by author, tag, year range, publication state, and title must not mutate input. Empty normalized title queries fail. Generic helpers retain item and key relationships.

## Required construction sequence

Implement duplicate-detecting index construction and order-preserving groupBy before the domain queries. Add narrowed published filtering, then deterministic query functions. Test duplicate positions, group order, source immutability, empty query, and tie behavior.

Keep the public surface small. Add private helpers only when they name a real step or invariant. Each exported function needs at least one success test and one boundary or failure test.

## Adversarial review

Use duplicate IDs, duplicate tags, missing IDs, empty collections, multiple records with equal sort keys, Unicode text, and records arriving in a different insertion order. Check whether the contract preserves source order or applies an explicit sort and tie-breaker. Confirm that query functions do not mutate or reorder the caller’s source collection.

## Prohibited shortcuts

Do not let Map silently overwrite duplicates, return `any`, sort the caller’s array, use locale-dependent order without policy, or introduce generic parameters that do not connect inputs and outputs.

A shortcut is prohibited because it destroys the reasoning target, not because the reference implementation uses a different style.

## Completion evidence

The laboratory is complete when lookup, membership, grouping, filtering, and sorting each have an explicit order and duplicate policy; generic helpers preserve a real input/output relationship; and source collections remain unchanged. Use equal-key and duplicate cases to prove deterministic behavior, then compare collection choices and invariants with the reference.

## Independent transfer

Return the first record for each normalized title while reporting every collision. Decide whether the result keeps source order or sorted title order and make the decision observable.

State whether the new ranking changes storage order or only result presentation. Define tie-breakers, preserve the input collection, and add equal-score cases so deterministic behavior is proved rather than inferred.


Include one short complexity note for each public query. State the dominant operation and expected collection size rather than claiming that one collection is always faster.

# Laboratory 4 — Inventory Transform

## Product and purpose

The inventory lab teaches identity and structural sharing with nested plain objects. A successful update changes exactly the path required by the domain; a rejected update changes nothing reachable from the caller.

## Entry standard

Draw the starter inventory as bindings and object identities. Mark which identities a valid update should replace and which should remain shared. Predict the Module 4 aliasing cases and record the expected `===` relationships. The starter test demonstrates one read; it does not prove immutable update behavior or failure atomicity.

## Public contract

Inventory contains a readonly item array. Items have positive IDs, nonempty names, nonnegative safe stock, and nested supplier contact. Every successful operation returns a new inventory and array. The changed item is new; untouched items are identical. Supplier contact update creates a new nested supplier only for that item.

## Required construction sequence

Draw the object graph before coding. Implement one internal update-by-ID operation, then rename, stock adjustment, and email update. Test semantic fields and `===` identities. Freeze selected fixtures during tests to expose accidental writes. Add missing-ID and invalid-result cases.

Keep the public surface small. Add private helpers only when they name a real step or invariant. Each exported function needs at least one success test and one boundary or failure test.

## Adversarial review

Retain aliases to the original outer object, item array, target item, untouched item, and nested supplier before each operation. Test missing IDs, zero delta, negative resulting stock, unsafe arithmetic, and an update that changes one nested field. Assert both semantic values and the identities that must remain equal or become different after success and after failure.

## Prohibited shortcuts

Do not use JSON cloning, `structuredClone`, global mutation, non-null assertions for missing IDs, or a full deep copy. A shallow top-level spread followed by nested mutation is also prohibited because it changes the original graph.

A shortcut is prohibited because it destroys the reasoning target, not because the reference implementation uses a different style.

## Completion evidence

The laboratory is complete when tests prove value correctness and identity behavior for the outer inventory, array, changed item, untouched items, and nested records. All validation must finish before the new graph is returned, and failures must leave every original identity unchanged. Compare the reference by drawing both heap graphs rather than counting spreads.

## Independent transfer

Implement bulk stock changes with candidate publication. A failure in any change must leave the original and every previously computed public result untouched.

Draw the before/after identity graph for a nested supplier update. Name every identity that must change and every identity that should remain shared, then add a failing validation case proving no candidate graph is published.

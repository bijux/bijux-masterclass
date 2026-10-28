# Module 4 Solutions

## A. Graphs

The first creates two outer objects sharing one nested object; both observe value `2`. The second creates two arrays sharing both element objects; mutation through `copy[0]` changes the original element. The third reassigns only the parameter binding; `source` still references the original object with value `1`.

## B. Methods

`push`, `sort`, `splice`, and `reverse` mutate the array. `map`, `filter`, `slice`, and `concat` create new arrays. None automatically deep-clones element objects.

## C. Repair

Map the original items. Return the original item for nonmatching IDs and `{ ...item, name }` for the match. Track whether a match occurred and throw before returning if not. Construct `{ ...state, items }` only from the successful candidate. The callback must not mutate `item`.

## D. Equality

Define equality from product meaning. A state-reconstruction test may compare all persisted fields while ignoring object identity. A “same study topic” query may compare normalized topic text only. One universal object equality is not required.

## E–F. Design notes

A correct immutable update gives new identity only to the changed path. If failure occurs, no shared object has been changed. StudyLedger’s application can therefore decide whether to persist the candidate without rollback logic for in-memory mutation.

## G. Readiness answer

Bindings contain primitive values or object references. Shallow copies duplicate one container and retain nested references. `readonly` controls static writes; freezing is runtime and shallow. Structural sharing intentionally reuses unchanged identities; deep cloning duplicates an entire reachable graph and is often unnecessary or lossy.

## Extended solution

The rename repair maps the array, returns unchanged item identities for nonmatching IDs, creates a new changed item, and throws after detecting no match. Validation of the new name occurs before mapping or inside candidate construction without mutating input. A non-null assertion on `find` hides the missing-ID path and mutation violates historical values.

For bulk adjustment, first validate the request vocabulary and uniqueness, then apply to an immutable candidate. The prefix invariant is: after `k` changes, candidate equals applying exactly the first `k` valid changes to the original, while the original graph remains unchanged. If change `k+1` fails, the candidate is discarded. A mutable staged copy can also satisfy the contract if no staged reference escapes before final publication.

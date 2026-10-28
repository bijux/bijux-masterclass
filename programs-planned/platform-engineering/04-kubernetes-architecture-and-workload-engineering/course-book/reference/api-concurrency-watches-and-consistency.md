# API concurrency, watches, and consistency

Kubernetes clients operate against a changing distributed API. Correct automation must assume that an object can change between read and write, watches can close, and list results represent a bounded view rather than a permanent truth.

## Resource versions are opaque

A resource version supports optimistic concurrency and list/watch continuity. Do not parse it as time or assume arithmetic ordering across unrelated resources. For a read-modify-write update, send the version you read; the API rejects the update if a newer version exists. The client then relists or rereads and recalculates.

Blind retries are unsafe when the intended update depends on old state. A retry should rerun the decision against current state, not merely resend stale bytes.

## List then watch

A controller commonly:

1. lists the relevant objects;
2. builds current state;
3. begins watching after the returned resource-version boundary;
4. updates its cache as events arrive;
5. relists when the watch is too old, closes, or encounters an error.

The controller must remain correct if an individual event is never observed. This is why reconciliation is level-triggered.

## Pagination and snapshots

Large lists can be paginated. Continue tokens belong to one list traversal and should not be reused as general cursors. A client must follow API semantics rather than assume that page boundaries are stable under arbitrary writes.

## Conflict classes

Distinguish:

- object-version conflict: another writer changed the object;
- apply field conflict: another manager owns the field;
- controller ownership conflict: two controllers claim one child population;
- domain conflict: two desired states cannot both be true;
- admission rejection: policy forbids the requested state.

Each needs a different repair. Force application solves only a deliberate field-ownership transfer and may make the wider design worse.

## Course proof

`ApiStore` models resource-version conflicts, watch history, managed fields, generation changes, and pending deletion. The model is deliberately smaller than Kubernetes, but its tests make each ownership invariant explicit.

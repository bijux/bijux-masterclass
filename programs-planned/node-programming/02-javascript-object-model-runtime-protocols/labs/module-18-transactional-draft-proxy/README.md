# Laboratory 18 — Transactional Draft Proxy

## Product

Build a revocable proxy around one plain attribute record. The proxy validates writes and deletes while a session is open. Commit returns one validated immutable snapshot and revokes the proxy. Rollback or disposal revokes without publication.

The proxy is not a transparent wrapper for arbitrary class instances. Its target is deliberately plain data, so private fields, method receivers, and class brands remain outside the intercepted boundary.

## Contract

`openDraft(source, validator)` returns:

- `draft`, the revocable proxy;
- `commit()`, which publishes once;
- `rollback()`, which closes without publishing;
- `state`, one of `open`, `committed`, or `rolled-back`;
- `[Symbol.dispose]`, equivalent to rollback while open.

Forbidden keys include `__proto__`, `prototype`, and `constructor`. Symbol writes are rejected unless the product explicitly lists them. All traps use `Reflect` and must preserve target invariants.

## Invariants

- source data is copied before editing;
- the source object is never mutated;
- every accepted value passes the supplied validator;
- commit and rollback are terminal;
- the proxy is unusable after a terminal operation;
- commit failure leaves the session open or closes it according to one documented policy;
- no trap lies about non-configurable target properties.

## Adversarial cases

Test repeated commit, rollback after commit, writes after revocation, forbidden keys, accessor definition, `defineProperty`, deletion, symbol keys, and validator failure.

## Transfer

Add nested object edits. Decide whether to create nested proxies lazily or require replacing complete nested values. State the identity, revocation, and validation consequences before implementing.

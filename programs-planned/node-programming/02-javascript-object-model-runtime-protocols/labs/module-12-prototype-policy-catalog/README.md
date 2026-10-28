# Laboratory 12 — Prototype-Based Policy Catalog

## Product

Build a policy catalog in which immutable defaults are delegated through a prototype and each tenant may own a small set of overrides. The product must report whether a resolved value came from the tenant or from the default policy, and it must never treat inherited properties from untrusted input as explicit overrides.

The point is not to recommend prototype-based configuration for every application. It is to make lookup, shadowing, receiver behavior, and validation observable in a bounded product.

## Contract

A policy contains `maxItems`, `retentionDays`, and a method that renders a label using the current receiver's tenant name and effective values. A tenant policy delegates to one frozen default object. Own overrides are defined explicitly. Reads may therefore succeed through own state or inherited state.

`resolvePolicy(policy, key)` returns both the effective value and the source (`own` or `default`). `decodeOverrides(unknown)` accepts only own enumerable keys from a null-prototype result and rejects dangerous names and unknown fields.

## Required reasoning

Trace these cases before coding:

- inherited data read;
- own shadowing;
- inherited getter using the tenant receiver;
- assignment to a frozen inherited data property being rejected, contrasted with explicit own-property construction;
- inherited setter receiving the tenant receiver;
- `in` succeeding for a prototype property while `Object.hasOwn` remains false.

## Invariants

- the default policy is frozen;
- every tenant policy has exactly the selected default as prototype;
- tenant name is an own non-empty string;
- override keys are validated by own-property checks;
- no decoder observes `__proto__`, `constructor`, or `prototype` as ordinary policy input;
- persistence records tenant name and own overrides, not inherited values or prototype identity.

## Adversarial cases

Test an input object whose prototype contains `maxItems`; a JSON-like object with a `__proto__` key created through `Object.defineProperty`; a tenant with no overrides; a tenant shadowing one default; and a receiver-sensitive inherited getter.

## Transfer

Add a second immutable policy family and reconstruct tenants from a persisted family name. Explain why changing a live object's prototype after construction is a different product contract from constructing it with the selected prototype.

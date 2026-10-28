# Typed Projection Engine

## The product

Build a projection library with three operations:

```ts
select(value, key)
valuesFor(value, keys)
project(value, keys)
```

`select` connects one proven key to one value type. `valuesFor` preserves the exact order and per-position types of a readonly key tuple. `project` returns a new readonly object containing exactly the requested keys.

The exercise is about generic relationships, not object-copy syntax. Read [Module 22](../../course-book/module-22-generic-relationships-inference-and-indexed-access/index.md) first.

## Public contract

A source containing string and symbol keys must remain usable:

```ts
const TOKEN = Symbol('token');
const user = { name: 'Ada', age: 37, [TOKEN]: true };

const values = valuesFor(user, ['age', 'name'] as const);
// readonly [number, string]

const view = project(user, [TOKEN, 'name'] as const);
// Pick<typeof user, typeof TOKEN | 'name'>
```

The caller’s tuple is the ordering authority. Do not rediscover keys with `Object.keys`. `project` should reject duplicate requested keys because duplicate input communicates either a mistake or an undefined merge policy.

The result is a new top-level object. Nested values remain shallow aliases; document that fact rather than claiming a deep copy.

## Milestones

1. Implement `select<T, K extends keyof T>` and explain every occurrence of `T` and `K`.
2. Define `ValuesFor<T, K>` as a mapped tuple rather than `(T[keyof T])[]`.
3. Preserve a const key tuple without forcing the caller to write explicit type arguments.
4. Implement `project` over `PropertyKey`, including symbols.
5. Detect duplicate keys before returning the result.
6. Add a dynamic-key boundary that validates a `PropertyKey` before selection.
7. Inspect declaration output for accidental widening of the key tuple.

## Adversarial cases

Test symbol keys, optional properties, an empty key tuple, repeated keys, and a dynamic string not present on the source. Under `noUncheckedIndexedAccess`, compare known property selection with open-record and array indexing.

Do not use `Object.fromEntries` followed by an unchecked broad assertion unless you can state the exact one-to-one construction invariant. A local assertion may be justified; a public assertion requirement is not.

## Design record

Explain:

- which argument owns inference for each generic parameter;
- whether `NoInfer` would improve or damage any overload;
- what happens if the source object mutates after projection;
- why `Object.keys` cannot implement the complete `keyof` domain;
- whether duplicate keys should reject, deduplicate, or preserve duplicates in each operation.

## Independent transfer

Build a typed CSV column selector or GraphQL-like field selector. Preserve requested order and model dynamic external field names honestly.

## Completion standard

A reader should be able to infer output types from the signature, predict runtime key order, and identify the only implementation assertion without inspecting source internals.

# Module 22 Reasoned Solutions

## A. Meaningful parameters

`count` does not need to expose the item type; `readonly unknown[]` states the required capability. `debug` should accept `unknown` if its policy truly attempts any value, though a production serializer must handle cycles and unsupported values. `repeat<T>` preserves the input type in every output element, so the parameter is meaningful.

## B. Inference

`p` is `readonly [string, number]` because ordinary parameter inference widens the primitive literals in this mutable-call context. `r` is `string`: the first argument selects the object type and contextualizes the callback; the callback return selects `U`. `d` is `readonly ['a', 'b']` because the `const` parameter requests literal-preserving inference.

## C. Key/value relation

`K` records the selected key. The return `T[K][]` therefore changes with the key. `T[keyof T][]` permits every property value regardless of which key was supplied. Optional fields correctly produce an element type including `undefined`; the runtime read must preserve that possibility.

## D. Tuple projection

```ts
type ValuesFor<T, Keys extends readonly (keyof T)[]> = {
  readonly [I in keyof Keys]: Keys[I] extends keyof T ? T[Keys[I]] : never;
};
```

The implementation assertion is justified only if it maps once over the original tuple, preserves order and length, and reads `value[key]` for the corresponding key. Filtering or sorting would invalidate the public tuple relation.

## E. `NoInfer`

The option tuple should select the union. The fallback is then checked against that union. `NoInfer<C>` prevents the fallback from expanding `C`. Runtime membership remains relevant when options or fallback cross an untyped boundary; the static relation only covers checked callers.

## F. Laboratory

A strong projection engine uses a `const` tuple parameter, rejects duplicate keys when the product promises unique columns, preserves symbol identity, and differentiates object projection from ordered row projection. The declaration tests should import the public entry point and assert both accepted and rejected keys.

## G. SchemaKit

`Schema<T>` produces `T` and accepts `unknown`, so covariance is intended. `Infer<S>` extracts the output through a conditional type. Literal schemas must preserve strings, numbers, booleans, and null without widening. A caller should never need to repeat the output type.

## H. API choices

`parse<T>(text)` is unsafe because no input selects or validates `T`; use a schema parameter. `length` does not need to return `T`, but the generic retains no public benefit unless callers need the specific input elsewhere; `{ length: number }` is usually enough. `combine<T>` is correct only when both inputs must share one item domain; two parameters are required for heterogeneous pairs. `decode` is a straightforward union because both inputs produce the same output by finite runtime branches.

## I. Reconstruction standard

A complete explanation separates:

- where a parameter is selected;
- what operations its constraint grants;
- when a default applies;
- why an explicit argument is not runtime proof;
- how `keyof` and indexed access preserve a key/value relationship;
- why `NoInfer` prevents a checking-only position from changing selection.

## I. Inference ownership

`NoInfer` is appropriate only when the API has a clear authoritative inference source. In `choose(value, fallback)`, the primary value or an explicit type argument can own `T`; the fallback should conform without widening it. In symmetric comparison, neither side is naturally secondary, so blocking one side may create surprising asymmetry. `register(handler, example)` needs a product decision: does the handler define accepted input, or does the example define a sample domain? The signature should reveal that authority.

## J. Symbols and tuple order

`keyof` can include symbols and numbers. `Reflect.ownKeys` is the complete own-key operation, while `Object.keys` includes enumerable own string keys only. The projection implementation should iterate the caller's key tuple directly, which preserves order and supports symbols without rediscovering keys from the source.

## K. Dynamic keys

`Object.hasOwn(value, key)` can justify `key is keyof T` for immediate property access, but the predicate is only as useful as `T`. Open index signatures may still yield uncertain values. Mutation can invalidate assumptions about optional members after the check. For external commands or configuration, converting a string into a closed application key often gives a stronger and more stable contract.

## L. Generic repairs

`label` needs no generic parameter. A `parse<T>(unknown): T` signature lies unless a runtime schema, decoder, or caller-supplied witness establishes `T`. `pair` should accept `right: B`. A `keys` function cannot return an arbitrary caller-selected `K[]`; it may return `(keyof T)[]` with documented runtime limitations, or accept a key witness that determines `K`.

## M. Uncertainty

Known property selection `T[K]` preserves the declared relationship. An open record read is `V | undefined`; array indexing is similarly uncertain. A known tuple literal index can be exact. A runtime bounds check can narrow local control flow, but a reusable API should return `V | undefined` or a result type unless it owns a stronger invariant. Non-null assertions are appropriate only when a separately proved invariant makes the impossible branch truly unreachable.

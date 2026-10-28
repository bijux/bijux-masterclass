# Course 3 Final Review

Complete this without implementation notes. Use the compiler only after committing to each answer.

## Part I — Explain

1. Why is structural compatibility not exact object validation?
2. What does `satisfies` preserve that a broad annotation may widen?
3. When does an excess-property error occur, and why can assigning through a variable change the result?
4. What relationship should a useful generic parameter express?
5. How does `K extends keyof T` differ from `key: string`?
6. When does a conditional type distribute?
7. Why does `never` disappear from a union?
8. What does `infer` extract rather than invent?
9. How can mapped types alter optional and readonly modifiers?
10. Why can template-literal types become computationally and cognitively expensive?
11. Define covariance, contravariance, and invariance using producer and consumer positions.
12. Why are method parameters a danger point in callback APIs?
13. What does a `.d.ts` file prove, and what does it not prove?
14. How can a declaration be internally consistent but wrong at runtime?
15. Why is adding an `exports` field potentially breaking?
16. What does the `types` condition solve for a TypeScript consumer?
17. Why must a runtime schema accept `unknown` rather than the type it promises to return?
18. How should an object schema distinguish a missing optional property from a present invalid value?
19. Name seven compatibility surfaces for a TypeScript library.
20. Why can adding a new union member break an exhaustive consumer?

## Part II — Predict and repair

For each case, state the type-check result and the smallest principled repair.

```ts
interface Point { x: number }
const source = { x: 1, y: 2 };
const a: Point = source;
const b: Point = { x: 1, y: 2 };
```

```ts
function select<T, K extends keyof T>(value: T, key: K): T[K] {
  return value[key];
}
const key: string = 'name';
select({ name: 'Ada' }, key);
```

```ts
type Boxed<T> = T extends unknown ? { value: T } : never;
type R = Boxed<'a' | 'b'>;
```

```ts
type Listener<T> = (value: T) => void;
interface Animal { name: string }
interface Dog extends Animal { bark(): void }
const dogListener: Listener<Dog> = (dog) => dog.bark();
const animalListener: Listener<Animal> = dogListener;
```

```ts
const runtime = { parse(value: unknown) { return String(value); } };
declare const typed: { parse(value: unknown): number };
```

## Part III — Architecture

Design a small ESM library that validates versioned job manifests. Produce:

- the runtime schema surface;
- the inferred output type;
- the public subpath exports;
- one declaration test;
- one malformed-input test;
- one compatibility fixture;
- the migration policy for a new optional field;
- the change that would require a major version.

## Part IV — Independent change

Add `discriminatedUnion(key, variants)` to SchemaKit. Begin with an impact map covering runtime parsing, static inference, duplicate discriminant detection, error paths, declarations, package surface, documentation, and compatibility. Do not begin from the reference solution because no reference implementation for this final extension is supplied.

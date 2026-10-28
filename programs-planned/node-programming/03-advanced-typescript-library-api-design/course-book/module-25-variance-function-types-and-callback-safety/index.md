# Module 25 — Variance, Function Types, and Callback Safety

> **Question:** Which direction may a generic type safely vary, and what does a callback API promise about the values it will supply and accept?

## Why this comes now

Courses 1 and 2 established functions, callbacks, methods, receivers, and object identity. Modules 21–24 established structural assignability and generic type transformations. Variance connects those subjects. It explains why some substitutions are safe for producers, why the direction reverses for consumers, and why mutable containers or read/write interfaces often require invariance.

TypeScript deliberately accepts some unsound programs for JavaScript compatibility. A mature library designer therefore asks two questions:

1. Does TypeScript accept the assignment?
2. Does the runtime protocol make the assignment safe for every value the caller may provide?

This module teaches a concrete arrow model rather than vocabulary memorization.

## Outcomes

By the end of the module, you can:

- classify a type parameter as produced, consumed, or both;
- derive covariance, contravariance, or invariance from those positions;
- explain why callback parameter direction reverses ordinary value assignability;
- distinguish function-property checking from method-parameter bivariance;
- use readonly views to remove mutation authority and enable safer substitution;
- recognize array and callback unsoundness that TypeScript permits deliberately;
- use `in` and `out` annotations only when they match structural behavior;
- design exact event maps rather than broad callback registries with assertions;
- review SchemaKit as a producer of validated output and a consumer only of `unknown`.

## 1. Start with a subtype relation

```ts
interface Animal {
  readonly name: string;
}

interface Dog extends Animal {
  bark(): void;
}
```

Every `Dog` is usable where an `Animal` is required:

```text
Dog  <:  Animal
```

Variance asks how a generic constructor changes this relation.

If `Box<Dog>` is assignable to `Box<Animal>`, `Box` is covariant in that parameter. If the direction reverses, it is contravariant. If neither substitution is safe, it is invariant.

## 2. Producers are covariant

```ts
interface Producer<out T> {
  get(): T;
}
```

A `Producer<Dog>` can safely serve as a `Producer<Animal>` because every produced dog is an animal.

```ts
const dogs: Producer<Dog> = { get: () => ({ name: 'Mina', bark() {} }) };
const animals: Producer<Animal> = dogs;
```

The consumer of `animals` only reads an `Animal`. It never asks the producer to accept an arbitrary animal.

SchemaKit's public schema behaves this way:

```ts
interface Schema<out T> {
  parse(input: unknown): T;
}
```

The schema accepts `unknown`, not `T`, and produces `T`. A schema producing dogs can be viewed as one producing animals, assuming no other member consumes `T`.

## 3. Consumers are contravariant

```ts
interface Consumer<in T> {
  accept(value: T): void;
}
```

A consumer that accepts every `Animal` can be used where a dog consumer is required:

```ts
const allAnimals: Consumer<Animal> = {
  accept(animal) {
    console.log(animal.name);
  },
};

const dogConsumer: Consumer<Dog> = allAnimals;
```

The direction reverses:

```text
Dog <: Animal
Consumer<Animal> <: Consumer<Dog>
```

The caller of `dogConsumer` supplies only dogs, and `allAnimals` can accept them.

The opposite is unsafe. A dog-only consumer may call `bark`; a context expecting an animal consumer may provide a cat.

## 4. Function parameters reverse the direction

A function type is a consumer in its parameters and a producer in its return:

```ts
type Mapper<Input, Output> = (value: Input) => Output;
```

It is contravariant in `Input` and covariant in `Output` under strict function checking.

Suppose an event source promises to call a listener with any `Animal`:

```ts
type Listener<T> = (value: T) => void;

declare function onAnimal(listener: Listener<Animal>): void;
```

This is unsafe:

```ts
const onlyDogs: Listener<Dog> = (dog) => dog.bark();
// onAnimal(onlyDogs);
```

The source may call the listener with an animal that has no `bark`. The principled repair is not a cast. Either broaden the listener, narrow inside it, or register against a dog-specific source.

## 5. Methods are a historical danger point

Under `strictFunctionTypes`, standalone function properties receive contravariant parameter checking more consistently. Methods retain bivariant behavior in some structural comparisons for compatibility with common JavaScript class and collection patterns.

Compare:

```ts
interface MethodHandler<T> {
  handle(value: T): void;
}

interface PropertyHandler<T> {
  handle: (value: T) => void;
}
```

Assignments involving `MethodHandler` may be accepted more permissively than equivalent function properties. This does not make the runtime safe.

For callback-bearing public interfaces, prefer function properties when parameter safety is the intended contract. Use methods when receiver behavior and object protocol genuinely matter, then test substitution explicitly.

## 6. Mutable containers consume and produce

A mutable box both returns and accepts `T`:

```ts
interface Cell<T> {
  get(): T;
  set(value: T): void;
}
```

It should be invariant. If `Cell<Dog>` were treated as `Cell<Animal>`, the wider view could insert a non-dog, after which the original dog view would return a value without `bark`.

JavaScript arrays are mutable and TypeScript allows some assignments that are not fully sound:

```ts
const dogs: Dog[] = [{ name: 'Mina', bark() {} }];
const animals: Animal[] = dogs;
animals.push({ name: 'Plain animal' });
// dogs[1]?.bark(); // runtime failure if called
```

The type system prioritizes compatibility and common usage over complete soundness. Library APIs should not use that permission as a proof.

## 7. Readonly views remove the write hazard

```ts
const dogList: readonly Dog[] = [{ name: 'Mina', bark() {} }];
const animalList: readonly Animal[] = dogList;
```

The wider view cannot insert a non-dog. Covariance is now aligned with the capability exposed.

This is one reason Course 3 public results use readonly arrays and readonly issue paths. The implementation may construct mutable arrays internally, then expose observation-only capability.

Readonly remains shallow and static, as Module 21 established. It is sufficient for variance only because the relevant write methods are absent from the type surface.

## 8. Variance annotations state intent and receive checking

TypeScript supports `in`, `out`, and `in out` annotations in appropriate generic declarations:

```ts
interface Source<out T> {
  read(): T;
}

interface Sink<in T> {
  write(value: T): void;
}

interface MutableSlot<in out T> {
  read(): T;
  write(value: T): void;
}
```

These annotations do not magically make an unsafe declaration safe. The checker verifies consistency in supported structural instantiation comparisons, and the actual member positions still matter.

Use annotations when they clarify a stable public abstraction and improve checking/performance. Do not add them to every generic alias. Readers should be able to derive the direction from the members.

## 9. Bivariant callback hacks are explicit unsoundness

Some libraries intentionally use a pattern similar to:

```ts
type BivariantCallback<T> = {
  bivarianceHack(value: T): void;
}['bivarianceHack'];
```

This exploits method bivariance. It may improve ergonomics for frameworks with specific event hierarchies, but it weakens the callback guarantee. A course library should not use it silently.

If broad compatibility requires such a design, document:

- which narrower callbacks may be accepted;
- which runtime values may actually arrive;
- who performs narrowing;
- which tests protect the assumption;
- why a safer generic event map is insufficient.

## 10. Exact event maps preserve callback relations

A safer event router starts from one map:

```ts
interface Events {
  connected: { readonly peer: string };
  failed: { readonly error: Error };
}

interface EventRouter<E extends object> {
  on<K extends keyof E>(name: K, listener: (event: E[K]) => void): () => void;
  emit<K extends keyof E>(name: K, event: E[K]): void;
}
```

`K` preserves the name/payload relationship. A broad registry such as `Record<string, ((value: unknown) => void)[]>` may be used internally, but the assertion boundary must be localized and justified by the fact that registration and emission share the same key-indexed API.

The implementation must not expose the broad internal table for mutation.

## 11. Callback lifecycle is part of safety

Static payload type is only one callback contract. A useful public API also defines:

- synchronous or asynchronous invocation;
- exact or minimum invocation count;
- ordering;
- reentrancy;
- error propagation;
- listener identity for removal;
- retention and cleanup;
- whether registration during dispatch affects the current pass;
- whether listeners receive a snapshot or live object.

A variance-safe callback can still produce a broken product if lifecycle is unspecified.

## 12. Generic inference and variance interact

A function that both accepts a value and a callback can infer `T` from competing positions:

```ts
function observe<T>(value: T, listener: (value: T) => void): void {
  listener(value);
}
```

The value is a producing/selection position; the listener parameter is a consuming/checking position. `NoInfer<T>` may be used on the listener when the first argument should select the exact type:

```ts
function observe<T>(value: T, listener: (value: NoInfer<T>) => void): void {
  listener(value);
}
```

Do not reach for `NoInfer` before understanding the desired variance. Sometimes the correct API uses two related type parameters or a key-indexed event map.

## 13. Predicate callbacks require special care

```ts
function isDog(animal: Animal): animal is Dog {
  return 'bark' in animal && typeof (animal as { bark?: unknown }).bark === 'function';
}
```

A type predicate claims a relationship between runtime check and narrowed type. The checker does not verify that the implementation is logically complete. If the predicate returns true incorrectly, downstream code may fail.

Predicates are proof-producing functions. Test them against counterexamples, inherited members, forged objects, and boundary values. Avoid predicates that merely cast inside and return true.

## 14. Schema refinements are callbacks too

SchemaKit supports a refinement combinator:

```ts
function refine<T>(
  schema: Schema<T>,
  predicate: (value: T) => boolean,
  message: string,
): Schema<T>;
```

The schema produces `T`; the predicate consumes `T`. A predicate accepting a broader type is safe. A predicate requiring a narrower subtype is not safe because the base schema may produce any `T`.

A transforming schema has two parameters:

```ts
function transform<Input, Output>(
  schema: Schema<Input>,
  map: (value: Input) => Output,
): Schema<Output>;
```

The map consumes the validated input and produces the new output. Its failure policy must also be explicit.

## 15. Public error handlers and `unknown`

Error callbacks should not assume every thrown value is `Error`:

```ts
function reportFailure(handler: (error: unknown) => void): void {
  try {
    // operation
  } catch (error: unknown) {
    handler(error);
  }
}
```

A handler accepting `Error` only is too narrow unless the caller converts every thrown value before dispatch. TypeScript's `useUnknownInCatchVariables` keeps this boundary honest.

## 16. A variance ledger

For each generic type parameter, mark every occurrence:

| Occurrence | Direction |
|---|---|
| return value / readonly property | produces `T` |
| function parameter | consumes `T` |
| mutable property | consumes and produces |
| callback parameter's parameter | direction reverses again |
| callback return | follows callback output |
| readonly array element | produces |
| mutable array element | produces and consumes |

Then record:

- expected variance;
- whether TypeScript enforces it strictly;
- any method bivariance;
- internal assertion boundary;
- runtime values actually delivered;
- lifecycle and cleanup contract.

## 17. Common wrong models

### “Dog is an Animal, so a dog callback is an animal callback”

Callback input direction reverses. The animal source may supply a non-dog.

### “The compiler accepted the method assignment, so it is safe”

Method parameters may be checked bivariantly.

### “Arrays are covariant, therefore mutation is safe”

TypeScript permits an unsound pattern. Readonly views remove the relevant write capability.

### “Variance annotations force the desired behavior”

They express and check intent; they cannot rescue contradictory members.

### “A type predicate is runtime proof because its return type says so”

The implementation must actually establish the claim.

### “Callback type is the whole callback contract”

Invocation order, errors, retention, and disposal remain runtime behavior.

## 18. Use the idea in a complete program

Module 25 reviews and adds:

- `Schema<out T>` as a producer-only public contract;
- readonly issue and result collections;
- refinement and transformation callback types;
- no bivariant callback hacks;
- exact key-indexed hooks in the SchemaKit testing subpath;
- assertions confined to runtime registration tables with tests proving key/payload alignment.

The event-router lab makes callback substitution the primary product rather than a schema concern.

## Practice sequence

1. Draw producer/consumer arrows for each workbook type.
2. Predict the eight Module 25 investigations.
3. Replace one mutable public array with a readonly view and explain the variance effect.
4. Complete [Variance-Safe Event Router](../../labs/module-25-variance-safe-event-router/README.md).
5. Implement the Module 25 SchemaKit callback contracts in [the capstone guide](../capstone.md#module-25--variance-and-callback-contracts).
6. Add one runtime counterexample for an unsafe predicate.

## Ready to continue

You are ready for Module 26 when you can explain:

- covariance, contravariance, and invariance from positions;
- why callback direction reverses;
- method bivariance;
- why readonly collections improve substitution;
- what variance annotations do and do not guarantee;
- how SchemaKit can be covariant while refinements consume output values;
- why callback lifecycle remains a runtime contract.

Next: [Declaration Files, Declaration Emission, and Type Tests](../module-26-declaration-files-emission-and-type-tests/index.md).

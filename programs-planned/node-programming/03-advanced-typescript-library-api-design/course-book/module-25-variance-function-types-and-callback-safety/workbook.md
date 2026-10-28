# Module 25 Workbook

Draw arrows. Do not decide from intuition or from whether the compiler happens to accept an assignment.

## A. Classify variance

For each parameter, classify intended variance and justify every occurrence:

```ts
interface Source<T> { read(): T }
interface Sink<T> { write(value: T): void }
interface Cell<T> { read(): T; write(value: T): void }
interface Factory<T> { create(): T; map<U>(f: (value: T) => U): Factory<U> }
```

## B. Callback substitution

Given `Dog <: Animal`, predict assignments among:

```ts
type Listener<T> = (value: T) => void;
```

Then repeat with a method-bearing interface and explain any more permissive result.

## C. Array counterexample

Construct the mutable-array runtime failure. Then redesign the API with readonly input and owned output. State exactly which write capability disappeared.

## D. Event map

Define an event map with three events and implement:

```ts
on<K extends keyof E>(name: K, listener: (event: E[K]) => void): () => void;
emit<K extends keyof E>(name: K, event: E[K]): void;
```

Add negative type tests for mismatched payloads and narrower callbacks.

## E. Predicate audit

Write five counterexamples for a user-defined predicate. Include inherited members, null, wrong callable shape, forged tag, and unexpected primitive.

## F. Independent laboratory

Complete [Variance-Safe Event Router](../../labs/module-25-variance-safe-event-router/README.md). The implementation must preserve removal identity, stable dispatch order, and snapshot semantics during reentrant registration.

## G. SchemaKit transfer

Review:

- `Schema<out T>`;
- readonly issue arrays;
- `refine` predicate;
- `transform` mapping;
- testing hooks;
- internal handler storage.

For every assertion, state the key/payload or schema/output fact that justifies it.

## H. Reconstruction

Explain why a dog producer can be an animal producer, why an animal consumer can be a dog consumer, and why a mutable cell permits neither substitution.

## I. Position analysis

Mark every appearance of `T` as produced, consumed, or both in these APIs: `PromiseLike<T>`, `Comparator<T>`, `MutableBox<T>`, `ReadonlyArray<T>`, `EventSource<T>`, and `(value: T) => T`. Derive the safe substitution direction from operations rather than memorizing labels.

## J. Method bivariance clinic

Write equivalent callback contracts once as a method and once as a function-valued property. Under strict function types, attempt to install a dog-only listener where an animal listener is required. Explain the different checker result and why the more permissive form can be unsound for stored callbacks.

## K. Mutable collection counterexample

Construct the classic array widening counterexample without assertions. Show the write that introduces an incompatible element and the later read that fails. Redesign the public API with readonly input and owned output.

## L. Router dispatch policy

Specify listener order, duplicate registration, removal during dispatch, registration during dispatch, thrown listener errors, and reentrant emission. Implement at least three policies explicitly instead of inheriting incidental `Set` behavior.

## M. SchemaKit audit

Classify `Schema<T>`, `OptionalSchema<T>`, refinement predicates, transformation callbacks, and lazy factories by variance. Identify any method syntax that makes a callback more permissive than the intended stored-callback contract.

## N. Error channel variance

Design a callback API that reports success and failure through separate functions. Analyze the variance of input, success output, and error output independently. Then compare it with a single discriminated result callback. Which design produces clearer substitution and ownership rules for stored handlers?

## O. Consumer-supplied implementation

Ask a second package to implement your listener interface. Change one method parameter and observe whether the implementor still type-checks. Record why public implementor surfaces deserve stricter compatibility review than helpers used only inside one package.

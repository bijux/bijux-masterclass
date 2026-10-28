# Module 25 Reasoned Solutions

## A. Classification

`Source<T>` is covariant because it only produces `T`. `Sink<T>` is contravariant because it consumes `T`. `Cell<T>` is invariant because it does both. `Factory<T>` produces `T`, while the mapping callback consumes `T` as part of an operation that produces a new factory; the overall public parameter remains producer-oriented when the method relation is correctly modeled.

## B. Callbacks

A listener accepting every animal is safe where a dog listener is required. A dog-only listener is unsafe where any animal may arrive. Method-bearing interfaces may be accepted bivariantly; that is compatibility behavior, not proof.

## C. Arrays

The failure inserts a non-dog through an `Animal[]` alias to a `Dog[]`. `readonly Animal[]` removes insertion and replacement methods from the widened view. Returning a new owned array preserves the original collection's element invariant.

## D. Events

The event key selects the payload type. A broad internal store can be hidden behind the generic methods, with one localized assertion based on the invariant that listeners enter and leave through the same key. Dispatch should snapshot the listener list if registration/removal during dispatch must affect only future emissions.

## E. Predicates

A correct predicate must reject values that merely have a tag or inherited property but violate the full contract. TypeScript trusts the declared predicate; adversarial runtime tests are the actual evidence.

## F. Laboratory

The reference architecture stores listeners by event key, exposes unsubscribe closures with stable identity, and never uses a bivariant callback type. Reentrant mutation is governed by a documented snapshot policy.

## G. SchemaKit

A schema is covariant because callers only receive its output. Refinement consumes exactly that output. Transform consumes input and produces output. Public arrays are readonly. Internal assertions are acceptable only around storage whose registration and dispatch API preserve the same key-index relation.

## H. Reconstruction standard

A complete answer derives variance from operations and then checks whether TypeScript's actual behavior is stricter or more permissive. Compiler acceptance alone is never the final argument.

## I. Position analysis

A pure producer can vary covariantly; a pure consumer can vary contravariantly; a read-write container is invariant. `PromiseLike<T>` principally produces fulfillment values, while a comparator consumes two `T` values. `(value: T) => T` both consumes and produces, so unrestricted substitution in either direction is unsafe. Derivation should use available operations because small API changes can change variance.

## J. Methods

TypeScript preserves method-parameter bivariance for compatibility with common object and class patterns. Function-valued properties are checked contravariantly under strict function types. A stored callback registry should prefer the stricter property/function form, because the registry may later supply any value in the declared domain. A dog-only callback cannot safely occupy an animal slot.

## K. Arrays

A mutable `Dog[]` treated as `Animal[]` permits writing a non-dog animal. Reading that element through the original `Dog[]` view and calling `bark` fails. A readonly input eliminates the write capability. If the operation needs mutation, create and return a new owned collection whose element type matches the broader result.

## L. Router policy

Snapshot iteration makes removal or registration during the current dispatch deterministic: changes affect future emissions. Duplicate handling can reject, deduplicate by identity, or permit repeated delivery. Listener exceptions may stop immediately or be collected; the choice must be documented. Reentrancy can be allowed with a nested snapshot or rejected with an active-dispatch guard. None of these behaviors follows from the callback type alone.

## M. SchemaKit

`Schema<out T>` produces `T`; it should not accept arbitrary `T` values. `OptionalSchema<T>` remains output-oriented. A refinement predicate consumes validated `T`, so its callback parameter must be checked contravariantly. Transform consumes `A` and produces `B`. A lazy factory produces a schema. Public method syntax should not accidentally permit a narrower callback where the implementation can supply wider values.

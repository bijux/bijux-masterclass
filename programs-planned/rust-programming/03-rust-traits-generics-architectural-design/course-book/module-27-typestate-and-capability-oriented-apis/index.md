# 27 — Typestate and Capability-Oriented APIs

**Course 3, day 7 · Module 27 of 90**  
`█████████░░░░░░░░░░░` **27/90**

[← Module 26: Composition and OOP-Style Design Without Inheritance](../module-26-composition-and-oop-style-design-without-inheritance/index.md) · [Course 3 overview](../index.md) · [Ninety-module map](../../../COURSE_MAP.md) · [Module 28: Boundary Traits and Adapters →](../module-28-boundary-traits-and-adapters/index.md)

## The question

> Which illegal operations can be removed from the API by representing protocol state and authority in types?

## Why this comes now

Composition handles variation among components; typestate handles variation over a protocol's lifetime. Consuming transitions and capability tokens remove illegal operations from the method set. The module also treats the cost: state explosion, generic leakage, and the point where a runtime enum is the better model.

## What you will be able to do

- Encode a finite protocol with marker states and consuming transitions.
- Decide which invalid operations deserve compile-time prevention.
- Prevent construction of forbidden states through visibility and sealed state markers.
- Erase typestate at a dynamic boundary without corrupting invariants.
- Quantify typestate complexity and choose a runtime state machine when appropriate.

## Core model

### Typestate moves protocol validity into method availability

A runtime state machine stores state as data and checks operations while the program runs. A typestate API represents selected states in the type, so methods can exist only where they are valid.

```rust
use std::marker::PhantomData;

pub struct Draft;
pub struct Reviewed;
pub struct Published;

pub struct Article<State> {
    title: String,
    body: String,
    _state: PhantomData<State>,
}
```

Construction yields one state:

```rust
impl Article<Draft> {
    pub fn new(title: String, body: String) -> Self {
        Self { title, body, _state: PhantomData }
    }

    pub fn review(self) -> Result<Article<Reviewed>, ReviewFailure<Article<Draft>>> {
        if self.body.trim().is_empty() {
            return Err(ReviewFailure(self));
        }

        Ok(Article {
            title: self.title,
            body: self.body,
            _state: PhantomData,
        })
    }
}
```

Only a reviewed article can publish:

```rust
impl Article<Reviewed> {
    pub fn publish(self) -> Article<Published> {
        Article {
            title: self.title,
            body: self.body,
            _state: PhantomData,
        }
    }
}
```

There is no `publish` method on `Article<Draft>`. The invalid call is unrepresentable at that API surface.

### Consuming transitions express replacement

A typestate transition usually consumes `self` because the old state should no longer coexist with the new state. If validation can fail, returning the original value preserves ownership:

```rust
pub struct TransitionError<T> {
    pub value: T,
    pub message: String,
}
```

This design is often stronger than mutating an internal state flag and then reporting an error, because failure leaves the original valid state intact.

Not every transition must consume. A method may borrow to inspect or mutate data while remaining in the same state. Choose the receiver from the protocol:

- `&self` — observation that does not change state;
- `&mut self` — mutation within the same state;
- `self` — replacement by a new state.

### Marker visibility controls which states users can name

Public marker types make states part of the public API. Private fields prevent users from constructing arbitrary values, but public state types still affect signatures and semver.

A crate may expose state names deliberately:

```rust
pub mod state {
    pub struct Draft;
    pub struct Reviewed;
}
```

or keep internal markers private and expose type aliases for supported states. The choice depends on whether callers need to store or mention intermediate states.

Do not rely on marker names alone for validity. The transition constructors and field privacy must ensure values cannot be forged.

### Capabilities represent authority rather than phase

A capability token proves that the caller possesses permission:

```rust
pub struct AdminToken {
    _private: (),
}

impl Workspace {
    pub fn delete(&mut self, token: &AdminToken, id: DocumentId) -> Result<(), DeleteError> {
        let _ = token;
        // ...
        Ok(())
    }
}
```

Only the module that can construct `AdminToken` grants deletion authority. The token may be borrowed for repeatable authority or consumed for one-shot authority.

Capabilities are useful for:

- authenticated or authorized operations;
- proof that validation occurred;
- ownership of a lease or permit;
- access to a scoped resource;
- ensuring initialization steps occurred.

A zero-sized capability still has semantic weight. Its power comes from construction privacy and type checking, not runtime bytes.

### Typestate builders enforce required configuration

A builder can encode missing and present components:

```rust
struct Missing;
struct Present<T>(T);

struct EngineBuilder<S, P, R> {
    source: S,
    policy: P,
    reporter: R,
}
```

Each method replaces one type parameter:

```rust
impl<P, R> EngineBuilder<Missing, P, R> {
    fn source<S>(self, source: S) -> EngineBuilder<Present<S>, P, R> {
        EngineBuilder { source: Present(source), policy: self.policy, reporter: self.reporter }
    }
}
```

`build` is implemented only when all components are present. This removes runtime “missing field” errors and can make configuration order flexible.

The cost is type-state proliferation. With many optional features, mutually exclusive modes, or configuration loaded dynamically, an ordinary builder returning a typed validation error may be simpler and produce better diagnostics.

### State explosion is a design warning

If five independent Boolean capabilities become type parameters, the conceptual state space has 32 combinations. Even when the compiler instantiates only used combinations, signatures and implementations can become difficult to understand.

Ask whether states are:

- **protocol phases** with different method availability — typestate may fit;
- **runtime domain data** that must be serialized, queried, or switched dynamically — an enum may fit;
- **independent options** — ordinary fields and validation may fit;
- **authority** — capability tokens may fit;
- **open implementations** — a trait object may fit.

Typestate is not a general replacement for enums.

### Erasure can occur after construction

A value may use typestate during setup and erase state at a runtime boundary:

```rust
trait Runnable {
    fn run(&mut self) -> RunResult;
}

fn into_runnable(engine: Engine<Ready>) -> Box<dyn Runnable> {
    Box::new(engine)
}
```

This hybrid is useful when compile-time construction guarantees are strong, but completed values must enter a heterogeneous registry. Erasure should occur only after the state-specific guarantee has served its purpose.

### Typestate does not prove everything

A state type proves only what its constructors and transitions establish. `Article<Reviewed>` does not magically prove high editorial quality unless `review` enforces a meaningful contract. A capability token does not prove the user is still authorized if external policy can revoke authority. A builder state does not prove external resources remain available after construction.

State the exact guarantee:

- “required components were supplied”;
- “the document passed these deterministic checks at revision 7”;
- “this lease owns one pool slot until dropped”;
- “the connection handshake completed.”

Avoid names such as `Valid`, `Safe`, or `Authenticated` without defining scope and freshness.

### A typestate decision checklist

Use typestate when all are true:

1. invalid operation order is a recurring source of defects;
2. states are known at compile time;
3. transitions replace values naturally;
4. callers benefit from unavailable methods rather than runtime errors;
5. the number of meaningful states remains understandable;
6. state does not need frequent runtime erasure or serialization.

Prefer an enum plus checked methods when state is data. Prefer a validation result when only construction needs checking. Prefer a capability when authority, not phase, is the concern.

#### State in the type parameter

```rust
struct Draft;
struct Reviewed;

struct Article<S> {
    title: String,
    body: String,
    state: S,
}
```

Methods are implemented only for valid states:

```rust
impl Article<Draft> {
    fn review(self) -> Result<Article<Reviewed>, ReviewError> { /* ... */ }
}

impl Article<Reviewed> {
    fn publish(self) -> PublishedArticle { /* ... */ }
}
```

A draft has no `publish` method. The compiler rejects the invalid protocol step.

#### Consuming transitions preserve ownership

A transition takes `self`, validates, and returns a new concrete type. The fields move into the new state; no duplicate live object exists.

#### What typestate proves

It proves that code possessing `Article<Reviewed>` reached a constructor or transition capable of creating that state, assuming visibility prevents forgery. It does not prove external facts such as legal approval unless the transition validates them correctly.

#### State markers often carry no data

Zero-sized marker types name compile-time states. Their constructors and the state field must be controlled; otherwise callers may forge `Article<Reviewed>` directly.

```rust
mod state {
    pub struct Draft(pub(crate) ());
    pub struct Reviewed(pub(crate) ());
}
```

A private field in `Article<S>` and restricted marker construction preserve the protocol.

#### Sealed state trait

A private sealing trait can restrict valid state parameters:

```rust
mod private { pub trait Sealed {} }
pub trait ArticleState: private::Sealed {}
```

This prevents meaningless `Article<MyRandomType>` instantiations when the generic type is public.

#### Marker data versus state data

Information specific to a state can live in the state type:

```rust
struct Reviewed { reviewer: ReviewerId }
```

Then transitions preserve evidence rather than only a label. Avoid storing the same truth both in the marker and a runtime enum field.

#### Success changes the type; failure should preserve useful ownership

A transition may fail validation. Returning only an error discards the draft:

```rust
fn review(self) -> Result<Article<Reviewed>, ReviewError>
```

If the caller needs to repair it, return the original value with the error:

```rust
struct TransitionError<T, E> { value: T, error: E }
```

This mirrors the Course 2 principle that failure paths must account for ownership.

#### Transactional transition

Build candidate state before committing irreversible effects. A typestate signature does not automatically guarantee failure atomicity.

#### Identity across state types

The Rust type changes while domain identity may remain the same. Keep stable IDs in shared data. Do not equate concrete Rust type identity with domain object identity.

#### Possession can authorize an operation

A capability value represents permission:

```rust
pub struct PublishPermit { _private: () }

impl Article<Reviewed> {
    pub fn publish(self, _permit: &PublishPermit) -> PublishedArticle { /* ... */ }
}
```

Only code able to obtain the permit can call the operation. Lifetimes can scope the permission; ownership can make it single-use.

#### Capability versus role flag

A Boolean `is_admin` is checked at run time everywhere. A capability centralizes authorization issuance and narrows the API. It does not replace security boundaries beyond the process; callers able to construct the token can act.

#### Linear-style use

A consuming capability can prevent reuse:

```rust
fn finalize(self, permit: FinalizePermit) -> Finalized
```

Rust does not provide full linear types, but ownership gives useful single-consumption behavior.

#### Required configuration in the type

```rust
struct Missing;
struct Present<T>(T);

struct Builder<S, R> {
    source: S,
    reporter: R,
}
```

`with_source` changes `S`; `with_reporter` changes `R`; `build` exists only for `Builder<Present<S>, Present<R>>`.

#### Benefits

- missing required components are compile errors;
- successful `build` may be infallible for presence checks;
- IDE completion shows available transitions.

#### Costs

- error messages expose state types;
- optional and order-independent fields can create many combinations;
- storing partially configured builders behind one dynamic type is awkward;
- public type names can become noisy.

A runtime builder returning `Result` is often better when configuration comes from a file or UI and errors must be accumulated.

#### Static state does not always survive storage or transport

A collection may need to hold articles in several states. Options:

- enum `AnyArticle` with variants carrying typestates;
- erase to a runtime state representation after validation;
- separate collections per state;
- trait objects when states are open and behavior is sufficient.

#### Preserve invariants during erasure

An enum can preserve which typestate produced each variant:

```rust
enum StoredArticle {
    Draft(Article<Draft>),
    Reviewed(Article<Reviewed>),
}
```

Serialization usually reconstructs through validated constructors. Deserializing bytes directly into a marker state would bypass evidence.

#### Boundary rule

Use typestate at APIs where the compiler can help a programmer sequence operations. Use runtime state where external data, persistence, or user choices determine state. Bridges must validate.

#### State-space explosion

Three independent binary requirements create eight generic state combinations. Ten create 1,024. Typestate is not free.

#### Good candidates

- short protocols with few states;
- construction requiring a small fixed set of fields;
- security- or safety-relevant capabilities;
- transitions controlled within one crate;
- APIs used by programmers rather than arbitrary external data.

#### Poor candidates

- dozens of independent options;
- states discovered from persistence;
- workflows that change frequently by configuration;
- operations that must report all invalid conditions at once;
- public APIs where generic state noise outweighs prevention.

#### Alternatives

An enum plus validated methods, a runtime builder returning rich errors, a capability token, or a private invariant-preserving constructor may solve the problem more simply.

The engine requires a source, reporter, and validated policy before `run` is callable. Three state axes would produce eight combinations, but the builder can represent absence with `Missing` and presence with `Present<T>` while implementing setters generically.

Construction from CLI files still produces runtime errors when parsing source or policy. Typestate prevents programmer misuse of the library; it does not turn invalid external data into compile-time errors.

After `build`, the final `Engine<S, R>` has no state markers. Typestate serves construction and disappears from execution.

### Review typestate as a product decision, not a type-level achievement

Typestate pays for itself only when the protocol is narrow, the illegal operations are important, and the state is known at the call site. Start with the runtime protocol, not with generic parameters. Write its nodes, legal edges, failure edges, and evidence carried by each successful transition. Only then decide which nodes deserve distinct Rust types.

A useful review table is:

| Question | Type-level answer is attractive when… | Runtime answer is attractive when… |
|---|---|---|
| Who knows the state? | the caller knows it statically | state arrives from storage, a network, or a heterogeneous collection |
| What changes at a transition? | ownership is consumed and replaced | one stable identity is mutated in place |
| What does failure need? | the original state should be returned for retry | all states share one recoverable error protocol |
| How many independent axes exist? | one short linear protocol dominates | many optional features combine independently |
| Who may construct states? | the crate can keep markers and fields controlled | external data must be validated into a runtime model |

The table prevents a common mistake: encoding every Boolean as a type parameter. Five independent yes/no axes create thirty-two combinations before domain states are considered. The compiler can represent them, but users must read them, diagnostics must name them, documentation must explain them, and downstream code must store them. A type-level state space can therefore be technically valid and still be a poor public API.

#### Preserve retry when failure is recoverable

A consuming transition such as `draft.review()` owns the draft. If review can fail and retry is meaningful, an error that discards the draft weakens the product. Return the surviving state with the error:

```rust
pub struct TransitionError<S, E> {
    pub state: S,
    pub error: E,
}
```

This pattern makes the ownership consequence explicit. It also distinguishes a validation failure, after which the draft remains usable, from a terminal transition that intentionally consumes or invalidates the resource.

#### Keep evidence in the state that needs it

Marker types need not always be zero-sized. A `Reviewed` state may carry a review identifier or validated digest. That evidence then exists exactly where later methods require it. Conversely, large shared product data usually belongs in the outer value, not in marker types duplicated across every transition signature.

#### Deserialization is a runtime boundary

Serialized bytes do not arrive with a Rust typestate proof. Decode into an unchecked or runtime representation, validate the protocol, then construct the appropriate trusted state through private constructors. Treating a deserialized state name as if it were compiler evidence allows external data to forge an invariant.

#### Erase state after it has done its job

A builder may use typestate to prevent `build` before source and reporter configuration exist, then return one non-generic `Engine`. The construction protocol has ended; retaining marker parameters would contaminate storage, trait-object boundaries, error types, and downstream signatures without adding protection. Typestate is most effective when its lifetime in the architecture is deliberately short.

## Use the idea in a complete program

The course capstone is **Review Engine**, a policy evaluation engine with static boundaries, a dynamic rule registry, and typestate construction. Build the engine through typestate so execution is unavailable until source, policy, and reporter are present. Keep the state machinery out of the finished engine's public behavior. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-07-typestate-publication/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 28 when you can:

- answer the module question—“Which illegal operations can be removed from the API by representing protocol state and authority in types?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Encode a finite protocol with marker states and consuming transitions;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)
- [Rust Reference: Visibility](https://doc.rust-lang.org/reference/visibility-and-privacy.html)

[← Module 26](../../../03-rust-traits-generics-architectural-design/course-book/module-26-composition-and-oop-style-design-without-inheritance/index.md) · [ninety-module map](../../../COURSE_MAP.md) · [Module 28 →](../../../03-rust-traits-generics-architectural-design/course-book/module-28-boundary-traits-and-adapters/index.md)

## Continue

1. Complete the [Module 27 workbook](workbook.md) and freeze every prediction before compiling.
2. Build [Laboratory 27 — Typestate Publication](../../labs/module-07-typestate-publication/README.md) from its public contract.
3. Apply the Module 27 increment in the [Review Engine engineering guide](../capstone.md).
4. Review the [reasoned solutions](solutions.md) only after an independent attempt, then revise the causal model rather than copying code shape.

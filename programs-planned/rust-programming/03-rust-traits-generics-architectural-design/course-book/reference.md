# Course 3 reference — Traits, Generics, and Architectural Design

## Start with the source of variation

Do not begin with a trait. Name what varies, who chooses it, when it is chosen, whether heterogeneous values must coexist, and whether downstream crates may add implementations.

| Requirement | First mechanism to consider |
|---|---|
| one concrete type owns behavior | inherent method |
| algorithm over ordinary inputs | free function |
| closed alternatives with variant-specific data | enum |
| caller chooses a concrete type and static dispatch is useful | generic parameter |
| implementation chooses one related type family | associated type |
| concrete return type should be hidden but remain static | `impl Trait` |
| heterogeneous runtime collection or plugin boundary | `dyn Trait` |
| one short construction protocol has illegal intermediate operations | typestate |
| adapt a foreign type or closure to a local contract | newtype or adapter |

## Trait contract checklist

A useful trait has:

- a real caller that needs substitution;
- a small primitive operation set;
- receiver choices that express capability;
- documented semantic laws;
- defaults derived from primitive methods rather than invented policy;
- bounds no stronger than the implementation body requires;
- contract tests shared across implementations.

The compiler proves signature compatibility, not determinism, idempotence, ordering, units, or semantic equivalence.

## Associated type or generic parameter?

Use an associated type when each implementation chooses one answer and callers should not repeatedly select it:

```rust
trait Source {
    type Item;
    type Error;
}
```

Use a generic parameter when the same implementation must support several caller-selected combinations. Equality constraints such as `Iterator<Item = Record>` make projections explicit. Introduce GATs only when the family genuinely depends on a borrow or other parameter.

## Coherence

An implementation is globally meaningful. The orphan rules require local ownership of the trait or the type. When a direct implementation is forbidden or would overlap:

- create a local newtype;
- create a local extension trait;
- narrow a blanket implementation;
- seal an implementation surface when external implementations would block evolution.

Do not use broad blanket impls to save a few lines if they consume future coherence space.

## Static versus dynamic dispatch

Static dispatch preserves concrete type information and enables monomorphized calls. Dynamic dispatch erases the concrete type behind a dyn-compatible trait and chooses behavior through a vtable.

Choose a trait object only when runtime heterogeneity is real. Check:

- object-safe/dyn-compatible method set;
- ownership container (`&dyn`, `Box<dyn>`, `Rc<dyn>`, later `Arc<dyn>`);
- object lifetime;
- need for downcasting—often evidence that the erased contract is incomplete;
- whether a closed enum is simpler and more inspectable.

## Composition patterns

Rust replaces inheritance-shaped designs with explicit parts:

- strategy: one replaceable policy;
- adapter: translate one boundary into another;
- decorator: wrap behavior while preserving the same contract;
- command: represent an operation as data or an object;
- state enum: closed runtime protocol;
- typestate: compile-time protocol for a small, local, valuable sequence.

Delegation should be explicit enough that the reader can see which component owns each invariant.

## Boundary traits

Create a port around a capability your application needs, not around an entire external library. The core should speak domain values; adapters own parsing, formatting, I/O, and foreign error conversion. Closure adapters are useful when the capability is truly one operation and state can live in the closure environment.

## Evolution review

For every public trait or enum, review two downstream roles:

1. callers that use the API;
2. implementors that supply behavior.

Adding a required trait method can break implementors. Adding a variant can break exhaustive matches. Broadening blanket impls can overlap downstream code. Sealing, default methods, non-exhaustive models, versioned traits, adapters, and deliberate MSRV policy preserve room to evolve.

## Course 3 readiness

You are ready for Course 4 when you can draw a variation map before coding, state trait laws, justify associated types, explain coherence ownership, choose static or dynamic dispatch, keep typestate local, design narrow ports, and analyze an API change from both caller and implementor perspectives.

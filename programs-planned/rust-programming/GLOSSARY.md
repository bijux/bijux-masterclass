# Program glossary

This glossary gives the program’s working meanings. Each module derives the terms in context; use this page for recall.

## Values, types, and ownership

**binding** — a name associated with a value or place. Bindings are immutable unless declared `mut`.

**expression** — syntax that produces a value and has a type. Blocks, `if`, and `match` are expressions.

**place** — an expression denoting a memory location, such as a variable, field, index, or dereference.

**move** — transfer of a non-`Copy` value’s usable ownership from one place to another.

**borrow** — temporary permission to access a value through a reference without transferring ownership.

**shared reference** — `&T`; permits shared inspection under Rust’s aliasing rules.

**mutable reference** — `&mut T`; permits exclusive access for its loan duration.

**slice** — a dynamically sized view of a contiguous sequence, represented through a pointer plus length.

**invariant** — a condition that must hold for every valid value or every reachable state of a component.

## Lifetimes and memory

**lifetime** — a static relationship describing where a reference may be used relative to the storage it borrows.

**reborrow** — a new, usually shorter loan created through an existing reference.

**RAII** — resource acquisition is initialization; an owned value’s destruction releases the resource.

**failure atomicity** — a stated guarantee about visible state after a failed operation, often “unchanged on every pre-commit failure.”

**liveness edge** — an ownership relationship that keeps an allocation alive, such as a strong `Rc` edge.

**interior mutability** — mutation through a shared outer reference using a type that enforces the required rules internally.

**validity** — the conditions a bit pattern and value state must satisfy for a Rust type. Correct size alone does not establish validity.

**layout** — size, alignment, and placement properties. Some are guaranteed; others are target- or implementation-conditioned.

**variance** — whether substitution through a generic wrapper preserves a capability relationship such as lifetime subtyping.

**pinning** — a contract that restricts safe movement of a value after an address-sensitive invariant is established.

## Contracts and architecture

**trait law** — a semantic property every implementation must preserve even though signatures alone cannot prove it.

**associated type** — a related type selected by a trait implementation.

**coherence** — the global consistency requirement that prevents conflicting trait implementations.

**static dispatch** — selection of concrete implementation through types, usually with monomorphization.

**dynamic dispatch** — runtime method selection through a trait object and vtable.

**dyn compatibility** — the requirements a trait must satisfy for use as `dyn Trait`.

**adapter** — a local component translating one interface, representation, or error model into another.

**typestate** — representation of protocol state in types so some operations exist only in legal states.

**sealed trait** — a public trait whose external implementation is intentionally prevented to preserve control or evolution room.

## Dataflow

**closure capture** — the values a closure environment borrows or owns.

**callable capability** — whether a closure can be called through `Fn`, `FnMut`, or only `FnOnce`.

**lazy traversal** — work performed only as an iterator consumer requests items.

**cardinality** — how many output items a stage may produce for its inputs.

**fold invariant** — what an accumulator means after processing a prefix of the input.

**short-circuit** — termination before all inputs are consumed because a result or failure is already determined.

**structural sharing** — immutable versions reuse unchanged substructure rather than copying the entire value.

**functional core** — deterministic domain decisions expressed as value-to-value transformations.

**effect shell** — the boundary that performs filesystem, terminal, process, clock, randomness, or other external actions.

## Metaprogramming

**source of truth** — the single authoritative declaration from which mechanical surfaces are generated.

**token tree** — a token or delimited group used by Rust macro systems.

**fragment specifier** — a `macro_rules!` matcher category such as `expr`, `ty`, `path`, or `tt`.

**hygiene** — rules controlling how names in macro input and generated code resolve.

**expansion** — production of Rust tokens from a macro invocation.

**procedural macro** — compiler-executed Rust code that transforms input token streams into output tokens.

**normalized model** — a validated internal representation from which generated code is emitted deterministically.

**build script** — a Cargo-managed program that runs before crate compilation to inspect inputs, emit directives, or generate artifacts under `OUT_DIR`.

## Systems boundaries

**endianness** — byte order used to encode a multi-byte integer.

**canonical encoding** — one deterministic byte representation for a logical value.

**commit point** — the transition after which an operation’s new state is externally installed or authoritative.

**provenance** — the allocation and derivation identity associated with pointer operations; an address alone is not the full permission story.

**uninitialized storage** — memory that does not yet contain a valid value of the intended type.

**allocation layout** — exact size and alignment used for allocation and required again for correct deallocation.

**ABI** — calling and representation convention shared across a language or binary boundary.

**opaque handle** — a foreign-facing pointer or token whose internal Rust representation is hidden and whose ownership protocol is specified separately.

**safety ledger** — a record connecting each unsafe operation to exact preconditions, establishing code, duration, panic behavior, cleanup, and safe-caller protection.

**strongest honest claim** — the most precise success statement supported by language, library, target, platform, and external evidence—never a stronger marketing phrase.

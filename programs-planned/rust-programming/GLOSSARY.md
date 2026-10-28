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

## Concurrency and parallelism

**concurrency** — multiple operations may be in progress during overlapping time, even when one processor interleaves them rather than executing them simultaneously.

**parallelism** — multiple operations execute at the same time on different execution resources.

**schedule** — one legal ordering of significant events across threads while preserving each thread’s local program order.

**data race** — conflicting unsynchronized accesses to one memory location, with at least one write; undefined behavior and prevented by safe Rust.

**race condition** — product correctness depends on relative timing or schedule. A race condition can exist without a data race.

**`Send`** — unsafe auto trait indicating that ownership of a value may cross a thread boundary safely.

**`Sync`** — unsafe auto trait indicating that shared references to a value may cross thread boundaries safely; equivalently, `T: Sync` permits `&T: Send`.

**structured concurrency** — spawned work is bounded by an explicit scope or owner that accounts for completion, results, failure, and cleanup.

**protected invariant** — the exact condition a synchronization guard makes safe to inspect or change as one transition.

**condition predicate** — state-based expression that determines whether a waiting operation may proceed. A condition variable only provides sleep and notification around that predicate.

**backpressure** — a protocol prevents a producer from accumulating work beyond downstream capacity.

**endpoint ownership** — the count and location of channel senders and receivers whose drop or disconnect behavior carries lifecycle meaning.

**deadlock** — a set of participants cannot make progress because each waits for an event that depends cyclically on another participant.

**starvation** — an operation remains eligible to make progress but is repeatedly denied the required resource or scheduling opportunity.

**cancellation** — a cooperative product protocol that asks work to stop at defined checkpoints; it is not arbitrary thread termination.

**happens-before** — an ordering relation that makes effects before one synchronization event visible to operations after its matching observation.

**memory ordering** — the ordering constraint attached to an atomic operation, such as `Relaxed`, `Acquire`, `Release`, `AcqRel`, or `SeqCst`.

**linearization point** — the conceptual instant at which a concurrent operation takes effect in a history consistent with its specification.

**ABA problem** — a compare-and-exchange observes the same representational value after intermediate changes and cannot distinguish the new state from the old state without additional identity or version information.

**reclamation** — proving when removed concurrent storage is no longer reachable by any participant and may be destroyed or reused safely.

**work stealing** — idle workers obtain tasks from other workers’ queues to balance a finite parallel computation dynamically.

**associative reduction** — a combine operation whose grouping does not change meaning, permitting a parallel runtime to choose its reduction tree.

**deterministic reconciliation** — conversion of nondeterministic completion events into one stable product order using explicit identities, indices, or keys.


## Async and networked services

**future** — lazy state machine that advances only when polled and eventually produces an output or remains pending.

**poll** — one attempt to advance a future using a pinned mutable receiver and task context. It returns `Ready(output)` or `Pending`.

**waker** — task-specific capability used by a readiness source to tell the executor that another poll may now make progress. Wakeups may be coalesced and are not queued messages.

**suspension point** — `.await` boundary at which an async state machine may return `Pending`; values needed afterward become retained future state.

**cancellation by drop** — ending an async operation by dropping its future. Rust drops retained local values, but external effects already performed are not automatically rolled back.

**task** — runtime-owned scheduled future with a lifecycle distinct from the function that spawned it.

**task tree** — ownership map connecting parent operations, spawned children, join handles, cancellation sources, and shutdown obligations.

**runtime worker** — executor thread that polls ready tasks. Blocking it prevents unrelated tasks assigned to that worker from progressing.

**framing** — protocol layer that reconstructs complete messages from an arbitrary sequence of byte-stream chunks.

**frame codec** — incremental encoder and decoder with explicit length, buffering, EOF, and malformed-input policy.

**connection state machine** — legal protocol phases and transitions for one peer connection, including negotiation, ready, closing, and terminal states.

**admission control** — authoritative decision that accepts, queues, or rejects work according to explicit current capacity.

**capacity envelope** — complete set of bounds over connections, tasks, queues, buffers, frames, bodies, active work, retained records, and retry amplification.

**cancellation safety** — property describing which invariants and external effects remain valid if a future is dropped at any suspension point.

**deadline** — absolute time budget propagated across nested operations. Recreating a full timeout at every layer accidentally expands the total budget.

**graceful shutdown** — phased protocol that stops admission, signals children, drains bounded work, aborts after a deadline, joins tasks, and publishes terminal state.

**transport completion** — successful local transport operation, such as writing bytes to a socket; it does not prove remote application acceptance or commit.

**ambiguous commit** — result in which the caller cannot know whether a remote operation committed because the response was lost or the deadline expired.

**idempotency key** — stable semantic identity that lets repeated transport attempts refer to one logical operation and retrieve or share its terminal result.

**retry budget** — bounded combination of attempt count, delays, per-attempt time, and overall deadline.

**scripted peer** — deterministic test double that controls byte chunking, response timing, disconnect, malformed messages, and ambiguous outcomes.

**health surface** — operational endpoint reporting a deliberately scoped state. Its response is only as authoritative as the component and instant it observes.


## Performance and production engineering

### Performance contract

A falsifiable statement connecting one operation, workload, environment, metric, threshold, and correctness oracle.

### Workload

The input sizes, distributions, skew, validity classes, arrival patterns, and state conditions under which a result is measured.

### Measurement boundary

The exact start and end of the operation whose cost is reported. Setup, validation, cleanup, and rendering belong inside or outside only by explicit product reasoning.

### Tail latency

Latency in the slower part of a distribution, commonly described by percentiles such as p95 or p99. It is not interchangeable with average latency.

### Cost model

A hypothesis connecting product work to input size, distribution, call count, allocation, memory access, synchronization, or system calls.

### Retained memory

Memory kept alive by ownership, shared views, capacities, queues, caches, or pools even when only a small part is immediately useful.

### Byte journey

A ledger that follows data through external transfer, buffering, views, parsing, ownership promotion, storage, and output while naming every copy, move, share, and retention edge.

### Saturation knee

The region where increasing offered load no longer produces proportional useful throughput and latency, queueing, or rejection begins to rise sharply.

### Structured event

A named diagnostic occurrence with stable typed fields rather than only free-form prose.

### Span

A causal unit of work with context, descendants, and duration.

### Cardinality

The number of distinct label combinations or identities a telemetry system must retain. Unbounded cardinality can make an otherwise small metric surface operationally unsafe.

### Service-level indicator

A precisely defined measurement of user-visible service behavior, including population, success condition, window, and data source.

### Service-level objective

A target for an SLI over a stated window.

### Error budget

The permitted gap between perfect behavior and an SLO. It guides risk decisions but does not weaken correctness or security requirements.

### Load shedding

Deliberately rejecting work before it consumes a protected scarce resource so accepted work can remain useful.

### Degraded mode

An explicit operating state that preserves a documented subset of semantics and reports missing, stale, or disabled behavior honestly.

### Threat model

A structured account of assets, actors, trust boundaries, capabilities, abuse cases, controls, evidence, and residual risk.

### Supply chain

The source, dependencies, registries, build scripts, procedural macros, CI identities, tools, and distribution systems that contribute to a release artifact.

### Build profile

A named Cargo configuration controlling optimization, debug information, assertions, overflow checks, code generation, link-time optimization, panic behavior, and stripping.

### Release manifest

Deterministic metadata connecting an artifact to its source revision, lockfile, toolchain, target, profile, features, size, and digest.

### Production readiness

The state in which a specific artifact and configuration have sufficient correctness, capacity, observability, reliability, security, release, rollback, and operational evidence for a stated workload envelope.

### Canary

A limited rollout population used to evaluate a new artifact under real conditions before wider promotion.

### Rollback rehearsal

An executed test of restoring the previous compatible artifact and configuration, rather than an untested written intention.

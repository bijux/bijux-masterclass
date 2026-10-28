# One Reasoning Model for All Ten Courses

Rust’s vocabulary changes across the program, but the reasoning does not restart. The same questions scale from a local integer to an unsafe allocator, a task tree, a network protocol, and a versioned public API.

## 1. What exists?

Name concrete entities before discussing behavior: values, places, owners, loans, types, variants, buffers, syntax nodes, files, handles, threads, tasks, queues, frames, protocol states, artifacts, and external actors. Separate a semantic value from its byte layout, a future from the task that polls it, and a generated declaration from the macro that produced it.

## 2. Who owns it, who may observe it, and who has authority to change it?

Record unique owners, shared liveness roots, temporary borrows, consuming transitions, callback views, worker endpoints, broker authorities, protocol commit points, and migration owners. Ownership answers who must eventually clean up. Authority answers who is allowed to decide the next valid state.

## 3. Which states are valid?

Write the invariant before the implementation. Include representation validity, domain validity, protocol legality, queue membership, partial initialization, compatibility state, and operating state. If several flags can contradict each other, the state model is not finished.

## 4. What contract is promised?

A function promises inputs, outputs, failure, and visible state. A trait adds laws. An iterator adds item shape, order, cardinality, and termination. A macro adds accepted syntax, rejected syntax, and generated surfaces. An unsafe wrapper adds proof obligations. A concurrent or async component adds progress, cancellation, and shutdown. A public format adds compatibility and migration.

## 5. When can the fact be established?

Use the earliest decisive phase or event:

```text
source parsing
    → macro expansion
        → name resolution
            → type and trait solving
                → borrow and drop checking
                    → build execution and monomorphization
                        → runtime validation
                            → operating-system or foreign action
                                → synchronization, poll, frame, or protocol event
                                    → measurement, rollout, or compatibility observation
```

A later success cannot retroactively prove an earlier assumption. Compilation cannot validate hostile file contents. A successful write cannot prove remote semantic commit. A benchmark cannot prove compatibility.

## 6. How do information and authority flow?

Trace inputs into validated representations, state transitions, effects, outputs, and durable or externally visible results. At every edge, record type, ownership, cardinality, order, failure, and authority. Parsers, iterator chains, macro pipelines, binary codecs, brokers, and services are all staged transformations when written clearly.

## 7. What can fail, block, suspend, panic, or remain live?

Follow the non-happy path first. State what has already changed, which owner cleans up, what may remain externally visible, whether retry is safe, who wakes waiters, and how every thread or task terminates. Distinguish rollback, cleanup, cancellation, timeout, disconnect, panic containment, and post-commit uncertainty.

## 8. What order is promised?

Name source order, traversal order, completion order, message order, byte order, modification order, generated declaration order, persistence order, response order, and migration order. Preserve an order deliberately, normalize it, or state that it is unspecified.

## 9. What bounds the work and retained state?

List every accumulation point: input size, allocations, history, queues, tasks, threads, buffers, connections, in-flight requests, retry attempts, duplicate waiters, idempotency records, telemetry labels, generated code, and compatibility fixtures. One bounded component inside an unbounded pipeline does not create a bounded product.

## 10. Which part is static, dynamic, erased, generated, unsafe, or external?

Choose where variation and proof live. Static types can remove invalid compositions; dynamic checks can respond to runtime data; erasure can support heterogeneous extension; generation can keep related surfaces consistent; unsafe code can implement a safe abstraction; external systems remain assumptions. Each mechanism creates a different review and evolution cost.

## 11. What evidence can falsify the claim?

Match evidence to the claim: compiler prediction, compile-fail cases, unit and integration tests, law tests, model oracles, malformed corpora, failure injection, deterministic clocks, Miri, thread-state exploration, FFI consumers, benchmarks, profiles, load tests, security review, artifact manifests, rollout drills, and compatibility fixtures. Record what each result does not prove.

## 12. What happens when the system changes?

Name downstream callers, implementors, stored data, generated syntax, features, toolchains, platforms, artifacts, operators, and migration paths. A change is complete only when authority remains singular and old behavior is preserved, migrated, rejected, or deliberately retired.

## The maturity path

| Course | The shared model becomes… | Working record |
|---:|---|---|
| 1 | Rust Foundations | How do Rust’s types, ownership rules, state models, and error boundaries combine into a complete program you can explain end to end? | type trace, ownership ledger, state-transition table, error map, and public-boundary map |
| 2 | Ownership, Lifetimes, and Memory | How do places, loans, lifetimes, destruction, shared liveness, representation, and address stability determine whether a memory design is valid? | place and move-path map, loan graph, lifetime relation, destruction trace, liveness graph, representation table, and pinning contract |
| 3 | Traits, Generics, and Architectural Design | How should a Rust architecture represent shared behavior, type relationships, runtime variation, protocol states, and downstream extension without importing an inheritance model? | trait-law table, associated-type relationship map, coherence ownership map, dispatch map, typestate transition graph, adapter boundary, and compatibility matrix |
| 4 | Functional Rust | How can Rust make capture, traversal, cardinality, ordering, failure, accumulation, structural sharing, effects, and cost visible in one dataflow? | capture map, iterator stage table, cardinality and order trace, failure-policy matrix, accumulator invariant, structural-sharing graph, effect boundary, and qualitative cost model |
| 5 | Rust Metaprogramming | Which facts deserve one compile-time source of truth, which generation mechanism is the least powerful adequate choice, and how can expanded code remain diagnosable ordinary Rust? | authority map, accepted grammar, token and repetition trace, hygiene/path map, expansion ledger, diagnostic contract, phase map, generated-surface inventory, and reproducibility record |
| 6 | Rust Systems Programming | What does each external boundary promise, which facts can Rust verify, which facts require a manual proof, and how does a safe interface contain those obligations? | binary-layout table, cursor/range proof, resource-state machine, durability timeline, path threat model, process contract, safety dossier, allocator layout record, ABI table, and foreign-liveness graph |
| 7 | Rust Concurrency and Parallelism | Which facts remain true across every legal thread schedule, and what ownership, synchronization, progress, failure, and normalization arguments make those facts reviewable? | thread ownership map, protected-invariant table, wait-for graph, predicate/wakeup record, channel topology, shutdown tree, happens-before graph, atomic state machine, work-partition map, and deterministic reconciliation table |
| 8 | Rust Async and Networked Services | How do suspension, wakeup, task ownership, framing, protocol state, capacity, cancellation, retry, and shutdown remain explicit when peers and timing are only partly observable? | future state table, wake-source map, task tree, buffer/frame ledger, connection state machine, protocol transition table, capacity ledger, cancellation trace, retry/commit matrix, and shutdown timeline |
| 9 | Rust Performance and Production Engineering | Which measurements, resource bounds, signals, security controls, artifact records, and operating policies make a Rust system defensible under representative load? | performance claim, workload description, benchmark boundary, cost model, allocation ledger, byte journey, saturation curve, signal dictionary, SLO/error-budget policy, threat model, dependency dossier, release manifest, and rollout decision |
| 10 | Advanced Rust Mastery | How do you design and evolve a Rust system whose type relationships, unsafe boundaries, compiler behavior, compatibility promises, verification evidence, and operating limits survive independent change? | compiler-phase record, trait-goal graph, lifetime family, witness proof, open/closed variation map, unsafe state-and-operation dossier, source-to-artifact observation, verification claim matrix, compatibility matrix, migration plan, and architecture decision record |

## A compact review template

For any unfamiliar Rust component, write:

```text
product promise:
entities and owners:
valid states:
primary authority:
decisive phase or event:
success transition:
failure and cleanup:
order and capacity:
external assumptions:
verification evidence:
compatibility stakeholders:
residual uncertainty:
```

If the component cannot be summarized this way, the architecture may be hiding several responsibilities behind one type or API.

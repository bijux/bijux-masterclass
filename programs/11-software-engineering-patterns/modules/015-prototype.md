---
module_id: SEPAT-015
program: Software Engineering: Patterns
level: 1
module_number: 15
title: Prototype
status: complete
last_verified: 2026-08-28
---

# Prototype

## One-Page Review

### Governing question

When should new objects be created by copying configured exemplars, and how can the copy preserve intended structure without sharing mutable identity, duplicating external authority, or propagating stale provenance?

### Essential definitions

- **Prototype** is the GoF creational pattern that creates products by copying an exemplar through a cloning contract.
- A **prototype registry** maps explicit keys to approved exemplars that clients can copy without naming Concrete Product classes.
- A **shallow copy** creates a new outer object while retaining references to nested objects.
- A **deep copy** recursively creates nested copies, subject to cycle and sharing rules.
- A **selective copy** classifies each relationship as copied, intentionally shared, rebound, recomputed, or rejected.
- **alias topology** describes which references in an object graph point to the same node; correct cloning may need to preserve that topology within the clone.
- A **copy invariant** states the behavioral, structural, identity, ownership, and provenance properties required after cloning.
- A **copy memo** maps source identities to clone identities so cycles terminate and repeated references remain repeated rather than duplicated.
- An **external resource** is state such as a socket, lock, transaction, file handle, thread, device session, or credential lease whose raw duplication is generally invalid.
- A **copy-on-write** representation shares state until mutation, then isolates the writer under explicit concurrency semantics.

### Central model, mechanism, or theorem

Represent an exemplar as labeled object graph (G=(V,E,\lambda)). Partition edges by copy policy:

$$
E=E_{own}\cup E_{share}\cup E_{rebind}\cup E_{reject}.
$$

A clone mapping (f) must create fresh identities for owned mutable nodes, preserve intentional shared nodes, resolve rebound dependencies in the target context, and fail for rejected resources:

$$
(u,v)\in E_{own}\Rightarrow f(v)\ne v,
\qquad
(u,v)\in E_{share}\Rightarrow f(v)=v.
$$

If two source edges alias the same owned node, both clone edges should normally alias one (f(v)), not two independent copies. Value equality alone is insufficient evidence of a correct clone.

### Critical invariants

- The clone and prototype have distinct root identity when independent lifecycle is promised.
- Mutable owned state is isolated; intentionally shared state is immutable or synchronized by contract.
- Internal alias relationships and cycles follow a documented topology policy.
- External resources are reacquired, leased, cleared, or rejected explicitly—never blindly duplicated.
- Unique identity, timestamps, audit fields, secrets, and environment bindings are regenerated or handled by policy.
- Clone failures release every partially created owned resource.
- Registry keys, exemplar versions, trust, and update semantics are explicit.
- Copy performance claims include graph size, depth, mutation rate, and measurement evidence.

### Common failures

Common failures include assuming assignment copies, equating shallow copy with independence, recursively duplicating everything, breaking internal sharing by copying one node twice, looping on cycles, cloning database identifiers or idempotency keys, copying locks and sockets, sharing mutable collections accidentally, registering untrusted exemplars, mutating a live registry prototype, treating serialization round trips as universally correct cloning, and using Prototype where a constructor or immutable value is clearer.

### Compact example

A workflow exemplar owns a mutable list of steps and shares an immutable retry-policy tuple. Its clone receives a new name, copies the step list, and retains the policy tuple. Adding `archive` to the clone does not change the prototype, while policy identity remains intentionally shared. The code proves only this selected graph and policy.

### Connections

[SEPAT-014](014-builder.md) assembles explicit construction decisions; Prototype begins from an exemplar. [SEPAT-016](../ROADMAP.md) examines single-instance access, which must not be confused with shared immutable prototype state. Graph copying connects to [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md), ownership to [Programming Languages: Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md), and identity to [Database Engineering](../../18-database-engineering/ROADMAP.md).

## Governing Question

What makes cloning a better creation mechanism than reconstructing from explicit configuration, and what copy policy makes the resulting object graph semantically safe?

Prototype fits when runtime product types are discovered dynamically, exemplars are expensive or intricate to configure, or a family of near-identical Products should vary without parallel factory classes. The exemplar becomes executable configuration.

That convenience moves complexity into copy semantics. Real objects are graphs containing mutable ownership, deliberate sharing, cycles, cached derivations, unique identity, external resources, and security context. “Deep copy” is not a policy; it is one recursion strategy that often copies too much and sometimes not enough.

## Why This Matters

Copy defects are delayed and nonlocal. A clone looks correct until a nested list changes both objects, a duplicated identifier overwrites the original row, a copied lock protects the wrong state, or an old credential remains embedded. Equality-based tests miss identity and lifecycle.

Prototype can also improve extensibility. A graphics editor can register shape exemplars; a simulation can clone calibrated immutable configurations; a test suite can derive scenarios from trusted fixtures. Clients need not know Concrete Product classes or repeat expensive setup.

Production design therefore specifies a graph transformation, not just a method named `clone`. It inventories every relationship and proves the desired identity, aliasing, ownership, provenance, and effect boundaries.

## Prerequisites and Retrieval

You should understand object identity, references, graphs, mutability, ownership, constructors, registries, and resource lifecycle. Retrieve these facts:

1. Assignment commonly creates another reference rather than another object.
2. Shallow copying preserves nested references.
3. Recursive deep copying needs a memo to handle cycles and repeated references.
4. Equality, identity, and observational equivalence are different relations.
5. Some state represents external authority and cannot be copied as memory.
6. A prototype registry adds configuration, version, concurrency, and trust policy.

## Learning Objectives

After completing this module, you should be able to:

- identify Prototype, Concrete Prototype, client, clone operation, and registry roles;
- derive Prototype from exemplar-based variation and runtime type forces;
- model a Product as an object graph with per-edge copy policy;
- distinguish shallow, deep, selective, serialized, and copy-on-write strategies;
- preserve cycles and internal alias topology with a memo;
- handle identity, provenance, secrets, and external resources safely;
- design graph-structural and mutation-based clone tests;
- replace Prototype when explicit construction becomes safer or clearer.

## Core Exposition

### Begin with the exemplar force

Prototype is useful when a valid object already embodies substantial configuration and copying it is the natural domain operation. Examples include diagram shapes with styles, simulation scenarios, parser configurations, or game entities with component templates.

Do not clone merely to avoid writing a constructor. Explicit construction makes dependencies and defaults visible. If the Product is a small immutable value, reuse it directly or create another equal value.

### Copy the graph, not the fields

Inventory the reachable object graph and label edges. An owned mutable child normally receives a fresh clone. An immutable interned policy can remain shared. A context service should be rebound. A live transaction should reject copying.

Field-by-field syntax can obscure graph topology. Two fields may point to the same list. Copying each field independently creates two lists and changes semantics; memoization maps the shared source node to one clone node.

### Shallow copying

A shallow copy makes a new root and retains child references. This is correct when children are immutable, explicitly shared, or copy-on-write. It is hazardous when the root appears independent but nested mutation is permitted.

Document which layer is isolated. “Clone” without depth or policy invites false assumptions.

### Deep copying

Generic deep copy recursively copies reachable compound objects. It needs a memo for cycles and repeated references. It can copy too much: immutable data, caches, service references, or large shared tables. It may not know how to copy native resources.

Prefer domain-specific selective cloning for nontrivial Products. The Product owner knows which relationships carry ownership and authority.

### Identity and provenance

Database primary keys, event IDs, idempotency tokens, version vectors, audit creators, creation time, signatures, and trace context need explicit policy. A draft template may clear persisted identity and record `derived_from`; a historical snapshot may preserve identity precisely because it is not a new entity.

Never regenerate blindly either. Domain meaning determines whether the result is a new entity, a value copy, a snapshot, a fork, or a view.

### External resources

Sockets, file handles, locks, threads, transactions, GPU contexts, device sessions, and credential leases cannot be made safe by duplicating fields. Options are:

- reject cloning while the resource is attached;
- clone configuration and reacquire later;
- share a reference-counted lease with explicit semantics;
- create a disconnected clone;
- transfer ownership and invalidate the prototype, which is move rather than clone.

Cleanup every partial acquisition if a custom clone fails.

### Prototype registries

A registry maps a bounded key to an exemplar and returns clones. Define key collisions, version selection, mutation freeze, replacement, concurrency, eviction, and provenance. Expose safe listing and errors.

Registry exemplars should normally be immutable after publication or replaced atomically. Cloning while an exemplar mutates yields nondeterministic mixed snapshots. Untrusted serialized exemplars are code/data loading boundaries requiring validation and isolation.

### Copy-on-write

Copy-on-write shares backing state and creates a private version on mutation. It can make large mostly-read clones cheap, but correctness depends on intercepting every mutation and coordinating concurrency. Hidden aliases or foreign interfaces can bypass detachment.

Measure read/write patterns and memory, not only creation time. A later mutation storm can move cost and latency to the worst moment.

### Serialization as cloning

Serialize-deserialize can create a disconnected graph and cross process/language boundaries. It usually drops live resources and may transform types, precision, aliases, private state, schema versions, and security context.

Use it when the serialization contract itself defines the desired copy. Do not use it as a generic shortcut around an unspecified clone policy.

### Behavioral clone contracts

State what remains equal and what becomes independent. Immediately after clone, Products may be observationally equivalent for selected operations. After allowed mutation of one, independence properties should hold. Shared immutable policies may retain identity.

For a clone (c=clone(p)), tests should check root identity, value correspondence, owned-child nonidentity, shared-child identity, alias topology, cycles, resources, provenance, and mutations in both directions.

### Evolution and versions

Adding a field requires an explicit default and copy policy. Older prototypes may lack it; newer code must migrate or reject them. Cached derived fields can be copied only if their dependency version matches; otherwise recompute or clear.

Record prototype schema and policy version. A registry key like `standard` without version can silently change reproducibility.

### Refactor away

If exemplar state becomes small explicit configuration, replace clone with a named creation function or Builder. If Products become immutable values, sharing may be correct and cloning unnecessary.

Keep Prototype only when exemplar-based creation remains clearer and its copy contract is owned and tested.

## Definitions and Notation

Let source graph be (G=(V,E)), source root (r), and clone mapping (f:V'\to V_c) for the cloned subset (V'). The mapping must be a function so one copied source node has one clone node:

$$
u=v\Rightarrow f(u)=f(v).
$$

For owned mutable nodes,

$$
v\in V_{own}\Rightarrow f(v)\ne v,
$$

while intentional shared nodes satisfy

$$
v\in V_{share}\Rightarrow f(v)=v.
$$

Edge preservation for copied topology requires

$$
(u,v,\ell)\in E_{copy}\Rightarrow(f(u),f(v),\ell)\in E_c.
$$

Cycles terminate because (f(v)) is entered in the memo before cloning successors. For mutation set (M) permitted on clone-owned state, independence requires selected prototype observations remain unchanged after (m\in M) is applied to the clone. These conditions do not define policy for omitted nodes; every reachable edge still needs classification.

## Mechanisms, Invariants, or Proof Structure

### Inventory graph and authority

Map roots, nested aliases, cycles, mutable ownership, immutable sharing, caches, identities, resources, secrets, and environment bindings.

### Assign per-edge policy

Choose copy, share, rebind, recompute, clear, lease, or reject. Record rationale and target-context requirements.

### Clone with topology preservation

Create the target root, memoize before recursion, then populate edges according to policy. Publish only after invariants hold.

### Verify selective copying

The executable example isolates mutable steps while sharing an immutable policy tuple.

<!-- bijux-verify: {"id":"selective-workflow-prototype","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"original: ingest steps=read,validate policy=retry:3\nclone: ingest-copy steps=read,validate,archive policy=retry:3\nsteps-independent=True\npolicy-shared=True\n","stderr":""}} -->
```python
class Workflow:
    def __init__(self, name, steps, policy):
        self.name = name
        self.steps = steps
        self.policy = policy

    def clone(self, name):
        return Workflow(name, list(self.steps), self.policy)

    def summary(self):
        return (
            f"{self.name} steps={','.join(self.steps)} "
            f"policy={self.policy[0]}:{self.policy[1]}"
        )


prototype = Workflow("ingest", ["read", "validate"], ("retry", 3))
clone = prototype.clone("ingest-copy")
clone.steps.append("archive")

print(f"original: {prototype.summary()}")
print(f"clone: {clone.summary()}")
print(f"steps-independent={prototype.steps is not clone.steps}")
print(f"policy-shared={prototype.policy is clone.policy}")
```

The run proves two identity relationships and selected values for one acyclic graph. It does not prove deep-copy behavior, thread safety, resource handling, registry safety, or general immutability.

### Test mutations and failures

Mutate every owned mutable node in both source and clone; verify intended isolation. Check shared state, alias topology, cycles, failure cleanup, provenance, and version migration.

### Compare reconstruction

Benchmark and review explicit construction, Builder, persistent values, and Prototype under representative graph sizes and mutation workloads.

## Alternatives and Trade-Offs

**Constructor or creation function.** Makes dependencies and identity policy explicit. Repeating intricate runtime configuration may be costly.

**Builder.** Reconstructs through named validated decisions. It is verbose when a valid exemplar already captures most state.

**Prototype.** Creates dynamic variants without naming Concrete Products. Copy policy, aliasing, identity, and resources are difficult.

**Shallow copy.** Fast and topology-preserving at one layer. Nested mutable state remains shared.

**Generic deep copy.** Convenient for plain data graphs. It may copy too much, mishandle authority, or hide expensive traversal.

**Selective clone.** Matches domain ownership and provenance. It requires explicit maintenance as the Product evolves.

**Copy-on-write.** Efficient for large read-mostly state. Mutation interception and concurrency are subtle.

**Immutable sharing.** Eliminates cloning when the whole Product is a value. It does not fit independent mutable lifecycle.

## Failure Modes and Misconceptions

1. **Assignment creates a clone.** It often creates another reference to the same root.
2. **Shallow copy means independent object.** Nested mutable children remain shared.
3. **Deep copy is always safest.** It can duplicate authority, caches, immutable data, and huge graphs.
4. **Field equality proves correctness.** Identity, aliases, resources, and post-mutation behavior matter.
5. **Copy every reference independently.** This can destroy intentional internal aliasing.
6. **Cycles are rare enough to ignore.** Parent, graph, observer, and cache links commonly cycle.
7. **Identifiers are ordinary fields.** Their duplication can violate uniqueness and idempotency.
8. **Resources can be cloned like data.** External authority needs rebind, lease, disconnect, or rejection.
9. **Registry prototypes may mutate live.** Concurrent clones can observe incoherent snapshots.
10. **Serialization is universal deep clone.** Schema, types, aliases, precision, and security semantics differ.

## Worked Examples

### Example 1

**Question:** What does the executable clone establish?

**Reasoning:** It creates distinct root and steps-list identity, intentionally shares an immutable tuple, and shows clone mutation leaves prototype steps unchanged.

**Conclusion:** Selective copy expresses ownership better than “deep versus shallow” alone.

### Example 2

**Question:** How should two fields sharing one mutable child be cloned?

**Reasoning:** If the alias is meaningful, both clone fields must reference one fresh copied child. A memo preserves the equivalence class while isolating it from the source.

**Conclusion:** Preserve alias topology, not only values.

### Example 3

**Question:** What happens to a parent-child cycle?

**Reasoning:** Allocate and memoize the clone parent before cloning children; child back-references resolve through the memo. Recursive copying without early memoization does not terminate.

**Conclusion:** Cycles make graph-aware cloning mandatory.

### Example 4

**Question:** Should a cloned database entity retain its primary key?

**Reasoning:** A new entity normally clears or regenerates identity and records derivation. A historical snapshot preserves identity because it represents the same event/state at another time.

**Conclusion:** Domain semantics, not copy depth, decide identity.

### Example 5

**Question:** Can a connected client be cloned?

**Reasoning:** Clone immutable connection configuration and return a disconnected client, or share an explicit managed pool. Duplicating socket and lock fields creates false ownership.

**Conclusion:** Reacquire external resources under a new lifecycle.

### Example 6

**Question:** When does a prototype registry help a graphics editor?

**Reasoning:** Tools register approved shape exemplars with style and component graphs; palette actions clone by stable versioned key. Freeze exemplars and test every shape copy contract.

**Conclusion:** Runtime product diversity plus configured exemplars supports a registry.

### Example 7

**Question:** Is copy-on-write automatically thread-safe?

**Reasoning:** No. Reference counts, detachment, mutation visibility, and foreign aliases need synchronization and memory-model analysis.

**Conclusion:** Copy-on-write is a representation policy, not a concurrency proof.

### Example 8

**Question:** Should a derived cache be copied?

**Reasoning:** Copy it only if immutable dependencies and version match; otherwise clear or recompute. A clone with changed inputs and stale cache violates correspondence.

**Conclusion:** Derived state needs dependency-aware policy.

### Example 9

**Question:** When is serialization an appropriate clone?

**Reasoning:** When the versioned serialization schema defines the intended transferable state and loss of live resources/aliases is explicit. Validate untrusted payloads before construction.

**Conclusion:** Serialization is one contract-specific transformation.

### Example 10

**Question:** When should Prototype be removed?

**Reasoning:** If an exemplar reduces to a small immutable configuration and clone policy dominates maintenance, use explicit creation or share the value.

**Conclusion:** Prefer visible construction when exemplar copying no longer earns its complexity.

## Cross-Program Connections

- **Algorithms & Data Structures:** graph traversal, cycle detection, equivalence classes, and asymptotic cost shape cloning.
- **Object-Oriented Programming:** identity, encapsulation, polymorphic clone contracts, and subtype state matter.
- **Functional Programming:** persistent immutable structures share safely and reduce cloning needs.
- **Systems Programming:** moves, ownership, handles, and RAII distinguish memory copies from resource transfer.
- **Programming Languages:** copy constructors, clone traits, serialization, reflection, and garbage collection differ.
- **Database Engineering:** entity identity, versions, snapshots, and uniqueness determine copy semantics.
- **Distributed Systems:** trace IDs, idempotency keys, vector versions, and sessions cannot be duplicated casually.
- **Security Engineering:** credentials, capabilities, signatures, and untrusted exemplars carry authority.
- **Testing & Quality Engineering:** metamorphic mutation tests and graph-identity assertions validate clones.
- **Performance Engineering:** copy-on-write and deep-copy claims require representative graph and mutation workloads.

## References

1. Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, [*Design Patterns: Elements of Reusable Object-Oriented Software*](https://www.pearson.com/en-us/subject-catalog/p/Gamma-Design-Patterns-Elements-of-Reusable-Object-Oriented-Software/P200000009480/9780321700698), Addison-Wesley, 1994. Canonical Prototype intent, structure, participants, consequences, registries, and implementation issues.
2. Python Software Foundation, [“`copy` — Shallow and Deep Copy Operations”](https://docs.python.org/3/library/copy.html), accessed 2026-08-28. Defines shallow/deep copy behavior, memoization, recursion, over-copying, customization, and unsupported resource-like types.
3. Joshua Bloch, [*Effective Java*, 3rd ed.](https://www.pearson.com/en-gb/subject-catalog/p/effective-java/P200000000138), Addison-Wesley, 2018. Examines Java cloning contracts and favors explicit copy mechanisms when `Cloneable` semantics are unsuitable.
4. Rust Project Developers, [“The `Clone` Trait”](https://doc.rust-lang.org/std/clone/trait.Clone.html), accessed 2026-08-28. Documents explicit duplication for types that cannot be copied implicitly and type-owned clone semantics.
5. Eric Evans, [*Domain-Driven Design: Tackling Complexity in the Heart of Software*](https://www.pearson.com/en-gb/subject-catalog/p/domain-driven-design-tackling-complexity-in-the-heart-of-software/P200000009375/9780321125217), Addison-Wesley, 2003. Supplies entity versus value identity and aggregate lifecycle context.
6. Bjarne Stroustrup and Herb Sutter, editors, [*C++ Core Guidelines*](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines), accessed 2026-08-28. Ownership and resource-management rules distinguish copying values from duplicating or sharing resource handles.

## Exercises

### Exercise 1

Draw the executable example as a labeled graph before and after cloning. State root, steps, and policy identity/equality relations and the mutation evidence.

### Exercise 2

Design a clone algorithm for a cyclic graph with two parent fields sharing one child. Give memo insertion order and prove the intended alias relationships for this finite graph.

### Exercise 3

Specify copy policy for a persisted Order containing identity, lines, immutable catalog values, payment authorization, audit data, cache, and domain events under both “duplicate as new draft” and “historical snapshot” operations.

### Exercise 4

Design a versioned, concurrent prototype registry for graphics plugins. Cover trust, immutable publication, replacement, clone failure, eviction, reproducibility, and observability.

### Exercise 5

An unfamiliar autonomous-vehicle platform clones calibrated driving scenarios for simulation and hardware-in-the-loop testing. Produce a graduate-level Prototype design covering graph topology, sensor/device handles, randomness, time, provenance, safety invariants, evidence, and human authorization.

## Answers to the Exercises

### Answer 1

Source root (w_0) has owned edge to mutable list (s_0) and shared edge to immutable tuple (p). Clone root (w_1) is distinct: (w_1\ne w_0). Its owned steps edge targets (s_1\ne s_0), initially value-equal to (s_0). Its shared policy edge targets the same (p), so both equality and identity hold for policy.

Appending `archive` mutates (s_1) only. The printed original remains `read,validate`, while clone becomes `read,validate,archive`; this is bounded mutation evidence for list isolation. It does not prove other fields, concurrent behavior, tuple deep immutability for arbitrary contents, or general graph cloning.

### Answer 2

Let source parent (a) have edges `left` and `right` to the same child (b), and (b.parent=a). Allocate clone (a') and immediately memoize (a\mapsto a'). Follow `left`: allocate (b'), memoize (b\mapsto b'), then follow `parent`; memo returns (a'). Assign (b'.parent=a'). Assign (a'.left=b'). Follow `right`; memo returns existing (b'), so assign (a'.right=b').

Thus (a'\ne a), (b'\ne b), (a'.left=a'.right=b'), and (b'.parent=a'). The finite traversal terminates because every recursive revisit finds a memo entry. This proves topology for the declared graph only; per-node state and external edges require additional policy.

### Answer 3

For “new draft,” generate a new Order identity, clear persistence version, payment authorization, fulfillment state, emitted-event IDs, and commit/audit timestamps. Copy line quantities and pricing inputs under a stated repricing policy; share immutable catalog values by stable version or re-resolve them explicitly. Record `derived_from` source identity and actor. Clear derived totals cache and create no pending domain events until the draft changes. Never duplicate an idempotency or payment token.

For a historical snapshot, preserve Order identity, version, lines, prices, audit provenance, and recorded event identities because it describes the same historical state. Payment authorization is represented by non-secret immutable reference/status, not a live capability. Snapshot collections are immutable and caches either verified against the captured version or recomputed. Neither operation copies a live database session, lock, Unit of Work, or credential.

### Answer 4

Use keys `(plugin_id, prototype_name, schema_version, artifact_digest)`. Authenticate signed plugin artifacts, validate metadata and clone contract, and construct exemplars in isolation. Publish an immutable registry snapshot atomically; readers select a snapshot/version and never observe partial replacement. Duplicate keys reject unless an explicit compare-and-swap replacement policy applies.

Cloning uses per-product bounded errors and cleans partial resources. Track source digest and registry generation in every clone for reproducibility. Replacement creates a new generation; existing readers may finish on their pinned snapshot. Evict only when no pinned readers or clones require the exemplar, with bounded memory and diagnostics. Metrics cover selection, clone duration/failure, generation, and safe error class without secrets. Untrusted plugin code runs under constrained capabilities; registry lookup is not authorization to execute arbitrary classes.

### Answer 5

Represent a scenario as immutable environment/road maps and model parameters intentionally shared, plus owned mutable actor states, sensor schedules, fault scripts, and result buffers copied with topology-preserving memoization. Vehicle, actor, and sensor references preserve declared internal aliases and cycles. Hardware devices, sockets, GPU contexts, locks, and simulator processes are rebound from approved configuration or rejected; never memory-copied.

Generate a new run identity and deterministic random-stream hierarchy from an approved master seed plus scenario digest and run index. Record seed derivation, simulation clock model, software/model/artifact digests, calibration versions, source prototype, operator, and transformations. Wall-clock handles are rebound; scenario time starts from a declared epoch. Mutation cannot alter the frozen registry exemplar.

Safety invariants cover coordinate frames, units, calibrated ranges, actor nonoverlap at initialization, sensor timing, actuator bounds, fault timing, and hardware limits. Test graph identities and aliases, cycles, bidirectional mutation isolation, reproducibility, controlled seed variation, stale caches, device-binding failure, resource cleanup, concurrency, and fault containment. Compare simulation and hardware-in-the-loop within stated model limits; neither establishes road safety alone. Named vehicle-safety, controls, simulation, hardware, security, verification, and operations authorities approve exemplars, calibration, evidence, and execution scope. Repository validation grants no vehicle authorization.

# Final Review — Reconstruct, Audit, and Change

Complete this review after all ten modules and laboratories. Do not read the [reasoned review guide](final-review-solutions.md) until a complete first attempt exists.

## Part I — Closed-book reconstruction

Draw and explain:

1. a property descriptor with every attribute and all legal category transitions;
2. the key sets observed by each major enumeration and copying operation;
3. a prototype lookup in which an inherited getter executes with a derived receiver;
4. a write that invokes an inherited setter rather than creating an own data property;
5. the difference among `.prototype`, internal prototype, `instanceof`, and private brand;
6. method, extracted, bound, arrow, explicit-`this`, and constructor invocation;
7. the complete `new` algorithm including explicit object return;
8. base and derived class initialization timelines;
9. an authority map comparing inheritance, delegation, forwarding, closure state, and a mixin;
10. the discovery and fallback paths for `Symbol.toPrimitive`, `Symbol.iterator`, and custom inspection;
11. iterable, iterator, iterator result, generator state, and early close;
12. a proxy operation that must preserve a target invariant;
13. a case where a proxy is observably not transparent;
14. a graph showing shallow copy, structural clone, sharing preservation, and domain-ID remapping;
15. an explicit cleanup protocol that does not depend on garbage collection;
16. ObjectAtlas's live-object, plain-record, debug, and persisted representations.

## Part II — Prediction examination

Select twenty unseen investigations, two from each module. Before running tools, record:

- type-check outcome;
- runtime outcome if execution is meaningful;
- first decisive phase;
- exact object-model rule;
- smallest requirement-preserving repair;
- one weak repair to reject.

Target at least sixteen correct initial classifications and a correct causal explanation for every corrected answer.

## Part III — Architecture clinics

### Clinic A — getter-triggering serializer

A serializer iterates `Object.keys(instance)` and reads every value. A newly added enumerable getter performs an expensive filesystem lookup and occasionally throws. Redesign the boundary so persistence remains data-only and inspection remains effect-aware.

### Clinic B — forged class instance

A decoder creates `Object.setPrototypeOf(record, Account.prototype)` and treats the result as an `Account`. The next private-field access fails. Explain every identity and initialization fact involved, then design legitimate reconstruction.

### Clinic C — lost receiver in registry

A command registry stores `service.execute` directly. Invocation later throws because `this.store` is undefined. Produce three valid repairs, compare their authority and allocation consequences, and reject one broad binding strategy.

### Clinic D — lying proxy

A proxy hides a non-configurable own property from `ownKeys`. Explain why the engine rejects the trap and design a legal redaction surface.

### Clinic E — clone identity collapse

A subtree is cloned with `structuredClone`, but internal references still contain old domain IDs and the resulting plain records have no node behavior. Separate structural data copying from domain reconstruction and define a remapping algorithm.

### Clinic F — finalizer as correctness

A cache increments a live-session counter when opening a resource and decrements it only in a `FinalizationRegistry` callback. Explain why capacity accounting eventually fails and redesign deterministic ownership.

## Part IV — Independent product

Build a small **SceneGraph** package without copying ObjectAtlas code. Requirements:

- stable domain IDs;
- private branded live nodes;
- ordered parent/child relationships;
- descriptor-safe debug inspection;
- preorder and breadth-first iteration;
- plain versioned persistence;
- subtree duplication with domain-ID remapping;
- one revocable plain-data edit draft;
- explicit session cleanup;
- unit and process-level tests.

Write a two-page architecture note explaining which mechanisms were deliberately not used.

## Part V — ObjectAtlas independent extension

Add **aliases** to ObjectAtlas.

An alias is an alternate validated name for a node. Aliases must be unique across the atlas and must not equal another node's ID. The change must address:

- live representation;
- descriptors and enumeration;
- private state and public read views;
- alias lookup;
- edit authority;
- traversal output;
- subtree cloning;
- persistence version policy;
- debug inspection;
- CLI parsing and rendering;
- compatibility with existing V1 files;
- tests for duplicates, removal, cloning, and reload.

Do not solve the requirement by placing aliases in an unvalidated public array or by rebuilding a global index opportunistically during lookup.

## Part VI — Oral defense

Answer without opening source:

1. Which ObjectAtlas fields are own, private, inherited, symbol-keyed, or persisted?
2. Which reads may execute code?
3. Why are live nodes not persisted directly?
4. Which operation owns graph mutation authority?
5. Why does traversal carry a structural revision?
6. Why is the edit proxy limited to a plain attribute object?
7. Which identities survive subtree cloning?
8. What cleanup is deterministic and what cleanup is merely garbage collection?
9. Which public changes would break downstream callers even if TypeScript still compiled?
10. Where would a simpler ordinary function be preferable to another class or protocol?

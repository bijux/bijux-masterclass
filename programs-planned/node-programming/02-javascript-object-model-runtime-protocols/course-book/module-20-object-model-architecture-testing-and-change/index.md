# Module 20 — Object-Model Architecture, Testing, and Independent Change

> **Question:** Can the complete product preserve object identity, encapsulation, protocol behavior, reflection, persistence, and lifecycle when a new requirement crosses every layer?

## Why this comes now

The course has developed one connected model:

```text
own properties and descriptors
        ↓
prototype lookup and receiver behavior
        ↓
call and construction semantics
        ↓
classes and private initialization
        ↓
composition and capability authority
        ↓
symbol-keyed runtime protocols
        ↓
iterators and generator state
        ↓
reflection and proxy invariants
        ↓
reachability, cloning, and disposal
```

A reader has not mastered these topics merely by explaining them separately. A real change can alter several surfaces at once. Adding node aliases, for example, affects property representation, key validation, iteration output, persistence, clone identity, inspection, proxy edits, and public compatibility. The final module teaches whole-product reasoning and requires an independent cross-layer change.

ObjectAtlas is completed here as a library and CLI. The goal is not to maximize use of advanced object features. The goal is to use each mechanism only where its semantics improve the product and to keep plain data and ordinary methods ordinary.

## Outcomes

By the end of this module, you can:

- produce a complete runtime-object map for a Node.js package;
- distinguish domain identity, JavaScript object identity, prototype identity, private brand, and persisted identity;
- audit a public API for descriptors, receivers, mutation authority, protocols, and lifecycle;
- design tests for property, prototype, iterator, proxy, clone, and disposal contracts;
- keep debug, persistence, and domain representations separate;
- evaluate compatibility effects of changing class, descriptor, and protocol surfaces;
- integrate ObjectAtlas as a deterministic ESM library and CLI;
- implement an unseen cross-layer feature without bypassing invariants;
- explain why each object mechanism was selected and which simpler alternatives were rejected.

## 1. Build a runtime-object map

Before changing the architecture, map its runtime values:

| Runtime value | Identity | State owner | Prototype or callable behavior | Lifecycle |
|---|---|---|---|---|
| `AtlasNode` instance | live node identity | private fields | class prototype | owned by atlas membership |
| `ObjectAtlas` instance | graph authority | node map, root order, revision | class prototype and iteration protocol | application-owned |
| node record | persisted data identity | plain object fields | ordinary prototype or validated null-prototype representation | temporary/serialized |
| read view | capability identity | snapshot or wrapper | narrow methods/getters | call-scoped or caller-owned |
| edit session | transaction identity | base snapshot, changes, terminal state | class + draft proxy | explicit commit/rollback/dispose |
| traversal iterator | traversal identity | stack/queue, revision, visited set | generator/iterator protocol | consumer-owned until close/completion |
| codec | behavior capability | no mutable graph authority | plain object or module functions | application lifetime |
| store | filesystem capability | path/configuration | class or object methods | explicitly owned |

This map prevents identity collapse. A node record is not a node instance. A read view is not mutation authority. A proxy is not the target. An iterator is not the atlas. A persisted ID is not JavaScript reference identity.

## 2. Maintain an invariant register

ObjectAtlas’s core invariants include:

1. node IDs are valid and unique;
2. every child ID refers to an existing node;
3. every non-root node has exactly one parent;
4. parent and child relationships agree in both directions;
5. the graph is acyclic;
6. root and child order are deterministic;
7. attributes use valid keys and bounded JSON-safe values;
8. live nodes are legitimate branded instances;
9. persistence contains plain versioned records, not runtime implementation state;
10. structural mutation increments the structural revision;
11. traversal never mixes structural revisions silently;
12. edit sessions publish at most once;
13. cloned subtrees receive new domain identities while preserving internal relationship mapping;
14. inspection and conversion are pure, bounded, and non-authoritative;
15. cleanup does not depend on garbage-collection timing.

For each public operation, list which invariants it reads, may change, and must re-establish. A method with no named invariant should be questioned.

## 3. Separate representations

ObjectAtlas has at least four representations:

### Live domain representation

Branded classes, private fields, maps, arrays, and revision counters optimized for safe domain operations.

### Persistence representation

Versioned plain data that can be validated from `unknown`, encoded canonically, and migrated later.

### Diagnostic representation

Bounded custom inspection and reflection reports intended for humans. Not stable storage.

### Command/process representation

CLI tokens, textual output, and exit statuses. Not direct object state.

A common architecture failure is to use one representation for all four jobs. Spreading a class instance into JSON couples persistence to enumerable property layout. Parsing custom inspect output couples program logic to debugging. Returning mutable internal maps exposes domain authority.

Every boundary should convert deliberately.

## 4. Public API review by operation class

Review exports under these categories:

### Construction

- Which inputs are raw?
- Which factories validate?
- Can callers create a partially valid object?
- Are constructors intended for subclassing?

### Observation

- Does a getter execute effects?
- Is returned data live, copied, frozen, or read-only only in TypeScript?
- Are order and identity documented?

### Mutation

- Which object owns authority?
- Is validation complete before publication?
- Are nested references exposed?
- Which revision changes?

### Protocol

- Which operation triggers it?
- Is it pure and bounded?
- Does it leak secrets?
- Is its output stable enough for the documented use?

### Lifecycle

- Who closes, commits, rolls back, removes listeners, and releases references?
- Are terminal operations idempotent?
- What happens after failure?

### Reflection

- Which keys and descriptors are public commitments?
- Are non-configurable properties justified?
- Does a proxy need coherent alternate traps?

This review is more useful than asking whether the API is “object-oriented.”

## 5. Testing property and descriptor contracts

Tests for a public property contract should inspect descriptors:

```ts
const descriptor = Object.getOwnPropertyDescriptor(node, 'id');
assert.deepEqual(descriptor, {
  value: 'root',
  writable: false,
  enumerable: true,
  configurable: false,
});
```

Do this only for descriptors that are intentional compatibility promises. Do not freeze incidental implementation details with tests.

Also test negative operations:

- assignment to a read-only property;
- deletion of permanent properties;
- enumeration omission of hidden metadata;
- getter-safe inspection;
- no inherited attribute acceptance.

A test that checks only `node.id === 'root'` does not prove the descriptor policy.

## 6. Testing prototype and brand contracts

Prototype tests should distinguish:

```ts
node instanceof AtlasNode
Object.getPrototypeOf(node) === AtlasNode.prototype
Object.hasOwn(node, 'method')
```

Brand tests should include a counterfeit:

```ts
const counterfeit = Object.create(AtlasNode.prototype) as AtlasNode;
```

A method touching private state must reject it. This proves that prototype membership and private brand are independent.

Do not expose a method solely so tests can ask whether a private field exists. Test public behavior and known counterfeit cases.

## 7. Testing receiver and callback contracts

For any callback API:

- pass a receiver-dependent method directly and prove static or runtime rejection;
- pass an arrow adapter and prove behavior;
- test retained bound function identity if removal is supported;
- test exact invocation count and order;
- test throw propagation or translation;
- test non-retention where lifecycle depends on it.

A callback contract is incomplete if tests only cover the happy return value.

## 8. Testing iteration as a state machine

A traversal test matrix should cover:

- fresh iterators;
- one-shot iterator consumption;
- empty and singleton graphs;
- deterministic multiple-root and sibling order;
- pre-, post-, and breadth-first orders;
- early break and cleanup;
- repeated terminal `next` calls where manual iterators exist;
- structural revision changes;
- defensive cycle detection;
- large depth and width within declared limits;
- no mutable-state escape through yielded views.

Order assertions are product assertions, not cosmetic snapshots.

## 9. Testing proxy and reflection boundaries

Edit-session tests should exercise every mutation path the proxy claims to govern:

- assignment;
- `Reflect.set`;
- `Object.defineProperty`;
- `Reflect.defineProperty`;
- delete;
- own-key reflection;
- invalid keys and values;
- post-revocation access;
- direct-target isolation;
- commit and rollback terminal states;
- no live-node change before commit.

Reflection reports should be tested with an accessor that throws if invoked. This proves observation stayed at descriptor level.

## 10. Testing clone and lifecycle contracts

Subtree-clone tests should retain references to source nodes and prove:

- source live identities are unchanged;
- destination nodes are new identities;
- every source ID maps to one destination ID;
- shared relationship mapping remains consistent;
- order is preserved;
- failure publishes nothing;
- private brands are legitimate because nodes are reconstructed;
- weak caches are not copied as domain state.

Lifecycle tests should not force garbage collection. They should call explicit terminal operations and inspect observable session state and released references through supported diagnostics.

## 11. Compatibility review

Changing object mechanics can break downstream users even when TypeScript declarations still compile.

Examples:

- making an enumerable property non-enumerable changes spread and JSON behavior;
- changing a prototype method to an arrow field changes own keys and function identity;
- making a property non-configurable blocks monkey patching and test substitution;
- adding a getter can introduce effects where callers previously read data;
- changing default iteration order alters results;
- adding `Symbol.toPrimitive` changes implicit coercion;
- wrapping returns in proxies changes identity and private-field behavior;
- changing snapshots from live views to copies changes observation timing;
- tightening clone policy can reject previously accepted graphs.

A release note should describe behavior, not merely type signatures.

Course 3 will study package and TypeScript API evolution more deeply. Here the lesson is that runtime object surfaces are part of compatibility.

## 12. ObjectAtlas package architecture

The completed capstone uses:

```text
src/
├── app.ts          command orchestration and candidate publication
├── atlas.ts        graph authority and traversal
├── codec.ts        unknown → validated V1 records → live graph
├── command.ts      CLI token grammar
├── draft.ts        attribute edit sessions and proxy surface
├── errors.ts       causal error hierarchy
├── node.ts         AtlasNode and NodeId invariants
├── protocols.ts    symbols and diagnostic protocols
├── render.ts       deterministic text output
├── storage.ts      asynchronous file replacement
├── types.ts        plain record and JSON value contracts
├── index.ts        supported library surface
└── main.ts         process boundary
```

The binary does not own graph rules. The codec does not mutate an existing atlas during parsing. The node does not access files. The proxy session does not own application persistence. Each object has a bounded authority.

## 13. CLI behavior

ObjectAtlas supports:

```text
objectatlas add <id> <kind> <label> [--parent <id>]
objectatlas set <id> <key> <json-value>
objectatlas delete-attribute <id> <key>
objectatlas move <id> <new-parent|root>
objectatlas remove <id>
objectatlas clone <source-id> <new-root-id>
objectatlas show <id>
objectatlas inspect <id>
objectatlas walk [<id>] [--order preorder|postorder|breadth]
objectatlas summary
objectatlas help
objectatlas version
```

Mutation commands:

1. load and validate the complete file;
2. build a valid live graph;
3. construct one candidate transition;
4. save the candidate record;
5. return deterministic output.

Read-only commands do not rewrite storage.

## 14. Independent final change: node aliases

Implement aliases as the unseen cross-layer feature.

Requirements:

- each node may have zero or more validated aliases;
- aliases are unique across the complete atlas;
- lookup accepts ID or alias but returns the canonical node identity;
- aliases are persisted in canonical sorted order;
- `show` and `inspect` report aliases differently: domain output versus descriptor/protocol report;
- iteration order remains based on graph structure, not aliases;
- subtree clone does not copy aliases unless the caller supplies a remapping policy;
- attribute draft proxies cannot mutate aliases;
- a failed alias addition changes nothing;
- custom inspection remains bounded;
- existing V1 files without aliases remain valid through an explicit migration/default policy;
- public types and errors distinguish unknown identifier from alias collision.

This change forces the learner to preserve every prior boundary rather than inserting one array field into a class.

## 15. Final architecture defense

A complete defense answers:

### Representation

Why are live nodes classes but persisted nodes plain records?

### Identity

How do JavaScript identity, node ID, alias, prototype, and private brand differ?

### Mutation defense

Which operations are candidate-based, which mutate one owned object, and who publishes?

### Protocols

Why are iteration and inspection symbol protocols while persistence and commit remain named methods?

### Reflection defense

Which descriptors are public commitments and which metadata stays hidden?

### Lifecycle defense

Who owns iterators, edit sessions, file operations, and cached diagnostics?

### Compatibility

Which runtime changes would be breaking even without a TypeScript error?

### Simplicity

Where did the design deliberately reject a proxy, subclass, symbol, mixin, or clone mechanism because an ordinary method was better?

Mastery means giving these answers from the code and product contract, not reciting slogans.

## Common wrong models

### “The final architecture should use every feature”

Mature design uses the least powerful mechanism that preserves the requirement.

### “If tests pass, the object model is correct”

Tests need to target descriptors, receivers, identities, order, failure, and lifecycle—not only final values.

### “Persistence can use the public object shape”

Runtime representation and storage compatibility have different responsibilities.

### “A TypeScript-compatible change is runtime-compatible”

Enumeration, coercion, prototype, identity, and protocol changes can break callers without a checker error.

### “An independent change is just another command”

A real change must be traced across invariants, representations, APIs, tests, persistence, and lifecycle.

## Practice sequence

1. Create the complete runtime-object map and invariant register.
2. Audit all exports by construction, observation, mutation, protocol, lifecycle, and reflection.
3. Complete missing descriptor, brand, callback, iterator, proxy, clone, and disposal tests.
4. Complete the Object Model Audit laboratory.
5. Finish ObjectAtlas and run its complete package tests.
6. Implement node aliases without following a prepared implementation.
7. Write a compatibility note for the alias change.
8. Defend the architecture orally from the seven questions above.

## Ready to complete Course 2

You are ready only when you can modify ObjectAtlas without confusing:

- own and inherited state;
- function and receiver;
- prototype membership and private brand;
- live instance and plain record;
- symbol protocol and ordinary method;
- iterable and iterator;
- proxy and target;
- shallow copy and domain reconstruction;
- garbage collection and deterministic cleanup.

Course 3 moves from runtime object mechanics to advanced TypeScript and public library API design. The runtime distinctions from this course remain the ground truth that the type system must describe rather than replace.

## Primary references

- ECMAScript Language Specification: object internal methods, classes, symbols, iterators, proxies, weak references, and explicit resource management.
- Node.js documentation: `util.inspect`, ESM, filesystem, test runner, and process behavior used by ObjectAtlas.
- TypeScript Handbook and reference: classes, symbols, iterables, visibility, explicit `this`, and strict configuration.

## Continue

- [Workbook](workbook.md)
- [Reasoned solutions](solutions.md)
- [Laboratory 20 — Object Model Audit](../../labs/module-20-object-model-audit/README.md)
- [ObjectAtlas engineering guide](../capstone.md)
- [Final review](../final-review.md)

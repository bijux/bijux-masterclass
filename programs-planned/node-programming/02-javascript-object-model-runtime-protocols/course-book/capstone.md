# ObjectAtlas Engineering Guide

ObjectAtlas is the cumulative product for Course 2. It is a persistent component graph and runtime-model explorer. The product is deliberately object-rich, but every advanced mechanism has a narrow responsibility.

## 1. Product contract

An atlas contains nodes with:

- a stable validated ID;
- a validated kind;
- a label;
- bounded JSON-safe attributes;
- zero or one parent;
- ordered children;
- runtime-only metadata such as creation revision and custom inspection state.

The atlas owns structural authority. A node may expose read behavior and narrow internal mutation hooks, but callers cannot mutate parent/child arrays or bypass global invariants.

Core invariants:

1. IDs are valid and unique.
2. Every child reference resolves to an existing node.
3. Every non-root node has exactly one parent.
4. Parent and child relationships agree.
5. The graph is acyclic.
6. Root order and child order are deterministic.
7. Attribute keys and values satisfy the selected bounded JSON policy.
8. Live nodes are legitimate branded instances.
9. Persistence contains versioned plain records, never implementation objects.
10. Every structural mutation increments the atlas structural revision exactly once.
11. Traversal does not silently combine different structural revisions.
12. Attribute edit sessions publish at most once.
13. Subtree cloning remaps domain IDs consistently and does not preserve external mutable aliases accidentally.
14. Runtime-only symbols, descriptors, accessors, prototypes, and caches do not leak into canonical storage.

## 2. Command language

```text
objectatlas add <id> <kind> <label> [--parent <id>]
objectatlas set <id> <key> <json-value>
objectatlas delete-attribute <id> <key>
objectatlas move <id> <new-parent|root>
objectatlas remove <id>
objectatlas clone <source-id> <new-root-id>
objectatlas show <id>
objectatlas inspect <id>
objectatlas walk [id] [--order preorder|postorder|breadth]
objectatlas summary
objectatlas help
objectatlas version
```

All terminal tokens begin as strings. JSON attribute values are parsed and then checked against a bounded JSON-safe policy. `move`, `remove`, and `clone` validate a complete candidate transition before publication.

## 3. Runtime architecture

```text
terminal tokens
      ↓
command parser
      ↓
typed command
      ↓
application orchestration
      ↓
ObjectAtlas structural authority
      ↓
AtlasNode branded live instances
      ↓
plain snapshot codec
      ↓
versioned storage
      ↓
deterministic renderer / process status
```

Suggested source layout:

```text
src/
├── app.ts
├── atlas.ts
├── codec.ts
├── command.ts
├── draft.ts
├── errors.ts
├── node.ts
├── protocols.ts
├── render.ts
├── storage.ts
├── types.ts
├── index.ts
└── main.ts
```

The public library surface exports domain types, errors, safe atlas operations, and codec entry points. It does not export private mutation tokens or internal node-construction shortcuts.

## 4. Representation boundaries

### Live node

A live `AtlasNode` has private state, prototype methods, runtime symbols, and a private brand. It may expose a stable ID through a non-writable descriptor. It is not JSON data.

### Read view

A view exposes least authority. It may contain primitive fields, frozen attribute snapshots, and derived child IDs. It does not expose mutable arrays or private state.

### Persistence record

A record is a plain validated object containing only versioned domain data. Reconstructing live nodes requires a factory that establishes brands and invariants.

### Debug representation

Custom inspection may reveal descriptors, revision, parent, and child counts. It must not be reused as persistence or accepted input.

### Traversal value

A traversal may yield read views or live read-only node objects according to a documented contract. It never grants structural mutation authority.

## 5. Module-by-module construction

### Module 11 — Node property contract

Create the package and an `AtlasNode` shell. Define the stable ID with an explicit non-writable, enumerable, non-configurable descriptor or justify a different complete descriptor. Store runtime metadata under a module-local symbol and prove that ordinary enumeration and JSON omit it.

Add descriptor tests. Do not add graph mutation yet.

### Module 12 — Kind policy delegation

Define small immutable policy prototypes or explicit policy objects for node kinds. Demonstrate own overrides and inherited defaults. Persist only kind names, never prototype objects. On load, choose a legitimate policy by validated kind.

Reject policies discovered through inherited keys on untrusted input.

### Module 13 — Receiver-safe commands and factories

Introduce factories and application commands. Do not place unbound methods directly into a registry. Either wrap one operation, bind at composition time, or use receiver-independent functions. Tests must call through the same registry shape used by the CLI.

### Module 14 — Branded nodes and initialization

Replace any public mutable shell with a class containing private state. Construction validates label, kind, parent, attributes, and child state. Decoding calls a legitimate reconstruction factory; it never uses `setPrototypeOf` to forge instances.

Document initialization order and avoid constructor calls to overridable methods.

### Module 15 — Capability architecture

Separate:

- `ObjectAtlas` structural authority;
- `AtlasNode` local invariant behavior;
- codec functions;
- asynchronous store capability;
- renderer;
- clock or revision source if needed;
- CLI process shell.

Application tests replace the store and renderer independently. No service locator or global mutable registry is required.

### Module 16 — Runtime protocols

Implement a deliberate set of protocols:

- `Symbol.toStringTag` for runtime tagging;
- `Symbol.toPrimitive` only if coercion has a clear product meaning;
- `util.inspect.custom` for bounded debug output;
- `Symbol.iterator` on the atlas for default preorder traversal.

Keep user rendering, debugging, coercion, and storage distinct. Test every supported hint and fallback.

### Module 17 — Deterministic traversal

Add:

- default preorder iteration;
- named postorder traversal;
- named breadth-first traversal.

Every traversal captures the structural revision at creation. A structural change during traversal produces a typed error rather than silently mixing versions. Early close releases traversal-local state. Roots and children preserve insertion order.

### Module 18 — Transactional attribute drafts

An edit session copies one node's plain attribute record into a draft target. A revocable proxy validates get/set/delete behavior and prevents dangerous keys. Commit validates the full candidate, publishes once, increments the appropriate revision, and revokes the proxy. Rollback/dispose revokes without publication.

Do not proxy the branded node instance. Private fields and method receivers make that boundary misleading.

### Module 19 — Subtree cloning and lifecycle

Clone in three phases:

1. traverse the source subtree and allocate every new domain ID;
2. reconstruct each live node with copied approved state;
3. connect relationships using the source-to-new map.

The required root ID is supplied by the command; descendants receive deterministic derived IDs under a documented policy. External references are rejected or handled explicitly.

Edit sessions support deterministic close/dispose. Weak references, if used for optional diagnostics, do not own correctness.

### Module 20 — Complete product and independent aliases

Finish:

- canonical V1 codec;
- missing-file policy;
- same-directory temporary replacement;
- deterministic rendering;
- unit tests;
- storage tests;
- process tests;
- import/public-surface tests;
- help and version;
- architecture documentation.

Then add aliases as the independent final extension described in the final review. The supplied reference capstone is complete for the V1 contract without aliases; aliases test transfer rather than fill an unfinished implementation.

## 6. Persistence format

A canonical JSON shape is appropriate because the course is about object semantics rather than binary codecs:

```json
{
  "format": "OBJECT_ATLAS_V1",
  "revision": 3,
  "roots": ["root"],
  "nodes": [
    {
      "id": "root",
      "kind": "folder",
      "label": "Root",
      "parentId": null,
      "children": ["child"],
      "attributes": {"color": "blue"}
    }
  ]
}
```

The codec validates exact keys, types, limits, duplicate IDs, root consistency, parent/child agreement, acyclicity, and deterministic ordering. It constructs new trusted records and then legitimate live instances.

## 7. Failure and publication order

A mutating command follows:

```text
parse command
    ↓
load and validate V1 data
    ↓
reconstruct live atlas
    ↓
validate complete candidate transition
    ↓
publish in memory
    ↓
encode canonical snapshot
    ↓
save candidate file
    ↓
report success
```

The storage layer uses same-directory temporary replacement. The documentation must not overclaim crash durability or multi-process writer coordination.

## 8. Required test families

- descriptor and enumeration tests;
- prototype/receiver tests;
- private-brand reconstruction tests;
- protocol tests;
- iterator order, early close, and mutation tests;
- proxy invariant and revocation tests;
- clone identity-map tests;
- persistence round trips and malformed input;
- storage replacement failure;
- real CLI exit and output tests;
- public import surface.

## 9. Architectural non-goals

ObjectAtlas does not:

- persist class instances directly;
- use inheritance as the primary graph model;
- expose mutable child arrays;
- make symbols responsible for secrecy;
- proxy branded nodes;
- use finalizers as cleanup;
- use JSON round trips as a general clone algorithm;
- depend on a framework or third-party runtime package;
- turn every operation into a method when an ordinary function is clearer.

The capstone is successful when another reader can trace every runtime identity, property surface, protocol, mutation authority, copy boundary, and cleanup obligation without reverse-engineering hidden conventions.

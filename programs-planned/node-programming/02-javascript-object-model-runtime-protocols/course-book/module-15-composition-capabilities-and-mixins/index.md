# Module 15 — Composition, Capabilities, Mixins, and Object Architecture

> **Question:** When an object needs several independent behaviors, should those behaviors be inherited, delegated, copied, closed over, or supplied as explicit capabilities?

## Why this comes now

Modules 11–14 explained how individual objects work: properties, prototypes, calls, construction, classes, and private state. Real programs rarely consist of one isolated object. A document may be searchable, taggable, versioned, renderable, and persistable. Those dimensions do not necessarily form one inheritance tree.

JavaScript offers many composition mechanisms:

- nested collaborator objects;
- closures;
- prototype delegation;
- class inheritance;
- object spread or assignment;
- mixin functions that transform constructors;
- higher-order factories;
- capability tokens and narrow interfaces.

The hard problem is not knowing that all these mechanisms exist. It is choosing a mechanism that makes authority, state ownership, conflicts, construction, and lifecycle visible.

ObjectAtlas nodes combine identity-bearing state with optional behavior such as labeling, attributes, traversal, and inspection. The architecture must avoid a hierarchy such as `InspectableIterableCloneablePersistentFolderNode`. It should instead keep node invariants in one place and compose independent capabilities around them.

## Outcomes

By the end of this module, you can:

- distinguish inheritance, delegation, forwarding, copying, and closure composition;
- identify the authority owned by each collaborator;
- design narrow capability interfaces instead of broad “service objects”;
- use constructor injection and factory composition without service-locator ambiguity;
- apply mixin functions with explicit state and conflict policies;
- distinguish copied methods from delegated methods and shared closure state;
- prevent method-name and private-state collisions in composed designs;
- explain when inheritance is substitutable and when it is only code reuse;
- choose an architecture that keeps testing and replacement local;
- design ObjectAtlas around one invariant-bearing core plus independent adapters.

## 1. Composition is about authority, not merely reuse

Suppose a report generator needs storage and formatting:

```ts
interface Store {
  load(id: string): string;
}

interface Formatter {
  format(value: string): string;
}

class ReportService {
  constructor(
    private readonly store: Store,
    private readonly formatter: Formatter,
  ) {}

  render(id: string): string {
    return this.formatter.format(this.store.load(id));
  }
}
```

This design does more than reuse code. It states:

- `Store` owns loading behavior;
- `Formatter` owns presentation behavior;
- `ReportService` owns orchestration;
- neither collaborator receives hidden authority over the other;
- tests can replace either capability independently.

A composition review should begin with an authority map:

| Capability | Owns | Must not own |
|---|---|---|
| storage | persistence lookup | formatting policy |
| formatter | value presentation | storage lifecycle |
| orchestrator | operation order and error translation | hidden mutable copies of collaborator state |

Without that map, “composition over inheritance” can degrade into one object containing every dependency in the process.

## 2. Nested composition makes dependencies explicit

A composed object can own collaborators as fields:

```ts
class SearchIndex {
  #tokens = new Map<string, Set<string>>();

  add(id: string, text: string): void {
    // update the index
  }

  find(query: string): readonly string[] {
    return [...(this.#tokens.get(query) ?? [])].sort();
  }
}

class Catalog {
  constructor(private readonly index: SearchIndex) {}
}
```

The public object chooses when to call the collaborator. The collaborator can have its own private state and lifecycle.

This differs from inheritance:

```ts
class Catalog extends SearchIndex {}
```

The inherited version claims a catalog *is a* search index and exposes search-index operations as catalog operations. It also couples construction and protected behavior. If the product relation is “catalog uses an index,” composition is more accurate.

## 3. Forwarding is an API decision

A composed object may forward selected operations:

```ts
class Catalog {
  constructor(private readonly index: SearchIndex) {}

  search(query: string): readonly string[] {
    return this.index.find(query);
  }
}
```

Forwarding is not free boilerplate. It decides:

- which collaborator capabilities become public;
- how errors are translated;
- whether results are copied, normalized, or filtered;
- whether future collaborator changes affect the public API.

Do not expose the collaborator object only to avoid writing forwarding methods:

```ts
// Weak boundary: callers now own search-index lifetime and mutation authority.
get searchIndex(): SearchIndex {
  return this.index;
}
```

Expose the minimum capability the caller needs.

## 4. Capability objects can be smaller than classes

A capability is a value that grants a narrow operation:

```ts
interface Clock {
  now(): number;
}

interface IdSource {
  next(): string;
}
```

Capabilities can be plain objects:

```ts
const systemClock: Clock = {
  now: () => Date.now(),
};
```

They need not inherit from a framework base class or carry unrelated methods. Narrow capability objects improve testability because a fake must implement only the actual dependency.

The danger is constructing one broad environment object:

```ts
interface Environment {
  clock: Clock;
  filesystem: unknown;
  logger: unknown;
  config: unknown;
  network: unknown;
  metrics: unknown;
}
```

Passing that everywhere hides authority. Prefer function- or component-specific capability bundles.

## 5. Closure composition owns private state without class identity

A factory can close over state:

```ts
interface Counter {
  increment(): number;
  read(): number;
}

function createCounter(): Counter {
  let value = 0;
  return {
    increment(): number {
      value += 1;
      return value;
    },
    read(): number {
      return value;
    },
  };
}
```

The closure provides runtime privacy. There is no shared prototype method and no `instanceof` relationship. Each factory call creates new method functions and a new lexical environment.

Use closure factories when:

- a small stateful capability needs no public class identity;
- construction is naturally a function;
- private state should be inaccessible without class machinery;
- method sharing across very many instances is not a concern.

Use a class when instance identity, shared prototype methods, private brands, static factories, or extension policies make the class surface clearer.

## 6. Copying methods is not delegation

Object spread can copy method-valued properties:

```ts
const searchable = {
  search(query: string): readonly string[] {
    return [query];
  },
};

const component = {
  ...searchable,
  id: 'c1',
};
```

The resulting object owns a `search` data property whose value is the same function object. Future changes to `searchable.search` do not affect `component.search`. Descriptor flags are normalized by spread. Accessors would be executed and replaced with values.

Delegation keeps lookup linked:

```ts
const delegated = Object.create(searchable) as {
  id: string;
  search(query: string): readonly string[];
};
delegated.id = 'c1';
```

Nested composition calls through an explicit field. These are three distinct architectures. Do not describe all of them as “mixing in behavior.”

## 7. Mixins transform a base constructor

A class mixin is often written as a function that accepts a constructor and returns a derived class:

```ts
type Constructor<T = object> = abstract new (...args: never[]) => T;

function WithTimestamp<TBase extends Constructor>(Base: TBase) {
  abstract class Timestamped extends Base {
    readonly createdAt = Date.now();
  }

  return Timestamped;
}
```

Real constructor typing often needs to preserve argument tuples and instance types more carefully. Course 3 studies advanced generic typing. Here the runtime questions are primary:

- which constructor runs first;
- where each field initializes;
- whether the mixin assumes base methods or state;
- whether two mixins define the same name;
- whether private fields are distinct;
- whether application order changes behavior;
- whether the resulting hierarchy remains understandable.

Mixins are appropriate when behavior truly needs class participation—such as lifecycle hooks tied to construction—and multiple independent class capabilities must be combined. They are weak when object composition would be simpler.

## 8. Mixin order and collision policy must be explicit

Suppose two mixins define `describe()`:

```ts
const Mixed = WithAudit(WithLabel(Base));
```

Which method wins depends on the returned class chain and whether methods call `super`. Reversing mixin order may change semantics.

A publishable mixin system needs:

- a documented application order;
- a rule for duplicate public names;
- a rule for constructor arguments;
- a rule for lifecycle hooks;
- tests for super-call composition;
- no reliance on class-name strings;
- no requirement to reach another mixin’s private fields.

If you cannot write this policy concisely, use explicit collaborators.

## 9. Private fields avoid accidental name collision but not semantic collision

Two mixins can each declare `#state`; the private names are distinct. That prevents storage collision. They may still conflict semantically:

- both may expose `reset()` with different meanings;
- both may register global listeners;
- both may assume ownership of `close()`;
- both may mutate shared base state;
- both may define incompatible initialization order.

Private names solve one namespace problem. They do not solve architecture.

## 10. `Object.assign`-style mixins have descriptor and receiver consequences

A common mixin copies methods from source prototypes:

```ts
function copyMethods(target: object, source: object): void {
  for (const key of Reflect.ownKeys(source)) {
    if (key === 'constructor') {
      continue;
    }
    const descriptor = Object.getOwnPropertyDescriptor(source, key);
    if (descriptor !== undefined) {
      Object.defineProperty(target, key, descriptor);
    }
  }
}
```

This preserves descriptors better than `Object.assign`, but it still copies behavior into one prototype. It does not establish a delegation link. It must define collision policy and may copy methods that expect source-specific private brands.

Never copy private-field methods from one class prototype onto unrelated instances. The method’s private names remain branded to the declaring class and will fail on foreign receivers.

## 11. Structural typing can hide runtime capability differences

TypeScript may accept two values with the same public shape:

```ts
interface Describable {
  describe(): string;
}
```

A class instance, object literal, proxy, and bound adapter may all satisfy that interface. Runtime differences remain:

- prototype and constructor;
- private brand;
- property descriptors;
- method identity;
- getter effects;
- proxy traps;
- disposal requirements.

Structural compatibility is useful, but it is not a promise that runtime object mechanics are identical. Public APIs should depend only on the behavior they actually require.

## 12. Capability security and least authority

A capability object can enforce least authority by simply not containing unrelated operations.

```ts
interface AttributeReader {
  get(name: string): unknown;
}

function renderNode(reader: AttributeReader): string {
  return String(reader.get('label'));
}
```

The renderer cannot mutate attributes if it never receives a mutation capability.

This is stronger than passing the entire `AtlasNode` and relying on convention. TypeScript’s readonly views help statically, but a narrow runtime wrapper or closure can also prevent access to mutating methods.

Use capability design for plugin and callback boundaries. It narrows the damage from mistakes and makes the contract easier to test.

## 13. Avoid service locators and ambient registries

A service locator hides dependency acquisition:

```ts
const globalServices = new Map<string, unknown>();
```

Any component can ask for anything by name. Consequences include:

- runtime key errors;
- hidden construction order;
- tests that modify global state;
- unclear ownership and disposal;
- broad accidental authority.

Constructor or factory injection makes requirements visible. Module-level singletons can be appropriate for immutable constants or process-wide platform facts, but mutable registries require explicit lifecycle and isolation policy.

ObjectAtlas keeps its node-kind policy registry inside each atlas instance. Separate atlases can coexist in one process without sharing registrations unless a caller deliberately shares a registry capability.

## 14. Composition and failure atomicity

When several capabilities participate in one operation, decide where candidate state and commit authority live.

```ts
class AtlasApplication {
  constructor(
    private readonly atlas: ObjectAtlas,
    private readonly store: AtlasStore,
  ) {}

  async rename(id: string, label: string): Promise<void> {
    const candidate = this.atlas.withRenamedNode(id, label);
    await this.store.save(candidate.toRecord());
    this.atlas.replaceWith(candidate);
  }
}
```

This sketch makes persistence order and in-memory publication explicit. Depending on the product, another authority may own the commit. The key is that collaborators do not each mutate hidden state and hope the overall operation succeeds.

Composition without transaction ownership can increase partial failure. Name the orchestrator responsible for cross-capability invariants.

## 15. ObjectAtlas increment

Refactor ObjectAtlas into clear responsibilities:

- `AtlasNode` owns one node’s invariants;
- `ObjectAtlas` owns graph membership, parent-child consistency, ordering, and identifier uniqueness;
- `AtlasCodec` converts between validated plain records and live instances;
- `AtlasStore` owns asynchronous file replacement;
- renderers receive read-only capability views;
- traversal remains a graph capability, not a subclass family;
- node kinds are represented by data plus policy objects, not one subclass per kind.

Add tests proving that:

- two atlas instances do not share registries or graph state;
- a renderer cannot mutate the atlas through its supplied capability;
- replacing a formatter does not change graph invariants;
- a failed composed operation does not publish partial state;
- method copying is not used to simulate multiple inheritance.

## Common wrong models

### “Composition means putting every service in one object”

Good composition assigns narrow authority and explicit orchestration.

### “Inheritance is needed for method reuse”

Prototype methods, collaborators, factories, and closures can share behavior without promising substitutability.

### “Object spread adds a capability”

It copies enumerable values and normalizes descriptors. It does not preserve a live delegation relationship.

### “Mixins solve multiple inheritance”

They introduce order, collision, construction, and lifecycle policies that must be designed explicitly.

### “Private fields make mixed behaviors independent”

They prevent private-name collision, not semantic conflict.

### “Structural typing proves runtime equivalence”

It proves compatibility with the required public type, not identical prototype, descriptor, brand, or lifecycle behavior.

## Practice sequence

1. Build an authority map for a three-component service.
2. Refactor a false inheritance relation into composition.
3. Compare closure factory, class, prototype delegation, and copied methods for one stateful capability.
4. Build two mixins with a deliberate method conflict and define a resolution policy.
5. Narrow a broad dependency to a least-authority capability.
6. Complete the Capability-Composed Document laboratory.
7. Refactor ObjectAtlas into node, graph, codec, store, and renderer responsibilities.
8. Defend one place where inheritance would be legal but composition is still clearer.

## Ready to continue

Continue when you can answer, for every collaborator:

- what state it owns;
- what operations it authorizes;
- whether behavior is copied, delegated, or forwarded;
- who constructs and disposes it;
- who coordinates multi-component failure;
- what conflicts can occur when behaviors are combined.

Module 16 studies symbols and standardized runtime protocols. Those protocols are another form of composition: an object opts into behavior by exposing a well-known symbol-keyed operation.

## Primary references

- ECMAScript Language Specification: ordinary objects, class inheritance, property definition, and symbol-keyed methods.
- TypeScript Handbook: classes, interfaces, constructor types, mixins, and structural compatibility.
- Node.js design conventions for explicit dependencies and avoiding import-time global mutation.

## Continue

- [Workbook](workbook.md)
- [Reasoned solutions](solutions.md)
- [Laboratory 15 — Capability-Composed Document](../../labs/module-15-capability-composed-document/README.md)
- [ObjectAtlas engineering guide](../capstone.md)

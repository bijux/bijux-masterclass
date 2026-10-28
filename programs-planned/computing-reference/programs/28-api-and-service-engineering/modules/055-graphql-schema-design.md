---
module_id: API-055
program: API & Service Engineering
level: 2
module_number: 55
title: GraphQL Schema Design
status: complete
last_verified: 2026-09-02
---

# GraphQL Schema Design

## One-Page Review

### Governing question

How should a GraphQL schema expose a stable domain capability graph that lets clients select useful data without mirroring storage, hiding business semantics in generic scalars, or making ordinary evolution unexpectedly break existing operations?

### Essential definitions

- A **schema** is the type system and root operation contract against which GraphQL documents are validated and executed.
- An **object type** exposes named fields; each field defines an output type and may define typed arguments.
- An **input object** groups named input fields for arguments and mutations; it is never an output type.
- A **non-null type** `T!` excludes `null`; a **list type** `[T]` describes an ordered collection and can combine independently with non-null at the list and element layers.
- An **interface** defines fields shared by implementing object types; a **union** names a set of possible object types without common fields.
- A **domain capability graph** organizes fields around stable user and business operations rather than tables, joins, or internal services.
- A **schema coordinate** identifies a schema element such as `Type.field` or `Type.field(argument:)` for governance and tooling.
- **deprecation** marks a field, argument, input field, or enum value as discouraged while retaining it for compatible clients.
- A **breaking change** can make a previously valid operation invalid or change its promised meaning incompatibly.

### Central model, mechanism, or theorem

Let $S$ be a schema, $O$ a previously accepted operation, and $V(S,O)$ GraphQL validation. A syntactically backward-compatible evolution must preserve

$$
V(S_{old},O)=valid\Rightarrow V(S_{new},O)=valid
$$

for supported operations $O$. Validation preservation is necessary but not sufficient: field meaning, authorization expectations, identifiers, ordering, null/error behavior, and side effects must also remain compatible.

Nullability composes structurally. `T`, `T!`, `[T]`, `[T!]`, `[T]!`, and `[T!]!` are distinct contracts. Strengthening an output from `T` to `T!` is usually validation-compatible but requires evidence that every execution path can uphold it; strengthening an input from `T` to `T!` rejects callers that omit or pass null and is breaking.

### Critical invariants

The schema names domain concepts and capabilities, not persistence tables or backend topology. Query fields are observational; mutations communicate domain commands and return typed payloads with stable identifiers and actionable results. Root fields are cohesive and discoverable. Every field, argument, input, enum, interface, and union has one durable semantic owner. Input and output types remain separate. IDs are opaque and stable within a documented scope; clients never decode them. Nullability reflects a promise, not optimism. List ordering, emptiness, duplicates, and element-null rules are explicit. Enums represent closed client-relevant sets; open-ended values use another governed representation. Interfaces and unions model real polymorphism with stable type resolution. Generic JSON scalars are exceptional, narrow, versioned, bounded, and documented. Descriptions are first-class contract text. Deprecated elements state a reason and migration path and remain through a measured support window. Evolution is checked against registered/observed operations and semantic invariants, not schema diff labels alone.

### Common failures

Generating one type per database table; exposing foreign keys and joins; naming root fields after services; a single `node(id:)` or `search` entry point with untyped blobs; separate near-duplicate mobile and web schemas; using output objects as inputs; accepting arbitrary JSON for convenience; nullable-everything schemas; promising non-null before dependencies can uphold it; confusing `[T!]!` with `[T]!`; returning `null` for hidden, absent, failed, and unauthorized without a contract; enum values copied from mutable internal states; numeric IDs clients can enumerate or decode; unstable union membership; mutation booleans without resource or error detail; mutation names such as `updateThing` that hide intent; adding required arguments/input fields without defaults; removing deprecated fields before usage drains; changing field meaning while preserving its type; aliasing old and new fields to inconsistent data; undocumented ordering; descriptions that repeat names; inconsistent casing; and treating introspection or generated documentation as sufficient governance.

### Compact example

An internal `orders` table has `customer_fk`, `state_code`, and nullable `shipment_fk`. The public schema exposes `Order.customer`, a client-relevant `OrderStatus` enum, and nullable `Order.shipment` because shipment is absent before dispatch. `cancelOrder(input: CancelOrderInput!): CancelOrderPayload!` expresses intent and returns the order, a stable operation ID, and typed user-facing problems. Adding an optional `reason` input is compatible; making it required immediately is not. **Conclusion:** model domain promises and commands, then evolve them against actual client operations.

### Connections

[Deadlines, Cancellation, and Metadata](054-deadlines-cancellation-and-metadata.md) bounds call context. [Resources, Representations, and Messages](001-resources-representations-and-messages.md) and [Error Translation](035-error-translation.md) supply durable domain and failure concepts. Resolver execution and batching belong to the next module; pagination and incremental delivery, then authorization and cost control, follow separately.

## Governing Question

Which domain capabilities deserve stable GraphQL fields, what exact value and nullability contracts do they promise, and how can the schema evolve without invalidating or semantically surprising the supported operation population?

## Why This Matters

GraphQL moves response selection from server endpoints into client operations, but it does not remove API design. The schema becomes a shared language between many clients and an execution system. A weak schema merely relocates coupling: table-shaped types expose storage migrations, generic JSON shifts validation to every consumer, and nullable-everything makes generated types nearly useless. A strong schema concentrates semantics so validation, tooling, documentation, governance, and client compilation can help.

The danger grows with success. Clients may persist operations for years, fragments spread across applications, and fields acquire meanings that are not visible in their GraphQL type. Removing a field is clearly breaking, but changing an ordering rule, identifier scope, authorization behavior, enum interpretation, or nullability behavior can be equally disruptive. Schema design therefore combines domain modeling, type theory, compatibility policy, and operational evidence.

This module treats the schema as a public capability graph. It covers type and root design, nullability, polymorphism, mutation shapes, descriptions, deprecation, and compatibility. It deliberately does not teach resolver scheduling/batching, connection execution, incremental transport, or authorization/cost enforcement; those require their own mechanisms and evidence.

## Prerequisites and Retrieval

Retrieve [Resources, Representations, and Messages](001-resources-representations-and-messages.md), [API Contracts and Behavioral Guarantees](021-api-contracts-and-behavioral-guarantees.md), [Reusable Schema Components](026-reusable-schema-components.md), and [Error Translation](035-error-translation.md). Be able to distinguish domain identity from storage keys, input validation from output guarantees, syntactic compatibility from semantic compatibility, and API absence from execution failure. Familiarity with GraphQL documents, variables, fragments, and introspection is useful but not assumed.

## Learning Objectives

After completing this module, you can:

1. derive a GraphQL capability graph from domain language rather than database or service topology;
2. choose object, scalar, enum, input object, interface, union, list, and non-null types with explicit semantics;
3. design root query and mutation fields that remain cohesive, discoverable, and evolvable;
4. reason precisely about list and element nullability, error propagation, and absence;
5. create stable opaque identity, typed mutation payload, and input patterns;
6. distinguish safe-looking schema edits from validation-breaking or semantic-breaking changes;
7. govern descriptions, schema coordinates, deprecations, and support windows;
8. test evolution against real operations and domain invariants; and
9. identify where resolver, pagination, delivery, authorization, and cost concerns leave schema design and enter later modules.

## Core Exposition

### Start from capabilities and domain language

Begin with the questions and commands users are authorized to perform: view an order, compare products, submit a claim, approve an invoice, or cancel a shipment. Identify stable domain entities, value objects, relationships, state transitions, and result concepts. Only then choose GraphQL names and shapes.

A table-shaped schema leaks normalization, foreign keys, junction tables, nullable migration columns, and row ownership. A service-shaped schema leaks present deployment boundaries. Both force clients to understand implementation details that the API owner should be free to change. The public graph may aggregate several stores or services behind one domain field; conversely, one table may support several capabilities with different authorization and semantic rules.

Prefer nouns for object/value concepts and verbs with explicit intent for commands. `Order.customer` is more durable than `Order.customerRow`; `approveInvoice` is clearer than `updateInvoice(status: APPROVED)`. The latter lets clients request illegal state transitions, obscures authorization, and makes audit intent harder to recover.

Root fields form the schema's entry vocabulary. A query root is required by the specification; mutation and subscription roots are optional and must be distinct object types when present. Keep root fields cohesive. Namespacing everything under backend teams makes organizational structure part of the contract. A domain namespace can be justified when it resolves genuine naming/ownership boundaries, but it adds traversal and null/error semantics.

### Choose named types by contract role

GraphQL defines scalar, object, interface, union, enum, and input-object named types, plus list and non-null wrapping types. Each carries a different promise.

Use scalars for atomic serialized values with stable parse/serialize rules. Built-ins cover `Int`, `Float`, `String`, `Boolean`, and `ID`. Define a custom scalar only with a published lexical/semantic contract, examples, bounds, and interoperable client mapping. `DateTime` needs timezone/offset, precision, normalization, and leap/invalid rules; `Money` is usually not atomic because amount and currency have independent structure.

Use enums for a closed client-relevant set where each value has durable meaning. Adding an enum value can break clients that exhaustively switch despite remaining schema-valid, so evolution policy and generated-client behavior matter. Do not copy an internal state machine wholesale. If providers can introduce unknown values independently, expose a governed string/code object or a stable coarse enum plus details.

Use object types for selectable output fields. Use input objects for named input structure. GraphQL intentionally separates input and output positions: output fields can have arguments and recursive selection; input fields are supplied values. Even when shapes look alike today, separate types let their semantics evolve independently.

Use interfaces when consumers benefit from shared selectable fields across implementing objects, such as `Node { id: ID! }` or `PricedItem`. Use unions when alternatives share no justified common field. Every possible runtime object must resolve consistently, and clients need a stable discriminant through `__typename`. Avoid a union merely to avoid naming a result or error contract.

The September 2025 specification includes one-of input objects through `@oneOf`: exactly one field must be supplied and non-null, while fields themselves are nullable and have no defaults. This can model exclusive alternatives more clearly than several optional fields, but client/toolchain support and rollout compatibility must be verified before adoption.

### Treat nullability as a composed promise

GraphQL defaults to nullable. Non-null wraps another type and changes both validation and execution behavior. For a field `T!`, returning null produces an execution error and propagates null to the nearest nullable ancestor; a deep optimistic non-null can therefore erase a larger response subtree.

Lists have two independent questions: can the list be null, and can an element be null?

- `[T]` permits null list and null elements.
- `[T!]` permits null list but excludes null elements when a list exists.
- `[T]!` promises a list but permits null elements.
- `[T!]!` promises a list and non-null elements.

Empty list is not null. Ordering and duplicate semantics are not encoded by the type and must be described. Use non-null only when the domain and every resolver/dependency path can uphold it under partial failure and authorization rules. Prefer an empty non-null list for a successfully evaluated collection with no members; reserve null for a distinct specified state.

Input nullability reverses some evolution intuition. Adding an optional argument/input field is generally validation-compatible. Adding a required field without a default rejects existing variable objects. Changing an optional argument to required is breaking. Removing non-null from an input can be schema-compatible for old callers but requires the implementation to define new null/omission meaning. Omitted and explicit null may be distinct; preserve that distinction where patch semantics need it.

### Design identities and references

`ID` signals an identifier serialized like a string, not secrecy or global uniqueness. Define the scope: unique within a type, tenant, graph, or time window. Opaque means clients compare, store, and return it but never decode routing, database, type, tenant, or authorization facts from it.

Global object identification can support normalized client caches and a `node(id:)` entry field. It is not mandatory for every graph, and a global ID must still enforce authorization. If IDs embed type or shard data, treat the encoding as server-private and provide migration/alias rules. Never authorize based on an unverified ID prefix.

Natural keys may be useful lookup arguments when stable and public, but do not make them the only durable identity if they can change. Model alternate identifiers explicitly and avoid ambiguous `id` arguments whose accepted scope varies by field.

### Shape queries for discoverability and bounded meaning

Field names should reveal one stable semantic operation. Prefer `order(id:)`, `orders(filter:)`, and `viewer` to a generic `get(type:, key:)`. Group related arguments into an input when they evolve together or exceed a small stable set. Avoid an options object that accepts arbitrary keys.

The schema type alone does not define ordering, case sensitivity, timezone, locale, consistency, freshness, or whether hidden records look absent. Descriptions must. Arguments need defaults only when the default is durable and observable. A default embedded in the schema becomes contract; changing it can alter old operations that omitted the argument.

Filtering and sorting inputs should name supported predicates and order keys. They should not expose SQL fragments, unrestricted field strings, or arbitrary expression trees. Pagination shape and execution are handled later, but the schema must not promise an unbounded list where cardinality is large.

Aliases and fragments are client document features, not separate server fields. Do not add synonyms solely for client naming preferences. Let clients alias a stable field, while server-side renames use an explicit deprecated transition when semantics genuinely improve.

### Model mutations as domain commands

A mutation root field should express one authorized intent: `cancelOrder`, `approveInvoice`, or `changeShippingAddress`. Its input object conventionally carries command fields and can include an idempotency/operation identity when retries matter. Keep authentication context outside domain input, but keep tenant/resource identifiers inside typed input when they affect the command and bind them to authenticated identity during authorization.

Return a non-null payload type rather than a bare Boolean. A useful payload can include the affected resource or edge, stable operation ID, domain result, and bounded typed user-facing problems. Transport/execution errors and domain rejections are different layers. Whether errors use unions, interfaces, or payload fields is a graph-wide policy; consistency matters more than fashion.

Do not expose `updateThing(input: JSON!)` or a universal CRUD mutation. Generic patches make illegal combinations representable, blur omitted versus null, and couple clients to storage fields. Intent-specific inputs give validation, authorization, audit, idempotency, and evolution clear ownership.

<!-- bijux-verify: {"id":"graphql-schema-shape","mode":"schematic","language":"graphql","toolchain":"none","reason":"The block illustrates an SDL contract for design review and is not an executable document in the repository."} -->
```graphql
interface Node {
  id: ID!
}

type Order implements Node {
  id: ID!
  status: OrderStatus!
  shipment: Shipment
}

enum OrderStatus {
  PENDING
  CONFIRMED
  DISPATCHED
  CANCELLED
}

input CancelOrderInput {
  orderId: ID!
  reason: String
  operationId: ID!
}

type CancelOrderPayload {
  order: Order
  operationId: ID!
  problems: [UserProblem!]!
}

type Query {
  order(id: ID!): Order
}

type Mutation {
  cancelOrder(input: CancelOrderInput!): CancelOrderPayload!
}
```

This shape still needs written contracts: why `order` or `shipment` may be null, whether a hidden order appears absent, reason bounds, idempotency scope, allowed state transitions, problem taxonomy, and enum evolution policy.

### Write descriptions as normative contract text

GraphQL descriptions are first-class schema elements and support CommonMark. Describe meaning, units, formats, identity scope, ordering, null conditions, authorization-sensitive absence, side effects, consistency/freshness, limits, defaults, and deprecation migration. Do not merely restate `createdAt: DateTime!` as “the created at.”

Examples belong in docs/tests when SDL cannot encode them. Custom directives can attach machine-readable policy, but every directive needs a stable definition, locations, ownership, composition behavior, and tooling support. Do not make clients infer essential semantics from a vendor directive they cannot see or understand.

Schema coordinates provide stable review vocabulary: `Order.status`, `Query.order(id:)`, or `@deprecated(reason:)`. Use them in ownership registries, change proposals, telemetry, allowlists, and incident reports. Coordinates identify elements; they do not version field meaning automatically.

### Evolve with validation and semantic evidence

Classify changes by position and client behavior. Removing or renaming a field/type, changing a field's output type incompatibly, adding a required argument, or adding a required input field without a default breaks validation. Changing a nullable output to non-null may preserve validation but can increase runtime null propagation if the promise is false. Changing non-null output to nullable can invalidate client variable/type assumptions and generated code expectations. Adding an enum value or union/interface possible type may surprise exhaustive clients even when GraphQL validation succeeds.

Adding a field is normally safe because clients select explicitly. Yet semantic changes can hide in “safe” diffs: change sort order, broaden/narrow results, alter currency units, reinterpret timestamps, change absent-versus-forbidden behavior, or route an old field to inconsistent data. Compatibility review must include descriptions and invariants.

Deprecate before removal. The reason should name the replacement and any semantic difference. Publish a support policy, measure field/argument/enum usage from parsed operations, identify client owners, migrate persisted operations, and wait through the required window. Introspection shows deprecation, but it does not prove clients saw it.

Validate against a corpus of supported operations. Static schema-diff tools are useful gates, not truth: they cannot know dynamic document construction, dormant clients, out-of-band consumers, or semantic expectations. Production operation telemetry needs privacy controls, normalization, retention, and owner mapping.

### Compute a compatibility classification explicitly

Represent a change by its position, edit, and supporting evidence. The following executable model is intentionally conservative: it calls required input additions and removals breaking, treats output strengthening and enum additions as requiring semantic/client evidence, and recognizes optional additions as generally compatible.

<!-- bijux-verify: {"id":"graphql-change-classification","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"add optional argument: compatible\nadd required input field: breaking\nstrengthen output nullability: evidence-required\nadd enum value: evidence-required\nremove field: breaking\n","stderr":""}} -->
```python
def classify(position, edit, required=False):
    if edit in {"remove", "rename"}:
        return "breaking"
    if position in {"argument", "input-field"} and edit == "add":
        return "breaking" if required else "compatible"
    if position == "output" and edit == "make-non-null":
        return "evidence-required"
    if position in {"enum", "union"} and edit == "add-member":
        return "evidence-required"
    if edit == "add":
        return "compatible"
    return "evidence-required"

cases = [
    ("add optional argument", "argument", "add", False),
    ("add required input field", "input-field", "add", True),
    ("strengthen output nullability", "output", "make-non-null", False),
    ("add enum value", "enum", "add-member", False),
    ("remove field", "output", "remove", False),
]
for label, position, edit, required in cases:
    print(label + ": " + classify(position, edit, required))
```

Real governance also checks defaults, descriptions, operation corpus, generated clients, runtime data, and support policy. A classifier cannot approve semantic compatibility.

### Govern schema ownership without fragmenting the graph

Assign every coordinate to a durable domain owner with reviewers and service objectives. Ownership answers who defines meaning and approves evolution, not necessarily which process resolves the field. In composed/federated graphs, composition rules, entity keys, field ownership, and cross-subgraph failures add constraints; the public schema must still feel coherent.

Avoid duplicate types/fields for each channel, backend, or team. Different authorization or latency needs can sometimes justify separate capabilities, but name them by semantic promise. A graph-wide naming, pagination, error, scalar, deprecation, and identity policy reduces client surprise.

Run lint/schema checks in CI, compare proposed schema, validate registered operations, review semantic descriptions, and canary execution. Track field usage and error/null rates by coordinate without high-cardinality or sensitive labels. A schema registry is evidence infrastructure, not the owner of meaning.

### Verify the contract at several layers

Schema tests parse and validate SDL, enforce naming/descriptions/directives, and diff against the accepted graph. Operation tests validate representative documents and generated client types. Contract tests execute null, absence, authorization, enum, interface/union, default, and mutation outcomes. Property tests can exercise scalar round trips and invalid values.

Adversarial cases include omitted versus explicit null; empty versus null list; null element at every wrapper; unknown enum input; new enum output against old exhaustive clients; impossible runtime type; malformed custom scalar; cross-tenant opaque ID; deprecated field through aliases/fragments; concurrent old/new writes; partial dependency failure; and schema composition conflict.

Observe actual operations before removal, but account for sampling gaps, persisted-operation registries, batch jobs, offline clients, and environments absent from telemetry. Rehearse rollback: restoring SDL without restoring old semantics or data is not a rollback.

## Definitions and Notation

Let $S$ be a GraphQL schema, $O$ an operation document plus variable definitions, and $V(S,O)$ its static validation result. Let $E(S,O,d,a)$ be execution under data state $d$ and authenticated actor $a$. Let $C$ be the supported operation corpus and $I_f$ the documented invariant set for schema coordinate $f$.

For an output position, `T!` is a server promise not to complete that field as null; violation raises an execution error and propagates null to the nearest nullable ancestor. For an input position, `T!` requires a non-null supplied/coerced value subject to default rules. `[]` is a present empty list; `null` is absence. Omission $\bot$ can differ from explicit null in input objects.

Define syntactic compatibility over $C$ as $\forall O\in C: V(S_{old},O)=valid\Rightarrow V(S_{new},O)=valid$. Define semantic compatibility as preservation of every promised $I_f$ observed by $O$ under its supported states/actors. The second cannot be established by SDL comparison alone.

## Mechanisms, Invariants, or Proof Structure

GraphQL validates selections against named and wrapping types before execution. Adding an unselected output field does not alter an existing selection, so it ordinarily preserves validation. Removing a selected field makes the operation invalid. Adding a required argument to a selected field makes an old invocation without it invalid. Thus compatibility depends on edit and type position, not merely whether text was added.

Null wrappers compose. If a resolver for `child: T!` produces null, the field error cannot be represented at `child`; execution substitutes null at its parent selection. If that parent field is also non-null, propagation continues. Therefore stronger non-null deep in a chain increases the possible blast radius. The type gives a guarantee only if implementation and dependencies uphold it.

Validation preservation is not semantic preservation. Construct a schema edit that leaves `price: Int!` unchanged but changes cents to whole currency units. Every old operation remains valid, yet values differ by a factor of 100 and violate the documented unit invariant. Therefore schema diff success is necessary evidence, never sufficient proof of compatibility.

Opaque IDs prevent contractual decoding but not guessing, leakage, or authorization failure. Authorization must bind authenticated actor, action, and resolved resource. A field returning null for both absent and forbidden can reduce existence leakage only if timing, errors, sibling fields, caches, and logs uphold the same policy.

## Alternatives and Trade-Offs

Nullable fields permit partial responses and easier evolution but shift absence/error handling to clients. Non-null improves generated types and expresses confidence but magnifies resolver defects and dependency failures. Choose by domain promise and measured execution, not a blanket rule.

Interfaces expose shared selectable fields and enable reusable fragments; unions preserve distinct alternatives without inventing a weak common abstraction. Interfaces create a stronger long-lived contract. Unions require per-type fragments. A result object is often simpler when alternatives are status/data fields rather than genuinely different object identities.

Enums improve validation, documentation, and generated types for closed sets. Strings or code/detail objects tolerate independently evolving/open sets but lose exhaustiveness and need explicit validation. A coarse stable enum plus raw provider code can isolate volatility, subject to privacy and bounds.

Intent-specific mutations provide strong authorization and audit semantics but create more fields/types. Generic CRUD or JSON patches reduce initial SDL size but export invalid state combinations and storage coupling. The extra explicit schema is usually the durable choice.

A global `Node` interface and `node(id:)` aid normalized caches and generic tooling. Domain-specific lookup fields can be clearer, better authorized, and easier to constrain. They can coexist if identity semantics and behavior agree.

One graph improves discovery and composition for clients; separate graphs can enforce organizational, trust, or lifecycle boundaries. Federation/composition can unify ownership while adding entity-key, planning, availability, and governance complexity. The public contract, not organizational fashion, should decide.

## Failure Modes and Misconceptions

- **“GraphQL means clients can query anything.”** Clients select only exposed fields and valid combinations; schema, authorization, and cost policy remain server-owned.
- **“The database schema is already typed.”** Storage types encode persistence constraints, not public domain meaning, authorization, compatibility, or task-oriented capabilities.
- **“Nullable means optional.”** Output nullability describes response representation/error propagation; input omission and explicit null have distinct coercion/patch semantics.
- **“Adding is always safe.”** Required inputs break validation, and enum/union additions or changed defaults/meaning can break client behavior.
- **“Non-null is better documentation.”** It is an executable promise; unjustified non-null turns a local absence into wider response loss.
- **“ID is secure and globally unique.”** `ID` is a serialization/type signal. Scope, opacity, authorization, retention, and aliasing require separate contracts.
- **“JSON is flexible evolution.”** It removes field-level validation, discoverability, generated types, compatibility analysis, and precise ownership.
- **“Deprecation removes the field.”** It only advertises discouragement; removal needs usage evidence, owner migration, policy, and elapsed support window.
- **“Introspection is documentation.”** It exposes structure and descriptions but cannot replace examples, invariants, migration guidance, or operational policy.
- **“A passing schema diff proves compatibility.”** It misses units, ordering, null causes, side effects, authorization, defaults, and client exhaustiveness.
- **“Every failure should be a union member.”** Transport/execution faults, programmer faults, and expected domain outcomes have different owners and retry semantics.
- **“Federation fixes schema ownership.”** It distributes implementation ownership; semantic coherence and change governance still require explicit decisions.

## Worked Examples

### Example 1

**Situation:** A team exposes `CustomerRow { customer_fk, segment_code }`. **Reasoning:** names leak relational storage and force clients to join meaning. Expose `Customer { id, segment }` with an owned enum/description and resolve storage internally. **Conclusion:** public types model domain concepts, not rows.

### Example 2

**Situation:** `Order.shipment: Shipment!` is queried before dispatch. **Reasoning:** absence is valid, so the resolver violates non-null and may null the entire order. Make shipment nullable and document pre-dispatch absence, or model a non-null shipment-state value if that is the real invariant. **Conclusion:** nullability follows domain truth.

### Example 3

**Situation:** `items: [Item]!` returns `[item, null]`. **Reasoning:** the list is promised present, elements are nullable. If clients require every element, use `[Item!]!` only after proving all paths uphold it. **Conclusion:** list and element promises are independent.

### Example 4

**Situation:** A mutation adds required `reason: String!` to an existing input. **Reasoning:** old variables omit it and fail validation/coercion. Add it nullable, define omission, migrate clients, then introduce a new command/version if it must become mandatory. **Conclusion:** required input additions break callers.

### Example 5

**Situation:** A provider adds `DELAYED` to an internal status copied into a public enum. **Reasoning:** old generated clients may exhaustively switch and crash. Map volatile provider states to stable public categories or coordinate enum evolution with clients. **Conclusion:** enum closure is a behavioral contract.

### Example 6

**Situation:** A global ID decodes to `tenant=7,row=19`. **Reasoning:** a client alters the tenant bytes and retrieves another record because the resolver trusts the ID. Treat encoding as opaque, validate integrity if applicable, resolve resource, and authorize actor/action/resource independently. **Conclusion:** opacity never replaces authorization.

### Example 7

**Situation:** `updateOrder(patch: JSON!): Boolean!` accepts arbitrary keys. **Reasoning:** validation, omitted/null meaning, legal transitions, audit intent, and typed errors disappear. Replace it with intent-specific mutations and typed inputs/payloads. **Conclusion:** flexibility at the schema often exports complexity to every participant.

### Example 8

**Situation:** Schema diff labels `price: Int!` unchanged while implementation changes cents to dollars. **Reasoning:** all documents validate but every consumer's arithmetic is wrong. Restore unit semantics or add a clearly named field/type with migration. **Conclusion:** semantic compatibility exceeds SDL compatibility.

### Example 9

**Situation:** A deprecated field shows zero traffic for seven days. **Reasoning:** offline mobile clients, monthly jobs, and an uninstrumented environment are absent. Combine operation registry, owner inventory, release adoption, representative retention, and support window before removal. **Conclusion:** absence of sampled traffic is limited evidence.

### Example 10

**Situation:** A union gains `ArchivedOrder`. **Reasoning:** fragments with a fallback remain valid, but generated exhaustive switches may fail and cache/type policies may lack the type. Test supported clients and announce the expansion even if schema validation calls it safe. **Conclusion:** possible-type growth needs client evidence.

## Cross-Program Connections

- **Software Engineering Patterns:** domain-driven boundaries and command/query separation keep the graph independent of storage and service topology.
- **Data Modeling and Databases:** keys, nulls, constraints, normalization, and migrations inform implementation but must be translated into public semantics.
- **Type Systems and Programming Languages:** sums, products, subtyping, partiality, and variance explain unions, objects, wrappers, and positional compatibility.
- **Distributed Systems Engineering:** partial failure and local knowledge constrain non-null guarantees, mutations, and outcome claims.
- **Security Engineering:** opaque identifiers, authorization-sensitive absence, input bounds, and introspection policy define trust boundaries.
- **Product and Client Engineering:** operation corpora, generated types, offline clients, and deprecation adoption supply compatibility evidence.

## References

1. GraphQL Foundation, “GraphQL Specification, September 2025,” type system, validation, execution, introspection, descriptions, deprecation, schema coordinates, and one-of input objects, verified 2026-09-02. [GraphQL specification](https://spec.graphql.org/September2025/).
2. GraphQL Foundation, “Learn: Schema and Types,” official overview of object, scalar, enum, list, non-null, interface, union, and input types, verified 2026-09-02. [GraphQL documentation](https://graphql.org/learn/schema/).
3. GraphQL Foundation, “Learn: Mutations,” official mutation fields, variables, input object, and payload guidance, verified 2026-09-02. [GraphQL documentation](https://graphql.org/learn/mutations/).
4. GraphQL Foundation, “Global Object Identification,” stable object refetching and `Node`/`node` conventions, verified 2026-09-02. [GraphQL specification](https://graphql.org/learn/global-object-identification/).
5. GraphQL Foundation, “Schema Design,” official nullability and continuous-evolution guidance, verified 2026-09-02. [GraphQL documentation](https://graphql.org/learn/schema-design/).
6. GraphQL Foundation, “Schema Change Management,” additive, breaking, dangerous, deprecation, operation-usage, and CI guidance, verified 2026-09-02. [GraphQL documentation](https://graphql.org/learn/governance-versioning/).

## Exercises

### Exercise 1

Define schema, object, input object, interface, union, enum, schema coordinate, deprecation, syntactic compatibility, and semantic compatibility. Explain why validation preservation is insufficient.

### Exercise 2

For each type `[Invoice]`, `[Invoice!]`, `[Invoice]!`, and `[Invoice!]!`, state whether null list, empty list, and null element are allowed. Explain the propagation consequence if a promised non-null element resolves null.

### Exercise 3

Redesign a table-shaped commerce graph with `orders`, `order_items`, `customer_fk`, numeric primary keys, `state_code`, and `updateOrder(patch: JSON!): Boolean!`. Specify domain types, identity, query roots, one intent mutation, input/payload, nullability, and descriptions.

### Exercise 4

Classify and plan these changes: add optional query argument; add required input field; remove deprecated field; add enum value; change cents to dollars without changing SDL; make nullable output non-null; add a union possible type. State needed evidence.

### Exercise 5

Design schema governance for a multi-tenant emergency coordination graph used by web, mobile, partner, and offline clients. Cover ownership, IDs, authorization-sensitive absence, mutations, nullability under partial failure, polymorphism, deprecation/removal, operation evidence, CI checks, rollback, and boundaries with later execution/cost modules.

## Answers to the Exercises

### Answer 1

A schema is the GraphQL type system and root operation contract. An object exposes selectable output fields. An input object groups named supplied values and cannot be an output. An interface defines shared fields implemented by objects; a union lists possible object types without requiring common fields. An enum is a named closed set of client-relevant values. A schema coordinate names an element such as `Order.status` or `Query.order(id:)`. Deprecation retains an element while marking it discouraged with a reason/migration.

Syntactic compatibility preserves validation of supported old operations under the new schema. Semantic compatibility also preserves documented meaning: units, ordering, identity, null causes, authorization behavior, defaults, side effects, and outcomes. `price: Int!` can remain textually identical while changing cents to dollars; validation passes and clients are still broken. Therefore operation validation and schema diffs are necessary but not sufficient.

### Answer 2

`[Invoice]` allows a null list, an empty list, and null elements. `[Invoice!]` allows a null or empty list but not null elements. `[Invoice]!` disallows a null list, allows empty, and allows null elements. `[Invoice!]!` disallows null list/elements and allows empty. Empty means successful present collection with zero members, not absence.

If an element wrapped as non-null resolves null, GraphQL records a field error and cannot place null at that element. Null propagates to the nearest nullable ancestor: perhaps the whole list, or farther through a non-null list/parent chain. The schema designer must assess that blast radius and prove resolver/dependency paths uphold the promise.

### Answer 3

Expose `Order`, `OrderLine`, `Product`, and `Customer` domain objects rather than table names or foreign keys. Give `Order.id: ID!` a documented tenant-scoped or graph-scoped opaque identity; authorize after resolution. `Order.customer: Customer!` is non-null only if every visible order must have a visible customer under the same policy. `Order.lines: [OrderLine!]!` can be present/empty if draft orders may have no lines. `Order.shipment` is nullable before dispatch. Map stable client-relevant states to `OrderStatus`; do not expose volatile internal codes.

Use `Query.order(id: ID!): Order`, documenting null for absent or policy-hidden resources, plus a bounded collection/connection field defined by the pagination policy. Replace JSON CRUD with `cancelOrder(input: CancelOrderInput!): CancelOrderPayload!`. Input contains `orderId`, optional bounded reason, and stable operation/idempotency ID. Payload returns operation ID, nullable order if policy permits, and a non-null list of typed user problems. Descriptions specify ID scope, money units, timestamp format, list order, null causes, legal command states, idempotency retention, and authorization-sensitive behavior.

### Answer 4

Adding an optional argument is generally validation-compatible; specify default/omission meaning and validate the corpus. Adding a required input field without a default is breaking; roll out optional first or introduce a new command. Removing even a deprecated field is breaking for any remaining selector; require owner/registry/telemetry evidence and the full support window.

Adding an enum value preserves GraphQL validation but can break exhaustive generated clients; inspect SDK behavior, test supported versions, notify owners, and consider a stable coarser enum. Changing cents to dollars is semantically breaking despite no SDL diff; restore semantics or add a named replacement and migrate. Making nullable output non-null is often validation-compatible but requires runtime proof across absence, authorization, and dependency failure because violations propagate. Adding a union possible type similarly needs generated-client, fragment fallback, cache, and owner evidence. All changes require descriptions, changelog/communication, representative operations, and rollback that restores both shape and semantics.

### Answer 5

Create a graph-wide registry mapping every schema coordinate to a domain owner, description/invariants, sensitivity, identity scope, null/error semantics, lifecycle, and reviewers. Use opaque stable IDs scoped explicitly; resolve then authorize actor/action/resource, never infer tenant from decoded ID. For resources whose existence is sensitive, define a consistent absent/forbidden policy across errors, timing, sibling fields, caches, and logs.

Model commands such as `acknowledgeIncident`, `assignResponder`, and `closeIncident` as intent-specific mutations with typed inputs, stable operation IDs/idempotency, and typed payload outcomes. Keep principal credentials out of domain input while including incident/tenant/resource identity where the command needs it and binding those facts to authenticated context. Describe commit/outcome recovery separately from GraphQL request completion.

Use non-null only for facts the domain plus every execution path uphold. Nullable relationships or typed availability/status objects represent partial provider failure without erasing an entire incident subtree. Use an interface for truly shared responder fields and a union for alternatives without a durable common selection; require deterministic runtime type and client fallback evidence. Keep personal or provider-specific blobs out of generic JSON/baggage.

CI parses/validates SDL, enforces descriptions/naming/directives, compares the accepted schema, validates persisted/registered operations, tests generated clients, and executes null/authorization/polymorphism/mutation contracts. Removal requires deprecation reason/replacement, owner inventory across web/mobile/partners/offline releases, telemetry with known coverage, support-window expiry, and migration sign-off. Canary old/new schema/resolvers and maintain a rollback that restores old semantics and data compatibility, not SDL alone.

Resolver batching, deadlines, caching, and per-field execution evidence belong to execution design. Pagination/incremental delivery owns collection and patch transport. Authorization and query-cost controls own field policy and bounded execution. Schema governance records their visible contracts and coordinates but does not claim that SDL alone enforces them.

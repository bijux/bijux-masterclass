---
module_id: API-026
program: API & Service Engineering
level: 1
module_number: 26
title: Reusable Schema Components
status: complete
last_verified: 2026-09-01
---

# Reusable Schema Components

## One-Page Review

### Governing question

When should repeated contract structure become a reusable component, and how can its identity, ownership, direction, composition, resolution, and evolution remain safe for every dependent operation?

### Essential definitions

- A **schema component** is a named or identified schema reused through references from one or more contract locations.
- A **component namespace** is a typed map such as OpenAPI `components.schemas` or `components.parameters`.
- A **schema resource** is a JSON Schema with its own identity and base URI, whether stored alone or bundled.
- **fan-in** is the number of dependents that reference a component; high fan-in increases both reuse value and change impact.
- A **resolved view** is the effective schema or OpenAPI object graph after references and applicable composition are processed.
- A **compound schema document** bundles multiple schema resources while preserving their distinct identities.
- A **reuse boundary** is the ownership and compatibility scope within which a shared component may change.

### Central model, mechanism, or theorem

Treat reusable contracts as a directed dependency graph $G=(C,E)$ where component or operation nodes $C$ own semantics and reference edges $E$ propagate obligations. Changing component $c$ affects its reverse-reachable dependent set $R^-(c)$. Reuse is justified when dependents share the same meaning, authority, direction, and compatibility policy—not merely the same current fields. The review cost of change grows with fan-in, transitive reach, and semantic diversity.

### Critical invariants

Every component has one durable purpose and owner. Its name describes domain meaning rather than storage or delivery sequence. References resolve under canonical URI bases and target the correct typed namespace. JSON Schema `$id` identities survive bundling. Request and response components are shared only where authority and requirements genuinely agree. `allOf` means intersection, not inheritance or property merge. Closure is applied at the intended composed boundary. Recursion terminates under bounded evaluation. Unused, duplicate, cyclic, and overly central components are audited. Every change tests resolved dependent views and representative consumer messages.

### Common failures

Extracting every duplicated fragment; naming components `Base`, `Common`, `Model`, `DTO`, `V2`, or after database tables; one universal resource schema for create, update, and response; treating `allOf` as subclassing; closing a base with `additionalProperties: false` then extending it; changing bytes behind the same `$id`; assuming a component is active because it exists; referencing a Response Object where a Schema Object belongs; letting a central `Error` or `Identifier` acquire unrelated meanings; network-fetching references at runtime; and bundling away resource identities.

### Compact example

`Money` can be reused when every dependent operation agrees on amount representation, currency semantics, scale, bounds, and evolution. `CreateInvoiceRequest` may reference `Money` for a caller-supplied limit, while `InvoiceResponse` may reference it for a computed total. Reuse is sound only if both positions mean the same value object; shared field names alone are insufficient. **Conclusion:** components share semantics and policy, not just syntax.

### Connections

[JSON Schema](022-json-schema.md) supplies resource identity, references, vocabularies, and composition. [OpenAPI Structure](023-openapi-structure.md) supplies typed component maps. [Request and Response Modeling](024-request-and-response-modeling.md) supplies directional ownership, and [Validation Constraints](025-validation-constraints.md) supplies the rules a component centralizes. [Examples and Executable Documentation](../ROADMAP.md) validates resolved use sites.

## Governing Question

How should an API team discover, name, publish, compose, validate, and evolve reusable schema components without turning convenience into hidden coupling or ambiguous public meaning?

## Why This Matters

Copying the same constraint into twenty operations invites drift. One schema may accept lowercase currency, another uppercase only, and a third use an unbounded string. A shared component can centralize meaning, tests, documentation, and evolution. Tooling can generate consistent types, render one concept, and compare dependent changes.

Reuse also multiplies blast radius. Tightening one shared `Identifier` may reject requests across several domains. Adding a field to a response component may affect signatures and strict consumers everywhere. A component named `User` can become a union of creation intent, administrative detail, public profile, database row, and authentication subject. At that point, “reuse” has erased ownership.

References add language semantics. OpenAPI has typed component namespaces and Reference Objects. Schema Objects use JSON Schema Draft 2020-12, where `$ref` is an applicator, `$id` changes resource identity and base URI, and `$defs` stores reusable subschemas without activating them by itself. A resolver must know which kind of object contains the reference.

The engineering goal is controlled semantic reuse: one enduring concept, one owner, explicit dependency edges, reproducible resolution, and compatibility evidence for all dependents. Deduplicated text is a possible side effect, not the primary success measure.

## Prerequisites and Retrieval

Retrieve JSON Schema resources, `$id`, `$ref`, `$defs`, anchors, applicators, annotations, OpenAPI Components and Reference Objects, request/response ownership, URI resolution, compatibility, package ownership, graph traversal, and consumer testing.

Before extracting a component, retrieve every candidate use site's meaning, direction, authority, requiredness, nullability, constraints, examples, media type, owner, release cadence, and compatibility policy. Similar-looking fields with different answers must remain separate.

## Learning Objectives

By the end of this module, you should be able to:

1. distinguish semantic reuse from textual deduplication;
2. choose between inline schemas, local `$defs`, OpenAPI components, and standalone resources;
3. preserve canonical identity and reference meaning through splitting and bundling;
4. compose value objects, directional models, unions, and recursive schemas safely;
5. analyze fan-in, transitive impact, cycles, dead components, and centrality;
6. govern naming, ownership, versioning, and publication; and
7. test components both independently and at every resolved use site.

## Core Exposition

### Extract by shared meaning

Start from two or more use sites and write the semantic contract beside each. A reusable component is credible when the sites agree on:

- domain concept and units;
- accepted JSON types and lexical representation;
- presence, null, and empty semantics at the component boundary;
- validation constraints and normalization;
- caller versus service authority;
- confidentiality and disclosure;
- compatibility direction and release policy; and
- documentation understandable without the original operation.

Two `{code, message}` objects may represent a public problem, an internal diagnostic, or a localization record. Their shapes match today, but their stability and sensitivity do not. Conversely, `Money` can be reused across many operations even when it appears under different property names because its value semantics remain stable.

Avoid premature extraction from one occurrence merely because a generator supports it. Inline a small operation-specific structure until its owner and meaning stabilize. Extract when independent drift would be a defect or when a concept deserves its own tests and identity.

### Choose the smallest appropriate scope

Inline schemas have the narrowest scope and best local readability. A `$defs` entry is useful for subschema reuse inside one JSON Schema resource. An OpenAPI `components.schemas` entry is convenient within one OAD and can be referenced with `#/components/schemas/Name`. A standalone schema resource with absolute `$id` supports reuse across documents, APIs, languages, or release units.

Wider scope creates more dependency governance. Do not publish every local fragment in an organization-wide registry. Promote through deliberate boundaries: operation-local, API-local, domain-owned, then organization-wide only when semantics and stewardship genuinely span those scopes.

OpenAPI components are typed maps. Schemas, responses, parameters, examples, request bodies, headers, security schemes, links, callbacks, path items, and media types occupy distinct namespaces. A matching key does not make their types interchangeable. Components have no effect until referenced or connected by a defined field.

### Name by enduring domain purpose

Good component names communicate meaning at the use site: `Money`, `OrderId`, `CreateOrderRequest`, `OrderSummary`, `OrderDetail`, `PageCursor`, or `ValidationProblem`. Names such as `BaseModel`, `CommonFields`, `Payload`, `Data`, `Misc`, `NewUser`, `UserV2`, and `ResponseDTO` hide ownership or delivery history.

Avoid encoding implementation layers such as ORM, controller, or serializer into public component names. Avoid a universal `ID` if identifiers differ by opacity, case, scope, length, or reuse. `OrderId` and `CustomerId` may share a primitive representation while remaining semantically distinct types that prevent accidental substitution.

Version identity belongs in a media type, resource URI, release policy, or clearly governed schema family. A durable name should state what the component represents. If two incompatible versions coexist, their identifiers must be unambiguous, but do not let temporary sequencing become the only semantics.

### Separate OpenAPI containers from JSON Schema resources

The following fragment contains OpenAPI component namespaces. `OrderId` is a Schema Object, while `OrderIdParameter` is a Parameter Object that references it.

<!-- bijux-verify: {"id":"typed-component-namespaces","mode":"data","language":"yaml","toolchain":"none","reason":"Declarative OpenAPI fragment illustrating separate Schema and Parameter component namespaces."} -->
```yaml
components:
  schemas:
    OrderId:
      type: string
      pattern: '^ord_[A-Za-z0-9]{16}$'
  parameters:
    OrderIdParameter:
      name: orderId
      in: path
      required: true
      schema:
        $ref: '#/components/schemas/OrderId'
```

The Parameter Object owns wire location, requirement, style, and parameter meaning. The Schema Object owns the JSON instance constraint. Reusing `OrderId` in a response property does not make that property a path parameter.

Inside a JSON Schema resource, `$defs` is a conventional location for reusable subschemas:

<!-- bijux-verify: {"id":"local-schema-definitions","mode":"data","language":"json","toolchain":"none","reason":"Declarative Draft 2020-12 schema illustrating local $defs reuse without creating a separate resource identity."} -->
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.example.test/order-line",
  "$defs": {
    "positiveQuantity": {
      "type": "integer",
      "minimum": 1,
      "maximum": 100
    }
  },
  "type": "object",
  "required": ["quantity"],
  "properties": {
    "quantity": {"$ref": "#/$defs/positiveQuantity"}
  }
}
```

The `$defs` entry is inert until referenced. It is a subschema, not automatically a separately addressable schema resource with independent release policy. Add `$id` only when a location should become a resource boundary; doing so changes base-URI behavior for relative references below it.

### Give shared resources canonical identity

A reusable standalone schema should declare an absolute `$id` under a namespace its owner controls. The URI identifies schema content; evaluation need not fetch it over the network. A registry can map the canonical URI to pinned reviewed bytes in builds and runtimes.

Do not overwrite incompatible content at one immutable identity. A cached validator, generated client, or archived contract must be able to reproduce earlier evaluation. Use immutable release identifiers or a content-addressed registry behind a stable governed alias, and record the exact resolved set used by each API publication.

Relative references resolve from the applicable base. Moving a file without changing `$id` should not change meaning when the registry is correct. Adding or moving `$id` can change nested resolution even when source text looks similar. Test canonical URIs, not just local paths.

Named `$anchor` fragments can create readable internal targets. JSON Pointer fragments couple references to document structure; anchors can survive some restructuring, but they are still public identifiers once external dependents use them. Rename or remove them only under compatibility policy.

### Compose constraints, not classes

JSON Schema `allOf` applies every subschema. It describes set intersection. It does not copy properties, override parent fields, inherit methods, or create a discriminator. If one branch requires `type: string` and another `type: object`, the intersection is empty. If both constrain a numeric maximum, the stricter result applies.

Object extension is a common trap. A base object closed with `additionalProperties: false` rejects properties declared only by an `allOf` sibling because its local coverage does not include them. Options include declaring the complete object in one schema, keeping reusable property value schemas rather than an extensible base object, or composing open branches and applying `unevaluatedProperties: false` at the outer Draft 2020-12 boundary.

`unevaluatedProperties` depends on annotations from successful evaluation, so tool support and branch behavior matter. Test the fully composed schema with valid base, valid extension, unknown property, failed branch, conditional, and reference fixtures. Do not assume a code generator implements annotation-sensitive closure correctly.

Prefer composition of stable value objects and explicit full shapes over “base entity plus subclasses.” Public data contracts rarely share all the substitutability rules implied by object-oriented inheritance.

### Reuse directionally

Create request, replace request, patch instruction, summary response, detail response, and administrator response have different requiredness and authority. One shared `User` schema with many optional fields obscures which inputs are writable and which outputs are visible.

Share invariant leaf components such as `OrderId`, `CurrencyCode`, or perhaps `Money` when semantics align. Build directional outer components explicitly. `CreateOrderRequest` can require caller intent. `OrderResponse` can require server-generated identity, totals, status, and timestamps. Annotations such as `readOnly` and `writeOnly` improve documentation but do not replace these boundaries or authorization.

Even leaf reuse needs direction review. A currency code in a request can be a supported choice from a closed set, while a response may need to tolerate new codes before an older consumer upgrades. The same lexical value does not guarantee identical compatibility variance.

When common fields are genuinely identical, use a carefully named shared object and test resolved directional schemas. Avoid a catch-all `CommonFields` that becomes the only place to add properties and thereby changes every operation.

### Model alternatives with explicit tags

Reusable unions need stable branch identity. Use a required property with `const` in each branch and a documented tag meaning. `oneOf` then verifies exclusivity when branches are disjoint; `anyOf` is correct when overlap is acceptable. An OpenAPI discriminator can help tooling but does not replace JSON Schema constraints.

Place common properties either in a separately composed schema or explicitly in each branch, depending on closure and generator behavior. Do not rely on a discriminator mapping to validate that an instance belongs to the branch. Test missing tag, unknown tag, wrong branch fields, overlap, and future tag behavior.

An enum component shared across unrelated fields can create accidental coupling. `status` for payment, order, and delivery may all currently include `pending`, but their state meanings and evolution owners differ. Reuse by domain concept, not token coincidence.

### Handle recursion and dynamic scope cautiously

Recursive components model trees, expressions, nested categories, or linked structures. A schema can reference itself directly or indirectly. Valid recursion must still be bounded by input depth, size, and evaluator limits. An unconstrained recursive branch can admit unexpected instances or exhaust tools.

Draft 2020-12 `$dynamicAnchor` and `$dynamicRef` support extensible recursive schemas whose target can vary through dynamic scope. This is powerful for meta-schemas and plugin-like extension points, but it increases reasoning and tool requirements. Prefer ordinary `$ref` unless dynamic scope solves a demonstrated ownership problem.

Dependency cycles are not automatically defects for schema recursion. Cycles among OpenAPI components can, however, break code generators, serializers, examples, or documentation tools. Label intentional recursive strongly connected components and reject accidental cycles in surfaces whose consumers require an acyclic model.

### Analyze the dependency graph

Maintain a graph from operations and components to their referenced components. Compute direct fan-in, transitive reverse reach, unresolved edges, unused nodes, duplicate semantics, and strongly connected components. These are review signals, not automatic quality scores.

High fan-in components deserve stricter ownership and compatibility review because a small edit reaches many operations. A component with zero reachable use from any entry operation is dead publication surface unless it is deliberately exported as a component library. Remove it or document that library contract.

The bounded checker below verifies a small acyclic component graph, reachable use, and type-compatible references. It cannot establish semantic reuse or JSON Schema conformance.

<!-- bijux-verify: {"id":"component-dependency-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"CreateOrderRequest=reachable\nMoney=reachable\nOrderId=reachable\nOrderResponse=reachable\ncomponents=4\nedges=5\nmax_fan_in=2\nunresolved=0\nevidence=bounded_component_graph\n","stderr":""}} -->
```python
components = {
    "OrderId": {"kind": "schema", "refs": []},
    "Money": {"kind": "schema", "refs": []},
    "CreateOrderRequest": {"kind": "schema", "refs": ["Money"]},
    "OrderResponse": {"kind": "schema", "refs": ["OrderId", "Money"]},
}
operation_refs = ["CreateOrderRequest", "OrderResponse"]

unresolved = sorted({ref for node in components.values() for ref in node["refs"] if ref not in components})
assert not unresolved

visiting = set()
visited = set()
def visit(name):
    if name in visiting:
        raise AssertionError("unexpected cycle")
    if name in visited:
        return
    visiting.add(name)
    for child in components[name]["refs"]:
        visit(child)
    visiting.discard(name)
    visited.add(name)

for root in operation_refs:
    visit(root)

fan_in = {name: 0 for name in components}
for node in components.values():
    for child in node["refs"]:
        fan_in[child] += 1
for root in operation_refs:
    fan_in[root] += 1

for name in sorted(visited):
    print(f"{name}=reachable")
print(f"components={len(components)}")
print(f"edges={sum(len(node['refs']) for node in components.values()) + len(operation_refs)}")
print(f"max_fan_in={max(fan_in.values())}")
print(f"unresolved={len(unresolved)}")
print("evidence=bounded_component_graph")
```

Graph evidence should link to source locations and owners. A high count does not say a component is wrong; it says the review blast radius is large. A low fan-in component can still be valuable when it has a stable standalone identity or complex independent tests.

### Bundle without erasing identity

Consumers often need one artifact even when authors maintain modular sources. A bundler can embed referenced resources into a compound document while retaining every `$id` and resolution boundary. A dereferencer may instead replace references with copied content, which can expand recursion, lose identity, duplicate annotations, or change tool behavior.

Choose bundle versus dereference explicitly. Compare evaluation of canonical modular resources and the published bundle against the same fixture corpus. Verify every absolute schema location in diagnostics where consumers depend on it. Never assume a visually similar output preserves semantics.

For OpenAPI, a publication bundle can collect external components while retaining the OAD's `$self` and Schema Object `$id` identities. OAS Reference Objects and Schema `$ref` require different processing rules. Use a tool that understands the exact OAS and JSON Schema dialect rather than a generic YAML pointer copier.

Record a dependency lock or manifest containing canonical URI, content digest, owner, source version, dialect, and retrieval provenance. Runtime resolution should not depend on the public network being available or unchanged.

### Design registries as governed resolution systems

A schema registry is more than file storage. It needs immutable identities, authorization, validation, provenance, ownership, dependency metadata, compatibility rules, deprecation, retention, and reproducible retrieval. Publishing a component can affect many teams; overwriting or deleting it can invalidate old messages and builds.

Separate a stable discovery alias from immutable evaluation identity where useful. Resolve aliases during build or approval, lock the immutable result, and evaluate with the lock. Prevent a mutable “latest” from changing production interpretation without a release.

Access policy matters. Public schemas must not embed internal hosts, secrets, private enum values, or sensitive examples. Private schemas still cross tool and team boundaries and need least privilege. A resolver must restrict URI schemes and sources to prevent arbitrary network or filesystem access.

### Test components and resolved consumers

Test a component's own positive, negative, and boundary fixtures. Then test every materially distinct resolved use site, because outer requiredness, closure, conditionals, direction, media type, and generator mapping can change behavior. Validate examples against resolved schemas.

Use at least one validator that supports the declared dialect. Use multiple implementations when portability matters. Run bundling equivalence tests. Generate representative clients and servers to expose recursion, union, decimal, map, nullability, and naming approximations. Compile and execute message fixtures rather than stopping at generation success.

Compatibility analysis should compare valid-instance sets in the correct direction and then add semantic consumer evidence. Generate witness instances accepted only by old or new versions. For a high-fan-in component, enumerate transitive operations and consumer owners in the review.

### Evolve through ownership, not surprise

Each component needs an owner authorized to define meaning and approve compatibility. The owner publishes change policy, support window, deprecation, and migration. Dependents need a way to pin, test, and learn about changes.

Do not add a field to a central component because one operation needs it. That operation can wrap or define a richer component. Promote the field only when the shared concept itself has changed and all dependents should observe the new meaning.

Breaking changes require a new immutable identity or governed version boundary. Additive changes still need consumer analysis: strict decoders, signatures, enum switches, generated code, closed outer schemas, and authorization can break. Keep old resources available for reproducibility and communicate a migration path.

## Definitions and Notation

Let $C$ contain operation roots and reusable components. Directed edge $(u,v)\in E$ means $u$ depends on $v$. Direct fan-in is:

$$
f(v)=|\{u\in C\mid(u,v)\in E\}|.
$$

The transitive impact set of changing $v$ is its reverse-reachable set:

$$
R^-(v)=\{u\in C\mid u\leadsto v\}.
$$

Let $m(u)$ be the semantic contract of a use site. Extracting use sites $U$ into component $v$ is sound only if the component-level obligations they delegate are equivalent under the intended direction and context. Syntactic equality is neither necessary nor sufficient.

A **leaf component** has no outgoing reference edges. A **root schema** is selected directly by an operation or published entry. A **strongly connected component** is a maximal mutually reachable node set and can represent intentional recursion. A **lock manifest** binds canonical identifiers to exact content. A **semantic duplicate** expresses the same governed concept independently. A **false friend** has similar structure but different meaning or policy.

## Mechanisms, Invariants, or Proof Structure

1. Compare candidate use sites by meaning, units, authority, direction, and evolution.
2. Choose the narrowest reuse scope that has one durable owner.
3. Name by domain purpose and place the object in the correct typed namespace.
4. Assign canonical `$id` identity to independently governed Schema resources.
5. Compose constraints using actual JSON Schema applicator and closure semantics.
6. Build and audit the reference graph for resolution, reachability, fan-in, and cycles.
7. Publish through a pinned registry and bundle without erasing identities.
8. Validate component fixtures and every materially distinct resolved use site.
9. Analyze changes across reverse-reachable operations and consumers.
10. Retain immutable versions, provenance, deprecation, and migration evidence.

The invariants are semantic equivalence at reuse points, single ownership, typed reference correctness, canonical resolution, directional integrity, composition correctness, bounded recursion, reachable publication, bundle equivalence, and transitive compatibility review.

## Alternatives and Trade-Offs

Inline schemas maximize locality and independent evolution but repeat constraints. Local `$defs` centralize within one resource without creating a broader contract. OpenAPI components serve one description. Standalone resources support cross-description reuse but require registry and release governance. Choose scope by ownership, not maximum reach.

Fine-grained leaf components enable type safety and consistency but can turn a schema into reference noise. Coarse object components improve readability when the object is stable but increase coupling. Extract concepts with meaningful independent policy; leave incidental one-line constraints local.

One shared directional schema reduces maintenance but relies on annotations and tool context. Separate request and response schemas duplicate some fields but make authority and requiredness explicit. Share stable value objects underneath distinct outer models.

Bundling preserves references and resource identity for portable delivery. Full dereferencing can help limited tools but explodes recursive graphs and may alter diagnostics or semantics. Publish both only when reproducible transformation and equivalence tests exist.

Central registries improve discovery and governance while creating organizational bottlenecks and large blast radii. Domain-owned registries or namespaces preserve stewardship; a catalog can provide discovery without transferring semantic ownership to one central team.

## Failure Modes and Misconceptions

- **“Duplicate text should always be extracted.”** Reuse requires shared meaning, authority, and compatibility, not syntax alone.
- **“Anything in `components` is automatically used.”** Components are inert until a reference or defined connection reaches them.
- **“All component maps hold schemas.”** OpenAPI namespaces are typed and not interchangeable.
- **“`$defs` creates independent published resources.”** It stores subschemas; `$id` establishes a resource identity.
- **“`$ref` copies text.”** It resolves and applies a target under the relevant language semantics.
- **“`allOf` is inheritance.”** It is intersection; conflicting constraints can make the valid set empty.
- **“A closed base can be extended freely.”** Local `additionalProperties` coverage commonly rejects sibling additions.
- **“One `User` model ensures consistency.”** It often collapses request authority, role-specific output, and lifecycle variants.
- **“A shared enum is harmless.”** Token coincidence can couple unrelated domain state machines.
- **“Relative file paths are stable identities.”** Canonical URIs and bases govern interoperable resolution.
- **“Bundling means deleting `$id`.”** Compound resources retain identities; erasing them can change reference meaning.
- **“Cycles are always errors.”** Schema recursion can be intentional, but tools and runtime evaluation need bounds.
- **“High fan-in proves good reuse.”** It proves blast radius; semantic coherence still needs review.
- **“Additive component edits are universally safe.”** Strict clients, signatures, unions, authorization, and outer closure can break.
- **“A registry's latest alias is reproducible.”** Evaluation needs an immutable locked resource set.

## Worked Examples

### Example 1

**Situation:** Three operations define identical three-letter currency strings. **Reasoning:** If all use ISO-like uppercase code semantics, normalization, and evolution, extract `CurrencyCode`; otherwise keep domain-specific variants. **Conclusion:** semantic review precedes extraction.

### Example 2

**Situation:** `CustomerId` and `OrderId` are both UUID strings. **Reasoning:** Separate components prevent substitution and allow scope or format to evolve independently. **Conclusion:** primitive equality does not imply domain equality.

### Example 3

**Situation:** `CreateUserRequest` references the full `User` response schema. **Reasoning:** It accidentally accepts role, ID, status, and audit properties. Share leaf value objects and define a directional request. **Conclusion:** reuse must preserve authority.

### Example 4

**Situation:** A base address closes unknown fields and an `allOf` country schema adds `region`. **Reasoning:** Local closure rejects the sibling field. Restructure the full object or apply outer `unevaluatedProperties` with tested tool support. **Conclusion:** composition is evaluated semantics, not property merge.

### Example 5

**Situation:** A reusable `status` enum serves payments and shipments. **Reasoning:** Both include `pending`, but their transitions and owners differ. Split them into `PaymentStatus` and `ShipmentStatus`. **Conclusion:** shared tokens can be false friends.

### Example 6

**Situation:** A schema file moves and relative references start resolving elsewhere. **Reasoning:** Assign canonical absolute `$id` values and resolve from a registry, not incidental checkout paths. **Conclusion:** identity decouples meaning from packaging.

### Example 7

**Situation:** A bundle removes nested `$id` fields to make one file. **Reasoning:** Relative references can change bases and diagnostics lose resource identity. Preserve compound resource boundaries and test equivalence. **Conclusion:** one file can still contain many resources.

### Example 8

**Situation:** `Money` has fan-in 47 and a proposed maximum drops by half. **Reasoning:** Enumerate reverse-reachable operations, distinguish request and response positions, replay fixtures, and create a new governed version if incompatible. **Conclusion:** centrality increases review obligation.

### Example 9

**Situation:** A recursive `Category` schema generates an infinitely nested sample. **Reasoning:** Schema recursion may be valid, but generators need depth policy and examples should be finite. Bound instance depth and tool behavior. **Conclusion:** valid recursion is not unbounded execution permission.

### Example 10

**Situation:** A component registry overwrites `https://schemas.example.test/address` with a stricter schema. **Reasoning:** Old builds and stored messages now evaluate differently under one identity. Restore immutable content and publish a new identifier plus migration. **Conclusion:** canonical identity must be reproducible.

## Cross-Program Connections

[Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) supplies value objects and semantic ownership. [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) supplies dependency direction and bounded contexts. [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies graph traversal and strongly connected components. [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) supplies schema ownership and shared-model governance. [Platform Engineering](../../29-platform-engineering/ROADMAP.md) can provide registries and tooling without taking domain meaning away from API owners.

## References

1. A. Wright, H. Andrews, B. Hutton, and G. Dennis, [*JSON Schema: A Media Type for Describing JSON Documents, Draft 2020-12*](https://json-schema.org/draft/2020-12/json-schema-core), including schema resources, references, dynamic scope, and bundling, 16 June 2022. Checked 2026-09-01.
2. A. Wright, H. Andrews, B. Hutton, and G. Dennis, [*JSON Schema Validation: A Vocabulary for Structural Validation of JSON, Draft 2020-12*](https://json-schema.org/draft/2020-12/json-schema-validation), 16 June 2022. Checked 2026-09-01.
3. JSON Schema, [*Draft 2020-12 Release Notes*](https://json-schema.org/draft/2020-12/release-notes), including dynamic references, tuple keywords, and evaluated-item changes. Checked 2026-09-01.
4. OpenAPI Initiative, [*OpenAPI Specification 3.2.0*](https://spec.openapis.org/oas/v3.2.0.html), especially Components, Reference, and Schema Objects, 19 September 2025. Checked 2026-09-01.
5. T. Berners-Lee, R. Fielding, and L. Masinter, [*RFC 3986: Uniform Resource Identifier (URI): Generic Syntax*](https://www.rfc-editor.org/rfc/rfc3986.html), Internet Standard, January 2005. Checked 2026-09-01.
6. P. Bryan, K. Zyp, and M. Nottingham, [*RFC 6901: JavaScript Object Notation (JSON) Pointer*](https://www.rfc-editor.org/rfc/rfc6901.html), Standards Track, April 2013. Checked 2026-09-01.

## Exercises

### Exercise 1

Given duplicate `Money`, `Address`, `status`, and pagination fragments across six operations, decide which to inline, reuse locally, publish as API components, or publish as standalone domain resources. State the semantic evidence required for each choice.

### Exercise 2

Refactor a universal `User` schema used for create, replace, public response, administrator response, and audit events. Design directional outer components and identify any safe shared leaf components.

### Exercise 3

A closed `BaseResource` is extended with `allOf` by three schemas, and generators disagree. Explain the validation semantics and propose two durable redesigns with fixture coverage.

### Exercise 4

Design a registry and bundling workflow for ten independently owned schema resources. Specify identity, locks, provenance, access, resolution, validation, deprecation, retention, and equivalence evidence.

### Exercise 5

Analyze a dependency graph where `Identifier` has fan-in 60, `Problem` fan-in 42, five components are unreachable, and one three-node cycle models a tree through wrappers. Decide what is a defect, what is a review signal, and what evidence is needed before changing each surface.

## Answers to the Exercises

### Answer 1

Reuse `Money` only if amount type, currency relation, scale, rounding, and evolution match; otherwise create domain-specific money concepts. `Address` often differs by billing, shipping, postal authority, locale, and verification, so compare semantics before sharing leaf lines or a full object. Split status by domain state machine even when tokens overlap. Pagination can be an API-level component only if cursor, ordering, query binding, limits, and metadata semantics match. Inline one-off operation constraints, use `$defs` within one resource, OpenAPI components within one OAD, and standalone `$id` resources only under a durable cross-document owner. Tests and compatibility policy must follow the chosen scope.

### Answer 2

Define `CreateUserRequest` for caller-owned initial intent, `ReplaceUserProfileRequest` for complete mutable profile state, `PublicUser` for safe ordinary fields, `AdminUserDetail` for separately authorized administration, and an event schema describing immutable event facts rather than a current response. Possible shared leaves include `UserId`, `DisplayName`, and perhaps `EmailAddress` if visibility and validation do not alter their value semantics. Role, status, audit actor, and timestamps remain service-derived; secret or restricted evidence never enters broad components. Test each resolved direction and do not rely on readOnly/writeOnly annotations for enforcement.

### Answer 3

`allOf` intersects constraints. `additionalProperties: false` in the base sees only properties covered locally and can reject fields declared by sibling branches. One redesign declares each final closed object completely while reusing leaf value schemas. Another composes open property-bearing branches and places `unevaluatedProperties: false` at the final Draft 2020-12 boundary, accepting stronger evaluator and generator requirements. Test base-only, every extension, unknown property, failed branch, nested reference, conditionals, validation output, and generated serialization across supported tools.

### Answer 4

Give each resource an immutable absolute `$id`, declared dialect, owner, source release, content digest, dependency list, and visibility classification. Resolve allowed canonical URIs through an authenticated registry, then create a lock mapping each URI to exact bytes. Validate dialect and references, run component and dependent fixtures, and build a compound bundle preserving every `$id`. Compare modular and bundled evaluation. Publish provenance and compatibility results; never resolve mutable aliases at runtime. Retain prior resources through documented support and archival requirements, deprecate rather than overwrite, and restrict network or filesystem resolver capabilities.

### Answer 5

Fan-in 60 and 42 are blast-radius signals, not automatic defects: inspect whether each component still has one meaning and owner, then enumerate transitive dependents before changes. Unreachable components are defects if the OAD is only an API entry surface; they may be intentional exports in a documented component library. The cycle can be valid recursion if it accurately models finite instances and all required validators, generators, examples, and serializers handle it under depth bounds; wrapper complexity may still justify simplification. Collect reference resolution, reachability, semantic ownership, fixture, tool compatibility, consumer, and bundle-equivalence evidence before edits.

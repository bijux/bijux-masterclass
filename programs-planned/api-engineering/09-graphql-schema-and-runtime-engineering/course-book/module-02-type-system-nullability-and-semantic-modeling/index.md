# Module 02 — Type System, Nullability, and Semantic Modeling

> **Program stage:** Course 9 of 10 — Compose governed client-shaped capabilities.

> **Central question:** How does the schema make useful promises without promising values the runtime cannot sustain?

## Where this module fits

Module 01 produced **Publish the graph boundary and operation-lifecycle trace**. This module extends that result by asking: **How does the schema make useful promises without promising values the runtime cannot sustain?**

The new capstone increment is **Release Analysis Graph API 1.0 type and nullability policies**. It becomes the prerequisite for **Resolver Architecture, Batching, and Source Ownership**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Design types around client concepts.
- Choose nullability from failure guarantees.
- Model lists, interfaces, unions, enums, scalars, and inputs.
- Apply OneOf input semantics.
- Detect schema promises the runtime cannot keep.

## Capstone increment

Release Analysis Graph API 1.0 type and nullability policies.

## Model client concepts, not database rows

Schema design starts from client tasks and stable domain language. A type may combine values supplied by several services, while each field retains a source. Conversely, two database tables may belong to one graph type if clients should not see the persistence split. Exposing tables mechanically produces awkward types, leaks implementation details, and makes schema evolution dependent on storage migrations.

The Analysis Graph keeps `AnalysisRun` cohesive for clients while marking `artifacts` and `deliverySummary` as separately sourced fields. The type is a client concept; source directives and ownership maps preserve the distributed reality.

## Nullability is a failure contract

In GraphQL every output is nullable unless wrapped in non-null. Non-null is not a preference for clean client types. It is a promise that successful completion of the containing selection can always produce a value. If a non-null field resolves to null, the error bubbles to the nearest nullable ancestor, possibly nulling an entire object or the top-level `data` value.

`Project.analysisRuns` is non-null because Analysis Control owns both project and run listing and the field is central to the root result. `AnalysisRun.artifacts` is nullable in the graph because Artifact Service can be unavailable independently. Returning an empty list during an outage would falsely claim authoritative emptiness. Null plus a path-specific error preserves truth.

## Lists contain two nullability decisions

`[Artifact!]` means the list may be null, but present items may not be null. `[Artifact!]!` means both the list and every item are non-null. `[Artifact]` permits both a null list and null elements. Each form creates different client control flow and bubbling behavior.

Use non-null items when an item without identity is unusable and the source can omit invalid rows before returning. Use a nullable list when the source dependency may fail independently. Avoid nullable list elements as a substitute for per-item error modeling unless the domain genuinely contains missing positions.

## Interfaces, unions, enums, and scalars

Interfaces express shared fields clients can select across possible object types. `Node` supplies `id`. Unions express a result that may be one of several objects without requiring shared fields; `SearchResult` can be a Project, AnalysisRun, or Artifact. Clients must use type conditions and should include `__typename` when behavior differs.

Enums are closed sets in the schema but evolve carefully: adding a value can break exhaustive client switches even though it is additive at the type-system level. Custom scalars such as `DateTime`, `Cursor`, and `Version` require documented serialization and coercion. A scalar named `JSON` is an escape hatch and must not become the default for unmodeled data.

## Input coercion and OneOf

Input objects distinguish omitted fields from explicit null. This matters for patches and defaulting. A required input field is non-null without a default; adding one later breaks existing operations.

GraphQL September 2025 includes OneOf Input Objects. `NodeLookup @oneOf` requires exactly one non-null member. This models alternatives more truthfully than an input with several optional fields plus undocumented precedence. Framework support must be measured; the semantic rule remains part of the released schema.

## Design from semantic invariants

A good schema begins with truths that clients may rely on, not with ORM classes or transport payloads. For each type, answer four questions:

1. What stable concept does this type represent?
2. Which fields are identity and which are observations?
3. Which service owns each fact?
4. Which failures can independently prevent a field from being produced?

For `AnalysisRun`, identity and lifecycle facts come from Analysis Control. Artifact metadata comes from Artifact Service. Delivery status comes from a Notification projection. The schema groups them because the client task is to understand one run, but nullability and source annotations preserve the different failure domains.

A database-row generator cannot make these decisions. It tends to expose internal primary keys, nullable columns, join tables, audit columns, and storage-specific enum values. It also encourages schema changes whenever persistence changes. The graph should outlive storage refactors and should not expose facts that no client task needs.

## Nullability as executable control flow

GraphQL output nullability determines how failures transform the response tree. The rule is mechanical:

- a nullable field may complete with null;
- a non-null field that completes with null raises an execution error;
- that null propagates to the nearest nullable ancestor;
- propagation can null an object, a list element, a list, or the entire `data` value.

Use this matrix during design:

| Declaration | Can field be null? | Can an item be null? | Typical meaning |
|---|---:|---:|---|
| `Artifact` | yes | n/a | optional or independently unavailable object |
| `Artifact!` | no | n/a | value is required whenever parent exists |
| `[Artifact!]` | yes | no | dependency may fail, but returned items are complete |
| `[Artifact]!` | no | yes | list always exists, but positions may be absent |
| `[Artifact!]!` | no | no | source can always produce a complete list |

The last form is attractive to client code, but it is a strong operational promise. `Project.analysisRuns: AnalysisRunConnection!` is defensible because Analysis Control owns the root project and the run query. `AnalysisRun.artifacts: [Artifact!]` is nullable because a separate service may fail. Returning `[]` when the service is down would collapse “authoritatively no artifacts” and “unknown because the source failed” into the same value.

Avoid making a field non-null merely because the current database column has a constraint. The graph promise must survive migrations, authorization redaction, remote-service failure, and historical records. Conversely, avoid making everything nullable to avoid thinking. Excessive nullability forces every client to handle impossible states and hides where the server actually owes a value.

## Semantic scalars and input coercion

A custom scalar creates a named semantic boundary, not automatic validation. `DateTime`, `Cursor`, and `Version` are useful only if the runtime defines how values are serialized, parsed, bounded, and rejected. The scalar implementation must be identical across query variables, literal values, results, persisted operations, and both language tracks.

For example, the course treats `Version` as an opaque optimistic-concurrency value. Clients may echo it but must not perform arithmetic on it. `Cursor` is opaque and bound to tenant, operation, filters, sort order, and traversal state. `DateTime` uses a normalized UTC representation. A custom scalar that accepts arbitrary strings but is described as “validated” is misleading.

Input coercion happens before execution. Missing, explicit null, defaulted, and present values are distinct. For an argument `first: Int! = 20`, omission produces the default, explicit null is invalid, and a positive integer is passed to admission. The GraphQL type system alone does not impose the course maximum; policy rejects values above the bounded page size.

OneOf Input Objects model exclusive alternatives. `NodeLookup @oneOf` requires exactly one non-null field, so `{id: ...}` and `{externalId: ...}` are valid while `{}` and `{id: ..., externalId: ...}` are not. This is superior to an input object whose resolver must guess precedence between two optional keys.

## Interfaces, unions, and polymorphism

Use an interface when several object types share a meaningful contract that clients can select directly. `Node` promises an opaque `id`, not a universal storage model. The runtime still needs safe type resolution and authorization; a global identifier is not proof that the caller may observe the object.

Use a union when alternatives share no field contract beyond being possible results. `SearchResult = Project | AnalysisRun | Artifact` forces clients to use `__typename` and type conditions. That explicitness is useful: a search result cannot pretend that every member has `name` or `status`.

Do not use unions as a universal error mechanism. A mutation result union is appropriate for expected, typed domain outcomes. Query execution and authorization failures still belong in GraphQL errors when the server cannot produce the selected field. A `UserOrError` union on every field creates a parallel error protocol and defeats normal null propagation.

## Enums are compatibility surfaces

GraphQL enums are not arbitrary strings. Adding an enum value is often source-compatible for the schema but can break clients that compile exhaustive switches. Removing or renaming a value is clearly breaking. Before exposing a source-service enum, decide whether the graph owns a stable public vocabulary or merely passes through an internal state machine.

`RunStatus` is a graph-level vocabulary aligned with Analysis Control. A source service may have additional internal states such as `LEASED` or `FINALIZING`; those do not belong in the client contract if clients cannot act on them. Mapping internal states to a stable public enum protects clients and permits internal evolution.

The release gate classifies an added output enum value as review-required, not automatically safe. Active operation validation cannot detect exhaustive client code, so client declarations and telemetry are part of the decision.

## A schema-design walkthrough

Suppose a client requests a project, the latest ten runs, artifact metadata, and delivery status. A weak design might expose one `ProjectRecord` with nested database-derived objects, make every list non-null, and return delivery counters as direct fields with no age.

The course design instead records:

- `Project` and `AnalysisRun` facts from Analysis Control;
- `AnalysisRun.artifacts` from Artifact Service, nullable on independent failure;
- `AnalysisRun.deliverySummary` from Notification Service, nullable and carrying `observedAt` plus `stalenessSeconds`;
- connections for pageable run collections;
- global identifiers for graph routing, with local identifiers decoded only inside trusted adapters;
- field-level authorization for artifacts and delivery data.

This model tells the client not only what values exist but what they mean when systems fail. That is the standard for a truthful graph type system.

## Schema review questions

Before approving a type change, ask:

- Does the type express a client concept rather than a storage artifact?
- Is each non-null promise sustainable across authorization and dependency failure?
- Does a list declaration distinguish source failure from an empty result?
- Are scalar parse and serialize rules executable and cross-language?
- Are enum additions classified for consumer risk?
- Does an interface express a real shared contract?
- Does a union force clients to handle alternatives explicitly?
- Does an input object distinguish omission, null, and mutually exclusive alternatives?
- Is every field linked to a source authority and a release owner?

The lab deliberately changes one nullable remote field to non-null and injects a source outage. The resulting null propagation is the proof that nullability is runtime behavior, not schema decoration.

## Worked capstone review

Review `AnalysisRun.artifacts`. Making it `[Artifact!]!` gives clients a simpler type but would null the whole run whenever Artifact Service is unavailable unless the gateway can provide an authoritative fallback. The honest release uses `[Artifact!]`; an empty list means authoritative empty, while null plus `DOWNSTREAM_UNAVAILABLE` means no answer was available.

## Python and TypeScript implications

Python dataclasses and TypeScript interfaces model the semantic types used by tests. The released SDL remains authoritative. Generated language types are consumers of the schema, not a second schema source.

## Evidence required before the next module

Complete the lab and checkpoint. The decisive artifact is the module report under `reports/module-02-*.json`; prose claims without its oracle do not pass.

## Module synthesis

You are ready to leave this module when you can **design types around client concepts, choose nullability from failure guarantees, and model lists, interfaces, unions, enums, scalars, and inputs** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Inject Artifact Service unavailability and repeat** and requiring the following oracle: **released remote field failure preserves the AnalysisRun object;; scratch non-null field increases the bubbling blast radius;; null list items obey item nullability;; invalid resolver output is an execution/completion error;.**

The cumulative platform now includes **Release Analysis Graph API 1.0 type and nullability policies**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Resolver Architecture, Batching, and Source Ownership](../module-03-resolver-architecture-batching-and-source-ownership/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.

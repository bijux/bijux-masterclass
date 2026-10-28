# Worked Answers — Module 02: Type System, Nullability, and Semantic Modeling

Use these solutions to audit your reasoning for **Type System, Nullability, and Semantic Modeling**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why is non-null an operational promise rather than a style preference?

A null value on a non-null field bubbles and can erase its parent. The declaration must match the runtime’s ability to sustain the value through expected failures.

**Decisive evidence.** Inject the expected dependency failure for the field and execute a supported operation. A non-null declaration is justified only when the runtime still supplies a value or intentionally bubbles to the documented ancestor.

The chapter’s decisive distinction is this: In GraphQL every output is nullable unless wrapped in non-null. Non-null is not a preference for clean client types. It is a promise that successful completion of the containing selection can always produce a value. If a non-null field resolves to null, the error bubbles to the nearest nullable ancestor, possibly nulling an entire object or the top-level data value.

## 2. Choose between `[Artifact!]` and `[Artifact!]!` for an independently available service.

Use `[Artifact!]` when Artifact Service can fail independently and no authoritative fallback exists. Present items remain valid; the list itself can be null with an error.

**Decisive evidence.** Disable Artifact Service while resolving a run. The chosen `[Artifact!]` contract must preserve the run, return `artifacts: null`, and attach a path-specific error rather than fabricate an empty list.

In the cumulative capstone, the rule becomes concrete: Project.analysisRuns is non-null because Analysis Control owns both project and run listing and the field is central to the root result. AnalysisRun.artifacts is nullable in the graph because Artifact Service can be unavailable independently. Returning an empty list during an outage would falsely claim authoritative emptiness. Null plus a path-specific error preserves truth.

## 3. What does an empty artifact list mean?

Artifact Service answered authoritatively that no artifacts exist. It must not be used to hide unavailability.

**Decisive evidence.** Run the healthy source with no artifacts and compare it with source unavailability. Only the healthy authoritative result may produce `[]`; the outage must remain distinguishable.

A useful way to reason about the boundary is: Review AnalysisRun.artifacts. Making it [Artifact!]! gives clients a simpler type but would null the whole run whenever Artifact Service is unavailable unless the gateway can provide an authoritative fallback. The honest release uses [Artifact!]; an empty list means authoritative empty, while null plus DOWNSTREAM UNAVAILABLE means no answer was available.

## 4. Why can adding an enum value require client review?

Generated clients may use exhaustive switches. The schema change is not a field removal, but supported clients may still crash or misbehave.

**Decisive evidence.** Compile or execute supported clients with an added enum member. Any exhaustive switch failure or unknown-value crash moves the change from automatic acceptance to explicit review.

The implementation consequence is: GraphQL enums are not arbitrary strings. Adding an enum value is often source-compatible for the schema but can break clients that compile exhaustive switches. Removing or renaming a value is clearly breaking. Before exposing a source-service enum, decide whether the graph owns a stable public vocabulary or merely passes through an internal state machine.

## 5. When is a union preferable to an interface?

Use a union when possible results do not share a meaningful client-facing field contract. Use an interface when shared fields are stable and useful.

**Decisive evidence.** Validate whether members share a meaningful field contract. Use an interface only when clients can safely select common fields; otherwise prove the union through inline-fragment operations.

The important nuance is: Use a union when alternatives share no field contract beyond being possible results. SearchResult = Project AnalysisRun Artifact forces clients to use typename and type conditions. That explicitness is useful: a search result cannot pretend that every member has name or status.

## 6. What must a custom DateTime scalar document?

Accepted input syntax, output serialization, timezone/offset requirements, precision, invalid values, and language mappings.

**Decisive evidence.** Validate canonical examples at boundaries: UTC offset handling, precision, leap-second policy, accepted lexical form, and serialization. Different language tracks must emit the same documented form.

Under concurrency or failure, the distinction becomes: A custom scalar creates a named semantic boundary, not automatic validation. DateTime, Cursor, and Version are useful only if the runtime defines how values are serialized, parsed, bounded, and rejected. The scalar implementation must be identical across query variables, literal values, results, persisted operations, and both language tracks.

## 7. Why is JSON a dangerous default scalar?

It removes field-level validation, selection, documentation, authorization, and compatibility evidence. Use it only for genuinely open or external data.

**Decisive evidence.** Search persisted operations and resolver outputs for untyped JSON. Each use must name its validation, size, compatibility, and authorization policy; unexplained JSON fails review.

The design remains honest only if: The release gate classifies an added output enum value as review-required, not automatically safe. Active operation validation cannot detect exhaustive client code, so client declarations and telemetry are part of the decision.

## 8. What is the semantic difference between omitted and explicit null input?

Omitted means no entry was supplied and defaults may apply; explicit null is a supplied null value if the type permits it. Patch semantics often depend on this difference.

**Decisive evidence.** Coerce one omitted variable and one explicit `null`. The resulting command or filter must show the intended distinction, especially for patch-like inputs and defaults.

The consumer-facing consequence is: Input coercion happens before execution. Missing, explicit null, defaulted, and present values are distinct. For an argument first: Int! = 20, omission produces the default, explicit null is invalid, and a positive integer is passed to admission. The GraphQL type system alone does not impose the course maximum; policy rejects values above the bounded page size.

## 9. What does @oneOf guarantee for NodeLookup?

Exactly one member is supplied and non-null. Multiple, zero, or null alternatives are rejected during coercion.

**Decisive evidence.** Run zero-member, two-member, null-member, and one-valid-member cases. Only exactly one supplied non-null lookup mode may reach the node dispatcher.

The operational consequence is: GraphQL September 2025 includes OneOf Input Objects. NodeLookup @oneOf requires exactly one non-null member. This models alternatives more truthfully than an input with several optional fields plus undocumented precedence. Framework support must be measured; the semantic rule remains part of the released schema.

## 10. Why should graph types not mirror database tables?

Storage is an implementation detail and often splits or combines differently from client concepts. Table mirroring leaks migrations into the public schema.

**Decisive evidence.** Compare the graph type with source-service contracts and persistence rows. A database-only column or join-table shape must not appear unless it is a deliberate client capability.

The strongest engineering interpretation is: Schema design starts from client tasks and stable domain language. A type may combine values supplied by several services, while each field retains a source. Conversely, two database tables may belong to one graph type if clients should not see the persistence split. Exposing tables mechanically produces awkward types, leaks implementation details, and makes schema evolution dependent on storage migrations.

## 11. When should a list element itself be nullable?

Only when positional absence is meaningful and clients can act on it. Do not use null elements to mask failed item resolution casually.

**Decisive evidence.** Inject a missing element inside an otherwise authoritative list. Nullable elements are justified only when preserving positions is meaningful and clients can act on the hole.

The defect-oriented view is: Use non-null items when an item without identity is unusable and the source can omit invalid rows before returning. Use a nullable list when the source dependency may fail independently. Avoid nullable list elements as a substitute for per-item error modeling unless the domain genuinely contains missing positions.

## 12. What evidence should justify changing a field to non-null?

Historical runtime evidence, source guarantee, failure testing, client compatibility, and a release plan. Type cleanliness alone is insufficient.

**Decisive evidence.** Provide outage, authorization, and historical-data evidence for all supported sources. The release gate must reject non-null promotion when any expected path can still produce null.

Across the Python and TypeScript tracks, the invariant is: Avoid making a field non-null merely because the current database column has a constraint. The graph promise must survive migrations, authorization redaction, remote-service failure, and historical records. Conversely, avoid making everything nullable to avoid thinking. Excessive nullability forces every client to handle impossible states and hides where the server actually owes a value.

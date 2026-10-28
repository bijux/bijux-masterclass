# Worked answers — Type System, Nullability, and Semantic Modeling

Compare the decision rule and evidence, not just wording.

## 1. Why is non-null an operational promise rather than a style preference?

A null value on a non-null field bubbles and can erase its parent. The declaration must match the runtime’s ability to sustain the value through expected failures.

**Decisive evidence.** Inject the expected dependency failure for the field and execute a supported operation. A non-null declaration is justified only when the runtime still supplies a value or intentionally bubbles to the documented ancestor.

## 2. Choose between `[Artifact!]` and `[Artifact!]!` for an independently available service.

Use `[Artifact!]` when Artifact Service can fail independently and no authoritative fallback exists. Present items remain valid; the list itself can be null with an error.

**Decisive evidence.** Disable Artifact Service while resolving a run. The chosen `[Artifact!]` contract must preserve the run, return `artifacts: null`, and attach a path-specific error rather than fabricate an empty list.

## 3. What does an empty artifact list mean?

Artifact Service answered authoritatively that no artifacts exist. It must not be used to hide unavailability.

**Decisive evidence.** Run the healthy source with no artifacts and compare it with source unavailability. Only the healthy authoritative result may produce `[]`; the outage must remain distinguishable.

## 4. Why can adding an enum value require client review?

Generated clients may use exhaustive switches. The schema change is not a field removal, but supported clients may still crash or misbehave.

**Decisive evidence.** Compile or execute supported clients with an added enum member. Any exhaustive switch failure or unknown-value crash moves the change from automatic acceptance to explicit review.

## 5. When is a union preferable to an interface?

Use a union when possible results do not share a meaningful client-facing field contract. Use an interface when shared fields are stable and useful.

**Decisive evidence.** Validate whether members share a meaningful field contract. Use an interface only when clients can safely select common fields; otherwise prove the union through inline-fragment operations.

## 6. What must a custom DateTime scalar document?

Accepted input syntax, output serialization, timezone/offset requirements, precision, invalid values, and language mappings.

**Decisive evidence.** Validate canonical examples at boundaries: UTC offset handling, precision, leap-second policy, accepted lexical form, and serialization. Different language tracks must emit the same documented form.

## 7. Why is JSON a dangerous default scalar?

It removes field-level validation, selection, documentation, authorization, and compatibility evidence. Use it only for genuinely open or external data.

**Decisive evidence.** Search persisted operations and resolver outputs for untyped JSON. Each use must name its validation, size, compatibility, and authorization policy; unexplained JSON fails review.

## 8. What is the semantic difference between omitted and explicit null input?

Omitted means no entry was supplied and defaults may apply; explicit null is a supplied null value if the type permits it. Patch semantics often depend on this difference.

**Decisive evidence.** Coerce one omitted variable and one explicit `null`. The resulting command or filter must show the intended distinction, especially for patch-like inputs and defaults.

## 9. What does @oneOf guarantee for NodeLookup?

Exactly one member is supplied and non-null. Multiple, zero, or null alternatives are rejected during coercion.

**Decisive evidence.** Run zero-member, two-member, null-member, and one-valid-member cases. Only exactly one supplied non-null lookup mode may reach the node dispatcher.

## 10. Why should graph types not mirror database tables?

Storage is an implementation detail and often splits or combines differently from client concepts. Table mirroring leaks migrations into the public schema.

**Decisive evidence.** Compare the graph type with source-service contracts and persistence rows. A database-only column or join-table shape must not appear unless it is a deliberate client capability.

## 11. When should a list element itself be nullable?

Only when positional absence is meaningful and clients can act on it. Do not use null elements to mask failed item resolution casually.

**Decisive evidence.** Inject a missing element inside an otherwise authoritative list. Nullable elements are justified only when preserving positions is meaningful and clients can act on the hole.

## 12. What evidence should justify changing a field to non-null?

Historical runtime evidence, source guarantee, failure testing, client compatibility, and a release plan. Type cleanliness alone is insufficient.

**Decisive evidence.** Provide outage, authorization, and historical-data evidence for all supported sources. The release gate must reject non-null promotion when any expected path can still produce null.

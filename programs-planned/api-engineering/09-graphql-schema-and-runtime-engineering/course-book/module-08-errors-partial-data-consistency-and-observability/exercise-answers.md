# Worked answers — Errors, Partial Data, Consistency, and Observability

Compare the decision rule and evidence, not just wording.

## 1. What prevents execution after a validation error?

The GraphQL execution pipeline does not run invalid operations. Admission and resolvers receive only selected, valid documents.

**Decisive evidence.** Submit an operation with an unknown field and instrument resolver entry. Validation must produce a request-error result and resolver/source counters remain zero.

## 2. Why include an error path?

It tells clients and operators which response position failed and supports correct partial-data handling.

**Decisive evidence.** Fail one nested artifact resolver in a two-edge response. The error path must include field aliases and list index so the exact null position is recoverable.

## 3. Why should concrete object IDs not be metric labels?

They create unbounded cardinality and can expose sensitive identifiers. Put them in controlled traces or logs.

**Decisive evidence.** Estimate metric-series growth when run or project IDs become labels. The cardinality guard must reject those dimensions and direct identifiers to controlled logs or traces.

## 4. What happens when a nullable field resolver fails?

The field becomes null, an execution error is recorded, and siblings can complete.

**Decisive evidence.** Disable an optional source. The field becomes null, siblings complete, and one execution error names the response path and source.

## 5. What happens when a non-null field resolves null?

The null bubbles to the nearest nullable ancestor, potentially nulling an object or all data.

**Decisive evidence.** Force a non-null field to complete with null. Verify bubbling reaches the nearest nullable ancestor and no response claims an impossible non-null position.

## 6. Why is `[]` not a generic fallback?

It asserts authoritative emptiness. During unavailability the truthful value is often null plus an error.

**Decisive evidence.** Compare a healthy authoritative empty result with outage. Tests must fail if the outage path returns `[]` without an error.

## 7. How is eventual consistency disclosed?

Return observation time or staleness metadata and apply the documented maximum-age policy.

**Decisive evidence.** Return `observedAt`, staleness age, or source version for the eventually consistent field and test behavior above the maximum-age policy.

## 8. What should a graph trace identify?

Operation hash/name, schema version, client, cost, field coordinates, batch sizes, downstream spans, cache outcomes, and stable error codes.

**Decisive evidence.** Inspect one trace for operation digest/name, client, schema release, admitted cost, field coordinates, batch sizes, downstream spans, cache outcomes, and stable error codes—without sensitive arguments.

## 9. How do you distinguish slow graph work from slow services?

Measure parse/validate/admit/compose phases separately and retain downstream child spans.

**Decisive evidence.** Inject host delay and downstream delay separately. Phase timers and child spans must attribute the latency to graph work or the source rather than one undifferentiated request duration.

## 10. When may partial data be unusable?

When a non-null critical field fails or the client cannot act safely without complete results. The schema and operation contract decide.

**Decisive evidence.** Use a supported client operation whose critical non-null path fails. Client behavior and schema semantics, not the mere presence of some sibling data, decide usability.

## 11. Why mask internal exception text?

It can leak implementation, credentials, SQL, paths, and topology. Stable public codes preserve utility without leakage.

**Decisive evidence.** Raise an exception containing SQL, file paths, tokens, and topology. The public response must contain a stable code and safe message while protected telemetry retains only approved details.

## 12. What proves partial failure semantics?

A controlled service outage with exact expected data null position, error path, code, and unaffected sibling values.

**Decisive evidence.** Run the declared outage fixture and compare exact data, errors, path, code, service, unaffected siblings, source-call log, and trace. All layers must agree.

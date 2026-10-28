# Worked Answers — Module 08: Errors, Partial Data, Consistency, and Observability

Use these solutions to audit your reasoning for **Errors, Partial Data, Consistency, and Observability**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. What prevents execution after a validation error?

The GraphQL execution pipeline does not run invalid operations. Admission and resolvers receive only selected, valid documents.

**Decisive evidence.** Submit an operation with an unknown field and instrument resolver entry. Validation must produce a request-error result and resolver/source counters remain zero.

The chapter’s decisive distinction is this: Execution errors occur after a valid operation begins: source unavailability, authorization denial, resolver exceptions, deadline expiry, or output completion failure. The response can contain both data and errors. Each error path identifies where the result became unavailable.

## 2. Why include an error path?

It tells clients and operators which response position failed and supports correct partial-data handling.

**Decisive evidence.** Fail one nested artifact resolver in a two-edge response. The error path must include field aliases and list index so the exact null position is recoverable.

In the cumulative capstone, the rule becomes concrete: An execution error includes a path such as analysisRun.artifacts or project.analysisRuns.edges[2].deliverySummary. The path identifies which response position could not be completed. A stable extension code supports client decisions and metrics; internal exception text is masked.

## 3. Why should concrete object IDs not be metric labels?

They create unbounded cardinality and can expose sensitive identifiers. Put them in controlled traces or logs.

**Decisive evidence.** Estimate metric-series growth when run or project IDs become labels. The cardinality guard must reject those dimensions and direct identifiers to controlled logs or traces.

A useful way to reason about the boundary is: Metrics use bounded dimensions. Traces may contain selected field coordinates as span events, but not one high-cardinality metric label per arbitrary path. Resolver spans are sampled or aggregated based on cost and failure; tracing every trivial scalar field produces noise.

## 4. What happens when a nullable field resolver fails?

The field becomes null, an execution error is recorded, and siblings can complete.

**Decisive evidence.** Disable an optional source. The field becomes null, siblings complete, and one execution error names the response path and source.

The implementation consequence is: A useful trace contains operation identity, schema version, client, admission cost, source-service spans, batch sizes, cache outcomes, and error coordinates. It does not create one metric label for arbitrary query text or field path with object IDs.

## 5. What happens when a non-null field resolves null?

The null bubbles to the nearest nullable ancestor, potentially nulling an object or all data.

**Decisive evidence.** Force a non-null field to complete with null. Verify bubbling reaches the nearest nullable ancestor and no response claims an impossible non-null position.

The important nuance is: If the field were [Artifact!]!, the same failure would make the run object invalid. If the connection node were non-null, null could bubble through the edge, connection, project, and potentially top-level data. The schema therefore determines blast radius.

## 6. Why is `[]` not a generic fallback?

It asserts authoritative emptiness. During unavailability the truthful value is often null plus an error.

**Decisive evidence.** Compare a healthy authoritative empty result with outage. Tests must fail if the outage path returns `[]` without an error.

Under concurrency or failure, the distinction becomes: Partial service failure differs from an authoritative empty result. An empty artifacts list means Artifact Service answered and owns no artifacts for the run. Null plus an error means the service did not provide an answer.

## 7. How is eventual consistency disclosed?

Return observation time or staleness metadata and apply the documented maximum-age policy.

**Decisive evidence.** Return `observedAt`, staleness age, or source version for the eventually consistent field and test behavior above the maximum-age policy.

The design remains honest only if: DeliverySummary is eventually consistent. The response includes observation time and staleness seconds. A summary within policy is data; one beyond policy may become null with STALE PROJECTION. The gateway never labels a stale replica authoritative.

## 8. What should a graph trace identify?

Operation hash/name, schema version, client, cost, field coordinates, batch sizes, downstream spans, cache outcomes, and stable error codes.

**Decisive evidence.** Inspect one trace for operation digest/name, client, schema release, admitted cost, field coordinates, batch sizes, downstream spans, cache outcomes, and stable error codes—without sensitive arguments.

The consumer-facing consequence is: A useful trace contains operation identity, schema version, client, admission cost, source-service spans, batch sizes, cache outcomes, and error coordinates. It does not create one metric label for arbitrary query text or field path with object IDs.

## 9. How do you distinguish slow graph work from slow services?

Measure parse/validate/admit/compose phases separately and retain downstream child spans.

**Decisive evidence.** Inject host delay and downstream delay separately. Phase timers and child spans must attribute the latency to graph work or the source rather than one undifferentiated request duration.

The operational consequence is: Resolver spans link to the existing service traces from Course 4. The graph gateway records composition time separately from downstream time. This lets operators distinguish slow parsing, overloaded admission, N+1 behavior, and source latency.

## 10. When may partial data be unusable?

When a non-null critical field fails or the client cannot act safely without complete results. The schema and operation contract decide.

**Decisive evidence.** Use a supported client operation whose critical non-null path fails. Client behavior and schema semantics, not the mere presence of some sibling data, decide usability.

The strongest engineering interpretation is: Some operations require all-or-nothing usefulness even if the schema permits partial data. A client can declare this in its operation contract, and the gateway can classify the outcome as incomplete for SLO or caching purposes. The GraphQL response remains standards-shaped; product-level completeness is an additional policy.

## 11. Why mask internal exception text?

It can leak implementation, credentials, SQL, paths, and topology. Stable public codes preserve utility without leakage.

**Decisive evidence.** Raise an exception containing SQL, file paths, tokens, and topology. The public response must contain a stable code and safe message while protected telemetry retains only approved details.

The defect-oriented view is: If the client aliases artifacts to outputs, the path uses outputs. This lets a client connect an error to the exact location in data. The server should also attach a stable bounded code in extensions, such as SOURCE UNAVAILABLE, FORBIDDEN, or DEADLINE EXCEEDED.

## 12. What proves partial failure semantics?

A controlled service outage with exact expected data null position, error path, code, and unaffected sibling values.

**Decisive evidence.** Run the declared outage fixture and compare exact data, errors, path, code, service, unaffected siblings, source-call log, and trace. All layers must agree.

Across the Python and TypeScript tracks, the invariant is: Artifact Service fails while Analysis Control succeeds. The run object remains, artifacts is null, and the errors array includes path analysisRun.artifacts, stable code, and service. Returning [] would be semantically false; making artifacts non-null would bubble away useful run data.

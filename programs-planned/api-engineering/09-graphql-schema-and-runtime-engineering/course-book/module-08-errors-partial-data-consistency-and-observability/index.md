# Errors, Partial Data, Consistency, and Observability

**Module 08 of 10**

> **Governing question:** How does the graph tell the truth when some fields succeed, some fail, and some are stale?

## Place in the program

Courses 1–8 established the contract, durable implementation, security, operations, performance, asynchronous events, typed RPC, and distributed ownership. Module 08 applies those guarantees to the graph interface; none are reset at the GraphQL boundary.

## Learning outcomes

- separate request and execution errors

- use error paths and stable codes

- predict null bubbling

- disclose staleness and partiality

- trace graph execution without cardinality explosions

## Capstone result

Return truthful partial data with path-specific errors and traces.

## Request errors and execution errors differ

Parse, validation, variable coercion, and operation-admission errors prevent execution. Their response has no meaningful field data. Execution errors happen after a valid operation begins and can coexist with partial data.

The distinction matters operationally. A spike in validation failures may indicate a client rollout or attack. A spike in `DOWNSTREAM_UNAVAILABLE` on `AnalysisRun.artifacts` indicates Artifact Service failure. Grouping both as GraphQL errors without phase loses the diagnostic signal.

## Error paths connect failures to data

An execution error includes a path such as `analysisRun.artifacts` or `project.analysisRuns.edges[2].deliverySummary`. The path identifies which response position could not be completed. A stable extension code supports client decisions and metrics; internal exception text is masked.

Path cardinality must be controlled in telemetry. Record the schema coordinate and error code as metric dimensions, while keeping concrete object IDs in traces or sampled logs under privacy policy.

## Null propagation enforces the schema promise

When a nullable field fails, its value becomes null and siblings can remain. When a non-null field fails, null bubbles to the nearest nullable ancestor. This behavior makes nullability an operational design decision.

The capstone declares independently sourced artifact and delivery fields nullable. An Artifact Service outage therefore preserves authoritative run fields. `Project.analysisRuns` remains non-null; if Analysis Control cannot produce it, the project object cannot satisfy the contract and bubbles accordingly.

## Staleness and completeness are data semantics

`DeliverySummary` is eventually consistent. The response includes observation time and staleness seconds. A summary within policy is data; one beyond policy may become null with `STALE_PROJECTION`. The gateway never labels a stale replica authoritative.

Partial service failure differs from an authoritative empty result. An empty artifacts list means Artifact Service answered and owns no artifacts for the run. Null plus an error means the service did not provide an answer.

## Tracing graph execution

A useful trace contains operation identity, schema version, client, admission cost, source-service spans, batch sizes, cache outcomes, and error coordinates. It does not create one metric label for arbitrary query text or field path with object IDs.

Resolver spans link to the existing service traces from Course 4. The graph gateway records composition time separately from downstream time. This lets operators distinguish slow parsing, overloaded admission, N+1 behavior, and source latency.

## Two error populations

GraphQL distinguishes failures that prevent execution from failures that occur during execution.

**Request errors** include parse errors, operation-selection errors, validation errors, and variable-coercion errors. The server does not execute fields and the response does not contain a partially executed result.

**Execution errors** occur after a valid operation begins: source unavailability, authorization denial, resolver exceptions, deadline expiry, or output completion failure. The response can contain both `data` and `errors`. Each error path identifies where the result became unavailable.

This distinction is more than terminology. It drives source-call oracles, HTTP profile behavior, client retry decisions, SLO populations, and security telemetry. A validation error should not count as a dependency outage. A source timeout should not be reported as malformed client demand.

## Error paths and aliases

An execution error path uses response keys, including aliases and list indices. For a failure in the first run's artifact field, a path might be:

```json
["project", "analysisRuns", "edges", 0, "node", "artifacts"]
```

If the client aliases `artifacts` to `outputs`, the path uses `outputs`. This lets a client connect an error to the exact location in `data`. The server should also attach a stable bounded code in `extensions`, such as `SOURCE_UNAVAILABLE`, `FORBIDDEN`, or `DEADLINE_EXCEEDED`.

Do not place stack traces, raw downstream responses, tokens, database identifiers, or private hostnames in `extensions`. Correlation IDs and retry classification are safer operational metadata.

## Null propagation walkthrough

Suppose `AnalysisRun.artifacts` is nullable. Artifact Service fails for one run. The field becomes null, an error path is added, and the surrounding run and project remain.

If the field were `[Artifact!]!`, the same failure would make the run object invalid. If the connection node were non-null, null could bubble through the edge, connection, project, and potentially top-level data. The schema therefore determines blast radius.

Output completion can also fail when a resolver returns an invalid value: a null for `id: ID!`, a string for `size: Int!`, or an unresolved union type. Treat these as server contract failures, not client errors. Tests should inject such values and prove the runtime does not silently serialize them.

## Partial data must be honest

Partial data is useful only when clients can tell what is authoritative, absent, forbidden, stale, or unknown. The capstone uses three mechanisms:

- null plus a path-specific execution error for independently unavailable fields;
- explicit staleness metadata for projection-backed delivery summaries;
- stable mutation-result objects for expected domain outcomes.

Do not replace a failed remote list with `[]`, a stale count with zero, or a forbidden string with an empty string. Those values claim successful knowledge. A client cannot recover if the server erases uncertainty.

Some operations require all-or-nothing usefulness even if the schema permits partial data. A client can declare this in its operation contract, and the gateway can classify the outcome as incomplete for SLO or caching purposes. The GraphQL response remains standards-shaped; product-level completeness is an additional policy.

## Consistency in a composed graph

One response can contain facts observed at different times. Analysis Control may return the current run version while Notification Service returns a projection observed fifteen seconds earlier. The graph must not imply one database snapshot across services.

The consistency policy records:

- authoritative source per field;
- projection or cache source where used;
- maximum declared age;
- version or observation timestamp;
- behavior when age exceeds policy;
- whether the client operation tolerates staleness.

`DeliverySummary` carries `observedAt` and `stalenessSeconds`. A cache or projection does not become authoritative simply because it is convenient for graph composition. Mutations always return the owning service's committed result.

## Observability without cardinality explosion

A GraphQL host needs operation-aware telemetry, but naïve field-level labels can overwhelm metric systems. The course uses:

- operation name or persisted digest, never raw document text;
- schema and gateway release;
- outcome phase and bounded error code;
- total calculated cost and source-service set;
- downstream call counts and durations;
- loader batch size and cache-hit summary;
- partial/complete outcome;
- subscription sequence and gap category where applicable.

Metrics use bounded dimensions. Traces may contain selected field coordinates as span events, but not one high-cardinality metric label per arbitrary path. Resolver spans are sampled or aggregated based on cost and failure; tracing every trivial scalar field produces noise.

The trace structure should mirror architecture:

```text
graphql.request
  ├─ operation.admission
  ├─ analysis-control.list-runs
  ├─ artifact-service.batch-artifacts
  └─ notification-service.batch-summaries
```

Asynchronous subscription delivery links to event trace context rather than pretending the long-lived connection is one synchronous parent span.

## HTTP status and response semantics

The course HTTP profile separates host failures from GraphQL responses. Malformed JSON, unsupported media type, or authentication middleware failure remains an HTTP error. A GraphQL request or execution response uses the GraphQL response media type and carries GraphQL errors.

Do not derive operational success from HTTP 200 alone. A response can be HTTP-successful while containing no data because validation failed, or partial data with a source timeout. SLIs use GraphQL phase and operation-completeness evidence.

## Error-policy review checklist

For every failure path, decide:

- phase that discovers it;
- whether field execution occurred;
- GraphQL error code and safe message;
- error path and null-propagation effect;
- whether data is partial, stale, forbidden, absent, or unknown;
- HTTP-profile status and media type;
- client retry classification;
- SLI population;
- trace and metric attributes;
- cacheability and invalidation behavior.

The module lab injects independent source failures and output-type violations. The checkpoint passes only when the returned data tree, error paths, telemetry phase, and source-call evidence all agree with the schema.

## Worked capstone review

Artifact Service fails while Analysis Control succeeds. The run object remains, `artifacts` is null, and the errors array includes path `analysisRun.artifacts`, stable code, and service. Returning `[]` would be semantically false; making artifacts non-null would bubble away useful run data.

## Python and TypeScript implications

Both tracks represent partial results as data plus structured errors. The optional frameworks may format errors differently internally, but public extension codes and paths remain stable.

## Evidence required before the next module

Complete the lab and checkpoint. The decisive artifact is the module report under `reports/module-08-*.json`; prose claims without its oracle do not pass.

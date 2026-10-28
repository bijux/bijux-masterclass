# Module 03 — Resolver Architecture, Batching, and Source Ownership

> **Program stage:** Course 9 of 10 — Compose governed client-shaped capabilities.

> **Central question:** How can nested graph execution remain faithful to service ownership without producing N+1 calls?

## Where this module fits

Module 02 produced **Release Analysis Graph API 1.0 type and nullability policies**. This module extends that result by asking: **How can nested graph execution remain faithful to service ownership without producing N+1 calls?**

The new capstone increment is **Replace N+1 nested calls with request-scoped batching**. It becomes the prerequisite for **Queries, Identifiers, Connections, and Pagination**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Map every field to one source.
- Construct request-scoped context.
- Explain and measure N+1.
- Implement batch loaders.
- Divide deadlines and observe fan-out.

## Capstone increment

Replace N+1 nested calls with request-scoped batching.

## Resolvers are adapters to authorities

A field resolver converts parent value, arguments, context, and selected information into a field value. It should not decide a business rule owned elsewhere. `Mutation.startAnalysis` delegates to Analysis Control. `AnalysisRun.artifacts` calls Artifact Service. The gateway may map service errors and identifiers, but it does not recreate run state transitions or artifact authorization.

A resolver ownership map gives every field a source. Fields computed entirely from the parent—such as formatting a stable global identifier—may be gateway-owned composition. The distinction is explicit and reviewable.

## Request context is not a global variable

The context carries authenticated principal, tenant, request identifier, deadline, client identity, loaders, and trace state for one operation. Request-scoped construction prevents cache leakage between users. A loader placed in a process-global singleton can return tenant A data to tenant B even when the source batch call was authorized correctly.

Context is immutable where possible. Resolver-local mutations create ordering dependencies that GraphQL query execution does not promise. Shared mutable state belongs in the owning service or a clearly synchronized request object.

## Why N+1 appears

GraphQL executes a field for each parent value. A project with twenty runs can cause twenty artifact calls and twenty notification calls if nested resolvers call services directly. The schema looks elegant while latency, load, and failure probability multiply.

N+1 is not solved by one generic cache. The runtime must collect compatible keys, perform a batch call to the correct owner, preserve output order, represent missing keys, and scope cached values to the request and authorization context.

## Batch loaders and dispatch boundaries

A batch loader collapses duplicate keys and dispatches them together. The source method returns a map keyed by requested identity; the loader restores each result to its resolver. The key must include every dimension that changes authorization or representation. A run identifier alone is insufficient if two tenants can use the same local identifier or if the field has locale variants.

Dispatch timing matters. A loader that dispatches immediately still performs N calls. A loader that waits without a bound can delay the entire operation. Complete GraphQL runtimes schedule field work in waves; the dependency-light course core makes dispatch explicit so the batching invariant is visible.

## Composition budgets and timeouts

One graph operation can call several services. Each call consumes the absolute request deadline inherited from Course 4. A resolver cannot start a fresh full timeout. The graph admission report estimates service fan-out before execution; runtime telemetry records actual calls and latency.

Batching reduces call count, not source workload automatically. A batch of ten thousand keys can still overwhelm a service, which is why list size and batch size are bounded. Batches may need chunking under a remaining deadline.

## Resolver boundaries

A resolver should be small, but “small” does not mean “contains no architecture.” Its responsibilities are precise:

1. read typed parent and argument values;
2. read the authenticated request context;
3. enforce field-specific policy or call a policy decision point;
4. obtain the remaining request budget;
5. call the source authority or a request-scoped loader;
6. translate source outcomes into graph values or typed execution errors;
7. attach bounded telemetry.

It must not own source-service transactions, reconstruct business rules, write another service's data, hide consistency, or start unbounded parallel work. Mutation resolvers delegate commands. Query resolvers obtain observations. Composition resolvers combine already-owned facts under a declared budget.

A resolver may be only ten lines and still violate every boundary if it opens a database connection to another service's tables. Conversely, a slightly longer adapter that decodes identity, checks policy, allocates a child deadline, and maps a source problem can be the correct design.

## Request context and lifetime

The request context is the trusted carrier for values established once per operation:

- subject and tenant;
- permissions and authentication assurance;
- trace and correlation identifiers;
- absolute deadline and cancellation signal;
- persisted-operation identity;
- schema and gateway release;
- request-scoped loaders;
- telemetry sink;
- bounded cache for repeated values.

Never place these values in process-global mutable state. GraphQL executes sibling fields concurrently in many runtimes, and one process serves many tenants. A global “current user” or global loader can leak data across requests. Async-local context can improve ergonomics, but explicit resolver context remains the ownership boundary and must be set and cleared correctly.

Loaders are request-scoped for the same reason. Their cache is a consistency and authorization decision, not a general application cache. A loader key should include every dimension that changes the result: tenant, principal or policy class where needed, source version, and local identity. The safest course design creates loaders after authentication and discards them with the operation.

## The N+1 mechanism

Assume one query loads twenty runs and selects `artifacts` for each run. A naïve field resolver produces:

```text
1 call: list twenty runs
20 calls: artifacts for run 1 ... run 20
---------------------------------------
21 calls for one field shape
```

Nested fields can multiply this further. If each artifact resolves an owner or storage tier independently, the call count becomes proportional to the product of list sizes. Latency becomes the maximum of many calls, connection pools saturate, and downstream services see bursts that the top-level request rate does not reveal.

A batch loader collects keys requested during one dispatch interval, deduplicates them, and calls a batch source method:

```text
load(run-1) ┐
load(run-2) ├─ dispatch → getArtifactsByRunIds([run-1, run-2, ...])
load(run-1) ┘
```

The batch result must preserve input-key association. Returning a positional list without checking keys is unsafe when the source omits missing records or returns a different order. The reference loader accepts a mapping and reconstructs values in requested order.

Batching does not make an unbounded query safe. A query that requests one thousand parents can still create a one-thousand-key batch. Admission bounds list cardinality; the loader bounds batch size and may split work into controlled chunks. Both controls are required.

## Loader semantics that frequently fail

**Caching `None` blindly.** A missing record can be authoritative, policy-concealed, or caused by a source failure. Cache only outcomes whose semantics are stable for the request.

**Reusing loaders across tenants.** A key of `artifact-7` is insufficient if the same local identifier can exist in another tenant or if policy differs.

**Loading after cancellation.** Dispatch must observe the operation deadline and cancellation signal. A client disconnect should not leave a large batch running without value.

**Hiding partial source errors.** A batch response may contain per-key problems. Map them to the corresponding graph paths rather than failing unrelated keys.

**Using one loader for differently authorized fields.** `Artifact.metadata` and `Artifact.downloadUrl` may require different permissions. A cached object must not bypass field-level output policy.

## Composition budgets

Course 4 established absolute deadlines and Course 5 established admission and concurrency controls. The graph gateway composes them. It receives one absolute deadline, reserves host overhead, and divides the remaining budget among source calls. Child calls never receive independent full timeouts.

For `GetProjectOverview`, one possible budget is:

```text
client deadline                    1,000 ms
host parse/validate/admit reserve     50 ms
Analysis Control budget             350 ms
Artifact batch budget                250 ms
Notification batch budget            200 ms
completion/serialization reserve     100 ms
safety margin                         50 ms
```

The exact numbers are workload evidence, not universal constants. The invariant is that child budgets fit within the parent budget and cancellation propagates. Retrying a source call consumes the same remaining budget and retry allowance; it does not reset the clock.

Parallel calls can reduce latency but increase instantaneous load. The execution plan must bound parallelism and preserve source-service bulkheads. A gateway that launches every nested call concurrently can become an amplification device.

## Python and TypeScript implementation pattern

The two tracks implement the same sequence idiomatically:

```python
async def artifacts(run, info):
    context = info.context
    context.policy.require("ARTIFACT_READ", run_id=run.id)
    context.deadline.raise_if_expired()
    return await context.artifacts_by_run.load(
        (context.tenant_id, run.id)
    )
```

```ts
async function artifacts(run: Run, ctx: Context): Promise<Artifact[] | null> {
  ctx.policy.require("ARTIFACT_READ", { runId: run.id });
  ctx.deadline.throwIfExpired();
  return ctx.artifactsByRun.load([ctx.tenantId, run.id]);
}
```

The syntax is not the lesson. The guarantees are: request scope, explicit policy, budget propagation, tenant-bound key, batched source authority, and a nullable failure contract.

## Resolver review method

For each resolver, inspect:

- the exact source-service method;
- number of calls as parent cardinality grows;
- batch-key identity and result association;
- authorization before and after object loading;
- deadline and cancellation propagation;
- handling of missing, forbidden, stale, and unavailable outcomes;
- telemetry attributes and privacy;
- whether the resolver adds a dependency-graph edge;
- whether the field remains correct under partial source failure.

The module lab runs one operation over many parent objects, records source calls, then introduces a deliberately per-parent resolver. The checkpoint passes only when call count stays bounded and cross-request cache leakage remains impossible.

## Worked capstone review

Two runs selected under one project schedule two artifact keys and two delivery keys. Each loader collapses duplicates and performs one service batch. A third occurrence of `run-1` reuses the request token. A second HTTP request creates new loaders, so no authorized value leaks across principals.

## Python and TypeScript implications

Both tracks implement a request-scoped `BatchLoader`. Python uses explicit load tokens and dispatch; TypeScript uses a generic loader. The shared invariant is one batch call per compatible key set and zero cross-request cache hits.

## Evidence required before the next module

Complete the lab and checkpoint. The decisive artifact is the module report under `reports/module-03-*.json`; prose claims without its oracle do not pass.

## Module synthesis

You are ready to leave this module when you can **map every field to one source, construct request-scoped context, and explain and measure N+1** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Use a dataset containing at least twenty runs, duplicate run references, and two tenants with overlapping local identifiers** and requiring the following oracle: **| Property | Required result | |---|---| | growth | source call count does not grow linearly with parent count | | duplicates | one source key per unique request-scoped identity | | association | values return to the correct keys despite source ordering | | tenancy | no cross-tenant or cross-request cache reuse | | authorization | denied keys do not enter an unauthorized source call | | cancellation | no unresolved loader future or runaway dispatch | | bounds | batch size never exceeds policy |**

The cumulative platform now includes **Replace N+1 nested calls with request-scoped batching**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Queries, Identifiers, Connections, and Pagination](../module-04-queries-identifiers-connections-and-pagination/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.

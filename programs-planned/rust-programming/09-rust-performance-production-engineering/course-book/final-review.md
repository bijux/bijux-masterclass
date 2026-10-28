# Course 9 Final Review

Complete this review after finishing Module 90 and the MetricRail capstone. Begin without consulting the chapters, source code, or notes. After the closed-book pass, use the course to correct weak answers and record what changed. The purpose is not recall for its own sake. It is to determine whether you can reconstruct the production-engineering method when a new system has different APIs, workloads, and failure modes.

A strong answer always separates four things:

1. what the program is required to mean;
2. what resources and failure states are bounded by design;
3. what a particular experiment observed under declared conditions;
4. what operational policy authorizes a release, retry, degradation, or rollback.

Do not use “fast,” “safe,” “reliable,” “observable,” “zero copy,” “production ready,” or “reproducible” as conclusions unless the rest of the answer supplies the contract and evidence behind the word.

## Part 0 — Reconstruct the production-engineering loop

Without notes, draw the complete reasoning loop used throughout this course. Your reconstruction must include at least these transitions:

```text
product objective
      ↓
semantic and resource contracts
      ↓
representative workload and correctness oracle
      ↓
measurement or review evidence
      ↓
causal hypothesis
      ↓
smallest justified intervention
      ↓
regression and displaced-cost checks
      ↓
release identity and operational policy
      ↓
rollout observation and incident learning
```

For every arrow, write one failure mode caused by skipping it. For example, moving from a profiler directly to a code rewrite can optimize an incidental frame, while moving from a benchmark result directly to rollout can ignore memory, tail latency, or compatibility damage.

Then answer these questions:

1. Why is “the implementation is faster” not a sufficient optimization claim?
2. Why is a benchmark a controlled model rather than a miniature production environment?
3. Why must the correctness oracle be executed before interpreting a performance result?
4. Why can a release be technically correct yet operationally unsafe?
5. Why is an unknown not automatically a blocker, and what makes an unknown acceptable for a limited rollout?

## Part 1 — Claim classification

For each statement, classify it as one of the following:

- semantic contract;
- resource contract;
- toolchain or artifact contract;
- measured observation;
- operational policy;
- unsupported claim.

Then rewrite the statement so that a reader can tell its scope, conditions, evidence, and limitations.

1. “The parser is zero copy.”
2. “The release binary is fast.”
3. “Queue depth is always exact.”
4. “The service is available.”
5. “The binary is reproducible.”
6. “Retries prevent failures.”
7. “Memory use is 24 bytes because the vector is 24 bytes.”
8. “Rust prevents security bugs.”
9. “p99 is 20 ms.”
10. “The health endpoint proves the dependency is healthy.”
11. “The optimized build is the same program.”
12. “A bounded channel bounds service memory.”
13. “The profiler proves hashing is slow.”
14. “No vulnerabilities were found.”
15. “The canary is healthy.”

A complete repair of the percentile statement, for example, identifies the operation population, workload, sample count, time window, host or environment, release identity, and whether failed or rejected operations were included.

## Part 2 — Benchmark design

You must compare two implementations of a telemetry parser. The candidate borrows fields from the input and validates numbers in place. The baseline splits the line into temporary strings and then builds owned domain values.

Write a benchmark charter containing:

- the exact operation boundary;
- the product decision the benchmark informs;
- the semantic correctness oracle;
- valid, malformed, boundary-size, and hot-identifier workload classes;
- corpus source and digest;
- setup excluded from the measured region;
- work deliberately included in the measured region;
- pinned toolchain, target, profile, features, and lockfile;
- parameters and sample sizes;
- warm-up and outlier policy;
- likely optimizer traps;
- latency and throughput summaries;
- allocation or retained-memory displaced costs;
- a predeclared decision threshold;
- an end-to-end confirmation scenario.

Now diagnose each weak experiment:

1. One parse is timed with `Instant::now()` in a debug build.
2. The baseline reads a file inside the measured region, while the candidate receives an in-memory slice.
3. The benchmark uses only one 24-byte valid record.
4. The candidate returns a constant because the result is never observed.
5. The benchmark reports a 4% difference without variance, sample count, or regression threshold.
6. The microbenchmark improves, but request p99 and peak memory worsen in the service scenario.

For each case, state whether the defect invalidates the comparison, narrows its interpretation, or reveals a displaced cost that changes the product decision.

Finish by explaining why a single wall-clock measurement cannot authorize a code change, and why a statistically stable result can still be irrelevant to the product.

## Part 3 — Profile and cost model

A representative scenario report shows:

```text
parse          8%
hash/lookup   37%
allocation    21%
sorting        4%
rendering     18%
other         12%
```

The team proposes manually unrolling the parser.

1. Explain why the proposal is weak.
2. Write at least three competing hypotheses for the hash/lookup cost.
3. Design a scaling experiment that varies unique series, identifier length, hot-key concentration, and input order.
4. Name the additional evidence required to distinguish CPU work from lock wait, cache misses, allocator contention, and queue residence.
5. Describe the semantic, memory, and operational trade-offs of interning identifiers.
6. Describe the trade-offs of changing the map, hash function, or key representation.
7. State what result would cause you to stop optimizing this path.
8. State what result would make you investigate a different layer despite the 37% profile share.

Draw a cost model for one accepted record. It should identify parsing, identifier validation, ownership promotion, lookup, aggregate update, queue wait, response rendering, and observability work. Mark which costs are fixed, input-dependent, state-size-dependent, contention-dependent, or optional. The model need not predict exact nanoseconds; it must produce testable hypotheses.

## Part 4 — Allocation, memory, and data movement

A service stores a 12-byte field as a shared view into a 1 MiB received frame.

Trace:

- inline handle representation;
- backing allocation;
- all owners and clones;
- queue movement;
- storage retention;
- last-use point;
- release of the backing allocation.

Compare that design with copying the 12 bytes into a compact owned value. Include:

- allocation count;
- live-byte peak;
- lifetime coupling;
- cache locality;
- API complexity;
- thread-transfer requirements;
- debugging difficulty;
- worst-case retention under many requests.

State when the copy is cheaper at product level even though it performs more byte copying.

Then create an ownership-cost ledger for this pipeline:

```text
socket buffer
    → connection buffer
    → parsed borrowed fields
    → validated owned identifiers
    → broker command
    → aggregate key
    → deterministic snapshot
    → response buffer
```

For every arrow, state:

- whether bytes are borrowed, moved, shared, or copied;
- who owns the backing storage;
- what event releases it;
- whether the transition is required by lifetime or architecture;
- what measurement would justify changing it.

Explain why `size_of::<Vec<T>>()`, allocation count, resident memory, retained heap bytes, and peak live bytes answer different questions.

## Part 5 — Runtime saturation and capacity

A load test produces:

| Offered/s | Admitted/s | Completed/s | p95 response | Queue depth |
|---:|---:|---:|---:|---:|
| 1,000 | 1,000 | 1,000 | 8 ms | 2 |
| 2,000 | 2,000 | 1,990 | 15 ms | 20 |
| 3,000 | 3,000 | 2,400 | 180 ms | 900 |
| 4,000 | 3,100 | 2,350 | 900 ms | 1,024 |

Identify:

- the likely saturation knee;
- why the final row does not prove 3,100/s useful capacity;
- the distinction among offered, admitted, started, and completed work;
- the additional queue-wait and service-time data required;
- the admission policy you would test;
- a safe initial production envelope;
- the failover and rollout headroom you would reserve.

Now assume CPU is 45%, memory is stable, and queue residence dominates response latency. Write at least four hypotheses, including one serialized authority, one downstream wait, one runtime scheduling issue, and one hidden capacity limit. For each hypothesis, define one signal and one controlled experiment that could falsify it.

Finally, review a batching proposal. The batcher may hold at most 256 items, but has no byte or age limit. Explain why the item bound is insufficient. Design a batching contract with maximum items, bytes, age, memory, and shutdown behavior. State which workload could benefit and which latency-sensitive workload should reject the design.

## Part 6 — Observability and diagnostic context

Design the signals for:

- ingestion request;
- malformed line;
- overload rejection;
- snapshot generation;
- dependency retry;
- readiness degradation;
- graceful shutdown;
- invariant violation.

For each event, choose an event, span, metric, audit record, or combination. Define:

- stable name;
- fields;
- units;
- label set;
- expected cardinality;
- redaction policy;
- source of truth;
- whether the signal is exact, sampled, approximate, or advisory;
- retention and access expectations.

Explain why arbitrary tenant, path, error-message, or request identifiers are dangerous metric labels. Give a trace field that is useful but unsafe as a metric label, and explain the distinction.

A dashboard shows high p99 response latency, normal CPU, flat error rate, and rising queue depth. Write the next five questions you would answer before editing code. The questions must distinguish admission wait, broker queue residence, lock wait, downstream wait, runtime starvation, and response-write delay.

Design one health endpoint and one readiness decision. State why neither proves end-to-end correctness, and how readiness changes during quiescing, dependency failure, store exhaustion, and a telemetry-exporter outage.

## Part 7 — Reliability, SLOs, and retry policy

Define one ingestion availability SLI, one latency SLI, one overload SLI, and one snapshot-freshness SLI. For each, specify numerator, denominator, exclusions, measurement point, window, and failure interpretation.

Then write a complete retry policy for an idempotent dependency call with a 750 ms user deadline. Include:

- retryable and non-retryable classes;
- maximum attempts;
- per-attempt timeout;
- one overall deadline;
- exponential or other bounded backoff;
- jitter policy;
- server retry hints;
- ambiguous commit handling;
- idempotency-key ownership and retention;
- retry telemetry;
- final returned outcome.

Show with a timeline how three independent 400 ms attempt timeouts can violate a 750 ms user deadline. Repair the policy using one absolute deadline.

Design a degraded mode for snapshot pressure. The mode must state:

- what remains available;
- what is rejected;
- whether data is complete or stale;
- how callers detect degradation;
- how recovery is detected;
- which correctness checks remain non-negotiable.

Explain why a degraded mode that silently omits rows is worse than an explicit rejection.

## Part 8 — Security and supply-chain reasoning

For a telemetry service, write a threat model containing:

- at least five assets;
- four actors or actor classes;
- six trust boundaries;
- eight abuse cases;
- controls and tests;
- residual risks and their owners.

The abuse cases must include malformed numeric input, line-size exhaustion, series-cardinality exhaustion, identifier-memory exhaustion, snapshot amplification, connection exhaustion, log injection or secret leakage, and dependency/build compromise.

Add the build and delivery path:

```text
source revision
  → dependency resolution
  → build script or generated input
  → compiler and linker
  → CI credentials
  → packaged artifact
  → artifact store
  → deployment system
```

For every edge, state the trust assumption and one possible control. Distinguish a vulnerability scan, an advisory database result, dependency review, provenance evidence, and exploitability analysis. “No known advisory” is not equivalent to “secure.”

Review this proposed control: “Log the entire malformed record so incidents are easy to debug.” Identify confidentiality, integrity, availability, and cardinality risks. Replace it with a bounded diagnostic design.

## Part 9 — Cargo profiles, release identity, and CI

Create a release record containing:

- semantic version;
- source revision;
- dirty-tree state;
- lockfile digest;
- Rust toolchain;
- target triple;
- Cargo profile;
- enabled features;
- dependency metadata;
- configuration-schema version;
- protocol and storage compatibility versions;
- artifact digest;
- build invocation;
- test and benchmark evidence identifiers.

Explain why a profiling artifact and a distribution artifact may deliberately differ. State which profile settings support useful profiles and which distribution settings prioritize size, startup, or runtime performance. Do not claim that one profile is universally best.

Design a feature matrix. Separate:

- combinations checked on every change;
- target-specific combinations;
- expensive periodic combinations;
- unsupported combinations that should fail early.

Design CI stages for formatting, linting, unit tests, integration tests, documentation tests, compiler investigations, security review, benchmarks, package construction, clean-machine installation, smoke tests, and rollback rehearsal. State which failures block merging, which block release, and which create a reviewed warning.

Finally, explain what “reproducible release” can mean at three strengths:

1. rebuildable from recorded inputs;
2. behaviorally equivalent under defined tests;
3. byte-for-byte identical.

State which strength the release process actually claims and what evidence would be required for the strongest claim.

## Part 10 — Rollout, capacity, and incident learning

You are given a service that passes all tests and meets its median latency target. Prepare a 15-minute production-readiness defense covering:

- semantic correctness;
- tail behavior;
- resource envelope;
- saturation knee;
- overload behavior;
- observability;
- security;
- dependency and toolchain trust;
- artifact identity;
- capacity and failover headroom;
- rollout stages;
- rollback trigger and mechanism;
- incident response.

The rollout plan must define:

- the first exposure population;
- maximum duration of each stage;
- success and failure signals;
- comparison baseline;
- automatic stop conditions;
- manual review conditions;
- configuration compatibility;
- rollback artifact and data implications.

Finish with three reasons to reject deployment and three unknowns that can be accepted temporarily if they are bounded, observable, reversible, and owned.

## Part 11 — Incident reconstruction

MetricRail version `9.3.0` is rolled out to 10% of traffic. Within eight minutes:

```text
accepted throughput      unchanged
p50 latency              slightly better
p99 latency              4.5× worse
CPU                       15% lower
RSS                       steadily rising
queue depth               rising
invalid-input rate        unchanged
snapshot failures         rising
```

The release changed identifier storage from compact owned strings to shared slices into received buffers and increased the connection limit from 256 to 1,024.

Construct an incident timeline containing:

1. initial detection;
2. immediate safety action;
3. evidence gathered before rollback;
4. rollback decision;
5. verification of recovery;
6. causal hypothesis;
7. confirming experiment;
8. corrective action;
9. regression evidence;
10. durable learning added to the course or release process.

Do not write “memory leak” until you distinguish unreachable lost memory from reachable retention. Explain how lower CPU, higher tail latency, rising queue depth, and rising RSS can coexist.

## Part 12 — Integrated design review

A team proposes these changes together:

- replace owned metric names with shared backing-buffer slices;
- double the connection limit;
- make the broker mailbox unbounded;
- retry all `ERR` responses up to five times;
- remove source revision metadata to improve reproducibility;
- enable link-time optimization in every profile;
- emit tenant identifiers as metric labels;
- deploy directly to 100% because unit tests pass.

Review every change. For each one, identify:

- the intended benefit;
- the missing contract or evidence;
- the likely displaced cost;
- the smallest experiment or design repair;
- whether it should be rejected, revised, or conditionally accepted.

Then propose a coherent alternative plan. The plan should preserve one source of truth for limits, one bounded admission path, deterministic result semantics, privacy-safe observability, exact artifact identity, and staged rollout.

## Independent construction

Build a small bounded report service that does **not** reuse MetricRail’s telemetry domain. Suitable examples include a package-index analyzer, a versioned inventory report service, or a bounded document-statistics daemon.

The product must:

- read a versioned line or frame format;
- validate all length, count, and cardinality limits before durable allocation;
- aggregate deterministic results;
- expose structured diagnostic events and bounded metrics;
- reject overload before committing work;
- distinguish invalid input, capacity rejection, transport failure, and internal failure;
- provide an offline mode and one bounded service mode;
- produce an artifact manifest;
- include a benchmark charter and one controlled load scenario;
- include a memory and data-movement ledger;
- include a threat model;
- include release, rollout, rollback, and incident instructions.

The transfer is successful only when the production-engineering method survives the new domain. Copying MetricRail’s nouns while preserving none of its reasoning does not satisfy the construction.

## Completion standard

You are ready to leave Course 9 when you can defend all of the following without vague adjectives:

- what the product promises;
- what the product bounds;
- what was measured and under which conditions;
- which profile evidence motivated a change;
- which allocation and retention costs remain;
- where demand can accumulate;
- which signals are authoritative and which are advisory;
- how overload, retry, degradation, and shutdown behave;
- which threats and supply-chain assumptions remain;
- which exact artifact is being released;
- how capacity and rollout decisions are made;
- how a production incident becomes a tested improvement rather than a narrative.

Return to the corresponding module whenever one of those answers depends on “probably,” “usually,” or “the tool says.” The goal of this course is not certainty about every environment. It is the ability to state what is known, what is measured, what is bounded, what is assumed, and what evidence would change the decision.

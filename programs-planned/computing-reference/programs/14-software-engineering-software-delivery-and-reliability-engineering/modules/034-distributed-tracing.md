---
module_id: SDRE-034
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 34
title: Distributed Tracing
status: complete
last_verified: 2026-09-06
---

# Distributed Tracing

## One-Page Review

### Governing question

How can engineers reconstruct one distributed operation well enough to explain its path, latency, outcome, and failures without mistaking an incomplete, sampled timeline for ground truth?

### Essential definitions

- a **trace** is a set of causally related operation records sharing a trace identifier;
- a **span** records one bounded operation, including identity, parent or links, name, kind, times, attributes, events, status, and resource;
- a **span context** is the small identity and sampling state propagated across a boundary;
- a **root span** has no parent and represents the trace's chosen observation boundary;
- a **child span** has one semantic parent; a **link** records another causal relationship without changing that parent;
- **instrumentation** creates and enriches spans at meaningful boundaries;
- **propagation** injects context into a carrier and extracts it at the receiver;
- **head sampling** decides near trace creation; **tail sampling** decides after observing later spans;
- **critical path** is the dependency-constrained sequence determining completion time, not necessarily the list of longest spans;
- **exclusive time** is span time not covered by selected child intervals under explicit clock and nesting assumptions;
- an **orphan** is a span whose intended parent is unavailable; a **broken trace** lacks expected causal records;
- a **trace waterfall** is a time-oriented rendering, not proof of causality or clock accuracy.

### Central model, mechanism, or theorem

Model a collected trace as a directed graph $G=(V,E_p,E_l)$. Each $v\in V$ is a span with interval $I_v=[s_v,e_v)$ and duration $d_v=e_v-s_v\ge 0$. Parent edges $E_p$ give every non-root span at most one parent and must be acyclic. Link edges $E_l$ express additional causes such as batch inputs.

If a parent interval and all direct-child intervals share a trustworthy time base and children are contained within the parent, then parent exclusive time is

$$
x_p=d_p-\mu\!\left(\bigcup_{c\in C(p)} I_c\right),
$$

where $\mu$ is interval length. The union matters because concurrent children overlap. Without the assumptions, negative or inflated exclusive time diagnoses data quality rather than service work.

### Critical invariants

- trace and span identifiers are valid, nonzero, and generated with sufficient unpredictability;
- every accepted parent edge resolves or is explicitly marked missing, and the parent graph is acyclic;
- context is extracted at receipt, made current only for the intended scope, and injected on each outgoing boundary;
- stable low-cardinality operation names are separated from attributes and individual identifiers;
- span kind, resource, outcome, status, times, and error evidence describe one semantic boundary;
- every started span is ended exactly once, including cancellation and exception paths;
- clocks, queues, retries, fan-out, asynchronous work, and links are modeled explicitly;
- sampling policy and effective probability accompany conclusions drawn from retained traces;
- baggage and propagated vendor state are bounded, validated, and excluded from secrets and personal data;
- missing spans, exporter loss, and backend rejection are observable as evidence limitations.

### Common failures

Common failures are creating a new root at every service, reusing an inbound parent ID on outbound calls, using raw URLs as span names, recording every function, ending a server span before asynchronous work finishes, treating retries as one child, parenting a batch to one arbitrary message, confusing status with an exception event, trusting remote sampling flags as authorization, propagating secrets in baggage, subtracting overlapping child durations, reading clock skew as causality, scaling tail samplers without trace-affine routing, and concluding that an unobserved span never ran.

### Compact example

A gateway extracts a valid remote context, starts a server span, and makes it current only while handling the request. It starts one client span per payment attempt, injects that span's context into each outbound request, records stable route and outcome attributes, and ends every span on success, timeout, or cancellation. A retry is a sibling attempt with its own identity. A queue producer ends after durable acceptance; a later consumer starts a new span linked to the message context. The collector records rejected spans and routes all spans for one trace to the same stateful tail-sampling decision. The resulting trace is useful evidence, but sampling and loss remain explicit.

### Connections

[SDRE-031](031-observability-versus-monitoring.md), [SDRE-032](032-structured-logging.md), and [SDRE-033](033-metrics-and-dimensionality.md) establish the evidence model. [SDRE-035](../ROADMAP.md) next adds change events; [SDRE-036](../ROADMAP.md) owns context propagation in greater depth. [API-010](../../28-api-and-service-engineering/modules/010-tracing-a-request-through-client-proxy-and-service.md) supplies the HTTP message path.

## Governing Question

A user sees one checkout, but the implementation may cross a browser, edge, gateway, account service, inventory service, payment provider, queue, and worker. Each component's local log can be correct while the end-to-end explanation is wrong. A shared trace identity and explicit causal edges let an investigator ask which operations belonged together, what depended on what, where time accumulated, and which attempt produced the outcome.

Tracing cannot replay reality. Instrumentation selects boundaries and attributes; propagation can break; clocks disagree; exporters drop records; sampling chooses only some traces; and a backend renders its interpretation. A trace is therefore a structured observation of a distributed execution, not the execution itself. Its value depends on semantic boundaries, continuity, completeness, and known uncertainty.

The governing question combines modeling and operations: what trace graph would distinguish the important failure hypotheses, and can the organization collect it safely at production scale? More spans do not automatically answer more questions. Excess detail raises latency, cost, privacy exposure, and cognitive load while unstable naming can make analysis harder.

## Why This Matters

Metrics reveal populations and trends; logs preserve selected events; traces connect selected work across boundaries. A latency histogram can show that a release worsened the tail, while a trace can reveal a serial retry after inventory and before payment. A log can preserve the payment provider's rejection body, while the trace locates that event within the attempt. These signals complement rather than replace one another.

The 2010 Dapper paper demonstrated that low-overhead, ubiquitous instrumentation in shared libraries plus sampling could make request paths useful at very large scale [5]. The 2007 X-Trace work separately showed the value and difficulty of propagating causal metadata across application, protocol, and administrative boundaries [8]. Their enduring lesson is architectural: broad continuity at meaningful boundaries is more valuable than bespoke instrumentation in a few services. Modern OpenTelemetry standardizes APIs, SDK responsibilities, context, sampling, span processing, and export without making one backend authoritative [1, 2].

W3C Trace Context standardizes the HTTP `traceparent` and optional `tracestate` fields for interoperable trace identity and vendor state [3]. It also makes security and privacy constraints explicit: the fields are correlation mechanisms, not safe containers for personal data, trust claims, or authorization. OpenTelemetry semantic conventions standardize many span names and attributes, but their stability varies by convention; a current implementation must record the convention version it follows [4].

Tracing also changes failure modes. Instrumentation can add allocation and serialization cost. Synchronous export can extend request latency. Unbounded attributes can overwhelm storage. Tail sampling can become a stateful distributed system whose routing errors split traces [7]. The tracing system itself requires metrics, logs, capacity controls, privacy review, and graceful degradation.

## Prerequisites and Retrieval

Retrieve process, thread, request, response, message, queue, causal dependency, directed graph, vertex, edge, tree, directed acyclic graph, interval, duration, wall clock, monotonic clock, concurrency, retry, timeout, cancellation, identifier, carrier, serialization, sampling probability, bias, cardinality, resource, and trust boundary.

From SDRE-031 retrieve the distinction between system state and evidence. From SDRE-032 retrieve structured event fields, event time, observed time, delivery limitations, and correlation identifiers. From SDRE-033 retrieve bounded dimensions, aggregate-versus-individual evidence, exemplars, and telemetry economics. From API-010 retrieve the difference between client, intermediary, and server observations.

## Learning Objectives

After completing this module, you should be able to:

1. model a collected trace as spans, parent edges, links, intervals, and resources;
2. choose service, client, producer, consumer, and internal span boundaries;
3. propagate context through synchronous and asynchronous protocols without creating false ancestry;
4. distinguish operation names, attributes, events, status, and resource identity;
5. validate identifiers, roots, missing parents, cycles, and end conditions;
6. reason about concurrency, retries, queues, clock skew, exclusive time, and critical paths;
7. compare head, parent-based, probability, and tail sampling;
8. diagnose broken traces and separate absence of evidence from evidence of absence;
9. bound instrumentation overhead, attribute risk, export pressure, and retention cost;
10. test trace semantics with controlled executions and known failure injection.

## Core Exposition

**Choose an observation boundary.** A trace commonly represents one externally initiated operation, but that is policy, not a law. A long workflow may need linked traces so retention and query size remain bounded. A streaming connection may contain many application operations. Define what starts a trace, what ends it, and which asynchronous consequences belong to it.

A span should represent an operation with a meaningful owner, start, and end: an inbound server request, outbound dependency call, durable message production, message consumption, database statement class, or substantial internal computation. Instrumenting every function adds nesting without new causal information. Omitting network and queue boundaries breaks continuity precisely where failures cross ownership.

OpenTelemetry distinguishes server, client, producer, consumer, and internal span kinds [1]. Kind states the relationship to a remote or asynchronous boundary; it does not replace transport attributes. A server span measures handling at the receiver, while a client span measures the caller's attempt. Their intervals need not match because network transit, proxy work, and independent clocks intervene.

**Create stable identity.** A trace identifier groups related spans; a span identifier names one span within that trace. The parent's span identifier records the primary ancestry. Identifiers should be opaque and unpredictable enough to resist collision and manipulation. They are not customer IDs, authorization tokens, or proof that two records are authentic.

Use low-cardinality names such as `GET /orders/{id}` or `payment.authorize`, not raw paths, account names, SQL text, or exception messages. Put bounded queryable distinctions in attributes, point-in-time occurrences in span events, deployment identity in resource attributes, and large or sensitive detail in governed logs linked by trace and span IDs.

Span status summarizes the operation outcome under a documented semantic convention. An exception event describes an occurrence; it does not automatically mean the operation failed, because the exception might be handled. Conversely a timeout can be an error without a language exception. Record the actual boundary outcome, stable error class, and relevant event separately.

**Propagate, then scope.** At an inbound boundary, extract supported fields from the carrier and validate them. Start a server or consumer operation from the resulting context or deliberately create a new root at a trust boundary. Make the new span current only across the logical operation. Before each outbound call, create its client or producer span and inject that new context into the outgoing carrier.

The W3C `traceparent` field carries version, trace ID, parent ID, and flags; `tracestate` carries bounded vendor-specific state [3]. The sampled bit communicates a recording decision but does not guarantee that every span exists, reaches storage, or may be trusted. Invalid input must not be allowed to crash a service, allocate without bound, poison indexes, or influence authorization.

Context propagation through asynchronous work depends on semantics. A task scheduled within one process may inherit current context if the runtime integration does so safely. A message should carry a serialized context captured at send time, not a reference to mutable thread-local state. When one message causes one consumer operation, remote parenting may fit. When a batch combines many messages or a job has several causes, choose one operational parent only if it truthfully owns the lifetime and represent the other causes with links.

**End spans on every path.** Start and end should bracket the semantic operation, not merely a convenient lexical block. A client span ends when the attempt reaches its documented terminal boundary. A producer span might end when the broker durably accepts the message, not when a future consumer completes. A server span should include response construction under the convention but not unrelated background work detached after response.

Exceptions, timeouts, cancellations, early returns, process shutdown, and callback failure all require end handling. Ending twice should not manufacture a second operation; forgetting to end can retain memory and prevent export. Late attributes or events after end may be rejected or ignored. Put sampling-relevant attributes and links at creation because a head sampler cannot use facts learned later [1].

**Read the graph carefully.** Parent edges form the primary call tree in the common case, but a distributed workflow can be a graph. Links represent batch inputs, retries related across traces, fan-in, or scheduled work without asserting one false parent. A link is not necessarily a timing dependency, and adjacency in a waterfall is not causality.

Wall-clock timestamps support a useful visualization but clocks can be offset or adjusted. A child displayed before its parent does not by itself disprove causality. Local duration should use a monotonic source where the implementation permits; cross-host ordering needs message relationships, not timestamp order alone. Preserve event time, observed time, and resource identity so skew can be diagnosed.

The root duration is the observed end-to-end interval at that boundary. Summing all span durations double-counts nested and parallel work. Subtracting direct children independently also double-counts overlaps. Under trustworthy, contained intervals, subtract the measure of their union to estimate exclusive parent time. If two children overlap from 10–70 and 50–100 within a 0–120 parent, their union is 90 and exclusive time is 30, not 10.

A critical path follows dependency constraints. The longest individual span may run mostly in parallel and not delay completion. Accurate critical-path analysis requires relationships for joins, waits, retries, queues, and asynchronous continuations plus compatible timing. A waterfall can suggest a hypothesis; controlled instrumentation or code knowledge must validate it.

The deterministic model below checks a simple tree and computes union-based exclusive time. It assumes one normalized clock, complete direct children, contained intervals, and no hidden work; it is not a general critical-path analyzer.

<!-- bijux-verify: {"id":"trace-interval-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"spans: 3\nroots: 1\ntrace duration: 120 ms\nchild union: 90 ms\nroot exclusive: 30 ms\n","stderr":""}} -->
```python
spans = [
    {"id": "root", "parent": None, "start": 0, "end": 120},
    {"id": "inventory", "parent": "root", "start": 10, "end": 70},
    {"id": "payment", "parent": "root", "start": 50, "end": 100},
]

identifiers = {span["id"] for span in spans}
assert len(identifiers) == len(spans)
assert all(span["end"] >= span["start"] for span in spans)
assert all(span["parent"] is None or span["parent"] in identifiers for span in spans)

root = next(span for span in spans if span["parent"] is None)
children = sorted(
    (span["start"], span["end"])
    for span in spans
    if span["parent"] == root["id"]
)
merged = []
for start, end in children:
    assert root["start"] <= start <= end <= root["end"]
    if not merged or start > merged[-1][1]:
        merged.append([start, end])
    elif end > merged[-1][1]:
        merged[-1][1] = end

child_union = sum(end - start for start, end in merged)
duration = root["end"] - root["start"]
print("spans:", len(spans))
print("roots:", sum(span["parent"] is None for span in spans))
print("trace duration:", duration, "ms")
print("child union:", child_union, "ms")
print("root exclusive:", duration - child_union, "ms")
```

**Treat collection as a lossy pipeline.** A recording span is not necessarily exported; an exported span is not necessarily accepted; an accepted span is not necessarily indexed or retained. Instrument SDK queues, batch processors, exporter attempts, rejections, collector queues, tail-sampler decisions, storage delay, and query errors. A trace with no visible error span may be healthy, unsampled, broken, delayed, expired, or rejected.

Head sampling decides before later outcomes are known. It is cheap and can keep an entire trace decision consistent through parent-based propagation, but rare failures may be missed. Tail sampling can retain traces based on final error, latency, route, or release attributes, but it must buffer spans, recognize trace completion imperfectly, and route one trace's spans coherently. Current OpenTelemetry guidance explicitly describes these operational costs [6, 7]. Module SDRE-039 owns sampling policy in depth; here the invariant is to disclose selection and loss when interpreting traces.

Independent per-span sampling fragments traces. If each of $n$ required spans were retained independently with probability $q$, the probability of retaining all would be $q^n$ under independence. At $q=0.1$ and $n=8$, that is $10^{-8}$. Real policies are not necessarily independent, but the calculation shows why a propagated trace-level decision is a different mechanism from sampling each record separately.

Sampling changes inference. A policy that retains every error trace and one percent of successes is excellent for diagnosis but cannot estimate the raw error rate by counting retained traces without weights and policy metadata. Tail latency among retained traces is not the population tail if selection depends on latency. Metrics remain the primary population summary unless trace sampling supports valid estimation.

**Control cost and risk.** Measure span creation latency, allocation, CPU, context-carrier bytes, queue occupancy, export bytes, accepted and rejected spans, active traces in tail sampling, index size, query latency, and retention. Apply bounded queues and nonblocking degradation so telemetry pressure does not take down the observed service. Preserve enough self-observation to know when evidence degraded.

Treat all inbound context as untrusted. Validate syntax and size, prevent arbitrary baggage from becoming indexed attributes, strip or restart context at documented trust boundaries, and never use a trace ID as authentication. Minimize attributes at creation, redact before export when feasible, govern tenant access, and set retention by purpose. A globally searchable trace can reveal service names, routes, timing, customer cohort, failures, and topology even without payloads.

**Test semantics, not just appearance.** Use a controlled request with known fan-out, one retry, one cancellation, and one queued continuation. Assert the expected roots, parent edges, links, names, kinds, resources, outcomes, and end states. Skew clocks, remove headers, corrupt IDs, overflow queues, reject export, and route trace fragments to separate collectors. Verify both the trace view and the telemetry system's loss indicators.

Compare traces against independent fixtures or logs using stable event identities. Do not demand one-to-one agreement where sampling differs; explain expected discrepancies. A rendered trace that “looks right” can still use the wrong parent, span name, resource, duration boundary, or success rule.

## Definitions and Notation

Let $V$ be the collected spans for one trace ID. For $v\in V$, let $i_v$ be its span ID, $p_v$ its optional parent ID, $I_v=[s_v,e_v)$ its reported interval, $d_v=e_v-s_v$, $k_v$ its kind, $r_v$ its resource, and $o_v$ its observed outcome. Let $E_p=\{(p_v,i_v):p_v\ne\varnothing\}$ and let $E_l$ contain explicit links.

A structurally valid collected parent graph has unique nonzero $i_v$, at most one parent per span, no self-parent edge, and no directed cycle. A missing parent may be accepted as an explicitly incomplete trace; silently promoting every orphan to a true root destroys the distinction between an initiated operation and lost ancestry.

For parent $p$ with direct collected children $C(p)$, union-based exclusive time is $x_p=d_p-\mu(\cup_{c\in C(p)}I_c)$ only if the intervals share a comparable clock, $I_c\subseteq I_p$, and the desired definition attributes overlapping child time once. It remains an observation over collected children, not CPU time.

Let $T$ be a controlled set of expected span identities and $O$ the collected identities. Controlled completeness is $c=|T\cap O|/|T|$ for nonempty $T$. In production, $T$ is generally unknown; exporter counters and synthetic fixtures provide bounded evidence rather than exact trace completeness.

For a sampling stratum $h$ with known inclusion probability $\pi_h>0$, a retained trace may carry inverse-probability weight $1/\pi_h$ for supported population estimates. This does not correct unknown loss after sampling, policy errors, or selection variables omitted from the model.

## Mechanisms, Invariants, or Proof Structure

**Parent-graph argument.** Unique IDs and at-most-one parents do not guarantee a tree; cycles are still possible. Acyclicity plus one root and complete parent resolution yields a rooted tree over the collected spans. Multiple roots may mean multiple initiated operations, an invalid grouping, or missing context. The structural result says nothing about semantic correctness.

**Overlap argument.** For child intervals $[10,70)$ and $[50,100)$, individual lengths sum to $60+50=110$, while union length is $60+50-20=90$. A 120 ms parent therefore has 30 ms outside the child union. The 10 ms result from naive subtraction double-counts the 20 ms overlap. Neither number is CPU utilization.

**Sampling argument.** Under independent inclusion, all $n$ required records survive with probability $\prod_{j=1}^n q_j$; equal $q$ gives $q^n$. A propagated parent-based decision creates dependence deliberately so one accepted trace is more likely coherent. Later export loss can still fragment it, so sampling consistency is not an end-to-end completeness guarantee.

**Causality limitation.** A send precedes its corresponding receive by mechanism even if clock offset makes the receive timestamp appear earlier. Therefore timestamp order is neither necessary nor sufficient for cross-process causal order. Parent and link relationships, protocol semantics, and local monotonic durations provide distinct evidence.

**Critical-path condition.** A longest-duration span need not lie on the completion-determining chain. If slow work finishes before a join waits on a different later dependency, the latter determines completion. Critical-path analysis requires dependency edges and join semantics, not sorting spans by duration.

**Evidence argument.** `not observed` has several generating mechanisms: no execution, no instrumentation, invalid propagation, sampling exclusion, buffer loss, export failure, backend rejection, retention expiry, or query filtering. Because multiple hypotheses produce the same view, absence of a span alone cannot identify nonexecution.

## Alternatives and Trade-Offs

1. **Manual versus automatic instrumentation.** Automatic hooks improve breadth and continuity at common libraries; manual spans express domain boundaries. Automatic detail can be noisy or semantically shallow, while manual coverage drifts. Combine governed library instrumentation with a small domain layer.
2. **Tree versus graph modeling.** A tree is simple for synchronous calls. Links represent fan-in, batching, and related work honestly, but analysis and user interfaces become harder.
3. **One trace versus linked trace segments.** One graph eases navigation. Segmenting long workflows bounds retention and size but requires durable linkage and explicit lifecycle semantics.
4. **Head versus tail sampling.** Head decisions are early, cheap, and easy to propagate. Tail decisions see outcomes but require state, trace-affine routing, completion timeouts, and overload behavior.
5. **Always-on recording versus low-overhead coverage.** Full capture improves individual evidence only if the pipeline survives. Sampling and attribute limits preserve service safety but reduce rare-case evidence.
6. **Rich attributes versus minimization.** More dimensions help search; they increase cost, schema drift, privacy exposure, and accidental indexing. Record only distinctions tied to questions.
7. **Remote parent versus link for messages.** Parenting gives a simple path for one cause. Links avoid false single ancestry for batches and fan-in, at the cost of more complex queries.
8. **Span events versus correlated logs.** Events keep concise occurrences in the trace. Logs better support larger structured detail and independent retention. Duplicating everything multiplies cost without adding evidence.
9. **Vendor extensions versus portable semantics.** Extensions can unlock backend analysis. W3C propagation and stable semantic conventions reduce migration and cross-team ambiguity.

## Failure Modes and Misconceptions

1. **“A trace is ground truth.”** It is selected, transformed, sampled evidence.
2. **“Same trace ID proves authenticity.”** An identifier correlates; it does not authenticate.
3. **“One incoming request means one process-local span.”** Network clients, servers, queues, and meaningful internal operations need distinct boundaries.
4. **“Every function deserves a span.”** Excess detail obscures ownership and adds overhead.
5. **“Raw URLs make useful names.”** They create unstable, high-cardinality operation identities.
6. **“An exception means failed span.”** Handled exceptions and nonexception failures refute this.
7. **“The sampled flag guarantees storage.”** Later loss, rejection, and retention still apply.
8. **“No error span means no error occurred.”** Instrumentation or collection may be incomplete.
9. **“Timestamps establish causality.”** Clock offset and adjustment can reverse apparent cross-host order.
10. **“Sum of durations is request latency.”** Nesting and concurrency double-count time.
11. **“Longest span is the critical path.”** Dependencies and joins determine the path.
12. **“One parent can represent a batch's many causes.”** It hides other causal inputs; use links.
13. **“Retries belong inside one client span.”** Separate attempts preserve count, timing, and outcome.
14. **“Baggage is a free metadata channel.”** It consumes carrier budget and can leak sensitive data.
15. **“Tail sampling scales like stateless export.”** It needs trace-affine state and overload policy.
16. **“Instrumentation cannot harm reliability.”** blocking export, allocation, cardinality, and queues can harm the service.

## Worked Examples

### Example 1

**Minimal synchronous path.**

**Situation.** A gateway handles one request and calls inventory once.

**Reasoning.** Start gateway server span `g` from the validated inbound context or as a root. Start inventory client span `c` with parent `g`, inject `c`'s context, and let inventory start server span `s` with remote parent `c`. The client and server spans represent different observation boundaries, so transit can appear between them.

**Conclusion.** A three-span path preserves caller attempt, transport boundary, and receiver handling rather than collapsing them into one duration.

### Example 2

**Overlapping fan-out.**

**Situation.** A 120 ms root has children 10–70 ms and 50–100 ms.

**Reasoning.** Child lengths are 60 and 50 ms with 20 ms overlap. Their union is $60+50-20=90$ ms. Root exclusive time under the declared assumptions is $120-90=30$ ms. Naively subtracting 110 gives 10 ms and double-counts overlap.

**Conclusion.** Interval union, not sum, is required for exclusive-time reasoning under concurrency.

### Example 3

**Apparent child before parent.**

**Situation.** A caller records send at 12:00:00.100, while the receiver's clock records start at 12:00:00.080.

**Reasoning.** The remote timestamp appears 20 ms earlier, but protocol causality says receive followed send. The trace can preserve that edge while flagging incompatible clocks. Adjusting the picture may aid display, but it must not be presented as a measured network duration.

**Conclusion.** Causal edges can remain valid when cross-host wall-clock order is not.

### Example 4

**Retry attempts.**

**Situation.** Payment attempt 1 times out after 200 ms; attempt 2 succeeds in 80 ms.

**Reasoning.** Create sibling client spans under the checkout operation with `attempt=1` and `attempt=2`, bounded outcome classes, and their own deadlines. One 280 ms “payment” child would hide the first failure, retry policy, and second success. The parent outcome reflects checkout, not merely the last child status.

**Conclusion.** One span per attempt preserves the mechanism that produced latency and success.

### Example 5

**Batch fan-in.**

**Situation.** A worker consumes a batch derived from messages `a`, `b`, and `c`.

**Reasoning.** Parenting the consumer to `a` falsely makes `b` and `c` unrelated. Start the batch-processing span under the worker's operational context and add links to the three message span contexts, with bounded link attributes describing input role. If the backend cannot render links, preserve them anyway and document the query limitation.

**Conclusion.** Links model multiple causes without inventing a single causal parent.

### Example 6

**Independent per-span sampling.**

**Situation.** An eight-span trace samples every span independently with $q=0.1$.

**Reasoning.** Under independence, complete retention probability is $0.1^8=10^{-8}$, or one in one hundred million. This does not mean exactly that frequency will occur in a finite run; it shows the mechanism systematically fragments traces. A trace-level propagated decision instead correlates inclusion.

**Conclusion.** Record-level probability sampling is not equivalent to coherent trace sampling.

### Example 7

**Biased retained population.**

**Situation.** A tail policy keeps 100% of error traces and 1% of successful traces. Storage contains 100 errors and 99 successes.

**Reasoning.** Raw retained counts suggest roughly 50% errors. If the inclusion probabilities are exactly known and no later loss occurred, weighted estimates are 100 error traces and $99/0.01=9{,}900$ successes, giving $100/10{,}000=1\%$. Diagnostic oversampling is useful but changes population inference.

**Conclusion.** Sampling metadata and weights are essential when traces support aggregate estimates.

### Example 8

**Broken propagation.**

**Situation.** A gateway trace ends at an outbound call, and the downstream service shows a separate root at the same time.

**Reasoning.** Test carrier injection at the gateway, forwarding at proxies, extraction at the service, supported format agreement, and trust-boundary restart policy. Similar timing and attributes are clues, not permission to merge IDs after the fact. A deliberate restart should emit a governed link or audit event if policy permits.

**Conclusion.** Diagnose each propagation mechanism before treating coincident roots as one trace.

### Example 9

**Tail-sampler scaling failure.**

**Situation.** Four collectors receive spans round-robin while each makes local tail decisions.

**Reasoning.** Spans for one trace land on different state holders, so no collector sees the complete candidate graph. Decisions can disagree and exported traces lose spans. Route by trace ID to a decision tier, then define rebalancing, late-span, memory-limit, and timeout behavior; observe all drops [7].

**Conclusion.** Stateful sampling requires trace affinity and explicit failure behavior.

### Example 10

**Adversarial context and baggage.**

**Situation.** An internet client sends syntactically valid trace fields plus large baggage containing an email and a fake premium-tier claim.

**Reasoning.** Validate bounded trace fields, discard or restart untrusted vendor state according to policy, reject or allowlist baggage, and never authorize from it. Generate local resource and tenant attributes from trusted state. Record only safe correlation evidence and observe rejection counts without reflecting sensitive input.

**Conclusion.** Propagation crosses a trust boundary; correlation state must not become identity, authorization, or an exfiltration channel.

## Cross-Program Connections

1. [API-010](../../28-api-and-service-engineering/modules/010-tracing-a-request-through-client-proxy-and-service.md) owns the client–proxy–service HTTP path; this module owns end-to-end trace evidence.
2. [API-033](../../28-api-and-service-engineering/modules/033-authentication-context-propagation.md) distinguishes authenticated security context from diagnostic trace context.
3. [API-061](../../28-api-and-service-engineering/modules/061-commands-events-and-messages.md) defines asynchronous message roles used by producer, consumer, and linked spans.
4. Distributed Systems Engineering owns formal causality and clock models; traces provide incomplete operational observations of them.
5. Security Engineering owns trust-boundary and privacy analysis; tracing must validate inbound carriers and minimize propagated data.
6. Data Engineering owns durable streaming transformation; collectors apply bounded telemetry transformations with evidence loss.
7. Database Engineering owns indexing and query internals; trace backends must control high-cardinality identities and retention.
8. Software Architecture owns service boundaries; span structure tests whether runtime ownership matches the intended architecture.
9. Platform Engineering owns shared instrumentation and collector products; service teams still own semantic operation boundaries.
10. [SDRE-039](../ROADMAP.md) develops sampling economics, while [SDRE-040](../ROADMAP.md) integrates logs, metrics, traces, and changes into diagnosable service instrumentation.

## References

1. OpenTelemetry, “Tracing API,” OpenTelemetry Specification 1.60.0, current specification retrieved 2026-09-06. https://opentelemetry.io/docs/specs/otel/trace/api/
2. OpenTelemetry, “Tracing SDK,” OpenTelemetry Specification 1.60.0, current specification retrieved 2026-09-06. https://opentelemetry.io/docs/specs/otel/trace/sdk/
3. W3C, *Trace Context*, W3C Recommendation, 23 November 2021; Level 2 work remains a separate draft, retrieved 2026-09-06. https://www.w3.org/TR/trace-context/
4. OpenTelemetry, “Trace Semantic Conventions,” current Semantic Conventions documentation, stability labels retained per individual convention, retrieved 2026-09-06. https://opentelemetry.io/docs/specs/semconv/general/trace/
5. Benjamin H. Sigelman et al., “Dapper, a Large-Scale Distributed Systems Tracing Infrastructure,” Google, 2010. https://research.google/pubs/dapper-a-large-scale-distributed-systems-tracing-infrastructure/
6. OpenTelemetry, “Sampling,” current concepts documentation, last-modified metadata 2025-10-16, retrieved 2026-09-06. https://opentelemetry.io/docs/concepts/sampling/
7. OpenTelemetry, “Scaling the Collector,” current Collector operations documentation, including stateful tail-sampling routing, retrieved 2026-09-06. https://opentelemetry.io/docs/collector/scaling/
8. Rodrigo Fonseca et al., “X-Trace: A Pervasive Network Tracing Framework,” NSDI 2007, USENIX Association. https://www.usenix.org/conference/nsdi-07/x-trace-pervasive-network-tracing-framework

## Exercises

### Exercise 1

**Precise understanding.**

Distinguish trace ID, span ID, parent ID, link, span status, and span event. State one invalid use for each of trace ID and status.

### Exercise 2

**Mechanism tracing.**

A root spans $[0,200)$ ms. Its direct children span $[20,90)$, $[60,130)$, and $[150,180)$. Under the normalized-clock and containment assumptions, calculate the child union and root exclusive time. Explain why subtracting child durations is wrong.

### Exercise 3

**Diagnosis.**

A message producer emits a span and injects context. The consumer creates new roots for half the messages, several spans never end, and exporter dropped-span count rises during bursts. Give a diagnosis sequence that separates propagation, lifecycle, and collection failures.

### Exercise 4

**Design comparison.**

Design a trace strategy for a service with 100,000 requests per second, a 0.05% error rate, strict overhead limits, and a need to diagnose slow successful requests. Compare head and tail sampling, and state the evidence limitations of your design.

### Exercise 5

**Unfamiliar transfer.**

A nightly job joins 10,000 input objects into 100 batches and one final report. Propose trace boundaries, parent/link semantics, naming, attributes, sampling, and privacy controls that avoid both a 10,101-child monolith and false single ancestry.

## Answers to the Exercises

### Answer 1

A trace ID groups records for the chosen distributed operation; a span ID uniquely names one recorded operation within it; a parent ID selects the primary semantic predecessor; a link names an additional related span context without making it the parent. Status summarizes the recorded operation's interpreted outcome under a convention. An event records a named occurrence at a time with optional attributes. A trace ID must not be used as authentication or customer identity. Status must not be treated as a substitute for exceptions, detailed error events, or the parent operation's independent outcome.

### Answer 2

The first two intervals overlap. Their union is $[20,130)$ with length 110 ms. The third interval is disjoint and has length 30 ms, so total union length is $110+30=140$ ms. Root exclusive time is $200-140=60$ ms. Individual lengths sum to $70+70+30=170$ ms; subtracting them would produce 30 ms because the 30 ms overlap $[60,90)$ is counted twice. The result remains wall-interval evidence over observed direct children, not CPU time.

### Answer 3

First use a controlled message with a known ID and inspect producer injection bytes, broker preservation, consumer extraction result, supported propagation format, trust-boundary restart policy, and resulting parent or link. This isolates the half-root symptom. Next enumerate every consumer exit—success, rejection, exception, cancellation, rebalance, shutdown—and assert one end per start; monitor active-span age. Finally compare SDK queue occupancy, processor drops, export attempts, collector acceptance, backend rejection, and trace-affine routing during a burst. Propagation explains ancestry, lifecycle explains unended spans, and collection counters explain recorded-but-missing spans; several can coexist.

### Answer 4

A reasonable design uses low-cost parent-based head probability sampling for a stable baseline and a bounded tail-decision tier for candidate traces that survive ingestion. Tail rules retain errors, policy-defined slow successes, and a small unbiased success sample; trace-ID routing keeps each candidate graph together. Instrumentation uses stable library boundaries, bounded attributes, batch export, and a nonblocking bounded queue. Capacity tests cover 100,000 requests per second and overload fallback. The 0.05% error rate is estimated from unsampled metrics, not raw retained traces. Limitations: head-dropped traces cannot be recovered by tail policy; late or missing spans can change decisions; threshold selection biases retained latency; post-sampling loss remains; and the tail tier is stateful. An acceptable alternative is pure head sampling if the overhead constraint precludes tail state, but it must admit that rare errors and slow successes can be missed.

### Answer 5

Create one orchestration trace or linked trace segment for the nightly job, one span per 100-object batch, and a separate final-report span. Do not attach 10,000 input objects as child spans. Record each input's durable processing event in the data system; give each batch span links to a bounded manifest or to a batch-manifest context rather than 100 indexed object identifiers. Link the final report to the 100 batch results or, if that is too large, to an aggregation checkpoint whose membership is durably auditable. Use stable names such as `batch.transform` and `report.assemble`; bounded attributes include job generation, batch ordinal, outcome class, region, and code release. Retain all failed batches and a probability sample of successes while keeping aggregate counts in metrics. Object names, tenant identifiers, payloads, and storage URLs remain out of propagated baggage and indexed attributes. Evaluation should reward truthful many-to-one causality, bounded graph size, durable membership evidence, and explicit sampling/privacy limits; linked per-batch traces are also acceptable if navigation and completion semantics are preserved.

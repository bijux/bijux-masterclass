---
module_id: SDRE-032
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 32
title: Structured Logging
status: complete
last_verified: 2026-09-06
---

# Structured Logging

## One-Page Review

### Governing question

How can a service record durable, queryable events that preserve meaning, identity, time, uncertainty, and failure evidence without leaking sensitive data or allowing the logging path to endanger the service?

### Essential definitions

- a **log record** is a timestamped representation of one observed occurrence or diagnostic statement;
- an **event** is a named occurrence with a stable semantic contract;
- **structured logging** records typed, named fields rather than embedding every fact in prose;
- an **envelope** contains cross-cutting fields such as event time, observed time, severity, resource, instrumentation scope, and correlation context;
- a **body** carries display-oriented or event-specific content;
- an **attribute** is a typed key-value fact used for interpretation, filtering, grouping, or correlation;
- an **event name** identifies a stable event class, not a per-occurrence value;
- a **schema** defines field names, types, meanings, requirements, and compatibility rules;
- **resource identity** names the service instance or runtime that emitted a record;
- **logical-operation identity** groups retries that pursue one intent; **attempt identity** distinguishes executions;
- **event time** is when the occurrence happened; **observed time** is when a downstream component received it;
- **log injection** lets untrusted data forge record boundaries or fields;
- **delivery semantics** describe loss, duplication, reordering, and delay—not a promise of exact truth;
- an **audit event** is a security- or governance-relevant record with stronger integrity, access, and retention requirements than ordinary diagnostics.

### Central model, mechanism, or theorem

Model a record as

$$
r=(n,v,t_e,t_o,s,b,a,\rho,\kappa),
$$

where $n$ is event name, $v$ schema version, $t_e$ event time, $t_o$ observed time, $s$ severity, $b$ body, $a$ typed attributes, $\rho$ resource identity, and $\kappa$ correlation context. Meaning comes from the schema and provenance of every transformation, not merely from valid JSON.

For a bounded asynchronous buffer with capacity $B$, current occupancy $q_0$, input rate $\lambda$, and export rate $\mu$, constant-rate overflow time is

$$
T_{overflow}=\frac{B-q_0}{\lambda-\mu}\quad\text{when }\lambda>\mu.
$$

This is a planning approximation; burstiness, batching, retry, and variable service time require stronger queue models and measurement.

### Critical invariants

- record one logical occurrence with a stable event name and explicit schema;
- use typed fields with documented units, allowed values, and ownership;
- bind records to service, release, configuration, operation, and attempt where relevant;
- preserve event time, observation time, clock quality, and transformation provenance;
- represent outcome, reason, error type, and uncertainty separately from free text;
- encode untrusted values so they cannot create record boundaries or new fields;
- exclude secrets and minimize personal or high-risk data before export;
- expect loss, duplication, delay, truncation, and reordering and expose them operationally;
- bound logging CPU, memory, I/O, network, storage, and query cost;
- separate diagnostic logs from audit records whose durability and integrity guarantees differ.

### Common failures

Failures include concatenating prose and reparsing it with regexes, using dynamic event names, serializing numbers as strings, changing units without a schema change, losing release or attempt identity, logging only exception messages, emitting multiline stack traces as multiple records, trusting severity as business impact, inserting raw tokens or payloads, allowing newlines to forge entries, blocking request threads on a failed collector, silently dropping buffer overflow, retrying exports into duplicates, assuming timestamp order is causal order, mutating records without provenance, and claiming JSON alone makes logs structured.

### Compact example

A payment attempt emits event `payment.authorization.completed` with schema `1.2.0`, event and observed timestamps, service and release identity, logical payment reference, attempt number, trace identifier, provider class, bounded outcome, error type, duration in milliseconds, and retryability. It excludes account number, token, payload, and provider message literals. The emitter JSON-encodes untrusted text, the collector records transformations, overflow counters expose loss, and the consumer deduplicates by event identity. A separate append-protected audit event records the authorization decision under stricter access and retention.

### Connections

[SDRE-031](031-observability-versus-monitoring.md) defines the diagnostic questions logs must support. [SDRE-033](../ROADMAP.md) next develops metrics and dimensionality. Security Engineering owns sensitive-data and audit threats; Data Engineering owns schema, transport, quality, and retention mechanisms.

## Governing Question

Plain text is excellent for human prose and poor as the only machine contract. The line `payment failed for 42 after 3` does not say whether 42 is an account, order, amount, or attempt; whether 3 is seconds, retries, or provider code; which release emitted it; or whether “failed” is final. A parser can guess until punctuation, wording, localization, or exception text changes.

Structured logging does not mean wrapping the same sentence in `{"message": ...}`. It means modeling the occurrence: choose a stable event, define typed fields, preserve identity and time, state outcomes and limitations, and carry the record through a fallible pipeline. The encoding may be JSON, Protocol Buffers, CBOR, a system journal, or another format. Structure is semantic before it is syntactic.

The governing problem spans two failure domains. A record may be misleading at creation because its fields are ambiguous, sensitive, or incomplete. A correct record may then be lost, duplicated, reordered, truncated, corrupted, transformed, over-indexed, or made inaccessible. A production design must make both domains testable.

## Why This Matters

Logs often become the only surviving account of an intermittent state transition. They support diagnosis, security analysis, customer support, capacity work, release evaluation, and post-incident learning. Yet logging is executable production code on hot and failure paths. It consumes resources and handles high-risk information precisely when systems are least stable.

Google's SRE troubleshooting guidance treats logs that expose operations and system state as essential diagnostic evidence alongside metrics, traces, and active examination [8]. The useful property is not prose volume but the ability to inspect what each component did with enough context to test a hypothesis.

The stable OpenTelemetry Logs Data Model provides a common representation for application, system, and other log sources and aims to preserve semantics across mappings [1]. Its current model distinguishes record fields such as timestamps, severity, body, attributes, resource, instrumentation scope, trace context, and event name. The broader logging specification explicitly accommodates legacy libraries and formats rather than assuming all producers can adopt one API [2]. These are interoperability mechanisms, not proof that an application's domain schema is useful.

Structured logs predate any current telemetry stack. RFC 5424 separates syslog message content from transport and defines structured-data elements for parseable information [3]. JSON's RFC 8259 defines a widely used typed object encoding and warns that duplicate object names produce unpredictable receiver behavior; interoperable exchanged JSON uses UTF-8 [4]. Neither standard supplies application event meaning automatically.

Security and lifecycle concerns are first-class. OWASP's logging guidance covers event attributes, data exclusion, injection, verification, transport, access, retention, and attacks on confidentiality, integrity, availability, and accountability [5]. NIST SP 800-92 remains the final NIST guide for organization-wide computer-security log management while a revision has only draft status on the current NIST project pages [6]. This chapter uses both as guidance and makes no compliance claim.

## Prerequisites and Retrieval

Retrieve observability, monitoring, event, state transition, invariant, schema, serialization, type, timestamp, clock skew, resource, release digest, configuration generation, trace, span, correlation, retry, idempotency, queue, buffer, backpressure, sampling, cardinality, privacy, integrity, retention, and audit.

From SDRE-031 retrieve system boundary, operational question, relevant state, observational equivalence, telemetry completeness, black-box and white-box evidence, and causal restraint. From SDRE-019 and SDRE-023 retrieve secret handling and identity separation. Structured logging implements evidence; it does not decide which evidence is sufficient.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish a structured event contract from a formatted message or serialization choice;
2. design a typed envelope and domain attributes for one operational occurrence;
3. define stable event names, schema versions, compatibility, and ownership;
4. represent time, resource, release, operation, attempt, outcome, and error semantics precisely;
5. prevent log injection and sensitive-data disclosure at the source;
6. reason about synchronous and asynchronous emission, backpressure, overflow, and shutdown;
7. handle loss, duplication, delay, reordering, truncation, and transformation explicitly;
8. choose indexing, sampling, retention, and archive policy from real queries and risk;
9. separate diagnostic, business, security, and audit evidence by guarantee;
10. test producers, pipelines, schemas, queries, and degraded logging behavior.

## Core Exposition

**Model occurrences, not sentences.** Start with a question or invariant: did authorization finish, why was work retried, which configuration rejected a request, what state transition occurred? Define one event at the point where the service has authoritative knowledge. A display message may summarize it for a person, but consumers query stable fields.

Use a fully qualified, low-cardinality event name such as `checkout.payment.authorization.completed`. Do not include order ID, exception class, status code, or user text in the name. Current OpenTelemetry event guidance says an event name identifies its structure and recommends attributes for varying values; that guidance is presently marked development, so pin and review any adopted convention [7].

Distinguish an event from a duration. A named event represents an occurrence or checkpoint. A span better represents an operation with start, end, and causal children. A metric better represents an aggregate rate or distribution. A log may still record a completion event and link to a span; avoid duplicating every span field without a question.

**Build a stable envelope.** Useful cross-cutting fields include event name and schema version; event and observed timestamps; severity number and text; body; typed attributes; resource identity; instrumentation scope and version; trace and span identifiers; and flags describing data quality. A transport may add receive, route, tenant, and storage metadata, but must distinguish these from producer-authored facts.

Resource identity answers who emitted the record: service name, instance or process identity, platform resource, region, and deployment environment. Release and configuration identities answer which effective behavior ran. Avoid mutable labels alone. Preserve immutable digests or generations where diagnosis depends on exact identity.

Instrumentation scope identifies the library or component that produced the schema. It helps separate an application event from a framework, runtime, proxy, or collector record. Do not pretend the collector is the originator merely because it serialized the final payload.

**Define domain attributes.** For each field specify name, type, unit, allowed or bounded values, requirement level, meaning, sensitivity, cardinality expectation, producer, and examples. Prefer `duration_ms: 153` or a standard duration unit over `duration: "153ms"`. Prefer bounded `outcome: "timeout"` plus `error.type: "provider_deadline"` over parsing prose.

Separate identifiers by role. A logical operation ID groups retries pursuing the same business intent; attempt ID distinguishes executions; event ID distinguishes emitted occurrences; trace and span IDs correlate execution context. One overloaded `request_id` cannot safely express all four.

Represent exceptions structurally: error type or code, sanitized message if useful, stack trace as one encoded field, cause chain, handled status, and retryability. Exception type is usually more stable for grouping than full messages. A successful fallback may produce an error event while the user outcome remains successful; record both mechanism and outcome.

Severity expresses the producer's assessment under a documented convention. It does not alone determine page priority, user impact, retention, or security significance. A high-volume debug event can exhaust a collector; a low-severity authorization decision may require strong audit retention. Keep these policies separate.

**Treat schemas as interfaces.** Give every event family an owner and version. Compatible additions are often safe for tolerant consumers; removal, rename, type change, unit change, meaning change, or requiredness change can break queries and alerts. Use a registry or source-controlled definitions, generated constants where suitable, and contract tests.

Avoid duplicate field names. JSON parsers may retain first, last, every, or no duplicate value [4]. Reject duplicates at serialization and ingestion. Keep field paths and casing canonical. Normalize enums deliberately rather than allowing spelling variants to fragment queries.

During a schema migration, identify consumers before changing producers. Dual-write only when cost and ambiguity are bounded, or transform with declared source and target versions. Measure old and new record counts, rejects, and query equivalence. End the compatibility window explicitly.

**Preserve time without inventing order.** Record event time at the authoritative occurrence and observed time when received. Their difference includes clock offset and pipeline delay. Prefer UTC timestamps with explicit offset; use monotonic clocks for durations within a process. Record clock synchronization or confidence when relevant.

Timestamp order across machines is not necessarily causal order. Trace context, message sequence, logical operation, attempt number, and domain generations can provide stronger relations. A collector may receive an older event after a newer one. Queries should state whether they order by event, receive, or storage time.

**Encode untrusted data.** Never concatenate untrusted strings into a line-oriented record. A newline, delimiter, quote, escape sequence, or terminal control character can forge boundaries or mislead a viewer. Use a well-tested serializer, one record framing method, UTF-8 validation where required, and output escaping. Keep raw values in typed fields only after validation and minimization.

Structured logging is not SQL parameterization or HTML escaping. Each destination has its own injection surface: JSON, syslog, terminal, query language, dashboard, CSV export, or shell tooling. Preserve the original value safely and escape at each rendering boundary. Do not render logs through `eval` or shell expansion.

The following Python example enforces a small domain schema before a record reaches an established serializer. It deliberately does not implement wire encoding. It is a deterministic teaching wrapper, not a complete logging, privacy, or audit library.

<!-- bijux-verify: {"id":"typed-event-wrapper","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"{'event.name': 'checkout.completed', 'event.schema': '1.0.0', 'service.name': 'checkout', 'trace_id': '0af7', 'order.class': 'standard', 'outcome': 'success'}\nrejected: forbidden field: authorization\n","stderr":""}} -->
```python
ALLOWED = {
    "event.name": str,
    "event.schema": str,
    "service.name": str,
    "trace_id": str,
    "order.class": str,
    "outcome": str,
}
FORBIDDEN = {"authorization", "password", "access_token"}

def validate_event(fields):
    forbidden = FORBIDDEN.intersection(fields)
    if forbidden:
        raise ValueError(f"forbidden field: {sorted(forbidden)[0]}")
    unknown = set(fields).difference(ALLOWED)
    if unknown:
        raise ValueError(f"unknown field: {sorted(unknown)[0]}")
    for name, value in fields.items():
        if not isinstance(value, ALLOWED[name]):
            raise TypeError(f"wrong type: {name}")
    return fields

record = {
    "event.name": "checkout.completed",
    "event.schema": "1.0.0",
    "service.name": "checkout",
    "trace_id": "0af7",
    "order.class": "standard",
    "outcome": "success",
}
print(validate_event(record))
try:
    validate_event({**record, "authorization": "<redacted-test-value>"})
except ValueError as error:
    print("rejected:", error)
```

The allowlist catches accidental schema and secret-field changes, while source values still require classification. A sensitive value under an innocent key remains sensitive. Production implementations must pass the validated structure to a proven contextual serializer and also need timestamp, resource, severity, buffering, failure handling, and integration with established language logging APIs.

**Minimize sensitive data before emission.** Do not log passwords, access tokens, session secrets, private keys, database connection strings, raw payment data, or unrestricted payloads. Personal and customer data requires purpose, authorization, minimization, access, retention, and deletion design. Hashing a small or guessable identifier may not anonymize it.

Use bounded classifications or authorized pseudonymous references when a legitimate query requires correlation. Redact at the source when possible; a collector cannot remove a secret already written to local disk, crash output, or an intermediate queue. Test error and debug paths, which often expose full objects.

Separate diagnostic from audit evidence. Audit records may require authenticated producer identity, append protection, restricted administrators, durable ordering or sequencing, longer retention, legal hold, and access audit. Ordinary logs optimized for debugging may be sampled, mutable, or short-lived. Copying a diagnostic record into an audit index does not create missing guarantees.

**Make emission bounded.** Synchronous writes simplify acknowledgment but add latency and can block service work when storage stalls. Asynchronous emission decouples the request path but introduces buffers, delayed failure, loss at crash, and shutdown coordination. Choose by event class and service risk.

For asynchronous logging, bound memory and declare overflow behavior: drop newest, drop oldest, sample, spill to bounded disk, or backpressure. No choice is universally safe. Never let unlimited log growth exhaust the service. Export occupancy, drops by event class, retry count, oldest age, and shutdown flush results through an independent or minimally dependent path.

The constant-rate overflow equation is a quick stress calculation. Real traffic is bursty, exporters batch, and retries can amplify load. Load-test distributions and failure intervals. Ensure an error storm does not produce enough logs to extend the outage—a feedback failure sometimes called log amplification.

**Assume imperfect delivery.** A successful logging call often means accepted into a local buffer, not durably stored or indexed. Network retry can duplicate records after an unknown acknowledgment. Multiple workers and collectors reorder events. Receivers may reject schemas or truncate oversized bodies. State the actual acknowledgment boundary.

Use event identity when deduplication matters, but do not assume globally unique IDs make delivery exactly once. A producer can emit twice with two IDs or crash before recording its ID. Make downstream analysis tolerant of duplicates and expose estimated or measured loss.

Record truncation explicitly with original length, retained length, and truncation flag. Preserve the structured envelope even if a body or stack must be bounded. Silent truncation can remove the only distinguishing evidence and can be exploited to hide suffix content; RFC 5424 discusses truncation and congestion risks in its protocol context [3].

**Govern the collection path.** Collectors parse, enrich, redact, route, sample, batch, and transform. Every transformation needs owner, version, input schema, output schema, failure policy, and observability. Preserve original producer identity and distinguish collector-authored attributes. Reject or quarantine malformed records rather than silently guessing.

Enrichment can race reality. A collector mapping instance IP to deployment may use stale metadata after reuse. Bind lookup time and source, prefer immutable platform identity, and measure misses. Conflicting producer and collector values require a precedence rule and conflict record, not silent overwrite.

Protect transport and storage. Authenticate producers where trust matters, encrypt untrusted links, restrict write and query identities, audit access, and isolate tenants. Logs are attacker-controlled inputs; parsers and indexing pipelines need size, depth, rate, and character limits.

**Design storage from queries.** Index fields needed for bounded frequent filters and groups; store other fields without indexing or in cheaper tiers. High-cardinality values may be appropriate in logs but expensive to index. Measure bytes, index expansion, query latency, retention, and egress by event class.

Retention follows diagnostic windows, incident discovery delay, security needs, contracts, privacy, and cost. Longer is not automatically safer. Define hot searchable, warm, archive, and deletion behavior. Test restoration and deletion across replicas, caches, extracts, and backups where policy requires it.

Sampling and rate limits are semantic transformations. Preserve all events needed for audit or exact counting unless another authoritative record exists. For diagnostic storms, retain the first occurrence, bounded exemplars, aggregated suppressed count, rare types, and a probability sample. Record the policy, probability, and suppressed count so absence is interpretable.

**Test end to end.** Unit-test field types, required fields, allowlists, redaction, encoding, exception structure, and size bounds. Contract-test schema evolution and consumer queries. Property-test arbitrary Unicode, delimiters, control characters, and large values. Fault-test full buffers, slow collectors, network partitions, partial writes, process crash, rotation, restart, duplicate acknowledgment, clock skew, and malformed enrichment.

Send a synthetic canary event through the production path and verify latency, schema, identity, access, and expiration. Compare expected event IDs with observed unique IDs in a controlled test to measure completeness. A passing emitter unit test cannot prove collection, indexing, query, or retention.

Review actual records before release. Render them as operators will see them, run representative queries, and confirm that an unfamiliar engineer can distinguish the intended hypotheses. A beautifully structured schema that does not answer a diagnostic question is still poor logging.

## Definitions and Notation

Let a domain event record be $r=(n,v,t_e,t_o,s,b,a,\rho,\kappa)$ as defined in the review. Let transformation $F_i$ map record representation at pipeline stage $i$ to stage $i+1$. Each $F_i$ declares whether it is semantics-preserving, lossy, enriching, redacting, filtering, or sampling.

For a controlled set of expected event identities $E$ and received accepted records $R$, define unique completeness

$$
C_E=\frac{|E\cap ids(R)|}{|E|},\qquad |E|>0.
$$

This measure applies only when expected identities are known. It is not a general production log-completeness estimator. Duplicate excess can be reported as $|R|-|ids(R)|$ when every accepted record has a valid identity, while duplicate causality still requires analysis.

For event time $t_e$ and observed time $t_o$, apparent pipeline delay is $L=t_o-t_e$. If producer clock offset is unknown, $L$ mixes transport delay and clock error. Negative $L$ is evidence of clock or timestamp problems, not negative transport time.

For a bounded buffer, constant rates, and $\lambda>\mu$, occupancy is $q(t)=q_0+(\lambda-\mu)t$ until capacity, yielding $T_{overflow}=(B-q_0)/(\lambda-\mu)$. If $\lambda\le\mu$ in this simplified model, sustained growth is absent, though bursts can still overflow.

## Mechanisms, Invariants, or Proof Structure

**Semantic structure argument.** A syntactically valid map is not enough. If a field lacks type, unit, identity, and event meaning, multiple interpretations remain possible. A schema reduces ambiguity by constraining valid interpretations; it cannot prove the producer recorded reality correctly.

**Source-encoding argument.** When an encoder treats untrusted content as a value, delimiters become escaped content under that encoding. String concatenation lets those delimiters alter syntax. Safe encoding prevents structural injection for that representation, while downstream renderers still require their own contextual escaping.

**Buffer proof.** Under constant arrival and service rates, net accumulation per unit time is $\lambda-\mu$. Capacity remaining is $B-q_0$. Dividing remaining capacity by positive net rate gives the first modeled overflow time. The proof does not apply unchanged to stochastic or batch service.

**Completeness limitation.** Received count alone cannot reveal loss because true emitted count is unknown and retries add duplicates. Controlled expected event identities create a finite denominator and make missing unique IDs detectable. Outside that experiment, heartbeat, sequence gaps, producer counters, collector counters, and reconciliation provide partial evidence rather than certainty.

**Ordering limitation.** Receiver order combines producer clocks, buffering, transport paths, retries, and storage. Therefore timestamp sorting alone cannot establish causality. Domain generations, trace relations, message offsets, and attempt sequencing may support narrower order claims under their own assumptions.

**Audit separation argument.** Diagnostic retention and mutation policies may permit sampling, deletion, or administrator rewrite. If an audit claim requires completeness, restricted deletion, or tamper evidence, a diagnostic channel lacking those mechanisms cannot establish it merely by relabeling records.

## Alternatives and Trade-Offs

**Text versus structured events.** Text is fast to author and readable locally. Structured fields support stable queries and validation. Keep a concise body for humans while treating fields as the machine contract.

**JSON versus binary or native formats.** JSON is inspectable and widely interoperable but verbose, has limited numeric nuance, and permits duplicate names syntactically. Binary formats can enforce schemas and reduce size but complicate ad hoc inspection and compatibility tooling. Pick encoding after semantic design.

**Synchronous versus asynchronous emission.** Synchronous acknowledgment narrows some loss windows but couples service latency to logging. Asynchronous buffering protects latency but adds crash loss and backpressure choices. Use stronger paths only for event classes whose value justifies them.

**Local files versus direct network export.** Files support local recovery and mature rotation but require tailing, identity, checkpoint, and disk controls. Direct export removes parsing layers but depends on network and collector behavior. Platform context and failure model decide.

**Producer versus collector enrichment.** Producers know domain state accurately at occurrence time. Collectors centralize platform metadata and policy. Prefer source-owned domain facts and collector-owned transport facts, with explicit precedence and provenance.

**Strict rejection versus tolerant ingestion.** Strict schema validation exposes defects but can discard valuable emergency evidence. Tolerant quarantine preserves malformed records without polluting trusted queries. Make the fallback visible and bounded.

**Index everything versus tiered fields.** Full indexing accelerates unpredictable queries but multiplies cost and attack surface. Tiered storage keeps bounded common fields indexed and allows slower scan or rehydration for rare detail.

**No sampling versus controlled suppression.** Complete diagnostic retention helps reconstruction but can collapse under storms. Controlled suppression preserves high-value classes and records what was omitted. Audit or exact-counting events require an authoritative unsampled path.

**Common versus domain schemas.** Common envelopes enable fleet correlation; domain events carry real meaning. A central team should own transport and shared identity while domain teams own event semantics under joint review.

## Failure Modes and Misconceptions

1. **“JSON makes a log structured.”** JSON can contain one opaque message or ambiguous fields; schema and meaning create structure.
2. **“We can parse text later.”** Wording and delimiters drift, and facts not emitted cannot be recovered.
3. **“Dynamic event names are expressive.”** They fragment schemas and indexes; varying values belong in attributes.
4. **“Severity equals user impact.”** Producer severity is one field, not an SLO or response policy.
5. **“Exception message is enough.”** Type, cause, outcome, retryability, and sanitized context are distinct facts.
6. **“Timestamps provide a global order.”** Clock offset, buffering, and retry can invert observed order.
7. **“A successful log call means durable storage.”** It may acknowledge only a process-local queue.
8. **“Retries make delivery reliable.”** They may add duplicates and load after an unknown acknowledgment.
9. **“Dropping debug logs is harmless.”** It is safe only when classification, suppressed count, and diagnostic consequences are understood.
10. **“The collector can redact later.”** Earlier files, buffers, crash reports, and routes may already expose the value.
11. **“Hashed identifiers are anonymous.”** Small or linkable domains can be reversed or reidentified.
12. **“More retention means better forensics.”** It also increases breach impact, legal exposure, and cost.
13. **“Diagnostic logs are an audit trail.”** Sampling, mutation, access, and deletion guarantees may be insufficient.
14. **“Duplicate keys are harmless.”** Receivers can interpret different values, making the record non-interoperable.
15. **“Logs should never affect the service.”** They consume real resources; the design must bound effects and choose explicit trade-offs.
16. **“No log means no event.”** Loss, filtering, sampling, access, or instrumentation failure are competing hypotheses.

## Worked Examples

### Example 1

**Situation.** A line reads `refund failed 17 3`.

**Reasoning.** At least four interpretations exist for each number. Replace it with event `refund.completed`, schema version, bounded outcome, error type, logical refund reference, attempt number, provider class, duration with unit, service/release identity, and event time. Keep a sanitized body only for display.

**Conclusion.** Structured fields remove parsing guesses only when their semantics are documented.

### Example 2

**Situation.** A service uses event names `login.failed.alice`, `login.failed.bob`, and so on.

**Reasoning.** Each occurrence creates a new event class and high-cardinality index value. Use stable `authentication.login.completed`, outcome `failure`, error type, and a permitted pseudonymous principal reference in a protected attribute when required. Never place the password or token in any field.

**Conclusion.** Event names identify schemas; occurrence identities and classifications belong in attributes.

### Example 3

**Situation.** An attacker submits username `eve\nseverity=INFO login ok` to a line-oriented logger.

**Reasoning.** Concatenation can create a forged second line. A serializer encodes the newline inside a string and record framing preserves one event. A terminal or CSV viewer must still escape the value for its own context. The producer also bounds length and control characters.

**Conclusion.** Use contextual serialization at every boundary; sanitization at one layer is not universal safety.

### Example 4

**Situation.** A buffer holds $B=10{,}000$ records, currently $q_0=2{,}000$. An error storm emits $\lambda=500$ records/s while export handles $\mu=300$ records/s.

**Reasoning.** Net growth is $200$ records/s and remaining capacity is $8{,}000$, so the constant-rate model gives $T_{overflow}=8{,}000/200=40$ seconds. The team must reduce emission, increase verified export capacity, or invoke a declared drop/spill policy before then. Bursts can overflow sooner.

**Conclusion.** Logging failure budgets need quantitative capacity and explicit overload behavior.

### Example 5

**Situation.** A client event time is 12:00:10 and collector observed time is 12:00:08.

**Reasoning.** Apparent delay is $-2$ seconds, which cannot be transport time. The client clock may be fast, the timestamp may use the wrong unit or zone, or parsing may be wrong. Preserve both times and clock confidence; order this workflow using logical generation or trace relations rather than wall clock alone.

**Conclusion.** Negative apparent latency is a telemetry-quality signal, not evidence of reverse time.

### Example 6

**Situation.** A collector stores an event, times out before acknowledging it, and the exporter retries.

**Reasoning.** Two stored records may represent one emitted event. A stable event ID permits query-time deduplication, while logical operation and attempt IDs preserve the fact that business work itself may also retry. Count raw and unique records and expose duplicate rate.

**Conclusion.** At-least-once transport requires duplicate-tolerant analysis; it does not imply duplicated business action.

### Example 7

**Situation.** `duration_ms` is renamed to `duration` and changed from integer milliseconds to floating seconds.

**Reasoning.** This is not a cosmetic rename. Existing comparisons and thresholds change by $1{,}000$. Introduce a new schema version and explicit unit, inventory consumers, dual-produce or transform for a bounded window, compare queries, and remove the old field only after consumer migration.

**Conclusion.** Type, unit, and meaning changes require governed schema evolution.

### Example 8

**Situation.** A debug object includes an HTTP authorization header and is serialized after an error.

**Reasoning.** Collector redaction is too late if the record touches stdout, local disk, or another exporter. Use allowlisted fields at the call site, test nested objects and exception paths, reject forbidden keys, rotate any exposed credential, and investigate every downstream copy under the incident policy.

**Conclusion.** Data minimization belongs before emission, with detection and response for failures.

### Example 9

**Situation.** One identical error occurs 100,000 times during a dependency outage.

**Reasoning.** Keeping every diagnostic copy may amplify the incident. Preserve the first event, a bounded probability sample, periodic exemplars, affected release and dependency dimensions, and exact suppressed count from a local counter. Keep unsampled user-impact metrics and required security/audit events on their authoritative paths.

**Conclusion.** Suppression can retain meaning only when the omitted population is measured and critical classes are protected.

### Example 10

**Situation.** An emitter unit test passes, but operators cannot find its record in production.

**Reasoning.** Trace the stages: local acceptance, buffer, exporter, network, collector receive, parse, transform, tenant route, storage, index, authorization, query, and retention. Compare event ID and stage counters; send a synthetic canary. Possible outcomes include drop, reject, route error, index lag, expired retention, or denied access.

**Conclusion.** Logging correctness is end-to-end; producer serialization is only the first boundary.

## Cross-Program Connections

1. **Data Engineering (DE):** supplies schema evolution, stream delivery, late data, deduplication, quality, and retention.
2. **Database Engineering (DBE):** supplies indexing, storage, query planning, transaction logs, and durability distinctions.
3. **Security Engineering (SEC):** owns event authenticity, log injection, sensitive-data minimization, access, and tamper threats.
4. **Distributed Systems (DIST):** supplies clocks, ordering, retries, duplicates, partial failure, and causal context.
5. **Operating Systems (OS):** supplies process output, journaling, file descriptors, buffering, rotation, and crash behavior.
6. **Networking (NET):** supplies transport framing, TLS, congestion, loss, and backpressure behavior.
7. **API and Service Engineering (API):** defines request, operation, error, and identity contracts reflected in events.
8. **Platform Engineering (PLAT):** owns shared emitters, collectors, routing, tenancy, storage, and query access.
9. **Software Testing and Quality Engineering (STQE):** supplies contract, property, fault, and end-to-end tests for logging.
10. **Software Architecture (SARCH):** supplies ownership boundaries and quality-attribute trade-offs among latency, cost, privacy, and evidence.

## References

1. OpenTelemetry Authors, “Logs Data Model,” status Stable in OpenTelemetry Specification 1.60.0. <https://opentelemetry.io/docs/specs/otel/logs/data-model/>. Accessed 2026-09-06.
2. OpenTelemetry Authors, “OpenTelemetry Logging.” <https://opentelemetry.io/docs/specs/otel/logs/>. Accessed 2026-09-06.
3. Rainer Gerhards, “The Syslog Protocol,” RFC 5424, March 2009. <https://datatracker.ietf.org/doc/html/rfc5424>.
4. Tim Bray, ed., “The JavaScript Object Notation (JSON) Data Interchange Format,” RFC 8259, December 2017. <https://www.rfc-editor.org/rfc/rfc8259>.
5. OWASP Foundation, “Logging Cheat Sheet.” <https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html>. Accessed 2026-09-06.
6. Karen Kent and Murugiah Souppaya, *Guide to Computer Security Log Management*, NIST SP 800-92, September 2006. <https://doi.org/10.6028/NIST.SP.800-92>.
7. OpenTelemetry Authors, “Semantic Conventions for Events,” status Development in Semantic Conventions 1.44.0. <https://opentelemetry.io/docs/specs/semconv/general/events/>. Accessed 2026-09-06.
8. Betsy Beyer et al., eds., “Effective Troubleshooting,” in *Site Reliability Engineering*, O'Reilly Media, 2016. <https://sre.google/sre-book/effective-troubleshooting/>. Accessed 2026-09-06.

## Exercises

### Exercise 1

Distinguish event name, body, attribute, resource, schema version, logical operation ID, attempt ID, and trace ID. Explain one failure caused by overloading them.

### Exercise 2

A logging buffer has capacity 50,000 records and occupancy 5,000. During an incident, arrival rate is 2,000 records/s and export rate is 500 records/s. Compute the constant-rate overflow time. State at least three assumptions that limit the result.

### Exercise 3

Design and test a structured event for a background invoice retry. Include event and observed time, outcome, identity, error, retry, schema, privacy, and delivery fields. Give one valid and two invalid cases.

### Exercise 4

Compare synchronous local file logging, asynchronous stdout collection, and direct network export for a latency-sensitive service. Choose a design for diagnostics and a separate design for security audit events, with explicit failure behavior.

### Exercise 5

A hospital device emits free-text alarm logs over an intermittently connected network. Design a migration to structured evidence that supports patient safety investigation without exposing patient identity. Address offline time, duplicates, ordering, schema evolution, local capacity, collection recovery, and validation.

## Answers to the Exercises

### Answer 1

Event name identifies a stable occurrence class and schema. Body is display-oriented content. Attributes are typed facts. Resource identifies the emitter. Schema version binds field meanings. Logical operation ID groups retries pursuing one intent; attempt ID identifies one execution; trace ID correlates a path of work. Using patient ID or order ID inside the event name creates unbounded event classes; using one `request_id` for operation, attempt, and trace makes duplicates and retries impossible to distinguish.

### Answer 2

Remaining capacity is $50{,}000-5{,}000=45{,}000$. Net growth is $2{,}000-500=1{,}500$ records/s. Therefore

$$
T_{overflow}=45{,}000/1{,}500=30\text{ seconds}.
$$

The result assumes constant arrival and export rates, immediate usable capacity, no batching or variable record sizes, no retry amplification, and no concurrent consumer change. Burstiness can overflow earlier; disk spill or priority queues change the model. A good answer states a declared overflow policy and measures actual queue age, occupancy, and drops.

### Answer 3

Use event `billing.invoice.retry.completed`, schema `1.0.0`, event/observed timestamps, service and release identity, pseudonymous invoice reference, logical operation ID, attempt number and attempt ID, trace ID when present, bounded outcome, error type, retryability, next-delay milliseconds, and event ID. Exclude invoice contents, token, payment data, and raw provider response. A valid case has `outcome=retry_scheduled`, integer nonnegative delay, and error type. Invalid case one omits attempt identity, making duplicate delivery ambiguous. Invalid case two embeds an access token or uses string `"five minutes"` for a millisecond field. Tests validate required fields, types, enum, redaction, encoding, and end-to-end delivery.

### Answer 4

Synchronous files provide a narrow acknowledgment and local recovery but add I/O latency, rotation, disk exhaustion, and tailing complexity. Asynchronous stdout collection is operationally simple on many managed platforms but can lose records at process/container boundaries and depends on buffering and collector behavior. Direct export preserves a typed protocol but couples to network, SDK buffers, and remote backpressure. For diagnostics, use a bounded asynchronous established logger with stdout or local agent collection, drop/sampling policy by event class, loss counters, and nonblocking failure. For audit, use a separately authenticated append-protected channel with local durable queue, explicit admission failure policy, restricted access, and reconciliation. The exact choice depends on platform and safety requirements.

### Answer 5

Define named alarm, acknowledgment, configuration, sensor-health, connectivity, and device-lifecycle events with versioned typed fields. Use device and firmware identity plus a rotating pseudonymous encounter reference rather than patient identity. Record monotonic sequence, event time, clock quality, observed time, event ID, alarm class, bounded values and units, operator action class, and offline status. Keep an encrypted bounded local queue with priority reservation for safety events, explicit overflow alarm, authenticated upload, retry, and deduplication by event ID. Never infer causal order from clocks alone; combine sequence and domain transitions. Migrate with dual parsing for a bounded window, schema contract tests, simulated disconnection/crash/clock drift, known expected-event completeness tests, access and deletion tests, and clinician review of whether evidence answers safety questions. A complete answer also states that diagnostic evidence does not itself prove the cause of harm.

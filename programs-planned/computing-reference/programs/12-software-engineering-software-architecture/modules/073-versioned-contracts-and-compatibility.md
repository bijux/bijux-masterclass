---
module_id: SARCH-073
program: Software Engineering: Software Architecture
level: 2
module_number: 73
title: Versioned Contracts and Compatibility
status: complete
last_verified: 2026-09-06
---

# Versioned Contracts and Compatibility

## One-Page Review

### Governing question

How can independently changing producers, consumers, stored data, and intermediaries coexist across versions without confusing parseability, source compatibility, behavioral substitutability, or a version label with an end-to-end compatibility guarantee?

### Essential definitions

- a **contract** is an owned agreement about observable interaction, including syntax, semantics, timing, errors, ordering, authority, security, and lifecycle where applicable;
- a **contract version** identifies a declared revision of that agreement; it is not proof that an implementation conforms;
- **wire compatibility** means selected old and new encoders and decoders can exchange representations under stated rules;
- **source compatibility** means consumer source can compile or interpret against a changed contract without modification in a named language and toolchain;
- **binary compatibility** means already built consumers can link or load against a changed provider in a named platform and ABI;
- **behavioral compatibility** means accepted observations remain within the promises on which consumers are entitled to rely;
- **data compatibility** covers values persisted or queued under one version and later read, replayed, rewritten, restored, or migrated under another;
- a **compatibility window** is the supported set of version combinations and the time or event conditions governing them;
- **deprecation** announces that use is discouraged and may change or end; **sunset** announces an expected loss of availability;
- **capability negotiation** selects mutually supported behavior from explicit capabilities rather than inferring it only from version order.

### Central model, mechanism, or theorem

Let producer version $P_i$ emit traces in $W_i$, and consumer version $C_j$ accept traces in $A_j$ while preserving required semantics $S$. Define a directional relation

$$
P_i\rightsquigarrow C_j\iff W_i\subseteq A_j\land S(P_i,C_j).
$$

For deployed producer versions $I$ and consumer versions $J$, the compatibility envelope holds only if every required pair is supported:

$$
\forall i\in I,\forall j\in J_{\mathrm{required}}:\;P_i\rightsquigarrow C_j.
$$

Parsing is necessary for many contracts but insufficient for semantic compatibility. Because “backward” and “forward” are used inconsistently across ecosystems, always state the direction: *new producer to old consumer*, *old producer to new consumer*, or another exact pair.

### Critical invariants

- the contract identifies owner, consumers, authority, and normative observable behavior;
- version direction, medium, encoding, language, toolchain, and deployment window are explicit;
- syntax, wire, source, binary, behavior, data, security, and operations are assessed separately;
- producers do not emit a new value merely because a schema can encode it;
- unknown fields and values have specified preservation, rejection, or default behavior;
- mixed-version, replay, rollback, restore, retry, and failure cases are tested;
- deprecation supplies alternatives, notice, usage evidence, support policy, and accountable sunset;
- tolerant parsing does not silently accept ambiguous, unsafe, or unauthenticated meaning;
- compatibility claims include transitive intermediaries and generated-code behavior where relevant;
- old versions retire only after rare, offline, seasonal, recovery, and external consumers have evidence-backed disposition.

### Common failures

Common failures include calling additive changes universally safe; reusing field identifiers; assuming an unknown enum is harmless; testing only latest-to-latest; treating HTTP method or status syntax as application semantics; changing defaults, ordering, units, time zones, error behavior, idempotency, or authorization invisibly; trusting semantic-version numbers without conformance evidence; versioning only URLs; allowing tolerant readers to normalize malicious ambiguity; dropping unknown data during read-modify-write; deprecating without migration support; sunsetting from traffic silence alone; and forgetting stored messages, caches, backups, replays, SDKs, gateways, and offline clients.

### Compact example

Version 2 adds `REFUNDED` to an order-status enum. The binary schema calls the addition wire-safe, yet an old generated consumer uses an exhaustive switch and treats unknown values as `PAID`. The producer therefore deploys the new schema without emitting the value, consumers upgrade to preserve or reject unknowns safely, contract tests exercise mixed pairs, and only then is emission enabled. Wire parseability was one condition; application semantics and rollout ordering determined compatibility.

### Connections

[SARCH-072](072-evolutionary-architecture-principles.md) supplies invariant-preserving transition states. [SARCH-064](064-architecture-fitness-functions.md) supplies executable contract feedback. [SARCH-074](../ROADMAP.md) next uses stable contracts as seams for incremental decomposition.

## Governing Question

Distributed change turns compatibility into a relation across time. A provider can deploy before a consumer, a message can wait in a queue, a database row can outlive its writer, an offline device can reconnect months later, and a rollback can revive code that predates new values. “Version 2 is backward compatible” hides all of these directions and populations.

The architectural task is to define the observable contract, enumerate required version combinations, constrain what may be emitted, verify behavior under coexistence, and govern retirement. A version identifier helps select or discuss a contract. It cannot compensate for ambiguous semantics or an unsupported deployment path.

## Why This Matters

Compatibility is what permits independent evolution. Without it, every contract change requires coordinated deployment, global downtime, or duplicated systems. With careless compatibility, systems appear to interoperate while corrupting meaning. The dangerous failures are often successful parses that produce a wrong decision.

Contracts are broader than APIs. They include library interfaces, command-line behavior, files, database schemas, events, queues, object storage, identity claims, infrastructure modules, configuration, observability fields, operational procedures, and human agreements. Each has a medium, consumers, lifecycle, and failure semantics.

Modern schema tools offer powerful compatibility rules, but their guarantees are deliberately scoped. Protocol Buffers documentation, for example, distinguishes binary wire-safe from conditionally compatible and wire-unsafe changes, and warns that a wire-safe change can still break application code [6]. Architecture must carry the reasoning from representation through behavior and rollout.

## Prerequisites and Retrieval

Retrieve interface, contract, protocol, representation, syntax, semantics, schema, encoder, decoder, parser, serializer, ABI, precondition, postcondition, invariant, substitutability, producer, consumer, broker, gateway, registry, idempotency, retry, replay, ordering, default, unknown field, enumeration, capability, content negotiation, migration, deprecation, sunset, service-level objective, telemetry, and rollback.

From SARCH-072, retrieve compatibility windows, expand-and-contract change, mixed-version states, single authority, retirement evidence, and rollback limits. From API engineering, retrieve HTTP and service contract mechanics. This chapter owns architectural compatibility reasoning across forms; it does not replace the detailed rules of a particular protocol, language ABI, serialization system, or data engine.

## Learning Objectives

After completing this module, you should be able to:

1. define contracts beyond syntax and identify their authority and consumer populations;
2. state compatibility direction without ambiguous backward/forward shorthand;
3. distinguish wire, source, binary, behavioral, data, operational, and security compatibility;
4. build and test a required producer-consumer compatibility matrix;
5. reason about additive fields, unknown values, defaults, identifiers, narrowing, and semantic changes;
6. design mixed-version rollout, emission gates, negotiation, replay, rollback, and restore tests;
7. use semantic versioning, registries, schemas, SDKs, and consumer tests within their evidence limits;
8. design deprecation and sunset with discovery, migration, observation, and accountability;
9. identify robustness behavior that entrenches ambiguity or creates security risk;
10. retire contract versions without abandoning hidden, rare, external, or recovery consumers.

## Core Exposition

**Identify the contract surface.** Begin with observable interactions and entitled expectations. An HTTP contract may include method semantics, resource identity, status codes, representations, headers, authentication, authorization, idempotency, pagination, rate behavior, caching, latency, and error recovery. An event contract may add delivery, duplication, ordering, partitioning, schema identity, retention, replay, and ownership.

A schema is part of a contract, not the whole contract. `amount: integer` does not state currency, scale, sign, rounding, authority, or whether absence differs from zero. These semantics determine whether an apparently valid value preserves behavior.

**Name ownership and authority.** Identify who may change the contract, who owns the business meaning, who operates each intermediary, and who accepts retirement consequences. Producers should not redefine a shared concept unilaterally merely because they publish bytes.

Consumer obligations also belong in the contract. A consumer may need to ignore unknown optional fields, preserve them during forwarding, bound retries, or avoid depending on undocumented ordering. Hidden consumer behavior can become a de facto contract, but widespread reliance does not automatically make an unsafe behavior desirable. Investigate and govern it.

**State direction explicitly.** Teams use *backward compatible* to mean at least two different things: a new implementation accepts old artifacts, or old consumers accept new producer output. Replace the adjective with the pair and operation.

Examples include old data read by new code, new data read by old code, old client calling new service, new client calling old service, old binary linking to new library, new writer coexisting with old reader, and old event replayed through new processing. A compatibility matrix makes these claims reviewable.

**Separate compatibility dimensions.** Syntactic compatibility means the representation conforms to a grammar or schema. Wire compatibility means encoding and decoding interoperate. Source compatibility is language- and compiler-specific. Binary compatibility depends on ABI, linking, layout, and runtime. Behavioral compatibility asks whether the observable result honors promises.

Data compatibility adds time: values can persist, be copied, compacted, restored, and rewritten. Operational compatibility covers deployment, monitoring, support, recovery, and capacity. Security compatibility asks whether old and new peers preserve authentication, authorization, confidentiality, integrity, audit, and downgrade resistance. Passing one dimension does not imply another.

**Model consumer reliance.** Behavioral subtyping provides a useful discipline: replacement must not demand stronger preconditions or promise weaker postconditions than the abstraction permits [8]. Network contracts are not class hierarchies, but the reasoning transfers. A new service that rejects inputs previously promised valid strengthens preconditions; one that silently weakens an integrity result violates postconditions.

Consumers may rely on errors, timing bounds, ordering, idempotency, side effects, stable identifiers, and absence semantics. Documented contracts define legitimate reliance, but observational testing and support history can reveal accidental dependencies that must be migrated rather than ignored.

**Build a compatibility matrix.** List producer and consumer versions that can coexist, including gateways, brokers, caches, SDKs, batch jobs, offline devices, restore tools, and replay processors. Mark each pair supported, unsupported, conditional, untested, or unavailable. Attach evidence and expiry.

The required matrix is determined by deployment reality, not convenience. If consumer versions 1 and 2 remain active when producer 3 begins emitting, both pairs need support unless routing prevents interaction. Latest-to-latest success is irrelevant to an old consumer receiving new data.

**Distinguish acceptance from preservation.** An old reader may parse and ignore a new field, allowing new-producer-to-old-consumer exchange. If the old consumer reads, modifies, and reserializes the object, it may discard the unknown field. A later new reader sees lost information. Test round trips through intermediaries, not only endpoint parsing.

Unknown values require policy. Rejecting them can halt processing; mapping them to a known default can corrupt meaning; preserving them while limiting behavior may be safer. Generated libraries differ, so verify the exact language and version rather than inferring behavior from the wire specification.

**Treat additive change as conditional.** Adding an optional field is often representation-compatible when old readers ignore it and new readers define a safe absence behavior. It can still break strict validators, signatures, hashes, cache keys, size limits, exhaustive destructuring, privacy rules, or consumers that reject unknown members.

Adding an enum value can be wire-safe yet behaviorally unsafe. Adding an endpoint may create route ambiguity. Adding an event can violate a closed-world assumption. “Additive” describes shape, not universal compatibility.

**Preserve stable identifiers.** Field numbers, column meanings, event type identities, resource identifiers, and error codes can outlive names. Reusing an identifier can cause old data to be interpreted as a new concept. Protocol Buffers explicitly instructs authors to reserve deleted field numbers and names rather than reuse them [6].

Rename operations can also break JSON names, reflection, query clients, metrics, policy, or generated source while leaving a binary encoding unchanged. Inventory all representations and toolchains before classifying the change.

**Define absence, null, default, and empty.** These states often carry different meaning. A missing value may mean unknown, not applicable, withheld, use default, or unchanged. A schema that collapses absence into a zero value prevents consumers from distinguishing these cases.

When adding a field, define new-reader behavior for old data and old-reader behavior for new data. Avoid changing the default of an omitted field silently. Persisted data and patch/update operations make presence semantics especially important.

**Constrain value domains during rollout.** A representation change from 32-bit to 64-bit integer may be decodable both ways for small values while losing large values in an old reader. Deploying the new schema is not permission to emit the expanded range. Separate *accept* and *emit* gates.

First make readers accept both domains, observe adoption, then allow writers to emit new values only after incompatible readers are gone or isolated. The same pattern applies to enum values, new required semantics, stronger algorithms, and larger messages.

**Design expand-and-contract contracts.** Expand by adding a representation or operation that old and new participants can coexist with. Migrate consumers and data. Contract only after evidence shows the old form is no longer required.

For a field rename, temporarily read old and new names, define precedence when both occur, write the old form until readers upgrade, then write both or the new form under an explicit plan, and finally retire the old form. Beware dual write: mismatched values require deterministic resolution and observability.

**Test mixed-version behavior.** Contract tests should exercise every required matrix pair, representative values, unknowns, omitted and null fields, limits, invalid inputs, error responses, retries, timeouts, duplicate delivery, ordering, authentication, authorization, and downgrade attempts. Include generated code and actual serialization routes.

Replay stored messages through new consumers, and send new messages through supported old consumers. Restore old backups into new software and, if rollback is claimed, new data into old software. A passing schema-diff rule is a useful early check, not complete evidence.

**Use consumer evidence without surrendering ownership.** Consumer-driven contract tests can reveal actual expectations and protect independently released consumers. They can also freeze incidental behavior, omit absent consumers, or let one consumer dictate a shared semantic contract.

The provider owns coherent domain semantics and service integrity; consumers supply evidence of reliance. Review conflicts through product and architecture authority. Verify test provenance, deployed consumer version, and whether generated requests represent production behavior.

**Use semantic versioning as communication.** Semantic Versioning 2.0.0 defines `MAJOR.MINOR.PATCH` changes relative to a declared public API [5]. It is a labeling convention, not an automatic compatibility proof. If the public API is vague, the version meaning is vague.

A major version announces possible incompatibility; it does not provide migration. A minor version can still break consumers when an “additive” behavior violates hidden or undocumented assumptions. Dependency ranges, lockfiles, resolution, transitive dependencies, prereleases, and artifact mutability determine what actually runs.

**Choose version selection deliberately.** Versions can appear in media types, protocol negotiation, message metadata, schema identifiers, package names, namespaces, URLs, or capabilities. No location is universally best. URL versioning is visible but can imply resource duplication; header negotiation can be less discoverable; message metadata can support asynchronous replay but must be trustworthy.

Separate contract version from product release and deployment instance. Several implementations may conform to one contract, and one deployment may support several contracts. Avoid using dates or build numbers as unexplained semantic versions.

**Prefer capabilities when version order is insufficient.** Version numbers assume a meaningful sequence, yet deployments can support different optional features. Capability negotiation identifies features or algorithms both peers support. It needs authenticated inputs, deterministic selection, downgrade protection, and a failure mode when no safe intersection exists.

Do not infer security capability from client-supplied version text alone. Record negotiated outcome for diagnosis. Retire weak capabilities explicitly rather than allowing permanent fallback.

**Apply robustness with caution.** Tolerant readers can support extension by ignoring information they do not understand. Excessive tolerance can normalize invalid messages, create divergent interpretations, preserve implementation bugs as protocol, and enable security attacks. RFC 9413 explains why indiscriminate application of the robustness principle can harm protocol evolution [3].

Be strict about security boundaries, message framing, ambiguous syntax, invariants, and corrupted data. Be intentionally extensible at specified points. Preserve unknown information when forwarding if the contract requires it, but do not execute unknown semantics.

**Version behavior, not only representation.** Changes to error status, retryability, idempotency, pagination, ordering, consistency, latency, rate limits, rounding, time zones, locale, authorization, and side effects can break consumers with identical schemas. Write quality-attribute and failure scenarios for the contract.

HTTP provides standardized method and status semantics [2], but application resource behavior still requires explicit definition. Do not use a successful HTTP parse or a `200` response as proof that the business contract was preserved.

**Account for intermediaries.** Gateways may strip headers, brokers may transform or redeliver, caches may serve old representations, service meshes may retry, SDKs may normalize, and ETL jobs may flatten fields. Each intermediary is both a consumer and producer in the matrix.

Test end-to-end paths and read-modify-write behavior. Preserve correlation and schema identity. A direct provider test cannot establish compatibility through an independently configured production gateway.

**Design deprecation as a migration service.** Deprecation identifies scope, date, reason, replacement, migration guide, owner, support channel, observed consumers, and planned decision points. It does not immediately remove availability. RFC 9745 standardizes an HTTP `Deprecation` response field and link relation for communicating deprecation [4].

Notice must reach people who can act. Headers help only clients that inspect them. Use documentation, registries, SDK diagnostics, account contacts, build warnings, dashboards, and governance appropriate to the consumer population.

**Distinguish sunset.** RFC 8594 defines the HTTP `Sunset` field as a signal that a resource is expected to become unavailable at a specified time and treats the timestamp as a hint rather than a guarantee [9]. Deprecation and sunset can be related but answer different questions.

A sunset decision needs authority, alternatives, notice obligations, usage evidence, exceptions, and behavior after the date. Avoid promising availability until the exact instant when dependencies, caches, clocks, and deployment schedules cannot support that precision.

**Observe adoption without equating silence with absence.** Measure calls by authenticated consumer identity, contract version, capability, route, and time. Include errors and rejected negotiation so incompatible attempts are not invisible. Respect privacy and avoid using telemetry as individual surveillance.

Traffic silence may miss offline, seasonal, disaster-recovery, batch, or blocked consumers. Combine telemetry with registry ownership, dependency scans, artifact downloads, support history, contracts, and explicit attestations. Define evidence windows based on use cycles.

**Retire completely.** Remove old routes, schemas where safe, SDKs, generated types, transforms, credentials, policies, dashboards, runbooks, replay paths, fixtures, documentation, and infrastructure. Reserve identifiers that must never be reused. Retain governed archival decoding where records outlive operational support.

After sunset, monitor unexpected access and have an authorized response policy. Do not quietly restore an insecure version indefinitely. Feed retirement findings back into ownership and discovery practices.

## Definitions and Notation

Let:

- $P_i$ be producer implementation or contract version $i$;
- $C_j$ be consumer implementation or contract version $j$;
- $W_i$ be the set of traces or representations $P_i$ may emit within the declared operating domain;
- $A_j$ be the set $C_j$ can accept without parse or protocol failure;
- $S(P_i,C_j)$ assert preservation of required application semantics for the pair;
- $P_i\rightsquigarrow C_j$ mean $W_i\subseteq A_j\land S(P_i,C_j)$;
- $M_{ij}\in\{\text{supported},\text{conditional},\text{unsupported},\text{untested},\text{unavailable}\}$ be a compatibility-matrix entry;
- $I_t$ and $J_t$ be producer and consumer versions deployed or otherwise reachable at time $t$;
- $J_t^*\subseteq J_t$ be consumers required by policy to interoperate;
- $E_{ij}$ be evidence for a pair, including toolchain, environment, values, behavior, and limits;
- $\tau_j$ be the retirement or review condition for consumer version $j$.

A trace can include inputs, outputs, timing, state transitions, errors, and side effects. Consequently $S$ is stronger than successful decoding. Real systems approximate the sets through specifications, tests, analysis, observation, and governance; they do not enumerate every possible trace.

## Mechanisms, Invariants, or Proof Structure

**Directional compatibility.** If $W_2\subseteq A_1$, new producer representations are parseable by the old consumer. This does not imply $W_1\subseteq A_2$, and neither inclusion implies $S$. Compatibility is not symmetric unless both directional and semantic obligations are established.

**Nontransitivity warning.** Even if a transformation makes $P_3$ compatible with $C_2$, and another makes $P_2$ compatible with $C_1$, it does not follow that $P_3$ is compatible with $C_1$. Transformations can lose or reinterpret information. Test required endpoint and intermediary compositions rather than assuming version adjacency composes.

**Executable matrix.** This toy program separates emitted enum values from accepted values.

<!-- bijux-verify: {"id":"directional-compatibility-matrix","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"P1->C1: supported\nP1->C2: supported\nP2->C1: unsupported (REFUNDED)\nP2->C2: supported\nrequired_envelope=false\n","stderr":""}} -->
```python
producer_values = {
    "P1": {"NEW", "PAID"},
    "P2": {"NEW", "PAID", "REFUNDED"},
}
consumer_values = {
    "C1": {"NEW", "PAID"},
    "C2": {"NEW", "PAID", "REFUNDED"},
}

matrix = {}
for producer, emitted in producer_values.items():
    for consumer, accepted in consumer_values.items():
        unknown = emitted - accepted
        matrix[(producer, consumer)] = not unknown
        detail = "supported" if not unknown else f"unsupported ({','.join(sorted(unknown))})"
        print(f"{producer}->{consumer}: {detail}")

required = {("P1", "C1"), ("P1", "C2"), ("P2", "C1"), ("P2", "C2")}
print(f"required_envelope={str(all(matrix[pair] for pair in required)).lower()}")
```

Execution verifies set inclusion for four finite value sets. It deliberately omits unknown-value preservation and application semantics, so it is an early incompatibility detector rather than proof of contract compatibility.

**Emission-gate invariant.** A producer can deploy code capable of a new value while remaining compatible if it does not emit that value to unsupported consumers. Capability and behavior activation are distinct state changes. Routing, negotiation, or global adoption evidence must make the gate enforceable.

**Round-trip counterexample.** Let an old intermediary accept a record with unknown field $u$ but serialize only known fields. Direct new-to-old parsing succeeds, yet new-to-old-to-new loses $u$. Therefore endpoint acceptance does not imply preservation through a chain.

**Retirement invariant.** A version is removable only when every required consumer has migrated, been isolated, been explicitly released from support by accountable policy, or been provided an authorized alternative. An empty recent traffic set is evidence, not logical proof, that the consumer set is empty.

## Alternatives and Trade-Offs

**Parallel versions versus one evolving version.** Parallel major versions isolate incompatible semantics but duplicate operations, fixes, security work, and documentation. One evolving contract reduces variants but demands careful mixed-version compatibility. Choose based on consumer control, change magnitude, and support horizon.

**Schema-first versus code-first.** Schema-first workflows make review and generation explicit but can drift from implementation. Code-first extraction follows source but may expose language accidents and unstable generation. In both cases, validate the published artifact against actual behavior.

**Strict versus tolerant readers.** Strict readers detect deviations early and protect invariants but can impede specified extension. Tolerant readers support extension but can conceal errors and diverge. Define extension points and strict boundaries rather than applying either rule universally.

**Version negotiation versus capability negotiation.** Version negotiation is compact and works for coherent revisions. Capabilities handle independent features but create combinations and downgrade risks. A protocol may use a base version plus a bounded, authenticated capability set.

**Provider tests versus consumer-driven tests.** Provider tests enforce coherent intended behavior; consumer tests reveal reliance. Either alone has blind spots. Maintain provider-owned semantics and combine representative consumer evidence with end-to-end mixed-version checks.

**Long compatibility window versus coordinated change.** Long windows support uncontrolled and offline clients but increase complexity and vulnerability exposure. Coordinated change can simplify rapidly when all participants share authority, yet creates deployment coupling. Match the window to real consumer control and consequence.

**Explicit break versus silent compatibility shim.** A major break forces migration visibility but can fragment consumers. A shim eases transition but may preserve obsolete semantics and become permanent. Give shims metrics, ownership, expiry, and removal tests.

## Failure Modes and Misconceptions

1. **“Backward compatible is precise.”** Direction and operation must be stated because ecosystems use the term differently.
2. **“Valid syntax means compatible behavior.”** A parsed message can still produce the wrong decision.
3. **“Additive is always safe.”** Strict readers, enums, signatures, limits, and privacy policies can break.
4. **“Unknown means ignore.”** Unknown values may require preservation, rejection, quarantine, or bounded behavior.
5. **“A major version solves migration.”** It labels incompatibility but supplies no coexistence or retirement mechanism.
6. **“A minor version cannot break.”** Semantic versioning depends on a declared public API and honest classification.
7. **“Latest-to-latest passing is enough.”** Required mixed pairs determine the deployment envelope.
8. **“The broker guarantees event compatibility.”** A broker transports records; application semantics and replay remain producer-consumer concerns.
9. **“An old reader that parses also preserves.”** Read-modify-write can discard unknown information.
10. **“A URL is the contract version.”** Behavior, schemas, dependencies, and capabilities may evolve independently.
11. **“Tolerant parsing is always robust.”** Ambiguity and downgrade tolerance can entrench bugs or enable attacks.
12. **“Deprecation means unavailable.”** It communicates discouraged use; sunset addresses expected unavailability.
13. **“A sunset timestamp is a guarantee.”** RFC 8594 describes it as a hint, and operations need explicit policy.
14. **“Zero traffic means zero consumers.”** Rare, offline, seasonal, recovery, and blocked consumers can be invisible.
15. **“Rollback means deploy old code.”** New persisted state, messages, and side effects may make old code unsafe.
16. **“Consumer tests define the domain.”** They reveal reliance but do not transfer semantic authority automatically.
17. **“Compatibility composes transitively.”** Intermediary transformations can lose or reinterpret information.
18. **“Retirement ends at route deletion.”** SDKs, data, identities, replays, documentation, and support paths remain.

## Worked Examples

### Example 1

**Situation.** Producer P2 adds `REFUNDED`; consumer C1 recognizes only `NEW` and `PAID`.

**Reasoning.** The schema decoder may preserve the unknown numeric enum, but C1's exhaustive business logic maps its default branch to paid. Thus successful decoding does not establish $S(P_2,C_1)$. Deploying P2 code is safe only while emission is gated away from C1 or C1 is changed to preserve or safely quarantine unknown values.

**Conclusion.** Enum extension is a directional representation claim whose behavioral safety depends on consumer code and rollout.

### Example 2

**Situation.** A JSON API adds optional `middle_name` to responses.

**Reasoning.** Most clients ignore it, but one signs the exact canonical field set and another rejects additional properties. A cache key includes serialized bytes, increasing variants. The provider cannot claim universal safety from optionality. It inventories supported clients, tests actual SDKs, updates the strict schema and signature rule, and gates exposure until required consumers accept it.

**Conclusion.** An additive field can break validation, integrity, and operational behavior without changing existing field meanings.

### Example 3

**Situation.** Field 7 is deleted from a binary message and later reused for `tax_identifier`.

**Reasoning.** Old stored messages contain field 7 with address semantics. New decoders can interpret those bytes as a tax identifier, causing corruption or disclosure. Removing current source references did not erase historical data. The correct evolution reserves the identifier and assigns a new number, with governed decoding for archives.

**Conclusion.** Stable wire identifiers belong to the lifetime of persisted data, not merely current deployments.

### Example 4

**Situation.** A new reader widens `quantity` from 32 to 64 bits; old readers remain active.

**Reasoning.** Small values exchange in both directions, but a value above the old maximum can truncate or fail. The team first deploys new readers everywhere, continues enforcing the old range at writers, verifies adoption and rollback, then separately enables larger emission. It records the range gate as a contract state.

**Conclusion.** Conditional wire compatibility requires controlling values, not just publishing a widened type.

### Example 5

**Situation.** An old intermediary ignores an unknown `consent_basis` field and forwards the record.

**Reasoning.** Direct parse succeeds, but the intermediary rebuilds JSON from its typed model and drops the unknown field. The downstream new service then applies a default basis, which is semantically and legally unsafe. Round-trip tests expose the loss. The path is blocked until the intermediary preserves unknowns or is bypassed through an authorized design.

**Conclusion.** Compatibility must cover transformations and information preservation across the entire path.

### Example 6

**Situation.** An HTTP operation changes a timeout response from `503` with `Retry-After` to `200` with `{status:"pending"}`.

**Reasoning.** The JSON parses and the method remains unchanged, but clients no longer activate bounded retry and may treat the order as complete. Monitoring based on 5xx rates also becomes blind. The provider must introduce the pending state as an explicit contract, update clients and outcome telemetry, and preserve idempotent polling semantics during coexistence.

**Conclusion.** Status and error behavior are part of the contract because they control client state transitions and operations.

### Example 7

**Situation.** A package changes from `2.4.1` to `2.5.0`, so maintainers assume every consumer can upgrade automatically.

**Reasoning.** The public API declaration excludes logging text, but a supported operations parser depends on a documented log field whose default changes. A broad dependency range resolves the new artifact on the next build. Semantic versioning communicates the publisher's classification; it does not test every consumer or freeze artifacts. The team narrows the public contract, adds a log-schema test, and uses lockfile review.

**Conclusion.** Version numbers support governance only when public API, resolution, artifacts, and conformance evidence are explicit.

### Example 8

**Situation.** A protocol server accepts duplicate conflicting length fields “for robustness,” while different intermediaries choose first or last.

**Reasoning.** Tolerance creates ambiguous framing and divergent interpretations across a request path. An attacker can exploit the disagreement. The maintained contract rejects ambiguity consistently, tests intermediaries, and documents the extension points where unknown fields may be ignored. Compatibility with a defective peer is handled through a bounded repair plan, not universal normalization.

**Conclusion.** Strictness at security-sensitive ambiguity boundaries can improve long-term interoperability and safety.

### Example 9

**Situation.** An API has emitted a deprecation signal for six months and shows no traffic for thirty days.

**Reasoning.** Registry review finds an annual reporting job, a disaster-recovery client, and a customer device that buffers offline. The team provides a replacement SDK, exercises recovery, observes a complete annual cycle or obtains accountable migration evidence, and defines post-sunset behavior. It communicates deprecation and sunset through both protocol fields and human channels.

**Conclusion.** Retirement evidence must match consumer use cycles; recent traffic silence is insufficient.

### Example 10

**Situation.** Two peers support protocol versions 3 and 4, but only some version-4 deployments support encrypted compression.

**Reasoning.** Selecting the maximum version does not establish feature intersection. Peers negotiate an authenticated capability set, reject unsafe downgrade, and record the selected algorithm. If there is no approved common capability, the connection fails explicitly. Version 4 remains the base semantics while capability negotiation handles optional independently deployed behavior.

**Conclusion.** Capabilities complement versions when feature support is not totally ordered, but require security and combinatorial discipline.

## Cross-Program Connections

- [OOP](../../02-programming-languages-object-oriented-programming/ROADMAP.md) supplies substitutability, interface evolution, and source/binary compatibility concerns within object systems.
- [CONPAR](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies ordering, atomicity, retry, and mixed-version concurrency reasoning.
- [SDRE](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) implements staged rollout, observability, artifact control, rollback, and deprecation operations.
- [DBE](../../18-database-engineering/ROADMAP.md) develops schema evolution, transaction boundaries, backup, restore, and migration behavior for persisted contracts.
- [DARCH](../../20-data-architecture-engineering/ROADMAP.md) connects schemas to lineage, ownership, retention, and downstream analytical consumers.
- [SEC](../../25-security-engineering/ROADMAP.md) develops downgrade resistance, parser ambiguity, authentication, authorization, and retirement of weak mechanisms.
- [SYSENG](../../26-systems-engineering/ROADMAP.md) supplies interface control, configuration baselines, supplier management, verification, and lifecycle disposition.
- [API](../../28-api-and-service-engineering/ROADMAP.md) provides protocol-specific API design and lifecycle practices complementary to this architecture-level treatment.

## References

1. Martin Kleppmann. *Designing Data-Intensive Applications*. O'Reilly Media, 2017.
2. Roy T. Fielding, Mark Nottingham, and Julian Reschke, eds. “HTTP Semantics.” RFC 9110, Internet Standard 97, June 2022. https://www.rfc-editor.org/rfc/rfc9110.html
3. Martin Thomson. “Maintaining Robust Protocols.” RFC 9413, Internet Architecture Board, June 2023. https://www.rfc-editor.org/rfc/rfc9413.html
4. Sanjay Dalal and Erik Wilde. “The Deprecation HTTP Response Header Field.” RFC 9745, IETF Standards Track, March 2025. Checked 2026-09-06. https://www.rfc-editor.org/rfc/rfc9745.html
5. Tom Preston-Werner. “Semantic Versioning 2.0.0.” June 2013. Checked 2026-09-06. https://semver.org/spec/v2.0.0.html
6. Google. “Protocol Buffers: Language Guide (proto3), Updating a Message Type.” Current documentation checked 2026-09-06. https://protobuf.dev/programming-guides/proto3/#updating
7. Apache Software Foundation. “Apache Avro 1.12.0 Specification.” 2024. Checked 2026-09-06. https://avro.apache.org/docs/1.12.0/specification/
8. Barbara H. Liskov and Jeannette M. Wing. “A Behavioral Notion of Subtyping.” *ACM Transactions on Programming Languages and Systems* 16, no. 6 (1994): 1811–1841. https://doi.org/10.1145/197320.197383
9. Erik Wilde. “The Sunset HTTP Header Field.” RFC 8594, May 2019. https://www.rfc-editor.org/rfc/rfc8594.html
10. David A. Wheeler and Gregory V. Trost. “Deprecating the ‘X-’ Prefix and Similar Constructs in Application Protocols.” RFC 6648, BCP 178, June 2012. https://www.rfc-editor.org/rfc/rfc6648.html

## Exercises

### Exercise 1

Define contract, wire compatibility, source compatibility, binary compatibility, behavioral compatibility, data compatibility, compatibility window, deprecation, sunset, and capability negotiation. Explain why “backward compatible” alone is underspecified.

### Exercise 2

Producer P1 emits `{OPEN,CLOSED}` and P2 emits `{OPEN,CLOSED,HELD}`. Consumer C1 accepts `{OPEN,CLOSED}`, C2 accepts all three but converts unknown future values to `CLOSED`. Compute representation inclusion for all four pairs and explain which semantic claims remain unresolved.

### Exercise 3

A schema registry approves an optional field addition, yet one consumer fails and another loses the field on forwarding. Diagnose why the registry result was insufficient and design focused mixed-version evidence.

### Exercise 4

Design a versioning, compatibility, deprecation, and retirement policy for an event contract used by internal services, customer webhooks, offline mobile clients, a yearly audit job, and long-lived archives.

### Exercise 5

A public emergency-alert interface must change its location encoding while serving assistive devices, municipal systems, radio gateways, mobile applications, and delayed disaster-recovery replays. Propose a compatibility transition without claiming that ordinary contract tests certify public safety or accessibility.

## Answers to the Exercises

### Answer 1

A contract is an owned agreement over observable interaction, including representation and relevant semantics, timing, errors, authority, security, and lifecycle. Wire compatibility concerns encoding and decoding. Source compatibility concerns recompilation or interpretation of consumer source in a named language and toolchain. Binary compatibility concerns already built artifacts and a named ABI/runtime. Behavioral compatibility preserves promises on which consumers may rely. Data compatibility covers persisted, queued, replayed, rewritten, restored, and migrated values. A compatibility window is the supported version set and its time or event bounds. Deprecation discourages use and announces likely change; sunset communicates expected unavailability. Capability negotiation selects explicitly shared behavior.

“Backward” can mean new code reads old data or old clients accept new output, among other directions. It also omits compatibility dimension and semantics. A useful statement names producer, consumer, operation, representation, environment, and supported behavior.

### Answer 2

For representation sets, $P1\rightsquigarrow C1$ passes inclusion, $P1\rightsquigarrow C2$ passes, $P2\rightsquigarrow C1$ fails because `HELD` is outside C1's accepted set, and $P2\rightsquigarrow C2$ passes. These set results establish only declared value acceptance.

They do not establish what C2 does with `HELD`, whether `CLOSED` substitution is permitted for a future unknown, whether unknown values survive forwarding, or whether timing, errors, authority, and side effects remain correct. C2's default-to-closed policy could be dangerous if an unknown status must not trigger closure. Semantic compatibility requires domain-specific postconditions and tests.

### Answer 3

The registry evaluated a schema rule, not every parser, validator, signature, generated model, or intermediary. The failing consumer may reject unknown properties; the forwarding consumer may deserialize into a closed type and reserialize only known fields. Both are compatible with the registry approving shape under narrower assumptions.

Evidence should include new-producer-to-each-supported-old-consumer tests with absent, null, default, boundary, and unexpected values; old-producer-to-new-consumer tests; read-modify-write round trips; exact generated libraries and versions; gateway or broker transformations; signature and size behavior; and application postconditions. Gate emission to consumers proven compatible, preserve unknown fields where required, and record unsupported pairs rather than weakening the registry rule into a universal claim.

### Answer 4

Assign semantic ownership and publish a versioned schema plus delivery, duplication, ordering, idempotency, security, privacy, and replay semantics. Maintain a matrix for producers, internal consumers, webhook versions, mobile releases, audit processing, archive readers, brokers, and transforms. Use stable identifiers, reserve removed values, define unknown and presence behavior, and separate reader deployment from new-value emission.

Internal services can use automated consumer evidence and staged emission. Webhooks need negotiated or endpoint-bound versions, signed payload rules, delivery telemetry, documentation, migration support, and contractual notice. Offline clients require a compatibility window based on reconnection behavior. The yearly job must be exercised or explicitly migrated before retirement. Archives need durable schema identity, decoding artifacts, integrity, retention, and restore/replay tests.

Deprecation names replacement, date, owner, support, and usage. Sunset requires accountable policy and behavior after the date. Retirement removes routes, schemas only where safe, transforms, credentials, SDKs, docs, replay paths, and support procedures while retaining required archival decoding. Evaluation requires explicit mixed pairs, semantics, rare-use evidence, and authority—not simply a schema-registry pass.

### Answer 5

Establish accountable public-safety, emergency-management, accessibility, security, privacy, legal, regulatory, municipal, device, and operations authorities. Baseline every encoding, coordinate system, unit, datum, precision, language, assistive behavior, gateway transform, offline store, signature, and replay path. Define invariants: one unambiguous location interpretation, authenticated provenance, preserved urgency and expiry, accessible rendering, bounded delivery, and no silent fallback to a wrong location.

Expand the contract with an explicit new location object and version or capability marker while retaining the old form. Define precedence if both appear, reject contradictions safely, and never infer units. Deploy tolerant-but-validating readers to controlled participants before enabling new emission. Use conformance suites, recorded governed messages, simulations, gateway round trips, assistive-device studies led by qualified accessibility experts, security analysis, and authorized emergency exercises. Segment telemetry without exposing sensitive recipients.

Gate emission by authenticated capability or known endpoint version; provide translation only where semantics are lossless and visible. Maintain old encoding for the authorized window, including delayed replays and offline devices. Deprecation and sunset require multi-channel notice, procurement and field-upgrade plans, exception authority, and post-sunset behavior. Reserve old identifiers and retain archival decoders. Ordinary contract tests support technical evidence but do not certify public safety, accessibility, legal compliance, or emergency readiness; those decisions remain with the responsible authorities.

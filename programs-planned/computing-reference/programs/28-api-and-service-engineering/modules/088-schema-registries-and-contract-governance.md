---
module_id: API-088
program: API & Service Engineering
level: 2
module_number: 88
title: Schema Registries and Contract Governance
status: complete
last_verified: 2026-09-02
---

# Schema Registries and Contract Governance

## One-Page Review

### Governing question

How should an organization identify, store, relate, validate, approve, distribute, observe, and retire API/event schemas so registry automation strengthens contract governance without mistaking structural compatibility for behavioral safety?

### Essential definitions

- A **schema registry** is a governed system of record/distribution for immutable schema or contract artifacts plus identity, references, metadata, policy, and lifecycle state.
- A **subject** is the compatibility lineage against which versions are compared; its boundary is a governance decision, not merely a storage key.
- A **schema identity** names exact content under a declared format/dialect; a version is an ordered position in a subject’s history.
- **canonicalization** normalizes permitted representation differences for comparison/deduplication; it must be format/version defined.
- **backward compatibility** usually asks whether a new reader can consume old data; **forward compatibility** whether an old reader can consume new data; exact meaning depends on format/tool/configuration.
- **transitive compatibility** compares a candidate with all governed prior versions rather than only the latest.
- A **reference** is a pinned dependency from one immutable artifact to another exact identity/version.
- A **contract bundle** includes schema plus operation/channel semantics, security, errors, examples, policies, ownership, and generated/test evidence.

### Central model, mechanism, or theorem

For candidate contract $c$ in subject $s$, registry admission is conjunctive:

$$
\operatorname{admit}(c,s) \Rightarrow V(c)\land I(c,s)\land P(c,s)\land R(c)\land A(c,s),
$$

where $V$ is syntax/dialect validation, $I$ identity/provenance integrity, $P$ configured structural policy against the correct comparison set, $R$ resolved immutable references, and $A$ required review/authorization evidence. Even when admitted, deployment additionally requires behavioral, security, compatibility, implementation, and consumer evidence outside the schema checker.

### Critical invariants

Published content is immutable and content-addressable; corrections create a new identity/version. Subject scope, format/dialect, canonicalization, comparison direction/set, tool/rule versions, owner, lifecycle, provenance, and decision evidence are explicit. References pin exact artifacts and cycles/deletion are controlled.

Producers/consumers negotiate or bind schema identity safely; unknown IDs fail boundedly. Registry/control-plane outage does not require unsafe per-message remote lookup on the data path. Policy changes are versioned and impact-tested. Generated clients/docs/tests trace to the same approved artifact. Structural pass never proves semantic, authorization, operational, or consumer compatibility.

### Common failures

One global subject; subject per deployment; mutable “latest”; sequential version mistaken for global identity; raw-text hashes across unstable formatting; hidden dialect defaults; latest-only checks after an incompatible historical version; backward/forward direction confused; policy changed silently; unresolved/floating references; deleting referenced schemas; circular imports; registry consulted synchronously per request/event; ID collision across environments; untrusted producer registers arbitrary schema; secrets/PII in examples; schema pass treated as design approval; generated artifacts drift; runtime payload differs from registered contract; rollback cannot read new data; unknown schema IDs poison queues; compatibility exceptions never expire; and no ownership/retirement/audit.

### Compact example

An event team adds optional field `currency` with a default. Registry backward-check passes against the latest Avro schema. Historical version 3 used the same field name with incompatible meaning, so a transitive comparison and semantic review fail. The subject stays unchanged; the team selects a new stable field, tests old/new readers and replayed records, and publishes immutable version 8 with provenance. **Conclusion:** format compatibility is one admission predicate, not the contract decision.

### Connections

[JSON Schema](022-json-schema.md), [OpenAPI Structure](023-openapi-structure.md), [Protocol Buffers Evolution](052-protocol-buffers-and-schema-evolution.md), [Event Schema Design](062-event-schema-design.md), and [AsyncAPI Contracts](063-asyncapi-contracts.md) supply format semantics. [Compatibility](081-backward-and-forward-compatibility.md), [Design Reviews](087-design-reviews.md), and [Consumer Inventory](085-consumer-inventory-and-usage-evidence.md) supply governance evidence.

## Governing Question

What exact registry identities, subject boundaries, compatibility rules, references, lifecycle states, authorization controls, delivery patterns, and evidence gates preserve contract integrity across HTTP, RPC, GraphQL, events, webhooks, generated artifacts, and independent deployments?

## Why This Matters

Schemas become coordination infrastructure. Producers serialize data, consumers generate code, gateways validate messages, documentation renders contracts, tests create fixtures, and governance makes release decisions from them. If those actors resolve different “latest” files, compatibility claims and incident diagnosis collapse.

A registry can make identity, history, comparison, ownership, and distribution reliable. It can also centralize mistakes. Wrong subject granularity compares unrelated contracts or lets coupled contracts evolve independently. A mislabeled compatibility direction gives false confidence. Mutable artifacts invalidate builds and audits. Synchronous data-path lookup turns control-plane trouble into production outage.

Schema languages describe different things. JSON Schema validation depends on dialect/vocabulary and instance shape. OpenAPI describes HTTP interfaces. AsyncAPI describes message-driven interfaces. Protobuf has field-number/wire/generated-language rules. Avro reader/writer resolution differs again. A generic “compatible” badge without format, direction, comparison set, and tool version is meaningless.

Most breaking changes are not purely structural. Tightened authorization, changed default, different currency unit, reduced quota, new side effect, changed ordering, removed error, or slower completion can pass a schema comparison. Registry governance must join machine checks with design, implementation, consumers, rollout, telemetry, and lifecycle evidence.

## Prerequisites and Retrieval

Retrieve [API Contracts and Behavioral Guarantees](021-api-contracts-and-behavioral-guarantees.md), [JSON Schema](022-json-schema.md), [OpenAPI Structure](023-openapi-structure.md), [Protocol Buffers and Schema Evolution](052-protocol-buffers-and-schema-evolution.md), [Event Schema Design](062-event-schema-design.md), [AsyncAPI Contracts](063-asyncapi-contracts.md), [Backward and Forward Compatibility](081-backward-and-forward-compatibility.md), [Consumer Inventory](085-consumer-inventory-and-usage-evidence.md), [API Style Guides](086-api-style-guides.md), and [Design Reviews](087-design-reviews.md).

Retrieve registry topology/configuration/version; supported formats/dialects; subject naming and tenancy; canonicalization/fingerprinting; compatibility modes and tool versions; all schema histories/references; producer/consumer bindings; generated artifacts; ownership/catalog; review/exception/deprecation records; ACL/audit/signing/supply-chain controls; backup/restore/replication; caches and unknown-ID behavior; runtime validation/telemetry; consumer inventory and replay/rollback requirements.

## Learning Objectives

After completing this module, you can:

1. distinguish artifact identity, version, subject, format, dialect, canonical form, fingerprint, and contract bundle;
2. choose subject boundaries from compatibility lineage, ownership, deployment, tenancy, and reuse;
3. specify backward, forward, full, latest, and transitive comparison semantics without direction ambiguity;
4. manage immutable references, dependency graphs, cycles, reuse, deprecation, retention, and deletion;
5. design registration/promotion authorization, provenance, signing, audit, and environment controls;
6. integrate registry checks with design review, style, semantic diff, generated artifacts, tests, rollout, and consumer evidence;
7. avoid control-plane/data-plane coupling through caching, pinning, embedding, and bounded unknown-ID behavior;
8. detect producer/consumer/runtime drift and prove rollback/replay across deployed versions;
9. govern policy migrations, compatibility exceptions, repair, disaster recovery, and federation; and
10. explain precisely what schema compatibility does and does not establish.

## Core Exposition

### Define the registry’s authority

Decide whether the registry is authoritative for source contracts, released artifacts, serialization IDs, generated packages, or discovery metadata. One system need not own all, but precedence and synchronization must be explicit.

Keep authored source in reviewed version control where appropriate, then publish verified immutable artifacts. The registry records provenance: repository/commit, build, signer, format/dialect, toolchain, review decision, owner, timestamp, and promotion environment. Reverse links make production identity traceable to source.

Do not let “uploaded successfully” mean “approved for production.” Model states such as proposed, validated, approved, published, deployed, deprecated, retired, quarantined, and revoked, with authorized transitions.

Define tenant and environment boundaries. A numeric ID meaningful in development must not be accepted as production identity unless namespace/issuer is authenticated.

### Design artifact and subject identity

Use immutable content identity plus ordered subject version. Content identity deduplicates exact canonical artifacts; subject version expresses lineage/order. Neither replaces a human/domain name and owner.

Subject boundary is the population that must remain mutually compatible under one policy. Event value schemas might be keyed by stable event type, not transient topic or deployment. Request/response contracts may evolve together as an API bundle. Shared component subjects increase reuse but also coupling and blast radius.

Avoid subject per deployment instance: it bypasses cross-release checking. Avoid one enterprise subject: unrelated contracts block each other. Record aliases, moves, splits, merges, and predecessor relationships without rewriting history.

Identity includes format and exact dialect/edition. The same JSON text interpreted under different JSON Schema dialects is not automatically the same governed contract.

### Canonicalize and fingerprint carefully

Raw bytes vary by whitespace/key order/comments; semantic normalization varies by format. Use a specified canonicalization algorithm and version, then collision-resistant digest over a domain-separated envelope including format/dialect where needed.

Canonicalization must not erase meaningful distinctions such as documentation/default/order/annotations when governance depends on them. Maintain raw authored artifact and canonical comparison form. A semantic diff can be separate from identity.

Never change canonicalization for old IDs silently. Introduce algorithm version and cross-map identities. Verify received content against claimed digest/signature before cache/use.

Sequential registry IDs are efficient wire references but scoped to registry/cluster. Carry authenticated namespace/issuer or globally safe identity when crossing environments/organizations.

### Define compatibility direction and comparison set

Write compatibility as reader/writer or client/server propositions, not only labels. In common event terminology, backward asks whether new consumers/readers can process old data; forward asks whether old consumers/readers can process new data; full requires both. Tool definitions/configurations are authoritative for their own mode, so record them.

Latest-only comparison permits a chain whose endpoints are incompatible if an intermediate transition masks history. Transitive mode compares against all governed history in scope. Choose from retention/replay/rollback/deployment realities, not speed alone.

For request/response APIs, direction is multi-sided: old client/new server and new client/old server for requests and responses. Generated clients, validators, tolerant readers, unknown enums/fields, requiredness/defaults, and error variants matter.

Policy records format, dialect, direction, transitivity, comparison baseline/set, tool/rule version, applicability, severity, exceptions, and effective time.

### Respect format-specific evolution

JSON Schema validation describes accepted instances under declared vocabularies; changes to required, type, bounds, enum, unevaluated properties, conditionals, references, defaults/annotations, and dialect can alter accepted sets. Default is usually annotation, not automatic instance mutation unless a tool says otherwise.

OpenAPI changes include paths/operations, parameters, security, request/response schemas, status/media/headers, callbacks/webhooks, and semantics not representable structurally. Pin the OpenAPI version and schema dialect; validate references and generated consumers.

Protobuf compatibility depends on wire types, field numbers, reserved deleted numbers/names, presence, enums, oneof, maps, services, JSON mapping, and generated languages. Official guidance distinguishes wire-unsafe, safe, and conditionally safe changes; registry policy must not flatten those categories.

AsyncAPI couples operations, channels, messages, bindings, correlation, servers/security, and payload/header schemas. Event compatibility also includes topic, key/partition, ordering, delivery, replay, and effect semantics beyond payload shape.

### Govern references and dependency graphs

References resolve by immutable identity/version, never floating `latest`. Store relationship type and source location. Validate format/dialect agreement, accessibility, integrity, and closure before admission.

Detect cycles according to format capability and tooling limits. Even legal recursion can break generators or validators; test supported toolchains. Compute reverse dependencies so changing/deprecating/deleting a shared type identifies affected contracts.

Deletion is constrained by references, retention, replay, audit, rollback, legal hold, generated builds, and deployed consumers. Tombstone discovery while retaining immutable bytes where required. Never reuse an identity/version.

Bundle references for offline/deterministic builds or pin a lock manifest. A build that resolves the same root to different transitives over time is not reproducible.

### Build the admission and promotion pipeline

Admission validates parse/syntax/dialect, stable identity, metadata/ownership, reference closure, style, structural compatibility, and required design/security/exception evidence. Produce deterministic findings tied to artifact/policy/tool versions.

Promotion adds generated SDK/doc/example checks, consumer contract tests, implementation conformance, runtime/security tests, semantic compatibility review, capacity/failure behavior, rollout/rollback/replay evidence, and approvals appropriate to exposure/risk.

Do not let a producer auto-register arbitrary production schemas from the data path. Restrict create/update/promote permissions, authenticate workloads, separate read from write/admin, review high-impact subject/policy changes, sign releases, and audit every transition.

CI checks candidate against authoritative remote baseline pinned by identity, not an incidental stale checkout. Handle concurrent registrations with compare-and-set/transactional ordering so two individually compatible candidates do not bypass pairwise policy.

### Bind producers and consumers safely

At build/deploy, pin the approved schema/contract identity and generated artifact provenance. Producers emit schema ID/fingerprint in a protected envelope where protocol requires; consumers resolve through trusted local cache or bundled descriptors and verify namespace/integrity.

Avoid synchronous registry lookup per message/request. Warm/cache known schemas, use bounded negative caching, timeouts/circuit isolation, and local last-known-good storage. Registry unavailability should block unsafe new publication, not necessarily already-approved data flow.

Unknown ID behavior is explicit: quarantine/dead-letter with limits and alerts, retry after bounded refresh, or reject safely. Never deserialize untrusted data using a guessed schema or allow poison IDs to create unbounded lookup storms.

Track which producer deployment writes which identity and which consumer versions can read it. This runtime evidence enables staged rollout and rollback decisions.

### Detect contract and runtime drift

Compare source, registered artifact, generated package, deployed configuration, and observed wire identity. Alert on unregistered payloads, unexpected schema IDs, stale generator/runtime, subject mismatch, reference failure, or contract/runtime validation divergence.

Sample validation may find defects but cannot prove absence. Privacy/security constrain payload capture. Prefer safe structural validation at producer/consumer boundaries, aggregate stable errors, and retain minimized provenance.

Contract tests verify behavior examples and consumer assumptions; semantic diff reviews nonstructural changes; telemetry confirms adoption/error/effect. A registry compatibility pass is only one evidence edge.

Reconcile drift before deprecation or incident claims. “No consumers of version 4” is unreliable if gateways strip IDs or telemetry retention misses seasonal replay.

### Evolve policies and handle exceptions

Policy changes can reject previously accepted histories or newly reveal incompatibility. Run proposed rules against the full representative corpus, classify findings, assess tool/version differences, publish effective dates, and migrate safely.

An exception records subject/artifact, exact policy/rule, reason/alternatives, affected producer/consumer/history, risk, compensating tests/controls, authority, owner, expiry, and removal condition. It never changes the meaning of a global compatibility badge silently.

Quarantine corrupted/malicious artifacts without destroying forensic/history evidence. Repair creates new signed records and explicit supersession. Communicate incidents to affected reverse dependencies.

Measure exception concentration: repeated waivers can reveal wrong subject boundary, faulty checker, missing format feature, or unsafe architecture.

### Operate, federate, and recover the registry

Define availability/durability/RPO/RTO for reads, registrations, policy, audit, and replication separately. Back up immutable artifacts, metadata, subject ordering, policies, identities, ACLs, keys/signatures, audit, and dependency graph; regularly restore/reconcile them.

Multi-region/registry federation needs ownership and conflict rules. Concurrent versions, ID allocation, replication lag, policy skew, and split brain can create histories no node individually validated. Prefer single-writer per subject or consensus/serialized admission with safe read replication.

Monitor admission/lookup latency/errors, cache hit/unknown IDs, replication lag, invalid/runtime drift, policy versions, broken references, unsigned artifacts, stale owners, exceptions, deprecations, storage, and audit gaps. Protect metadata because it maps sensitive systems and evolution.

Plan vendor/tool migration by exporting raw/canonical content, subject order, identities/mappings, references, policies, metadata, decisions, ACL/audit, and consumer bindings. Validate equivalence; do not assume compatibility modes share exact semantics.

### Govern retirement and outcomes

Deprecate subject/version with replacement, owner, dates, affected reverse dependencies, producers/consumers, retention/replay/rollback requirements, and notices. Prevent new bindings while serving entitled old readers through the promised window.

Retire only after no required producers emit it, all consumers/replays/restores can use replacement, references are migrated, generated artifacts/docs are updated, telemetry is healthy, rollback constraints are resolved, and evidence retention is satisfied.

Measure reproducible builds, unregistered/drift incidents, compatibility escapes, rollback/replay success, unknown-ID rate, policy/check false results, review/admission lead time, exception age, ownership freshness, and consumer migration—not schema count.

The registry succeeds when independent evolution becomes safer and more explainable, not when every artifact has an ID.

## Definitions and Notation

Let immutable contract artifact be $c$, subject lineage $s$, and governed historical comparison set $H_s$. Let $V(c)$ validate syntax/dialect, $I(c,s)$ identity/provenance, $P(c,s,H_s)$ configured structural policy, $R(c)$ reference closure/integrity, and $A(c,s)$ review/authorization evidence.

Admission requires their conjunction. Let dependency graph $G=(N,E)$ contain artifact nodes and pinned reference edges; reverse reachability identifies potentially affected dependents. Let deployed writer identities be $W_t$ and reader capabilities $Q_t$ at time $t$; safe rollout/rollback claims require evidence over relevant pairs, not registry history alone.

A **compatibility mode** is a tool/policy-defined comparison relation. **Latest** and **transitive** define comparison sets. **Fingerprint** identifies canonical bytes under named algorithm; **registry ID** may be only namespace-local. **Promotion** authorizes an admitted artifact for a lifecycle environment/use.

## Mechanisms, Invariants, or Proof Structure

**Admission conjunction.** A valid schema with missing reference cannot build; a compatible schema with untrusted provenance cannot be safely promoted; an authorized artifact with invalid syntax cannot be interpreted. Each predicate can independently fail, so admission requires conjunction rather than an average score.

**Transitivity counterexample.** Candidate $c_3$ can be compatible with latest $c_2$ while incompatible with retained $c_1$ because $c_2$ introduced an intermediate representation/default. If $c_1$ data or readers remain, latest-only comparison is insufficient; compare the governed history required by replay/rollback.

**Structural-limit counterexample.** Two contracts have identical schemas, but one changes `amount` units from cents to dollars or permits a new side effect. Structural comparison passes while consumer behavior breaks. Therefore schema compatibility is not behavioral compatibility.

**Reference immutability argument.** If reference `latest` can resolve to $d_1$ during review and $d_2$ during build, the same root identity yields different effective contracts. Pinning immutable reference identity is necessary for reproducibility and decision traceability.

Operational invariants are: immutable artifacts; explicit namespace/format/dialect/canonicalization; correct subject lineage; policy direction/set/version explicit; references pinned/closed; admission authorized/audited; data path isolated from control plane; runtime binding/drift observable; exceptions bounded; histories recoverable; and retirement evidence complete.

## Alternatives and Trade-Offs

Central registry improves discovery/policy but concentrates outage, compromise, and organizational bottleneck. Federated registries improve autonomy/locality but complicate global identity, policy, references, and replication. Federate ownership with interoperable immutable identity and explicit trust.

Fine-grained subjects reduce coupling but may permit jointly released pieces to diverge. Coarse bundles enforce coherence but serialize unrelated evolution. Choose compatibility lineage from actual deployment/consumer atomicity.

Transitive checks protect retained history but cost more and can block legacy anomalies. Latest checks are fast but unsafe for long replay/rollback. Scope historical guarantees explicitly and repair/migrate rather than hide history.

Runtime validation catches drift but adds latency/cost and may expose sensitive payloads. Build-time-only checks are cheap but miss runtime divergence. Combine producer/consumer validation, safe sampling, stable error metrics, and provenance.

Automatic registration is convenient but expands supply-chain and policy bypass risk. Reviewed CI promotion is safer but slower. Allow low-risk draft namespaces and restrict production subject/policy transitions.

Shared schemas reduce duplication but create dependency blast radius. Local copies permit divergence. Reuse stable semantic types with ownership/versioning; do not centralize incidental shapes.

## Failure Modes and Misconceptions

- “Registry version is schema identity.” It is an ordered subject-local position.
- “Same text means same schema.” Dialect, format, and resolution context matter.
- “Canonical means semantically equivalent.” Canonicalization has bounded rules.
- “Backward compatible means safe.” Direction, set, format, semantics, and consumers matter.
- “Latest comparison protects history.” Older retained data/readers can still break.
- “Optional is always additive.” Defaults, generators, semantics, and validation can break.
- “OpenAPI pass proves implementation.” Runtime can diverge.
- “One subject per topic/deployment.” Topic/deployment boundaries may not be compatibility lineages.
- “Use latest references.” Floating resolution destroys reproducibility.
- “Delete unused schemas.” Replay, rollback, audit, references, or dormant consumers may need them.
- “Fetch the registry for every message.” Control-plane failure then breaks the data plane.
- “Unknown ID can be ignored.” It can cause corruption or poison-loop amplification.
- “Auto-registration is harmless.” Compromised producers can publish contracts/policy surprises.
- “All tools mean forward/backward identically.” Record exact tool semantics/version.
- “Compatibility exceptions are permanent.” They are owned, scoped, expiring risks.
- “Many schemas means adoption.” Outcomes are safe independent evolution and traceability.

## Worked Examples

### Example 1

Whitespace/key-order changes produce different raw bytes but the same versioned canonical JSON Schema digest. Raw source remains stored; the canonical algorithm/dialect are recorded so deduplication is auditable.

### Example 2

Two teams use subject `payments` for unrelated command and event schemas. Comparisons conflict. Governance splits durable lineages and records aliases/predecessors rather than resetting history silently.

### Example 3

Protobuf field 7 is deleted and later reused for a different type. A checker rejects it; reserving the number/name prevents old bytes from being misinterpreted.

### Example 4

Schema $c_3$ passes latest comparison with $c_2$ but fails against retained $c_1$. Replay still contains $c_1$ data, so transitive policy blocks promotion until a migration/reader strategy exists.

### Example 5

JSON field `amount` remains integer but changes cents to dollars. Structural check passes; semantic review/test fails. A new explicit unit field/version and consumer migration are required.

### Example 6

Registry outage occurs after deployments cached signed approved descriptors. Existing traffic continues; new schema publication stops. Bounded unknown IDs quarantine rather than trigger unbounded lookups.

### Example 7

OpenAPI source, registered digest, generated SDK, and deployed service disagree. CI/runtime provenance flags drift and blocks promotion until regeneration and implementation conformance pass.

### Example 8

A compromised producer lacks registration permission but can write data. Unknown unsigned schema identity is quarantined, alerts fire, and existing approved consumers are not tricked into arbitrary deserialization.

### Example 9

A shared address schema has 70 reverse dependencies. Proposed required field triggers affected-owner review; a new optional semantic type avoids silently breaking all bundles.

### Example 10

Migration exports schemas but omits subject ordering, policies, references, and ID mappings. Restore cannot decode old messages. A full export/restore rehearsal catches the incomplete portability plan.

## Cross-Program Connections

[Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) supplies contracts, coupling, dependency graphs, decision records, and evolution boundaries.

[Software Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies compatibility/contract tests, differential testing, static-analysis validity, fixtures, and runtime conformance.

[Data Engineering](../../19-data-engineering/ROADMAP.md) supplies schema evolution, lineage, catalogs, data quality, replay/backfill, provenance, and pipeline contracts.

[Security Engineering](../../25-security-engineering/ROADMAP.md) supplies registry authorization, signing/supply chain, tenant separation, malicious schemas, audit, secrets/privacy, and incident response.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies replication, consistency, caching, partitions, serialized admission, event ordering/delivery, replay, and recovery.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) supplies registry control planes, CI policy, generators, catalogs, environment promotion, paved paths, tenancy, and operational ownership.

## References

1. OpenAPI Initiative, [OpenAPI Specification](https://spec.openapis.org/oas/latest.html).
2. JSON Schema, [Draft 2020-12 Core Specification](https://json-schema.org/draft/2020-12/json-schema-core).
3. AsyncAPI Initiative, [AsyncAPI Specification](https://www.asyncapi.com/docs/reference/specification/latest).
4. Protocol Buffers, [Language Guide (proto 3): Updating a Message Type](https://protobuf.dev/programming-guides/proto3/#updating).
5. Confluent, [Schema Evolution and Compatibility Types](https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html).
6. Buf, [Detecting Breaking Changes](https://buf.build/docs/breaking/).
7. IETF, [RFC 8785: JSON Canonicalization Scheme](https://www.rfc-editor.org/rfc/rfc8785.html).

## Exercises

### Exercise 1

Design subjects, immutable identities, references, policies, and lifecycle for HTTP/OpenAPI, Protobuf RPC, and event schemas shared across teams, regions, environments, replay, and generated SDKs.

### Exercise 2

Given versions $c_1,c_2,c_3$ where $c_3$ is compatible with $c_2$ but not $c_1$, decide latest versus transitive policy for a stream retaining $c_1$ data and a service supporting rollback to a $c_1$ reader.

### Exercise 3

Create an admission/promotion evidence pipeline for a new public API contract. Separate what schema/style tools can establish from design, security, runtime, consumer, rollout, and lifecycle evidence.

### Exercise 4

Design safe producer/consumer behavior during registry outage, cache miss, unknown/malicious ID, replication lag, policy skew, and disaster recovery without unsafe guessing or unbounded amplification.

### Exercise 5

Plan migration between registry products while preserving identity, histories, references, compatibility decisions, generated artifacts, deployed bindings, audit, and ability to decode old records.

## Answers to the Exercises

### Answer 1

Use compatibility lineages, not deployments: one governed OpenAPI bundle per stable public API/version family; Protobuf packages/services/messages according to atomic release/consumer needs; event value/key/header schemas per stable event type/lineage, not transient topic instance. Include organization/environment namespace, format and exact dialect/edition, canonicalization algorithm/version, digest and subject-local version. Pin shared types by immutable digest/version with reverse dependencies and lock bundles. Separate development draft from signed production promotion and prevent cross-environment numeric-ID confusion. Policies declare direction, transitivity/history retention, tool/rule version, exceptions, and semantic review. Replicate safe reads while serialize writes per subject. Generated SDK/descriptors/docs carry source/registry digest and build provenance. Retain schemas/references for replay, rollback, audit, and deprecation evidence; aliases/splits/moves preserve history.

### Answer 2

Latest-only admits $c_3$ because it compares only $c_2$, but retained $c_1$ data and rollback reader are explicitly in the compatibility population. Compare $c_3$ against $c_1$ and $c_2$ (transitive/full direction appropriate to reader/writer rollout); current evidence fails. Do not publish with a generic “compatible” label. Options are modify $c_3$ to preserve $c_1$, migrate retained data and prove replay, upgrade/remove rollback reader with replacement rollback strategy, or introduce a new subject/version lineage with adapters and consumer migration. Record exact tool semantics, pairs tested, data fixtures, generated readers, rollout order, and exception only if authority accepts bounded risk. Re-test runtime semantics because pairwise structural success would still be insufficient.

### Answer 3

Admission parses exact OpenAPI/schema dialect, validates reference closure/integrity, computes immutable identity, checks ownership/provenance/signature, applies style and structural/semantic-diff candidates against pinned authoritative history, and links design/exception authorization. Tools can establish bounded artifact facts only. Promotion requires reviewed consumer tasks/domain/state; HTTP/error/security/privacy semantics; threat and authorization evidence; implementation conformance; generated SDK/docs/examples; old/new consumer contract tests; compatibility inventory; capacity/failure/idempotency/rollback tests; deployment config binding; staged rollout telemetry; deprecation/support plan; and owner/authority decision for the exact digest. Deterministic findings name tool/policy versions. Production write/promotion permissions are separate, and concurrent candidates serialize. Release observes runtime schema IDs and behavior rather than inferring implementation from registration.

### Answer 4

Pin/bundle approved descriptors at build/deploy and maintain verified bounded local caches/last-known-good. Existing known traffic continues during control-plane outage; registration/policy mutation fails closed. On cache miss, perform authenticated namespace-aware bounded lookup with timeout, circuit/bulkhead, request coalescing, size/rate limits, digest/signature verification, and negative cache. Unknown/malformed/unauthorized IDs are quarantined/dead-lettered with bounded retention/retry and alerts, never guessed or deserialized dynamically. Replication lag does not permit writes against stale policy; use single-writer/serialized subject admission and read version indicators. Back up/restore artifacts, IDs/mappings, order, refs, policies, ACL/keys/audit and test decoding/replay. Monitor cache/unknown/lookup/lag/skew/quarantine. Provide manual incident resolution without changing historical IDs.

### Answer 5

Inventory/export raw and canonical artifacts, format/dialect, canonical algorithm, digests, subject order/aliases/states, global/local IDs and mappings, references/reverse graph, policies with exact tool semantics/versions, findings/decisions/exceptions, owners/metadata, signatures/keys, ACLs/audit, generated package provenance, producer/consumer deployment bindings, retention/replay/rollback and deprecation records. Build deterministic old-to-new mapping without reusing IDs. Import into isolated target, verify bytes/digests/reference closure/order/policy equivalence, run both checkers on representative/full histories, and investigate differences rather than relabel modes. Generate/contract-test artifacts, shadow/dual-publish metadata where safe, canary readers/writers, preserve old decode mapping/cache, and rehearse rollback plus disaster restore/replay. Cut writes with serialization, reconcile deltas, monitor unknown/drift, retain source registry read-only until all governed histories and consumers are proven.

---
module_id: SEPAT-068
program: Software Engineering: Patterns
level: 2
module_number: 68
title: Claim Check
status: complete
last_verified: 2026-08-29
---

# Claim Check

## One-Page Review

### Governing question

How can a message flow carry a small, stable reference to large, sensitive, or temporarily unnecessary content while preserving payload identity, integrity, availability, authorization, replay, lifecycle, and end-to-end failure recovery?

### Essential definitions

- A **Claim Check** replaces some or all message payload with a reference to content in an external store; an authorized consumer may later redeem the reference.
- The **payload object** is the immutable byte sequence stored outside the broker, not merely its current logical filename.
- A **claim descriptor** states object identity/version, digest, length, media/schema type, security classification, and any safe routing facts needed without retrieval.
- A **claim token** locates or names the object. Possession of it must not silently imply authorization.
- **check luggage** is the producer-side step that stores content and emits the descriptor; **claim luggage** is the consumer-side retrieval and verification step.
- A **dangling claim** refers to missing, expired, unauthorized, or unreadable content.
- An **orphan object** was stored but has no live published obligation referencing it.
- **content-addressed identity** derives an object key from a cryptographic digest, making content/version changes visible.
- **retention** is the time the object remains retrievable; it must cover queue delay, retries, replay, audits, and every declared subscriber obligation.
- A **terminal lifecycle state** records why an object may be retained, legally held, archived, or deleted; one consumer acknowledgement is not automatically global deletion authority.

### Central model, mechanism, or theorem

Let payload bytes be $B$, cryptographic digest $h=H(B)$, length $n=|B|$, immutable object identity/version $o$, and claim descriptor

$$
C=(o,h,n,t,s),
$$

where $t$ identifies media/schema type and $s$ the nonsecret security/lifecycle metadata required by policy. Redemption is valid only if the authenticated principal is authorized for the current purpose and tenant, the exact object version is retrieved, and

$$
H(B')=h\quad\land\quad |B'|=n.
$$

If broker retention/replay is $R_b$, maximum unresolved processing/retry horizon is $R_p$, and audit or domain policy requires $R_a$, then absent a stronger obligation ledger the object lifetime must satisfy

$$
R_o\ge\max(R_b,R_p,R_a).
$$

This is a lower bound, not deletion authorization: legal holds, multiple subscriptions, backups, and privacy requirements may impose different outcomes.

### Critical invariants

- The payload is durably stored and verified before any claim becomes deliverable; failed publication leaves a discoverable orphan, never a delivered dangling claim.
- A claim identifies one immutable object version and includes integrity, length, type/schema, and stable business/message identity.
- Routing and admission facts needed by intermediaries remain in a minimal authenticated envelope; routers do not fetch sensitive content merely to decide.
- Redemption authenticates the caller and reauthorizes tenant, purpose, object, operation, region, time, and current domain state; reference possession alone is insufficient.
- Consumers stream with byte, time, decompression, parser, and concurrency limits, then verify digest and type before effects.
- Retries and redrives reuse stable message/claim identity; object mutation or key reuse cannot change the historical meaning of a message.
- Retention covers all live subscriptions, lag, retry, replay, audit, restore, and legal obligations; deletion is idempotent, governed, observable, and reconciled.
- Sensitive claims and payloads are not leaked through logs, traces, dead letters, metrics, URLs, caches, or error messages.
- Broker, object store, keys, schema registry, and authorization dependencies have explicit availability, regional, backup, and disaster-recovery contracts.
- Every message and object reaches a reconcilable terminal state: published/live, orphaned, quarantined, archived/held, or deleted under policy.

### Common failures

Common failures include publishing before storage, losing stored-but-unpublished objects, overwriting a reused key, treating a URL as object identity, treating an unguessable token as authorization, putting long-lived bearer URLs in messages, omitting digest/version/type, deleting after the first subscriber, expiring payload before queue retention, allowing replay to find missing content, routing by fetching the whole object, downloading unbounded compressed data, acknowledging before retrieval/effect, leaking claims into telemetry, scanning content with different bytes than consumers retrieve, cross-region object gaps, ignoring encryption-key lifecycle, and calling offloading an atomic transaction without a reconciliation protocol.

### Compact example

A producer stores immutable bytes under `sha256/<digest>`, records length and type, then publishes a small descriptor through an outbox relay. A consumer authenticates independently, retrieves that exact version, verifies length and digest, processes idempotently, and acknowledges. A crash before publish creates an aged staged object that reconciliation can remove; a crash after publish is retried against the same bytes. Deletion waits for the subscription/lifecycle ledger, not the first successful consumer.

### Connections

[SEPAT-067](067-competing-consumers.md) governs concurrent claim redemption; [SEPAT-069](../ROADMAP.md) handles terminally unredeemable claims through a Dead-Letter Channel. Claim Check also connects to [Data Engineering](../../19-data-engineering/ROADMAP.md), [Security Engineering](../../25-security-engineering/ROADMAP.md), [Cloud and Infrastructure Engineering](../../30-cloud-and-infrastructure-engineering/ROADMAP.md), [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md), and [Platform Engineering](../../29-platform-engineering/ROADMAP.md).

## Governing Question

What must travel with a reference—and what protocol must surround it—so removing bytes from a message reduces broker load and exposure without removing the content's identity, meaning, availability, or governance?

The pattern is often summarized as “put the file in object storage and send a link.” That summary hides the hard parts. A location may change contents; a link may be a bearer credential; an object may disappear before a delayed subscriber reads it; and storage plus broker publish rarely form one transaction. A production claim is a versioned integrity and lifecycle contract, not a string field.

## Why This Matters

Messaging systems are normally optimized for many modest messages. Large payloads consume broker memory, replication bandwidth, storage, network, serialization, encryption, inspection, and retry capacity. They may exceed configured or product limits and amplify head-of-line blocking. Sensitive fields also become visible to routing, monitoring, dead-letter, and support surfaces that do not need them.

Externalizing content lets the broker carry control and routing metadata while a purpose-built store serves large bytes. Consumers retrieve only when needed and may stream or range-read. Yet the design introduces another system, consistency boundary, authorization decision, cost surface, and lifecycle. The pattern is valuable only when these new obligations are more controllable than carrying the bytes directly.

## Prerequisites and Retrieval

You should understand message envelopes, content filters/enrichers, object/version identity, cryptographic hashes, transactions/outbox, authorization, encryption/key management, retention/replay, idempotency, backpressure, and disaster recovery. Retrieve these facts:

1. A locator says where to ask; it does not prove which bytes will be returned.
2. A digest detects byte change but does not authenticate the producer unless the envelope itself is authenticated.
3. Store and broker normally fail independently; operation order determines orphan versus dangling-claim risk.
4. Separate pub/sub subscriptions progress independently, so one acknowledgement cannot generally authorize object deletion.
5. Signed or presigned URLs are bearer capabilities for their validity and permission scope and can leak like secrets.
6. Encryption at rest does not replace object-level authorization, integrity verification, or deletion governance.
7. Compression, parsing, and content inspection create resource and security limits beyond nominal stored size.

## Learning Objectives

After completing this module, you should be able to:

- distinguish Claim Check from inline payloads, chunking, shared mutable records, caches, and generic hyperlinks;
- design a minimal descriptor with immutable identity/version, digest, length, type/schema, classification, and business correlation;
- close store-before-publish and publish-before-store failure windows with staging, outbox, reconciliation, and idempotency;
- authorize redemption independently from token possession and minimize exposure across observability and support paths;
- stream and validate claimed content under byte, time, decompression, parser, concurrency, and malware controls;
- calculate payload/broker amplification and lower bounds for object retention;
- coordinate deletion across subscriptions, retry/replay, audit, legal hold, backup, and privacy requirements;
- preserve meaning across schema evolution, mutable producers, region failure, key rotation, and redrive;
- instrument message-to-object obligations, orphans, dangling claims, integrity failures, access denial, cost, and cleanup;
- verify the pattern through crash matrices, corruption, replay, authorization, retention, load, restore, and high-stakes review.

## Core Exposition

### Decide whether to externalize

Use Claim Check when payload size exceeds the broker contract, large objects harm shared broker performance, most intermediaries do not need the bytes, or sensitive content should remain in a more tightly governed store. Measure envelope size, payload distribution, replication factor, fan-out, retries, broker quotas, object-store reads, egress, and latency.

Do not externalize every small message by reflex. An extra network read and dependency can dominate small payloads and complicate atomicity. A documented threshold may choose inline versus claimed representation, but consumers then support both explicit schema variants. Avoid an ambiguous field that is sometimes bytes and sometimes a URI.

### Separate envelope facts from payload bytes

Keep stable message ID, event/command type, occurred time, source, tenant, partition/routing key, schema/type, payload digest/length, classification label, and claim identity in the authenticated envelope. Include only facts that intermediaries genuinely require. Do not duplicate sensitive fields “for routing convenience” without their own governance.

The envelope is not a second mutable truth. If it contains a derived routing fact, define how it was computed and bind it to the claimed digest/version. A consumer that needs authoritative content verifies the object rather than trusting an unbound preview.

### Make object identity immutable

A path such as `customers/42/latest.pdf` is mutable and therefore cannot preserve historical message meaning. Use object version identifiers, write-once keys, or content-addressed keys. Never overwrite a key referenced by an already published message. If correction is needed, store a new version and publish a correction/supersession event.

Record a strong cryptographic digest over the exact transported bytes, byte length, media type, content encoding, schema version, and optionally a producer signature or authenticated envelope. Digest comparison detects corruption/substitution; trust in the expected digest comes from authenticated publication and producer controls.

### Store before making the claim visible

Publishing a claim before successful durable storage can deliver a permanently dangling reference. Instead, create a staged object/metadata record, upload, verify durability/integrity, record an outbox message, and let a relay publish idempotently. Only then mark the object published/live.

Object storage and a relational outbox may still lack one transaction. A durable workflow records states such as `staging`, `stored`, `publish_pending`, `published`, `retention_eligible`, and terminal cleanup outcomes. Reconciliation finds aged staging objects, missing outbox rows, duplicate publications, and published claims whose object is unavailable. Store-first converts ambiguity into recoverable orphans rather than consumer-visible missing data.

### Design idempotent publication

Retries use the same stable message ID, object version, and digest. Re-upload of identical content should confirm or reuse the immutable object, not create uncontrolled copies; repeated relay publication is deduplicated or tolerated by consumers. If multipart upload can remain incomplete, govern and expire those partial resources separately.

A producer must not compute a claim over bytes and later upload a different serialization. Hash the final encoded/compressed/encrypted representation or explicitly record digests for each layer and define which layer the consumer verifies.

### Authorize redemption, not just routing

An opaque identifier reduces guessing but is not access control. The object service authenticates the workload and authorizes exact tenant, object/version, purpose, operation, region, and current policy. Prefer short-lived delegated access minted after authorization over long-lived credentials embedded in messages.

Presigned URLs are bearer tokens: anyone possessing a usable URL can exercise its scoped access until it or underlying credentials expire under product rules. Protect them from logs, traces, tickets, analytics, referrers, and dead-letter payloads. Keep duration, method, path, network, content-length, and other supported constraints narrow. For long queue delays, send an opaque claim ID and mint access at redemption time rather than publishing a URL that may expire early or remain exposed too long.

### Retrieve defensively

Before download, validate envelope schema, identity, type, expected length, classification, and policy. Stream instead of buffering unbounded content. Enforce maximum stored and decompressed bytes, ratios, duration, redirects, ranges, parser complexity, recursion, file count, and concurrency. Fetch only from allowlisted services/identities; arbitrary URLs create server-side request forgery risk.

After retrieval, verify exact object version, length, digest, content type/encoding, and when applicable signature and malware/content policy. A successful HTTP status is not integrity evidence. Quarantine mismatches rather than “repairing” the message to match unexpected bytes.

### Place acknowledgement after the effect

Retrieval does not complete the business obligation. Validate content, perform the idempotent effect, record outgoing work, and then acknowledge/checkpoint. A retry should re-redeem the same immutable object or observe the prior effect. Caches may optimize reads only if keyed and verified by object version/digest and protected by the same classification policy.

If claimed content is very large, processing may outlive a queue lease. Coordinate lease renewal and Claim Check retrieval with Competing Consumers; fence stale effects. Do not extend object retention solely through an untrusted worker heartbeat without an obligation ledger.

### Coordinate multiple subscribers

In pub/sub, each subscription may retrieve at a different time. Deleting after the first acknowledgement breaks slower groups and replay. Track the intended obligation set and per-subscription terminal state, or retain by a conservative policy covering the longest supported lag/replay. Dynamic subscription creation and backfill require explicit start/retention semantics.

Reference counting is reliable only when the complete obligation set is known and state transitions are durable. It fails when subscribers appear later, acknowledgements are lost, or a consumer reads without recording completion. Retention-window cleanup is simpler but costs more and must account for holds and delayed backups.

### Govern retention and deletion

Define creation, publication, read, quarantine, archive, legal hold, retention eligibility, deletion request, delete confirmation, backup expiry, and tombstone/audit states. The message and object may have different retention regimes; the shorter one must not invalidate the longer business obligation.

Deletion should be idempotent and reconciled. Object deletion may not immediately erase replicas, versions, caches, search indexes, derived data, backups, or encryption-key access. Document whether policy requires cryptographic erasure, version purge, backup aging, or immutable retention. A lifecycle rule is an implementation mechanism, not the policy itself.

### Preserve replay and schema meaning

Replay must retrieve the same historical bytes and the schema/translator needed to interpret them. A claim to `latest` or an overwritten key makes replay nondeterministic. Retention/compaction decisions should state when replay becomes unavailable and what snapshot or archive replaces it.

If a correction changes content, publish a new immutable claim linked to the superseded claim. Consumers decide whether to compensate/rebuild under domain policy; silently mutating the old object defeats audit and idempotency.

### Plan availability and disaster recovery

The effective message flow depends on broker, object metadata, object bytes, authorization, encryption keys, schema registry, network path, and sometimes malware scanners. Define aligned regional placement, replication, recovery-point/time objectives, failover identity, key availability, and read-after-failover behavior.

Test a broker restored to an older snapshot against object lifecycle and vice versa. A valid message whose object expired during restore is a dangling claim. Cross-region replication lag can produce transient missing objects even though the primary upload succeeded; do not publish into a region until the declared durability/availability condition is met.

### Observe and reconcile

Measure staged objects by age, outbox/publish latency, published claim count, retrieval rate/latency/bytes, cache hit, authorization denial, missing/version mismatch, length/digest/type failure, decompression rejection, per-tenant concurrency, object/broker egress and storage cost, subscriber completion, retention eligibility, deletion lag/failure, orphan age, and dangling claims.

Correlate by opaque message/object IDs; never label metrics with raw URLs, tokens, patient names, or payload. Periodic reconciliation joins object metadata, outbox/broker evidence, subscription obligations, effects, and lifecycle state. Sampling cannot prove absence of dangling claims when every obligation matters.

## Definitions and Notation

| Symbol or term | Meaning |
| --- | --- |
| $B$ | Exact stored/transported payload byte sequence |
| $H$ | Declared collision-resistant digest algorithm |
| $h=H(B)$ | Expected payload digest in authenticated envelope |
| $n=|B|$ | Expected payload byte length |
| $o=(key,version)$ | Immutable object identity and version |
| $C$ | Claim descriptor binding object, digest, length, type/schema, and safe policy metadata |
| $R_b$ | Supported broker retention or replay horizon |
| $R_p$ | Maximum unresolved processing/retry horizon |
| $R_a$ | Audit/domain retention requirement |
| orphan | Stored content without a live published obligation |
| dangling claim | Delivered/live claim whose required content cannot be validly redeemed |
| bearer capability | Token whose possession enables the scoped operation without another identity decision |
| tombstone | Durable record that an identity was intentionally deleted or superseded |

Confidentiality, integrity, authenticity, availability, and authorization are distinct. Encryption can support confidentiality; digest supports byte integrity; authenticated envelope supports provenance of the expected digest; authorization decides who may redeem; retention and recovery support availability.

## Mechanisms, Invariants, or Proof Structure

### Integrity argument

Assume the authenticated envelope binds expected $(o,h,n,t)$, the object store returns exact version $o$, and the consumer rejects unless retrieved $B'$ satisfies $H(B')=h$ and $|B'|=n$ before parsing/effect. Corruption or replacement that changes bytes is detected except with digest collision or compromise of envelope/trust boundary. The argument does not prove confidentiality, authorization, semantic correctness, or malware safety.

### Publication-safety argument

If durable verified storage precedes claim visibility, a crash before publication can create an orphan but cannot expose a claim to bytes that were never stored. A durable outbox/workflow retries publication with stable identity. Reconciliation eventually classifies aged unpublished objects. The argument depends on store durability semantics, visibility gating, idempotent relay, and reconciliation; it is not a cross-system atomic transaction.

### Retention lower bound

Any supported replay at age $R_b$, unresolved retry at age $R_p$, or required audit retrieval at age $R_a$ needs the bytes. Therefore deletion before their maximum violates at least one contract. Keeping until the maximum is necessary but may not be sufficient: subscription-specific lag, legal hold, backup, supersession, privacy and derived-data policy can alter the terminal outcome.

### Executable finite model

The model stores immutable bytes under a deterministic model checksum, returns a descriptor, verifies checksum and length, rejects tampering, and retires the object. The checksum is intentionally non-cryptographic because the safe finite-model runner has no library imports; a real system must use a vetted collision-resistant digest such as SHA-256. The model is deliberately in-memory and does not represent durable upload, authentication, encryption, transactions, concurrency, retention, replication, or secure deletion.

<!-- bijux-verify: {"id":"claim-check-integrity","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"stored=True bytes=11 immutable=True\nretrieved=True digest_verified=True\ntamper=rejected\nafter_retire=missing\n","stderr":""}} -->
```python
def model_checksum(payload):
    value = 0
    for byte in payload:
        value = (value * 257 + byte) % (2**64)
    return f"{value:016x}"


class ClaimStore:
    def __init__(self):
        self.objects = {}

    def put(self, payload):
        digest = model_checksum(payload)
        key = f"model/{digest}"
        self.objects.setdefault(key, payload)
        return {"key": key, "checksum": digest, "bytes": len(payload)}

    def fetch(self, claim):
        payload = self.objects[claim["key"]]
        actual = model_checksum(payload)
        if len(payload) != claim["bytes"] or actual != claim["checksum"]:
            raise ValueError("claim integrity failed")
        return payload

    def retire(self, claim):
        self.objects.pop(claim["key"], None)


store = ClaimStore()
payload = b"artifact-v1"
claim = store.put(payload)
same_claim = store.put(payload)
print(
    f"stored={claim['key'] in store.objects} bytes={claim['bytes']} "
    f"immutable={claim == same_claim}"
)

retrieved = store.fetch(claim)
print(f"retrieved={retrieved == payload} digest_verified=True")

store.objects[claim["key"]] = b"artifact-v2"
try:
    store.fetch(claim)
except ValueError:
    print("tamper=rejected")

store.retire(claim)
try:
    store.fetch(claim)
except KeyError:
    print("after_retire=missing")
```

## Alternatives and Trade-Offs

| Design | Advantage | Cost or limitation | Best fit |
| --- | --- | --- | --- |
| Inline payload | One transport/retention boundary | Broker limits, replication cost, exposure | Small routinely needed data |
| Claim Check | Small envelope, specialized storage/security | Extra read, lifecycle, atomicity and availability dependency | Large/sensitive/rarely needed content |
| Chunk and aggregate | Works through bounded message sizes; parallel transfer | Ordering, completeness, memory and duplicate complexity | Streams where object storage is unavailable and chunk semantics are owned |
| Shared database row ID | Transactional with domain state in one database | Coupling, mutable-read and access-control risk | Same bounded context and immutable/versioned row |
| Content-addressed object | Natural dedupe and integrity identity | Existence/privacy leakage and garbage-collection complexity | Immutable reusable artifacts |
| Presigned bearer URL | Simple direct access with bounded lifetime | Token leakage, expiry versus queue delay, signer permissions | Short controlled transfers outside durable message retention |
| Authenticated claim ID | Central current authorization and audit | Extra authorization-service dependency | Durable queues, sensitive objects, changing access |
| Cache reference | Low retrieval latency | Eviction makes it unsuitable as source of truth | Optimization behind durable origin only |

Conditional offloading reduces small-message latency but creates two representations. Full-payload offloading gives one convention but adds a store read to every consumer. Partial offloading can minimize exposure but makes schema and integrity composition harder. Select deliberately and test every supported representation.

## Failure Modes and Misconceptions

- **“A unique URL is secure.”** Unguessability is not identity-based authorization, revocation, purpose limitation, or audit.
- **“A digest proves who produced the file.”** It detects byte mismatch relative to a trusted expected digest; it does not establish provenance by itself.
- **“Store then publish is atomic.”** It prefers orphan over dangling failure, but still needs outbox state and reconciliation.
- **“The latest object is good enough.”** Mutable reads destroy historical message meaning, replay, and idempotency.
- **“Object storage is always cheaper.”** Per-operation, egress, replication, retrieval, scan, cache, and retention costs may dominate.
- **“Delete when the consumer acknowledges.”** There may be other subscribers, retries, audits, restores, or legal holds.
- **“Broker retention and object lifecycle are independent.”** A message retained longer than its payload is not replayable.
- **“Encryption at rest protects the claim.”** Claims/tokens can leak and authorized-but-wrong consumers can still retrieve.
- **“Routers can fetch when needed.”** This increases coupling, latency, availability dependencies, and sensitive-data exposure.
- **“Content type from upload is trustworthy.”** Verify allowed type, signature/magic/schema, length, encoding, and parser behavior.
- **“Stored size bounds processing.”** Compression bombs, archives, recursive structures, and parser complexity can expand resource use.
- **“One checksum at upload covers all transformations.”** Compression, encryption, transcoding, and reserialization change bytes; define verification layer.
- **“A cache can own the payload.”** Eviction/expiry creates dangling claims unless a durable origin exists.
- **“Lifecycle deletion proves erasure.”** Versions, replicas, backups, caches, derivatives, indexes, and keys require explicit policy.
- **“A green queue means claims are healthy.”** Early acknowledgements or silent missing-object handling can hide data loss.

## Worked Examples

### Example 1

**Situation.** A 20 MiB document is published to five subscriptions and may redeliver twice per subscription. Compare inline broker-carried bytes with one stored object and small claims, ignoring replication and envelope size.

**Reasoning.** Inline logical delivery can move up to $20\times5\times2=200$ MiB through subscriber paths. Claim Check stores 20 MiB once, then consumers still retrieve according to their needs; it reduces broker bytes but not necessarily total payload egress. Cache or shared regional reads may help, while every subscriber still owns integrity and effect processing.

**Conclusion.** The pattern shifts and can reduce broker amplification; it does not make payload transfer free.

### Example 2

**Situation.** Messages below 64 KiB are inline; larger messages use a claim. A consumer assumes `data` always contains JSON.

**Reasoning.** The threshold created two wire variants. Define a tagged union such as `payload_mode=inline|claim` with separate required fields, schema validation, and tests at 65,535/65,536/65,537 bytes. Routing facts must be identical in meaning across both.

**Conclusion.** Conditional Claim Check needs an explicit versioned envelope, not a polymorphic string.

### Example 3

**Situation.** The producer uploads object O and crashes before publishing its outbox row.

**Reasoning.** No consumer sees a dangling claim, but O is orphaned. A staging metadata record with owner, digest, creation time, and publication state lets reconciliation either recreate the intended outbox event from durable intent or delete after a conservative unpublished-object grace period.

**Conclusion.** Store-first makes this failure recoverable only if staged intent and orphan reconciliation exist.

### Example 4

**Situation.** The producer publishes claim C and then attempts to upload object O; upload fails.

**Reasoning.** Consumers can immediately receive an unredeemable claim. Retry may eventually succeed, but ordering, retention, and terminal failure are uncertain. Visibility should be gated on verified durable storage; do not use publish-first merely to avoid orphans.

**Conclusion.** Prefer recoverable unpublished storage over consumer-visible missing content.

### Example 5

**Situation.** A claim points to `reports/customer-7/current.csv`; nightly generation overwrites the key.

**Reasoning.** A retry tomorrow reads different bytes for yesterday's message. Idempotency and audit now depend on timing. Use a write-once/versioned key and digest; publish a new claim for the new report and a supersession relationship if required.

**Conclusion.** Logical filenames are navigation aids, not immutable claim identity.

### Example 6

**Situation.** Storage returns the correct key but one byte differs after a faulty transfer.

**Reasoning.** The consumer verifies expected length and SHA-256 from an authenticated envelope before parsing. It quarantines the mismatch, records object version and observed digest without raw sensitive data, and does not acknowledge as successful. Retry from another replica may distinguish transient corruption from source corruption.

**Conclusion.** Successful retrieval is insufficient; verify exact bytes before effects.

### Example 7

**Situation.** Search, billing, and audit subscribe. Search finishes first and deletes the payload.

**Reasoning.** Billing and audit now have dangling claims. Either track the known three obligation states and delete only after all terminal policies permit, or apply retention covering the maximum supported group lag/replay/audit horizon. Audit may require archival rather than deletion.

**Conclusion.** Deletion authority belongs to the lifecycle policy across obligations, not to the fastest subscriber.

### Example 8

**Situation.** A presigned download URL valid for 24 hours is placed in a queue retained seven days and copied into error logs.

**Reasoning.** Delayed messages fail after URL expiry, while anyone reading logs during validity may exercise the bearer capability. Send a nonsecret claim ID; after authenticated authorization, mint a narrowly scoped short-lived URL just before retrieval and redact it from telemetry.

**Conclusion.** Bearer lifetime cannot simultaneously solve long queue delay and leak resistance; separate durable identity from delegated access.

### Example 9

**Situation.** Object lifecycle deletes after 30 days, but disaster recovery can restore broker messages from 45 days ago.

**Reasoning.** Restored messages between days 31 and 45 reference missing bytes. Align object retention with the maximum recoverable broker history plus recovery margin, or declare and enforce a shorter replay boundary with snapshots/archive. Test cross-system restore.

**Conclusion.** Recovery validity is the intersection of message, object, schema, key, and authorization availability.

### Example 10

**Situation.** A clinical image claim waits two days. The patient revokes research consent, but an analytics worker still has the message.

**Reasoning.** The reference is not enduring authority. At redemption, authenticate workload, recheck tenant/purpose/consent and legal basis, and deny access if no longer valid. Record a policy terminal outcome; do not leak the image or token into dead-letter diagnostics. Care delivery and research may require separate objects/policies.

**Conclusion.** Sensitive Claim Check separates storage exposure only when current purpose-bound authorization governs every redemption.

## Cross-Program Connections

- [Data Engineering](../../19-data-engineering/ROADMAP.md): immutable datasets, checksums, lineage, schema, partitioning, compaction, and replay determine payload meaning.
- [Security Engineering](../../25-security-engineering/ROADMAP.md): bearer capabilities, workload identity, authorization, encryption, key lifecycle, malware controls, and audit govern redemption.
- [Cloud and Infrastructure Engineering](../../30-cloud-and-infrastructure-engineering/ROADMAP.md): object versioning, replication, lifecycle rules, signed access, egress, and regional recovery implement the storage boundary.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md): cross-system publication, failure ambiguity, reconciliation, retention, and restore expose the non-atomic protocol.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): quotas, policy admission, observability, orphan cleanup, cost, and incident tooling make claims operable.
- [SEPAT-067](067-competing-consumers.md) handles concurrent redemption and retry; [SEPAT-069](../ROADMAP.md) owns unredeemable terminal failures.

## References

1. Hohpe, Gregor, and Bobby Woolf. *Enterprise Integration Patterns*. Addison-Wesley, 2003. Claim Check, Content Enricher, Content Filter, and Message Store.
2. Hohpe, Gregor. “Claim Check.” *Enterprise Integration Patterns* website, copyright 2003–2023. <https://www.enterpriseintegrationpatterns.com/patterns/messaging/StoreInLibrary.html>. Accessed 2026-08-29.
3. Microsoft. “Claim-Check pattern.” *Azure Architecture Center*. <https://learn.microsoft.com/en-us/azure/architecture/patterns/claim-check>. Accessed 2026-08-29.
4. Amazon Web Services. “Download and upload objects with presigned URLs.” *Amazon S3 User Guide*. <https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html>. Accessed 2026-08-29.
5. Amazon Web Services. “Checking object integrity in Amazon S3.” *Amazon S3 User Guide*. <https://docs.aws.amazon.com/AmazonS3/latest/userguide/checking-object-integrity.html>. Accessed 2026-08-29.
6. Amazon Web Services. “Retaining multiple versions of objects with S3 Versioning.” *Amazon S3 User Guide*. <https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html>. Accessed 2026-08-29.
7. Google Cloud. “Pub/Sub quotas and limits.” Current documentation. <https://docs.cloud.google.com/pubsub/quotas>. Accessed 2026-08-29.
8. National Institute of Standards and Technology. *FIPS PUB 180-4: Secure Hash Standard*. August 2015. <https://csrc.nist.gov/pubs/fips/180-4/upd1/final>.
9. Hardt, Dick. *RFC 6750: The OAuth 2.0 Authorization Framework: Bearer Token Usage*. IETF, October 2012. <https://www.rfc-editor.org/rfc/rfc6750>.
10. Rose, Scott, et al. *NIST SP 800-207: Zero Trust Architecture*. NIST, August 2020. <https://csrc.nist.gov/pubs/sp/800/207/final>.
11. Kleppmann, Martin. *Designing Data-Intensive Applications*. O'Reilly, 2017. Encoding, replication, stream processing, and derived-data foundations.
12. Anderson, Ross. *Security Engineering*, 3rd ed. Wiley, 2020. Capabilities, access control, cryptography, and lifecycle risk foundations.

Product quotas, signed-access behavior, storage consistency, versioning, lifecycle, and checksum support change by service and configuration. Current official documentation was checked on 2026-08-29; an implementation must verify its exact broker, object store, region, identity, encryption, retention, and client contracts.

## Exercises

### Exercise 1

Specify the minimal fields of a durable claim descriptor and explain what each field proves—or does not prove.

### Exercise 2

A 12 MiB payload is delivered inline to four subscriptions, each averaging 1.5 attempts. Estimate logical payload delivery bytes. Then state which bytes Claim Check can remove from the broker and which object-store/network costs remain. If broker replay is 14 days, maximum retry is 21 days, and audit retrieval is 90 days, derive the retention lower bound.

### Exercise 3

Design a store-before-publish state machine and reconciliation process that handles crashes before upload, after upload, after outbox commit, after broker acceptance but before relay confirmation, and during deletion.

### Exercise 4

Review this design: a mutable object key and seven-day presigned URL are sent to a 30-day retained topic; consumers log the URL, trust `Content-Type`, buffer the whole gzip file, and the first success deletes it. Identify defects and propose a production design.

### Exercise 5

Design Claim Check for cross-region transfer of genomic result files to care, audit, and consent-governed research subscribers. Address immutable identity, integrity, publication, authorization, privacy, malware/parser controls, regional/key failure, independent obligations, replay, deletion/legal hold, telemetry, and human review.

## Answers to the Exercises

### Answer 1

Include stable message/business identity; immutable object key plus version; digest algorithm/value; exact byte length; media type, content encoding, and schema/version; tenant/security classification and safe purpose/lifecycle identifiers; creation/expiry or retention-policy identifier; and correlation/provenance bound by an authenticated envelope. Object/version locates exact bytes. Length and digest detect mismatch relative to trusted expected values. Type/schema declares interpretation but must still be validated. Classification/policy metadata drives admission but does not itself authorize. The token does not prove producer identity, reader authorization, semantic correctness, confidentiality, availability, or malware safety; those require authenticated publication, current authorization, encryption/access control, retention/recovery, and content controls.

### Answer 2

Average logical payload delivery is

$$
12\text{ MiB}\times4\times1.5=72\text{ MiB}.
$$

Claim Check removes most of those payload bytes from broker storage/replication and claim-message delivery, replacing them with small descriptors. It still stores 12 MiB plus replicas/versions and incurs upload, retrieval per subscriber/attempt unless cached safely, scanning, encryption, operations, egress, retention, backup, and cleanup. The necessary basic object-retention lower bound is

$$
R_o\ge\max(14,21,90)=90\text{ days}.
$$

Legal hold, slow subscriptions, restore margin, backups, or privacy policy may require a different terminal decision; 90 days is not automatic deletion authorization.

### Answer 3

Use durable states `intent_recorded -> uploading -> stored_verified -> publish_pending -> published -> retention_eligible -> delete_pending -> deleted`, plus `quarantined/held`. Stable message ID, object version, digest, owner, timestamps, and outbox identity accompany all states. A pre-upload crash leaves intent eligible for retry/cancel. An after-upload crash leaves a staged object; reconciliation verifies it and resumes outbox creation or retires it after policy. Outbox commit atomically records publish intent with producer state; relay publishes idempotently. Broker acceptance with lost confirmation causes safe duplicate publication using the same message/claim identity, not a new object. Published state is established from confirmation/reconciliation evidence. Deletion begins only after the obligation/lifecycle ledger permits it; retries are idempotent, and a tombstone/confirmation lets reconciliation distinguish pending, already absent, held, versioned, backup-aged, and failed deletion. Alerts cover aged states and published claims without retrievable verified objects.

### Answer 4

The mutable key permits bytes to change under a historical message. The URL can expire before the 30-day message and, as a bearer capability, leaks through logs. `Content-Type` is untrusted, full buffering is unbounded, gzip may expand enormously, and first-consumer deletion breaks other groups/replay. Use a write-once/versioned or content-addressed object; bind digest, length, encoding, schema and classification in an authenticated envelope; send an opaque nonsecret claim ID; authenticate and authorize current tenant/purpose at redemption; mint short-lived scoped access only then; redact tokens; allowlist stores; stream with stored/decompressed byte, time, ratio, parser, redirect and concurrency limits; verify version/digest/type before effect; acknowledge afterward; and retain/delete from an independent subscription/lifecycle ledger. Add store-before-publish outbox/reconciliation, multi-region/key recovery, metrics for missing/integrity/access/age, and crash/corruption/replay/load/security tests.

### Answer 5

Store each exact genomic file as an immutable version under a random or content-derived internal identity with strong digest, length, encoding, schema, provenance, patient/tenant classification and region policy bound into an authenticated claim envelope. Because a content hash may reveal equality, do not expose it as a globally queryable locator; use opaque tenant-scoped claim IDs and access-controlled metadata. Upload, scan and verify in the permitted region, durably record publication intent/outbox, then expose claims. Reconcile staging, replication, outbox, broker, and obligation states.

Care, audit, and research are separate subscriptions with distinct identities, purposes, fields, retention and effects. At every redemption, authorize current patient/tenant, workload, region and purpose. Research additionally checks current consent and approved protocol; withdrawal produces a policy terminal outcome and downstream deletion/cessation workflow. Use short-lived delegated reads, customer/region-appropriate encryption keys, protected key recovery, private network paths, streaming size/decompression/parser limits, format validation and malware controls. Verify version, digest and provenance before idempotent effects.

Replication readiness gates regional publication; disaster tests restore broker, object/version metadata, bytes, schema, identity policy and encryption keys together. Track each subscription's terminal state; legal/clinical audit holds can prevent deletion even when research requires access withdrawal, so separate access revocation from physical retention. Govern versions, backups, derived datasets, caches and tombstones. Telemetry uses opaque IDs and records staging age, retrieval/integrity/auth failures, regional lag, obligations, holds and deletion evidence without genomic content or bearer tokens. Named security, privacy, clinical/genomic and legal reviewers must approve threat model, consent semantics, retention/erasure, failure recovery and validation evidence before production claims.

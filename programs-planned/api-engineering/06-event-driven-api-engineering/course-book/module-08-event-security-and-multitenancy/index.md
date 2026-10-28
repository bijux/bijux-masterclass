# Module 08 — Event Security, Multi-Tenancy, Privacy, and Trust

> **Program stage:** Course 6 of 10 — Extend the promise across asynchronous time.

> **Central question:** How are producers authenticated, consumers authorized, tenants isolated, payloads minimized, and event bytes protected?

## Where this module fits

Module 07 produced **Implement windowed analysis metrics, watermark progression, late-event correction revisions, and quarantine**. This module extends that result by asking: **How are producers authenticated, consumers authorized, tenants isolated, payloads minimized, and event bytes protected?**

The new capstone increment is **Add producer policy, tenant-scoped subscriptions/replay, exact-byte signatures, freshness, classification, and privacy rules**. It becomes the prerequisite for **Event Reliability, Backpressure, Dead Letters, and Recovery**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Authenticate producers and consumers independently of message content.
- Authorize publication by producer, source, channel, event type, and tenant.
- Authorize subscriptions by consumer effect and data classification.
- Preserve tenant isolation in subjects, envelopes, partition keys, storage, and projections.
- Minimize sensitive information in long-lived event payloads.
- Sign and verify exact canonical bytes with key identity and freshness policy.
- Distinguish duplicate delivery from hostile message injection or replay.
- Design key rotation and revocation without making retained history unverifiable.

## Capstone increment

Add producer policy, tenant-scoped subscriptions/replay, exact-byte signatures, freshness, classification, and privacy rules.

## Core event model

### 1. Transport identity and event authority are separate

A broker credential authenticates the connection or account. It may allow publication to a set of
subjects. The event envelope claims a `source`, `type`, tenant, and subject. The system must bind the
authenticated producer identity to those claims.

The capstone `ProducerGrant` lists permitted sources, channels, event types, and tenants. A valid
signature from a key that is not authorized for `AnalysisRunCompleted` remains unauthorized.

Broker ACLs and application-level authorization should agree. Defense in depth is useful only when the
layers have clear scope; duplicating inconsistent wildcard rules creates gaps.

### 2. Consumer authorization is data access

Subscribing to a channel is equivalent to receiving an ongoing data feed. Consumers need least-privilege
access to event types, tenants, and classifications. A debugging tool that can subscribe to all raw
datasets is a privileged production system, not a harmless client.

The consumer catalogue names accepted types and classification. Broker accounts/subjects enforce coarse
access; the dispatch layer verifies envelope tenant and type before handler invocation. Projections
partition state by tenant and use owner-aware queries.

A consumer may be authorized to know that an analysis completed but not to receive raw input, error
detail, or artifact location.

### 3. Tenant identity must survive every boundary

Tenant identity appears in the authenticated producer context, envelope, partition strategy where
applicable, inbox/projection keys, dead-letter records, replay plan, and audit evidence. It is never
inferred solely from a mutable payload field supplied by an untrusted producer.

A channel shared across tenants can be safe when authorization and storage remain tenant-scoped. A
subject-per-tenant design can strengthen isolation but creates catalogue and operational cardinality.
The choice is policy-driven.

Cross-tenant correlation IDs, caches, dedupe keys, or replay filters can leak or suppress another
tenant’s data even when the payload is correct.

### 4. Retained messages require data minimization

Event retention replicates data across brokers, archives, consumer logs, dead letters, replay stores, and
projections. Removing sensitive data from the source database may not remove those copies. The safest
event payload is the minimum stable fact consumers require.

Access tokens, webhook secrets, raw datasets, exception stacks, private filesystem paths, and full
identity records are prohibited. Use opaque resource IDs and let authorized consumers query the source
API when they need current sensitive details.

Classification, retention, encryption, and deletion policy are catalogue fields. “Internal topic” is
not a privacy classification.

### 5. Exact-byte signatures protect integrity across hops

The capstone signs canonical event bytes together with an explicit UTC timestamp and key ID using
HMAC-SHA256. Verification selects the key by ID, enforces freshness, recomputes the MAC, and compares in
constant time.

Signing a parsed object is ambiguous if languages serialize numbers, nulls, or key order differently.
Signing transport headers without a canonical profile may omit the payload schema or tenant. The course
profile signs the complete canonical semantic envelope.

HMAC is suitable for the controlled shared-trust exercise. Public-key signatures may be preferable when
many consumers should verify without gaining publish capability.

### 6. Signature freshness is not event deduplication

A timestamp freshness window limits injection of an old captured signed message through a live endpoint.
It does not eliminate normal broker redelivery after the window or retained replay. Durable consumers
use event ID/effect identity for dedupe, not signature timestamp.

A relay or archive may verify at ingestion, record verification evidence, and later deliver retained
events under trusted storage provenance. Requiring the original transport signature to remain fresh for
years would make replay impossible.

Security design therefore distinguishes live ingress replay defense, durable event identity, and
authorized historical replay.

### 7. Key rotation needs overlap and provenance

Producers sign with an active key ID. Consumers accept a bounded set of active/retiring verification
keys. Rotation publishes the new verification material before producers switch. Old keys remain
available for the required verification/replay horizon or their verified records carry trusted
ingestion evidence.

Revocation after compromise is different from routine retirement. Operators must identify events
accepted under the key, affected tenants/types, and whether source-of-truth reconciliation can confirm
or reject them.

Secrets never enter the AsyncAPI document, examples, event log, dead letters, or proof reports.

### 8. Security events and audit must remain bounded

Rejected publication, invalid signature, unauthorized tenant, forbidden type, malformed payload, and
suspicious replay produce structured security evidence with pseudonymized identifiers and safe reason
codes. Raw message bodies are not logged by default.

Rate limits and admission control from Courses 3 and 5 apply to producers, consumers, replay operators,
and dead-letter repair. A valid credential cannot create unlimited retained data or replay storms.

Audit evidence supports investigation but does not replace the authoritative domain and broker records.

## Engineering requirements

| Rule | Required behavior | Failure if omitted | Decisive evidence |
|---|---|---|---|
| Producer binding | Authenticated producer identity is bound to source, channel, type, and tenant grants. | A credential can forge facts outside its ownership. | Grant evaluation and broker ACL review |
| Consumer least privilege | Subscription and handler dispatch are limited by effect, type, tenant, and classification. | Consumers receive unrelated or sensitive streams. | Consumer catalogue and authorization tests |
| Tenant-scoped state | Inbox, projection, dead letter, replay, and audit keys preserve tenant. | Cross-tenant suppression or disclosure occurs. | Shared hostile vectors |
| Payload minimization | Public events exclude secrets and unnecessary sensitive data. | Retention multiplies data exposure. | Schema/classification review and sensitive-key scan |
| Canonical signature | Signature covers exact profile bytes, timestamp, and selected key. | Equivalent-looking representations verify differently or fields remain unsigned. | Cross-language signature vectors |
| Fresh ingress | Live signed ingress enforces bounded timestamp and authorization. | Captured messages can be injected indefinitely. | Freshness/replay tests |
| Rotation evidence | Key states, overlap, retirement, and compromise response are documented. | New keys fail or old keys remain trusted forever. | Rotation exercise |

## Worked failures

### Case 1 — broker ACL allowed a forged source

A worker credential can publish to `analysis.events.>` and emits a completion event claiming the control
plane source. Bind the credential to permitted event types/sources and narrow subjects. Reject before
handler dispatch even if the JSON schema is valid.

### Case 2 — tenant was omitted from inbox identity

Two tenants coincidentally receive the same imported event ID. One inbox row suppresses the other’s
effect. Include tenant in the trust context and ensure event IDs are globally unique under profile;
tenant-scoped storage remains an additional isolation control.

### Case 3 — signature protected a mutable serialization

Python signs sorted JSON while TypeScript signs ordinary `JSON.stringify`. Property order differences
cause valid messages to fail, and a proxy can reserialize. Use the shared canonical JSON profile and
exact bytes.

### Case 4 — legitimate replay failed freshness

Historical events are reprocessed months later and rejected because their original transport timestamp
is old. Verify live ingress at acceptance, retain trusted provenance, and authorize replay separately.
Event dedupe and replay scope, not a five-minute signature window, govern historical processing.

## Python implementation

Python security controls live in:

```text
capstone/tracks/python-fastapi/src/event_engineering/security.py
capstone/tracks/python-fastapi/tests_event/test_stream_security.py
```

`authorize_message()` checks a `ProducerGrant` against source, channel, type, tenant, and sensitive-key
policy. `sign_message()` signs canonical bytes and timestamp; `verify_message()` selects a key and enforces
freshness.

The workshop adds authenticated producer identity as an input to authorization rather than trusting a
`producerId` field inside `data`. It also records safe rejection events without storing the raw body.

## TypeScript implementation

TypeScript uses `crypto` primitives over the same canonical bytes:

```text
capstone/tracks/typescript-fastify/src/event-engineering/security.ts
capstone/tracks/typescript-fastify/test-event-core/security-reliability.test.mjs
```

Convert signatures and IDs without implicit Unicode normalization or unsafe string concatenation. Validate
timestamp syntax and key ID before expensive schema/handler work. Use timing-safe comparison on equal-length
buffers.

Broker credentials remain outside source and examples. Local fixtures use explicitly marked synthetic keys.

## Cross-language invariant

Given one event, timestamp, key ID, and secret, both tracks must produce the same body digest and signature
and accept/reject the same freshness, authorization, sensitive-data, and tenant cases. A signature created in
Python must verify in TypeScript and vice versa.

Shared security vectors are the decisive dependency-light evidence.

## Design review

Review the path from authenticated connection to committed effect. At each stage, name the identity,
authorization decision, tenant scope, data classification, and audit output. Then review retention copies:
broker, archive, dead letter, logs, traces, projections, backups.

A design that secures publication but leaves wildcard consumer access or raw dead letters is incomplete.

## End-to-end worked example

The control-plane producer authenticates with a credential mapped to source
`urn:bijux:analysis-control`, lifecycle channels, allowed event types, and tenant set. It constructs a
canonical completion event, writes it to the outbox, and the relay signs exact bytes with active key `evt-2`.

The broker accepts the permitted subject. A notification consumer authenticates separately, receives only
completed/failed events for authorized tenants, verifies trusted ingestion/signature evidence, validates the
payload, and applies tenant-scoped inbox identity.

An attacker replays the signed body through live ingress after the freshness window; ingress rejects it. An
authorized operator later launches a bounded historical replay from the trusted retained stream; that path
uses replay authorization and event dedupe rather than pretending the original signature is fresh.

## Failure patterns

- **TLS-only trust.** Connection protection is mistaken for authorization to assert a specific fact.
- **Envelope trust.** Source or tenant claims inside the message are accepted without binding to producer identity.
- **Wildcard consumer.** A debug or analytics credential can read every tenant and classification.
- **Sensitive event log.** Long retention stores tokens, paths, raw inputs, or exception details.
- **Noncanonical signing.** Languages sign different representations of the same object.
- **Freshness/dedupe confusion.** A short signature window is used as the only replay or duplicate control.
- **Permanent retired key.** Old verification secrets remain active indefinitely with no provenance plan.

## Module synthesis

You are ready to leave this module when you can **authenticate producers and consumers independently of message content, authorize publication by producer, source, channel, event type, and tenant, and authorize subscriptions by consumer effect and data classification** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Plant a noncanonical serializer and require cross-language signature failure** and requiring the following oracle: **Only the valid authorized event, legitimate duplicate, and approved historical replay reach handlers. Forged, cross-tenant, sensitive, altered, unknown-key, stale-ingress, and unauthorized-subscription cases are rejected with safe evidence. Both languages agree on signature bytes. Rotation has no rejection gap.**

The cumulative platform now includes **Add producer policy, tenant-scoped subscriptions/replay, exact-byte signatures, freshness, classification, and privacy rules**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Event Reliability, Backpressure, Dead Letters, and Recovery](../module-09-event-reliability-and-recovery/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.

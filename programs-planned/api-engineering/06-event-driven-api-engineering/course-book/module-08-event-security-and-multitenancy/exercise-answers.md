# Worked Answers — Module 08: Event Security, Multi-Tenancy, Privacy, and Trust

Use these solutions to audit your reasoning for **Event Security, Multi-Tenancy, Privacy, and Trust**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Bind a producer

Grant the authenticated producer ID the control-plane source URI, lifecycle channels, event types completed/failed v1, and explicit tenant set. Exclude artifact channel/type because the artifact owner publishes that fact. Align broker publish ACLs with the application grant.

The chapter’s decisive distinction is this: The control-plane producer authenticates with a credential mapped to source urn:bijux:analysis-control, lifecycle channels, allowed event types, and tenant set. It constructs a canonical completion event, writes it to the outbox, and the relay signs exact bytes with active key evt-2.

## 2. Authorize a consumer

Grant notification-v1 receive access only to terminal lifecycle event types and allowed tenant scopes/classification. It does not need progress or raw dataset channels. Handler dispatch rechecks type/tenant, and the consumer has only an outbound notification-intent capability.

In the cumulative capstone, the rule becomes concrete: The consumer catalogue names accepted types and classification. Broker accounts/subjects enforce coarse access; the dispatch layer verifies envelope tenant and type before handler invocation. Projections partition state by tenant and use owner-aware queries.

## 3. Find a tenant leak

Inbox dedupe may work, but projection queries or updates can mix tenants with identical run/resource IDs, and authorization can expose another tenant’s result. Tenant must be part of projection ownership keys and query predicates, not only the envelope.

A useful way to reason about the boundary is: Two tenants coincidentally receive the same imported event ID. One inbox row suppresses the other’s effect. Include tenant in the trust context and ensure event IDs are globally unique under profile; tenant-scoped storage remains an additional isolation control.

## 4. Minimize a failure event

Include run ID, stable safe failure code/category, terminal timestamp, retryability if contractually meaningful, and perhaps attempt count. Exclude stack traces, raw exception text, access tokens, filesystem paths, raw dataset content, worker lease tokens, and full user records.

The implementation consequence is: Given one event, timestamp, key ID, and secret, both tracks must produce the same body digest and signature and accept/reject the same freshness, authorization, sensitive-data, and tenant cases. A signature created in Python must verify in TypeScript and vice versa.

## 5. Compare TLS and signatures

TLS protects confidentiality/integrity between connected peers and authenticates endpoints according to configuration. Message signatures protect selected bytes across relays/storage and identify a key. Neither proves that the asserted completion really occurred; authorization and source-of-truth reconciliation do.

The important nuance is: The capstone signs canonical event bytes together with an explicit UTC timestamp and key ID using HMAC-SHA256. Verification selects the key by ID, enforces freshness, recomputes the MAC, and compares in constant time.

## 6. Compute signature input

Sign the canonical complete event body plus the normalized signature timestamp, selected key ID by context, and profile-defined separator. Canonicalization fixes key order, number validity, null/missing handling, and UTF-8 bytes. Ordinary serialization can differ across runtimes.

Under concurrency or failure, the distinction becomes: Signing a parsed object is ambiguous if languages serialize numbers, nulls, or key order differently. Signing transport headers without a canonical profile may omit the payload schema or tenant. The course profile signs the complete canonical semantic envelope.

## 7. Distinguish two replays

Hostile replay injects captured bytes through a live ingress outside freshness/authorization and is rejected. Historical replay reads trusted retained records under an approved plan, effect version, tenant/type scope, maximum count, side-effect policy, and durable dedupe. The original event time may be old by design.

The design remains honest only if: Historical events are reprocessed months later and rejected because their original transport timestamp is old. Verify live ingress at acceptance, retain trusted provenance, and authorize replay separately. Event dedupe and replay scope, not a five-minute signature window, govern historical processing.

## 8. Rotate a key

Distribute the new verification key first; confirm consumers loaded it; switch a canary producer to the new key ID; observe verification; switch remaining producers; retain old verification for overlap/retained provenance; stop signing with old key; retire or archive it according to replay and compromise policy.

The consumer-facing consequence is: Producers sign with an active key ID. Consumers accept a bounded set of active/retiring verification keys. Rotation publishes the new verification material before producers switch. Old keys remain available for the required verification/replay horizon or their verified records carry trusted ingestion evidence.

## 9. Respond to compromise

Identify key ID, active interval, producers, channels/types/tenants, broker records and signatures accepted, outbox/source records, consumer effects, and anomalies. Revoke live use, reconcile events against authoritative state, quarantine uncertain effects, publish corrections if needed, and rotate credentials.

The operational consequence is: A worker credential can publish to analysis.events. and emits a completion event claiming the control plane source. Bind the credential to permitted event types/sources and narrow subjects. Reject before handler dispatch even if the JSON schema is valid.

## 10. Secure dead letters

Store event ID/type/subject/tenant in pseudonymized or authorized form, channel/partition/offset, consumer/effect, attempt count, safe failure code, schema/profile versions, body digest, and encrypted restricted payload only if repair requires it. Limit access, retention, export, and replay.

The strongest engineering interpretation is: Event retention replicates data across brokers, archives, consumer logs, dead letters, replay stores, and projections. Removing sensitive data from the source database may not remove those copies. The safest event payload is the minimum stable fact consumers require.

## 11. Protect a shared channel

Authenticate producer/consumer, bind grants to tenant/type, validate envelope tenant, scope inbox/projection and replay, and prevent wildcard credentials. Subject-per-tenant may aid broker-level isolation for highly regulated or separately operated tenants, but increases subject/catalogue cardinality and does not replace application checks.

The defect-oriented view is: Tenant identity appears in the authenticated producer context, envelope, partition strategy where applicable, inbox/projection keys, dead-letter records, replay plan, and audit evidence. It is never inferred solely from a mutable payload field supplied by an untrusted producer.

## 12. Audit rejection

Record time, authenticated producer ID/pseudonym, source claim, type, tenant pseudonym, channel, body digest, safe reason code, policy version, and correlation/trace identity. Exclude raw body, secret headers, tokens, and sensitive payload fields. Rate-limit repeated rejection evidence.

Across the Python and TypeScript tracks, the invariant is: Rejected publication, invalid signature, unauthorized tenant, forbidden type, malformed payload, and suspicious replay produce structured security evidence with pseudonymized identifiers and safe reason codes. Raw message bodies are not logged by default.

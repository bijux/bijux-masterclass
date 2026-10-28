# Reference Answers — Module 08: Worked answers — Module 08 — Event Security, Multi-Tenancy, Privacy, and Trust

Read after attempting all twelve Event Security, Multi-Tenancy, Privacy, and Trust exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Bind a producer

Grant the authenticated producer ID the control-plane source URI, lifecycle channels, event types completed/failed v1, and explicit tenant set. Exclude artifact channel/type because the artifact owner publishes that fact. Align broker publish ACLs with the application grant.

## 2. Authorize a consumer

Grant notification-v1 receive access only to terminal lifecycle event types and allowed tenant scopes/classification. It does not need progress or raw dataset channels. Handler dispatch rechecks type/tenant, and the consumer has only an outbound notification-intent capability.

## 3. Find a tenant leak

Inbox dedupe may work, but projection queries or updates can mix tenants with identical run/resource IDs, and authorization can expose another tenant’s result. Tenant must be part of projection ownership keys and query predicates, not only the envelope.

## 4. Minimize a failure event

Include run ID, stable safe failure code/category, terminal timestamp, retryability if contractually meaningful, and perhaps attempt count. Exclude stack traces, raw exception text, access tokens, filesystem paths, raw dataset content, worker lease tokens, and full user records.

## 5. Compare TLS and signatures

TLS protects confidentiality/integrity between connected peers and authenticates endpoints according to configuration. Message signatures protect selected bytes across relays/storage and identify a key. Neither proves that the asserted completion really occurred; authorization and source-of-truth reconciliation do.

## 6. Compute signature input

Sign the canonical complete event body plus the normalized signature timestamp, selected key ID by context, and profile-defined separator. Canonicalization fixes key order, number validity, null/missing handling, and UTF-8 bytes. Ordinary serialization can differ across runtimes.

## 7. Distinguish two replays

Hostile replay injects captured bytes through a live ingress outside freshness/authorization and is rejected. Historical replay reads trusted retained records under an approved plan, effect version, tenant/type scope, maximum count, side-effect policy, and durable dedupe. The original event time may be old by design.

## 8. Rotate a key

Distribute the new verification key first; confirm consumers loaded it; switch a canary producer to the new key ID; observe verification; switch remaining producers; retain old verification for overlap/retained provenance; stop signing with old key; retire or archive it according to replay and compromise policy.

## 9. Respond to compromise

Identify key ID, active interval, producers, channels/types/tenants, broker records and signatures accepted, outbox/source records, consumer effects, and anomalies. Revoke live use, reconcile events against authoritative state, quarantine uncertain effects, publish corrections if needed, and rotate credentials.

## 10. Secure dead letters

Store event ID/type/subject/tenant in pseudonymized or authorized form, channel/partition/offset, consumer/effect, attempt count, safe failure code, schema/profile versions, body digest, and encrypted restricted payload only if repair requires it. Limit access, retention, export, and replay.

## 11. Protect a shared channel

Authenticate producer/consumer, bind grants to tenant/type, validate envelope tenant, scope inbox/projection and replay, and prevent wildcard credentials. Subject-per-tenant may aid broker-level isolation for highly regulated or separately operated tenants, but increases subject/catalogue cardinality and does not replace application checks.

## 12. Audit rejection

Record time, authenticated producer ID/pseudonym, source claim, type, tenant pseudonym, channel, body digest, safe reason code, policy version, and correlation/trace identity. Exclude raw body, secret headers, tokens, and sensitive payload fields. Rate-limit repeated rejection evidence.

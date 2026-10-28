---
module_id: API-033
program: API & Service Engineering
level: 1
module_number: 33
title: Authentication Context Propagation
status: complete
last_verified: 2026-09-01
---

# Authentication Context Propagation

## One-Page Review

### Governing question

How can a service transform presented credentials into a verified, typed authentication context and propagate the minimum necessary identity evidence across internal calls without confusing user, client, workload, tenant, or delegation identities?

### Essential definitions

- **authentication** establishes confidence that a presented identity claim is bound to the requester under a named mechanism.
- A **principal** is the identified security subject on whose identity a decision may depend.
- A **client identity** identifies the application using an authorization protocol; it is not automatically the end user.
- A **workload identity** identifies a running service, job, or deployment instance.
- **authentication context** is immutable verified evidence such as issuer, subject, audience, client, assurance, time bounds, and credential provenance.
- **delegation** permits one actor to act with bounded authority on behalf of another; **impersonation** substitutes an effective actor and requires explicit policy and audit.
- **token exchange** obtains a new credential for a downstream audience rather than replaying the original credential everywhere.
- A **trust boundary** is a crossing at which identity assertions must be established or revalidated under explicit policy.

### Central model, mechanism, or theorem

Let credential $k$ be validated by policy $P$ for recipient $R$ at time $t$. Context construction is partial:

$$
V_P(k,R,t)\rightharpoonup C=(i,s,a,c,w,d,q,e),
$$

where issuer $i$, subject $s$, audience $a$, client $c$, workload $w$, delegation chain $d$, assurance $q$, and expiry $e$ are verified. Propagation is not copying $C$ blindly. Each hop derives a least-information context or obtains a new audience-bound credential, with provenance linking it to the upstream authenticated request.

### Critical invariants

Credentials are untrusted until signature or introspection, issuer, audience, type, time, and sender binding policies pass. ID tokens are not accepted as API access tokens. User, client, workload, tenant, and effective actor remain distinct fields. Request bodies and arbitrary headers cannot override verified context. Context is immutable and request-scoped. Downstream credentials are audience-restricted, short-lived, least-privileged, and never logged. Every receiving service validates what it relies on. Delegation depth and authority do not increase across hops. Background work stores durable provenance without persisting a reusable inbound bearer token.

### Common failures

Decoding a JWT without verifying it; accepting any algorithm or key selected by hostile headers; skipping issuer or audience checks; using an ID token at an API; treating `client_id` as user; deriving tenant solely from an untrusted request field; copying `X-User`, roles, or scopes from the internet; forwarding one bearer token through every service; storing tokens in jobs, URLs, or logs; trusting network location; letting service B accept service A's audience; losing the original actor during impersonation; merging conflicting identities silently; and authorizing from stale or privacy-excessive claims.

### Compact example

Gateway receives an access token for `orders-api`, validates the issuer profile and sender binding, and constructs context `{subject: buyer-7, client: mobile-app, tenant: t-2, workload: edge}`. Orders service revalidates its audience and maps only verified values. To call inventory, it exchanges for a short-lived `inventory-api` token containing the needed delegated identity and records the original request ID—not the inbound token. **Conclusion:** identity provenance continues, while credential applicability and disclosed claims narrow per hop.

### Connections

[Request Parsing and Validation](032-request-parsing-and-validation.md) safely parses credentials and request data. [Authorization Checks](../ROADMAP.md) next applies context to resources and actions. [OAuth Authorization Flows](../ROADMAP.md) and [Applying OpenID Connect at API Boundaries](../ROADMAP.md) later cover protocol-specific acquisition and identity details; this module owns context construction and propagation inside a service call chain.

## Governing Question

Which validation, typing, derivation, token-exchange, hop-by-hop verification, and audit rules preserve trustworthy identity provenance across synchronous and asynchronous service boundaries?

## Why This Matters

Authentication is often described as middleware that turns a token into a user ID. Production systems need a richer model. A request can involve an end user, an OAuth client, a calling workload, a tenant, an administrator acting on behalf of a user, and a chain of services. These identities have different security meanings. Flattening them into `userId` creates privilege escalation and weak audit trails.

Credential validity is contextual. A correctly signed token can be expired, intended for another audience, issued by an untrusted issuer, of the wrong token type, replayed without its sender proof, or valid under a different tenant policy. Decoding claims proves only that bytes have a structure. Context construction begins after cryptographic or introspection verification and profile-specific checks.

Propagation creates another hazard. Forwarding the same bearer token to every downstream service expands its exposure and may give intermediaries authority they do not need. Copying plain identity headers relies on network trust and makes spoofing easy. Secure propagation combines workload authentication, audience restriction, least privilege, token exchange or trusted signed assertions, hop-by-hop verification, and explicit provenance.

## Prerequisites and Retrieval

Retrieve HTTP authentication fields and `WWW-Authenticate`; bearer-token handling; JWT/JWS structure and validation; issuer metadata and key rotation; OAuth audiences, scopes, resource indicators, introspection, token exchange, sender constraint, and current security best practice; OpenID Connect subjects and authentication claims; workload identity; trust boundaries; authorization; tenant isolation; secure logging; asynchronous jobs; and distributed tracing.

Before implementing propagation, retrieve accepted credential profiles, trusted issuers and keys, exact resource audience, algorithms, clock-skew policy, token types, required claims, revocation/introspection behavior, sender-binding mechanism, downstream audiences, token broker, workload identity, delegation model, tenant source, privacy classification, and incident-revocation procedure.

## Learning Objectives

By the end of this module, you should be able to:

1. validate credentials in context rather than merely decode claims;
2. distinguish subject, client, workload, tenant, delegator, and effective actor;
3. construct immutable typed authentication context with provenance;
4. choose hop-by-hop validation, token exchange, or trusted internal assertions;
5. propagate identity through synchronous and asynchronous work safely;
6. handle key rotation, expiry, revocation, failure, privacy, and observability; and
7. prevent confused-deputy, token substitution, replay, and header-spoofing failures.

## Core Exposition

### Start with identities, not token fields

Model the parties before selecting claims:

- the **subject** represented by the credential;
- the **resource owner** where delegation exists;
- the **client** that obtained or presents an access token;
- the **calling workload** that established the current connection;
- the **effective actor** whose action is being evaluated;
- the **delegator or impersonator** when different from the effective actor;
- the **tenant or organization context** under which data is selected; and
- the **issuer** that made the authenticated assertion.

These can coincide but must not be assumed equal. In a client-credentials grant, the subject can identify an application rather than a human. A support agent can act on behalf of a customer while remaining the accountable actor. A service can call another service on behalf of a user, presenting both workload and delegated subject evidence.

Use distinct types or named fields. `principal_id`, `client_id`, `workload_id`, `tenant_id`, `actor_id`, and `subject_id` are clearer than one `user`. Define each identifier's namespace: subject values are often meaningful only as the issuer-subject pair $(iss,sub)$.

### Treat credentials as untrusted input

An access token, session cookie, client certificate, API key, or signed internal assertion arrives from outside the application policy boundary. Parse it under strict size and syntax limits, but do not populate trusted context until its profile passes.

For a signed JWT access token, validation commonly includes:

1. explicit accepted token type/profile;
2. explicitly configured algorithms, never whatever `alg` requests;
3. issuer-to-key binding from trusted metadata or configuration;
4. signature validation with an appropriate key and use;
5. exact trusted issuer comparison;
6. audience containing the current resource server;
7. expiry, not-before, issued-at, and maximum-age policy;
8. required subject, client, token ID, or profile claims;
9. mutually exclusive rules that reject ID tokens and other JWT kinds;
10. sender proof where a sender-constrained token is used; and
11. local revocation, status, or risk policy where applicable.

RFC 8725 requires callers to constrain algorithms and validates issuer and audience to prevent substitution. RFC 9068 defines a JWT access-token profile including `iss`, `exp`, `aud`, `sub`, `client_id`, `iat`, and `jti`, but not every deployment uses this profile. Detect the profile; do not assume every bearer string is a JWT.

Opaque tokens require authorization-server introspection or a local trusted reference mechanism. Successful introspection still requires current audience, client, token type, activity, and policy checks. Cache only within safe bounds no longer than credential validity and revocation requirements allow.

### Distinguish authentication from authorization

Authentication context contains verified evidence. It does not itself decide whether an actor may read order `o-7`, change `tenant_id`, approve a payment, or see a hidden resource. Scopes, roles, groups, and entitlements are inputs to authorization policy, not universal permission names.

The same scope string can have meaning only for audiences declared by its profile. A role can be tenant-relative or stale after organizational change. A verified `admin` claim must not bypass object ownership and separation-of-duty policy unless the authorization model explicitly says so.

Keep context facts and authorization decisions separate. A context might state `authentication_assurance=phishing-resistant` and `scopes={orders.read}`. The next module's policy decides whether that evidence is sufficient for the action, resource, tenant, and current state.

### Construct one immutable request context

After verification, construct an immutable value containing only understood fields. A useful shape includes:

- credential profile and validation method;
- trusted issuer and issuer-subject principal key;
- client identity and grant/delegation type where known;
- connection/workload identity;
- intended audience validated for this service;
- issued, not-before, expiry, and validation times;
- sender-binding identity or proof status;
- verified authentication method/assurance where relevant;
- tenant context with provenance;
- bounded scopes or entitlements with issuer and audience meaning;
- actor/delegator chain;
- token identifier represented safely for replay/audit controls; and
- internal request/correlation identity separate from credentials.

Do not include the raw token in ordinary application context. A component needing token exchange should use a secure credential broker handle or tightly scoped mechanism, not expose the credential to every function.

Immutability prevents later middleware or domain code from replacing the actor. Derive narrower child contexts rather than mutating a parent. Bind context lifetime to the request unless creating a governed durable job record.

### Establish provenance for every field

Each field needs a source and validation rule. Tenant might come from a token claim issued specifically for the resource, from a verified hostname-to-tenant mapping, or from the resource record after lookup. A body `tenantId` is a requested target, not trusted context.

When sources coexist, define precedence and consistency checks. If verified token tenant is `t-1` and path targets `t-2`, do not silently choose one. Treat it as a denied or concealed cross-tenant attempt under authorization policy.

Do not copy all JWT claims into a generic map. Unknown claims lack semantics; URI or key-valued claims can trigger unsafe lookups; privacy-sensitive claims spread unnecessarily. Map an allowlist to typed values and reject malformed required claims.

Claim names do not guarantee claim quality. Email can change and is often inappropriate as a stable principal key. Display name is not an identity. Group lists can be large, stale, or privacy-sensitive. Prefer stable issuer-scoped subject identifiers and fetch current attributes under policy when required.

### Validate at every resource boundary

A gateway can authenticate externally and strip spoofable inbound identity headers, but a downstream service must establish why it trusts the gateway and the propagated assertion. Network location alone is insufficient.

Common patterns are:

1. **end-token forwarding:** downstream validates the original token and must be an intended audience;
2. **token exchange/delegation:** a broker issues a new short-lived token for the downstream audience with reduced authority and actor provenance;
3. **signed internal assertion:** a trusted issuer signs a narrowly scoped context for the receiver, combined with authenticated workload transport; and
4. **workload-only call:** downstream acts solely on the service identity when no user delegation is needed.

End-token forwarding is simple but expands credential exposure and often violates audience restriction. It is valid only if the token explicitly targets every recipient, claim disclosure is acceptable, and each service verifies it.

Token exchange is usually clearer across distinct resources. The new token can narrow audience, scopes, lifetime, and claims. The token broker records the delegation relationship. Exchange does not magically authorize the requested action; it creates bounded evidence for downstream policy.

Signed internal headers must not be plain `X-User-Id`. Strip any external versions at ingress, authenticate the sending workload, bind assertion to recipient and short time window, protect integrity, and prevent replay. Prefer standardized token profiles where they fit rather than inventing cryptography.

### Preserve workload and user identity together

Downstream policy may need to know both “orders-service called” and “buyer-7 initiated.” The workload is accountable for secure handling and may have its own service permission. The user supplies delegated authority. Neither should erase the other.

Represent a call as actor chain such as:

$$
d=(u,c,w_0,w_1,\ldots,w_n),
$$

where user $u$ acted through client $c$ and workloads $w_i$. Bound the maximum depth and preserve only security-relevant hops. Trace identifiers can connect telemetry but are not proof of this chain.

A downstream service checks that the immediate caller workload may invoke it, the delegated token targets it, and the effective subject is allowed for the resource. Compromise of one service should not let it mint arbitrary upstream users.

### Model delegation and impersonation explicitly

Delegation narrows an existing authority for another actor or service. Impersonation allows an operator or system to act as an effective subject and is higher risk. Both require explicit policy, visible context, limited duration, reason, and audit.

Do not replace `actor=agent-4` with `actor=customer-9`. Preserve `actor=agent-4`, `effective_subject=customer-9`, `mode=impersonation`, authority source, ticket/reason reference, and start/expiry. Authorization can impose stronger controls and response/UI can indicate the mode where appropriate.

Delegation chains should satisfy monotonic authority:

$$
\Pi(C_{j+1})\subseteq\Pi(C_j),
$$

where $\Pi(C)$ is the privilege set potentially represented by context $C$. A downstream exchange must not add an unrelated tenant or permission. Some systems transform privilege vocabulary between audiences; require an explicit mapping and prove the resulting capability is no broader in effect.

### Restrict audience and sender

An audience restriction says where a token is intended to be accepted. Every resource server verifies its own identifier. A token for `orders-api` must not be accepted by `inventory-api` merely because both trust the issuer.

RFC 9700 recommends audience-restricted and sender-constrained access tokens. Sender constraint binds token use to proof of a key or certificate, reducing replay of a stolen token. Mutual TLS and DPoP are examples; their exact protocol mechanics belong to later security modules.

The receiver must validate the binding on every relevant request and bind the proof to method and target where the mechanism requires it. A gateway that validates sender proof and forwards the bearer token beyond the bound channel can destroy the property unless it exchanges the token or propagates a new trusted assertion.

Bearer tokens require especially strict handling. Send them in the authorization header over authenticated TLS, never URLs. Redact them from access logs, traces, errors, crash reports, analytics, queues, and metrics.

### Handle keys and issuer metadata safely

Retrieve keys only from trusted issuer metadata configured for the exact issuer. Do not follow arbitrary `jku`, `x5u`, or claim URLs from a token. That can enable server-side requests or attacker-selected keys.

Cache keys with bounded refresh. On unknown `kid`, refresh from the trusted endpoint under rate limits and concurrency control; do not fetch on every hostile request. Retain old keys long enough for still-valid tokens during planned rotation. Reject if no trusted valid key exists.

Key fetch failure is not permission to skip signature validation. Decide whether cached keys can continue until their policy expiry. Monitor unknown key rates, issuer failures, and rotations without logging tokens.

Pin allowed algorithms and key uses per issuer/profile. An algorithm name in the token is input to be checked, not configuration. Keep validation rules mutually exclusive for access tokens, ID tokens, logout tokens, internal assertions, and other JWT applications.

### Handle time, expiry, and revocation

Validate expiration and not-before with an authoritative clock and a small documented skew allowance. Skew is not an extension of business session duration. Enforce a maximum token age where issuer profile requires it, even if `exp` is far away.

Context cannot outlive the credential evidence on which it depends. A long request or stream needs a policy: authenticate at establishment, periodically revalidate, terminate at expiry, or allow a bounded established session. State the behavior.

Self-contained tokens trade immediate local validation for delayed revocation. Use short lifetimes, event-driven revocation, token status, or introspection according to risk. Do not claim a signed JWT is “not revoked” merely because its signature passes.

When an issuer or key is compromised, revoke trust centrally, invalidate caches, reject new contexts, identify affected audiences and token times, and preserve safe audit evidence. Rotation and emergency revocation are operational requirements, not only cryptographic ones.

### Propagate through asynchronous work

A queued job can execute after the inbound credential expires. Storing and replaying that token is usually wrong: it broadens exposure and ties durable work to a transient bearer secret.

At enqueue time, authorize creation of a durable work item and store minimum provenance: issuer-subject principal key, client/workload, tenant, requested action, authorization decision reference or policy version, request identity, delegation/impersonation facts, and creation time. Do not store raw credentials unless a protocol explicitly requires secure token custody and the risk is accepted.

At execution time, the worker authenticates with its workload identity and either:

- executes authority durably granted to the work item under current cancellation/revocation policy;
- re-evaluates current authorization from provenance; or
- obtains a new audience-specific delegated credential through an authorized broker.

Choose semantics explicitly. Re-evaluation can make queued work fail after role changes; snapshot authority can execute after access removal. Financial, administrative, and privacy-sensitive actions often need stronger current checks and cancellation paths.

### Separate identity context from observability context

Trace and correlation headers help follow calls but are caller-controlled unless a trusted layer replaces or validates them. They do not authenticate the subject, client, tenant, or workload.

Logs should record safe stable identifiers, outcome, issuer category, authentication method, delegation mode, and a non-secret token fingerprint or identifier only when policy permits. Do not log tokens, proofs, session cookies, full claim sets, personal display data, or high-cardinality group lists.

Audit records need tamper resistance, retention, access controls, and clock quality. Preserve original and effective actors for administrative actions. A trace span optimized for debugging is not automatically a compliant audit record.

### Fail safely and consistently

Missing or invalid credentials generally produce `401` with a suitable `WWW-Authenticate` challenge under HTTP authentication semantics. Valid authentication with insufficient authority generally leads to authorization handling, often `403` or concealed `404`. Do not use `403` to describe an invalid signature or expired token internally.

Public token errors reveal only what helps legitimate clients recover. Avoid distinguishing unknown subject, revoked account, wrong tenant, and signature details when it aids attackers. Log a safe internal category and correlation identifier.

Issuer outage, key-refresh failure, introspection timeout, and token-broker failure are dependency conditions. Do not treat them as authenticated success. Depending on cached evidence and policy, fail closed or use still-valid cached state; never silently switch to unverified claims.

The bounded checker below validates a pre-parsed claim set for type, issuer, audience, time, and subject. It is not a JWT decoder, signature verifier, key fetcher, or authorization engine.

<!-- bijux-verify: {"id":"authentication-context-policy","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"valid=accepted:user-7\nwrong_type=rejected:token_type\nwrong_audience=rejected:audience\nexpired=rejected:expired\nmissing_subject=rejected:subject\n","stderr":""}} -->
```python
def context(claims, now):
    if claims.get("typ") != "at+jwt":
        return "rejected:token_type"
    if claims.get("iss") != "https://issuer.example/":
        return "rejected:issuer"
    if "orders-api" not in claims.get("aud", []):
        return "rejected:audience"
    if claims.get("exp", 0) <= now:
        return "rejected:expired"
    if not claims.get("sub"):
        return "rejected:subject"
    return f"accepted:{claims['sub']}"

base = {
    "typ": "at+jwt", "iss": "https://issuer.example/",
    "aud": ["orders-api"], "exp": 2000, "sub": "user-7",
}
cases = {
    "valid": base,
    "wrong_type": {**base, "typ": "id+jwt"},
    "wrong_audience": {**base, "aud": ["inventory-api"]},
    "expired": {**base, "exp": 1000},
    "missing_subject": {**base, "sub": ""},
}
for name, claims in cases.items():
    print(f"{name}={context(claims, now=1000)}")
```

The `valid` result establishes only that selected claims passed this toy policy. A real validator must verify cryptographic integrity or introspection, algorithm, key, sender binding, all required profile claims, and operational trust.

### Test the trust chain

Test malformed, oversized, unsigned, wrong-algorithm, wrong-key, wrong-issuer, wrong-audience, expired, future, wrong-type, and missing-claim credentials. Include key rotation, unknown `kid` floods, metadata outage, revocation, introspection timeout, sender-proof replay, and clock boundaries.

Test identity separation: client credentials do not become users; body tenant cannot override context; service identity remains alongside delegated user; impersonation retains original actor; downstream context narrows audience and privilege; trace headers cannot assert identity.

Integration tests must include the actual gateway, TLS/workload identity, header stripping, token broker, resource server library, cache, and key metadata configuration. A unit test of claim mapping cannot detect a gateway forwarding spoofable `X-User` headers.

Property tests can assert no accepted context has an untrusted issuer, missing current audience, expired evidence, unknown token type, or privilege wider than its parent. Operational drills verify rotation, compromised issuer response, audit search, and secret redaction.

## Definitions and Notation

Credential validation $V_P(k,R,t)$ is partial and yields context $C$ only under policy $P$, recipient $R$, and time $t$. Principal key $p=(iss,sub)$ prevents subjects from different issuers being conflated.

Let context be:

$$
C=(p,c,w,a,\tau,q,d,\pi),
$$

with principal $p$, client $c$, workload $w$, validated audience $a$, time interval $\tau$, assurance $q$, delegation chain $d$, and bounded asserted privileges $\pi$.

Derivation $g_R(C)$ for downstream recipient $R$ must preserve provenance, set audience to $R$, minimize disclosed claims, and satisfy effective privilege monotonicity $\Pi(g_R(C))\subseteq\Pi(C)$. This is a design invariant; exact comparison requires a policy-aware mapping across audience vocabularies.

An **identity assertion** is authenticated evidence from an issuer, not a final authorization decision. **Ambient credential** is a secret automatically available beyond the code that needs it. **Confused deputy** occurs when a service uses its authority for a requester without correctly binding the requester's permitted intent. **Credential provenance** records issuer, profile, validation mechanism, and derivation without retaining the reusable secret.

## Mechanisms, Invariants, or Proof Structure

1. Enumerate subject, client, workload, tenant, actor, and delegation roles.
2. Parse credentials as untrusted bounded input.
3. Select one mutually exclusive credential profile.
4. Verify issuer/key, algorithm, integrity or introspection, audience, time, type, and sender binding.
5. Map only understood claims into immutable typed context with provenance.
6. Keep authentication evidence separate from authorization decisions.
7. Derive or exchange a short-lived least-privilege downstream credential for each audience.
8. Authenticate the immediate workload and preserve delegated/effective actors explicitly.
9. Store minimum non-secret provenance for asynchronous work and audit.
10. Test every hop, failure, rotation, redaction, and privilege-narrowing invariant.

The trust claim is conjunctive: cryptographic validity alone is insufficient. Context exists only if every required profile and deployment predicate passes. Propagated evidence is trustworthy only to the extent that the receiver verifies its issuer, recipient binding, freshness, sender, and derivation policy.

## Alternatives and Trade-Offs

Self-contained tokens enable local low-latency validation but carry claims until expiry and complicate immediate revocation. Opaque tokens centralize current status and minimize disclosure but add an introspection dependency and cache consistency. Risk and latency determine the choice.

Forwarding the original token preserves end-user evidence and is simple, but broadens audience, exposure, and privacy. Token exchange adds broker dependency and operational work while narrowing each hop. Use original forwarding only when the original audience and threat model genuinely include every recipient.

Gateway authentication centralizes external protocol complexity. Service validation preserves independent trust boundaries and resists bypass. A gateway-signed assertion can combine them if services authenticate the gateway, validate recipient and lifetime, strip external headers, and retain workload identity.

Rich tokens reduce directory calls but spread personal, group, and entitlement data and become stale. Minimal tokens improve privacy and force current policy lookups. Include only claims with clear audience-specific use.

Snapshotting authority into a durable job yields predictable execution but can outlive access removal. Re-evaluation reflects current policy but can invalidate accepted work. State which semantics users and operators can rely on.

Failing closed on identity dependency outages protects trust but reduces availability. Valid cached keys or introspection results can improve resilience within explicit expiry and revocation bounds. Unverified fallback is never equivalent.

## Failure Modes and Misconceptions

- **“JWT decoding authenticates the caller.”** Only full profile and cryptographic validation can establish evidence.
- **“A valid signature is enough.”** Type, issuer, audience, time, sender, claims, and policy also matter.
- **“An ID token identifies the user to any API.”** It targets an OpenID relying party and must not substitute for an API access token.
- **“Subject means human user.”** Client-credential and workload profiles may represent applications.
- **“`client_id` is the actor.”** Client, resource owner, effective subject, and workload are distinct.
- **“Tenant in the request is trusted context.”** It is an untrusted target until bound by verified evidence and policy.
- **“The gateway authenticated it, so headers are safe.”** Services need an authenticated, recipient-bound trust path and ingress stripping.
- **“Internal networks are trusted.”** Network location neither proves workload identity nor delegated user authority.
- **“Forward the token everywhere.”** This expands bearer exposure and may violate audience and privacy constraints.
- **“Scopes are global permissions.”** Their meaning is issuer-, resource-, and policy-specific.
- **“Tracing propagates identity.”** Trace context supports correlation, not authentication.
- **“Impersonation replaces the original actor.”** Both original and effective actors must remain visible and auditable.
- **“A signed token cannot be revoked.”** Signature validity and current acceptability are different claims.
- **“Store the inbound token with the job.”** Durable work should carry minimum provenance or obtain new bounded credentials.
- **“Key fetch failure permits cached claims forever.”** Cache use is bounded; failed verification never degrades to trust.

## Worked Examples

### Example 1

**Situation:** API accepts a JWT after Base64 decoding and reads `sub=admin`. **Reasoning:** No integrity, issuer, audience, type, or time check occurred. Apply a configured access-token profile and reject before constructing context. **Conclusion:** parsed claims are untrusted data.

### Example 2

**Situation:** An ID token issued to a web client is sent to `orders-api`. **Reasoning:** Its audience and purpose are the relying client, not the resource API. Require an access token with mutually exclusive type and orders audience. **Conclusion:** token-kind substitution must fail even when issuer and subject are familiar.

### Example 3

**Situation:** Client-credentials token has `sub=reporting-worker` and code treats it as customer user. **Reasoning:** Model subject kind and client/workload identity explicitly; no resource-owner user exists. **Conclusion:** subject interpretation depends on credential profile and grant context.

### Example 4

**Situation:** Gateway adds `X-User: u-7`, but external callers can also send it. **Reasoning:** Strip external identity headers, authenticate gateway workload, sign a recipient-bound short-lived assertion, and validate it downstream. **Conclusion:** a header name does not create a trust boundary.

### Example 5

**Situation:** Orders service forwards an `orders-api` bearer token to inventory. **Reasoning:** Inventory is not the audience and receives unnecessary claims. Exchange it for an `inventory-api` token with reduced scope and preserve delegation provenance. **Conclusion:** token exchange narrows applicability per hop.

### Example 6

**Situation:** Support agent impersonates a buyer, and audit records only buyer ID. **Reasoning:** Preserve agent actor, effective buyer, mode, reason/ticket, approval, start, and expiry; authorization applies impersonation policy. **Conclusion:** effective identity must not erase accountability.

### Example 7

**Situation:** Token says tenant `t-1` while path targets `t-2`. **Reasoning:** Treat path as requested resource scope and verified claim as context; never overwrite either. Authorization denies or conceals the mismatch and records safe evidence. **Conclusion:** conflicting identity sources require explicit rejection policy.

### Example 8

**Situation:** Unknown `kid` causes a metadata fetch for every request. **Reasoning:** Attackers can create outbound and CPU load. Fetch only trusted issuer metadata under single-flight, rate limits, cache, and negative handling; reject if no trusted key exists. **Conclusion:** key rotation paths require abuse resistance.

### Example 9

**Situation:** A queued refund runs tomorrow using today's stored bearer token. **Reasoning:** Authorize creation, store non-secret actor and decision provenance, then let the worker use workload identity and current delegated authority or an explicit snapshot policy. **Conclusion:** durable work must not depend on replaying ambient credentials.

### Example 10

**Situation:** DPoP-bound token is verified at gateway, then forwarded as bearer internally. **Reasoning:** The original sender binding no longer protects the internal hop. Exchange for a service-bound token or create a new authenticated internal assertion bound to receiver and caller workload. **Conclusion:** propagation must preserve or deliberately terminate security properties.

## Cross-Program Connections

[Security Engineering](../../25-security-engineering/ROADMAP.md) owns cryptography, identity protocols, credential lifecycle, threat modeling, and authorization foundations. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies hop, failure, time, and asynchronous-work reasoning. [Network Engineering](../../24-network-engineering/ROADMAP.md) supplies TLS, proxies, and connection identity. [Platform Engineering](../../29-platform-engineering/ROADMAP.md) can provide workload identity and token brokers. This API module owns binding verified evidence to service request and downstream call semantics.

## References

1. T. Lodderstedt, J. Bradley, A. Labunets, and D. Fett, [*RFC 9700: Best Current Practice for OAuth 2.0 Security*](https://www.rfc-editor.org/rfc/rfc9700.html), BCP 240, January 2025. Checked 2026-09-01.
2. V. Bertocci, [*RFC 9068: JSON Web Token (JWT) Profile for OAuth 2.0 Access Tokens*](https://www.rfc-editor.org/rfc/rfc9068.html), October 2021. Checked 2026-09-01.
3. Y. Sheffer, D. Hardt, and M. Jones, [*RFC 8725: JSON Web Token Best Current Practices*](https://www.rfc-editor.org/rfc/rfc8725.html), BCP 225, February 2020. Checked 2026-09-01.
4. M. Jones and D. Hardt, [*RFC 7519: JSON Web Token (JWT)*](https://www.rfc-editor.org/rfc/rfc7519.html), May 2015. Checked 2026-09-01.
5. N. Sakimura et al., [*OpenID Connect Core 1.0 incorporating errata set 2*](https://openid.net/specs/openid-connect-core-1_0.html), OpenID Foundation, 15 December 2023. Checked 2026-09-01.
6. M. Jones et al., [*RFC 8693: OAuth 2.0 Token Exchange*](https://www.rfc-editor.org/rfc/rfc8693.html), January 2020; and D. Fett et al., [*RFC 9449: OAuth 2.0 Demonstrating Proof of Possession*](https://www.rfc-editor.org/rfc/rfc9449.html), September 2023. Checked 2026-09-01.

## Exercises

### Exercise 1

For a request involving a buyer, mobile OAuth client, edge gateway, and orders service, identify subject, client, workload, audience, tenant, effective actor, and credential provenance.

### Exercise 2

Trace validation of a JWT access token through parsing, profile selection, algorithm/key, issuer, audience, time, sender binding, claim mapping, and context construction. State what each step proves.

### Exercise 3

Diagnose a call chain that forwards one bearer token, accepts `X-User`, overwrites tenant from the body, stores tokens in jobs, and logs all claims. Propose the smallest coherent repair.

### Exercise 4

Compare original-token forwarding, token exchange, gateway-signed assertions, and workload-only calls for a three-service workflow with privacy-sensitive user claims.

### Exercise 5

Design authentication-context propagation for an administrator approving a delayed operation on behalf of a customer, including impersonation, asynchronous execution, revocation, audit, and downstream audience restrictions.

## Answers to the Exercises

### Answer 1

The buyer is the resource-owner subject and usually effective actor. The mobile application is `client_id`; it is not the buyer. Edge and orders are successive workload identities. The access token audience must include orders, not merely the client or edge. Tenant is a separately verified or resource-bound context, not inferred from a body alone. Credential provenance records issuer, access-token profile, validation method, time, and sender binding. If edge creates an internal assertion, its workload becomes immediate issuer/caller while buyer and client provenance remain explicit.

### Answer 2

Bounded parsing proves only syntactic structure. Profile selection prevents using an ID or other JWT kind. Algorithm configuration and issuer-bound key verification establish integrity from a trusted issuer under an accepted mechanism. Issuer comparison identifies the trust domain; audience proves intended resource; time checks bound freshness; sender proof binds presentation to a key or certificate. Required-claim validation establishes profile structure. Allowlisted mapping creates typed evidence but grants no resource permission. Only when all required predicates pass is immutable context constructed; authorization remains separate.

### Answer 3

Strip external identity headers and authenticate each workload hop. Validate the inbound token for its recipient, then exchange it for audience-specific short-lived downstream tokens or signed recipient-bound assertions rather than forwarding broadly. Keep verified tenant separate and compare requested tenant during authorization. At enqueue, store minimum principal/client/tenant/delegation and decision provenance, not the bearer token; worker obtains current bounded authority. Redact tokens and sensitive claims, log only approved identifiers and outcome. These changes establish one typed context and remove ambient credential spread.

### Answer 4

Original forwarding is simplest but requires every service in the audience, exposes all claims, and expands bearer replay risk. Token exchange adds broker dependence but minimizes audience, scope, lifetime, and disclosed claims per service while preserving delegation. A gateway-signed assertion is efficient internally only with authenticated workload transport, external-header stripping, receiver binding, short expiry, replay resistance, and careful claim minimization. Workload-only calls best fit operations that need no user authority; using them for user-governed actions risks a confused deputy. For privacy-sensitive claims, prefer exchange or minimal assertions and keep workload identity alongside delegation.

### Answer 5

At acceptance, authenticate administrator, validate assurance, and authorize impersonation under explicit customer, operation, reason, approval, and duration. Store original administrator, effective customer, mode, tenant, requested action, decision/policy reference, request identity, expiry, and cancellation status—never the bearer token. The worker authenticates as its workload and re-evaluates current administrative/delegated authority or follows a documented snapshot rule. It obtains a short-lived token for each downstream audience with only required capability and actor chain. Revocation or approval withdrawal cancels pending work under policy. Audit records both actors, every exchange, outcome, and artifact identity with protected retention.

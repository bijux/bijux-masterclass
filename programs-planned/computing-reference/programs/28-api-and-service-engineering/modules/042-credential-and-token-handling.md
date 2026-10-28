---
module_id: API-042
program: API & Service Engineering
level: 1
module_number: 42
title: Credential and Token Handling
status: complete
last_verified: 2026-09-01
---

# Credential and Token Handling

## One-Page Review

### Governing question

How should an API issue, deliver, store, transmit, validate, scope, rotate, revoke, observe, and destroy credentials and tokens so that compromise is difficult, bounded, detectable, and recoverable?

### Essential definitions

- A **credential** is secret or cryptographic evidence used to authenticate an actor or client.
- A **token** is an issued artifact carrying or referencing authority, identity, session, or protocol state for a defined audience and use.
- A **bearer token** can be used by any party that possesses it; possession is the proof.
- A **sender-constrained token** is accepted only when the presenter also proves possession of a bound key.
- An **access token** authorizes a client to call a protected resource within its audience, scope, subject, and lifetime.
- A **refresh token** is presented to an authorization server to obtain new access tokens; it is not an API access token.
- An **opaque token** is a reference whose security attributes are resolved by the issuer/resource server; a **self-contained token** carries signed or protected claims.
- **Rotation** introduces replacement credential material and retires old material through a controlled overlap; **revocation** invalidates authority before natural expiry.

### Central model, mechanism, or theorem

Credential safety is a lifecycle property:

$$
L=(G,I,D,S,T,V,U,R,X,E),
$$

where $G$ is secure generation, $I$ issuance/binding, $D$ delivery, $S$ storage, $T$ transport, $V$ validation, $U$ use/authorization, $R$ rotation/revocation, $X$ expiry/destruction, and $E$ evidence/response. For a signed access token $z$, acceptance by resource server $r$ at time $t$ requires every configured predicate:

$$
\operatorname{accept}(z,r,t)=\bigwedge\{\text{format/type},\text{algorithm/key},\text{issuer},\text{audience},\text{time},\text{sender},\text{token state}\}.
$$

Acceptance establishes token validity for the resource server; it does not by itself authorize the requested object or action.

### Critical invariants

Secrets use cryptographic randomness and are never human-chosen identifiers. Authority is least-privileged by audience, subject/client, permissions, tenant, resource, purpose, and lifetime. Credentials never travel in URLs or ordinary logs. Transport authenticates the intended peer end to end. Token kind and validation rules are explicit and mutually exclusive. Algorithms are server-configured, not selected by untrusted token input. Issuer, audience, time, and sender binding are verified, not merely decoded. Refresh tokens stay at the authorization boundary. Access-token claims become authenticated context, then object/action authorization still runs. Rotation supports a bounded overlap and observable retirement. Revocation expectations match token architecture and incident response. Every copy, cache, proxy, trace, support tool, backup, and client store is part of the threat surface.

### Common failures

Using API keys as usernames; putting tokens in query strings; storing raw keys in databases or tickets; logging `Authorization`; accepting any key found at an attacker-selected JWKS URL; allowing `alg=none` or algorithm confusion; verifying signature but not issuer/audience/type/time; accepting ID or refresh tokens at an API; issuing one broad non-expiring credential; embedding mutable authorization forever in long-lived JWTs; rotating without proving old-key retirement; confusing logout with access-token revocation; returning different token-validation diagnostics to attackers; sharing secrets across environments; and assuming TLS repairs insecure endpoints, clients, logs, or dependencies.

### Compact example

An orders API receives `Authorization: Bearer ey...`. It selects the access-token validation profile before parsing claims, accepts only configured algorithms, resolves a cached key from the configured issuer, verifies the signature, exact issuer, orders-API audience, `typ`, expiry/not-before with bounded skew, and required sender proof, then constructs immutable context. It still checks `order.cancel` on the target order. Logs contain only a keyed token identifier hash and outcome class. **Conclusion:** decoding a token is data processing; validation plus contextual authorization is the security boundary.

### Connections

[API Threat Modeling](041-api-threat-modeling.md) identifies credential attack paths, while [Authentication Context Propagation](033-authentication-context-propagation.md) uses the verified result and [Authorization Checks](034-authorization-checks.md) makes object/action decisions. [OAuth Authorization Flows](../ROADMAP.md) next selects safe ways to acquire tokens; [Applying OpenID Connect at API Boundaries](../ROADMAP.md) separates authentication identity from API authorization.

## Governing Question

For each credential and token class, who may obtain it, where may it exist, what exact authority does it carry, how is it verified at each boundary, how quickly can compromise be contained, and what evidence proves correct handling?

## Why This Matters

Credentials collapse complex policy into small high-value artifacts. A bearer access token copied from a log can be replayed without the user's password. A service API key committed to a repository can survive for years and cross environments. A correctly signed JWT intended for another audience can become privilege if an API checks only the signature. A refresh token accepted at a resource server converts long-lived renewal authority into direct API access.

Token handling crosses organizational boundaries: issuer, client, browser or device, gateway, resource service, identity libraries, key-distribution endpoints, caches, logs, tracing, support systems, backups, and incident tooling. The security of the design is limited by the weakest uncontrolled copy and validation path. A strong signature cannot erase a token recorded in analytics; TLS cannot protect a compromised client store; a short lifetime does not help if refresh authority is equally exposed.

Handling must therefore be designed as a lifecycle, not as one middleware call. Generation and issuance determine entropy and authority. Delivery and storage determine exposure. Transport and validation determine whether attackers can redirect or substitute artifacts. Rotation, revocation, expiry, and incident response determine compromise duration. Evidence determines whether the team can detect drift and prove retirement.

This module focuses on handling artifacts once a credential/token architecture is chosen. It does not choose OAuth grants in detail—that is the next module—and does not treat a valid token as sufficient authorization. It builds the boundary discipline on which both depend.

## Prerequisites and Retrieval

Retrieve cryptographic randomness, entropy, hashing/keyed hashing, symmetric and asymmetric keys, TLS peer authentication, bearer capability, OAuth roles and token classes, JWT/JWS basics, issuer and audience, scopes/permissions, expiry and clock skew, key identifiers and JWKS, secrets management, operating-system/browser storage, rotation, revocation, token introspection, mutual TLS, proof of possession, logging/redaction, incident response, and object-level authorization.

Before approving a token design, retrieve issuer and resource owners, client types and compromise model, credential classes, issuance/enrollment, entropy/key generation, exact audiences and token types, subject/client/tenant semantics, permission model, maximum lifetimes, renewal rules, sender constraint, algorithms and key sources, transport path/TLS termination, client/server storage, caches and replicas, gateway forwarding, logging/tracing/analytics, introspection/revocation behavior, rotation cadence and overlap, clock assumptions, environment separation, emergency containment, recovery and re-enrollment, inventory, and verification/monitoring.

## Learning Objectives

By the end of this module, you should be able to:

1. distinguish passwords, API keys, client credentials, access/refresh tokens, and sender-constrained tokens;
2. minimize authority and exposure across generation, issuance, delivery, storage, transport, and use;
3. define an explicit validation profile for opaque and self-contained access tokens;
4. prevent token substitution, key confusion, replay, leakage, and cross-environment use;
5. design bounded rotation, revocation, expiry, and compromise response;
6. construct safe telemetry and inventory for credential operations; and
7. verify lifecycle behavior through negative, rotation, replay, failure, and incident tests.

## Core Exposition

### Classify the artifact before handling it

Use names that express semantics rather than calling every secret a “token.” Common classes differ:

- **User password/passphrase:** authenticates a human to an authentication service; it should not be forwarded to ordinary resource APIs.
- **API key:** usually a high-entropy issuer-created secret identifying/authenticating a calling project or client. It may support metering, but possession alone often carries authority and lacks user context.
- **Client secret:** authenticates a confidential client to an authorization server or other endpoint; it is not an access token and cannot remain secret in public clients.
- **Private key/workload credential:** proves control of asymmetric key material, often through mTLS or signed assertions; the private key should remain non-exportable where possible.
- **Access token:** presented to a resource server for bounded API authority.
- **Refresh token:** presented only to the authorization server to renew access; usually longer-lived and higher-value.
- **ID token:** conveys an authentication event to an OpenID Connect client; it is not an access token for an arbitrary API.
- **Session cookie:** browser session evidence with cookie-specific origin, CSRF, and storage properties; it is not automatically interchangeable with an API bearer token.
- **One-time code/link:** narrowly scoped recovery, enrollment, or confirmation authority whose consumption and expiry need atomicity.

Record issuer, holder, presenter, verifier, audience, authority, secret/public status, lifetime, storage, transport, rotation, revocation, and owner for each class. Do not let the same bytes serve multiple token kinds or environments. RFC 8725 recommends explicit typing and mutually exclusive validation rules for different JWT kinds because otherwise a token valid in one context can be substituted in another.

An API key sometimes identifies only a project for quota while user authentication supplies actual authority. State that explicitly. If the key authenticates a service, generate sufficient entropy, store only a verifier/keyed digest where protocol permits, scope it, and treat it as a bearer secret—not a public identifier.

### Minimize authority at issuance

Every credential should answer: authority for whom, through which client, to which resource server, for which tenant/resources/actions, until when, and under what sender proof? Reject “all APIs forever” as a default.

Access tokens use an audience naming the intended resource server or resource set. The resource server compares against configured acceptable audiences; it does not accept a token merely because `aud` exists. Permissions/scopes express coarse delegated capability, but the API still combines them with subject, tenant, resource, action, state, and policy. Avoid packing a complete mutable authorization database into a long-lived token.

Make lifetimes proportional to exposure and recovery. A short access-token lifetime limits bearer compromise, but too-short lifetimes can create availability load and encourage unsafe caching. Long-lived refresh tokens need stronger client storage, rotation/replay detection or sender constraint where applicable, revocation, and user/admin visibility. Machine credentials should prefer renewable short-lived workload identity over copied static secrets when infrastructure supports it.

Separate production, staging, development, test, tenant, region, and workload authority. A non-production issuer or key must not mint artifacts accepted in production. Do not reuse symmetric secrets across consumers: every verifier that knows a MAC key may be able to mint tokens. Asymmetric signatures let resource servers verify without receiving issuer private keys.

Issuance is a privileged event. Authenticate/enroll the recipient, bind client and redirect/endpoint metadata, apply approval and least privilege, record safe credential identity, deliver once through a protected channel, and require confirmation when appropriate. Never send a new long-lived secret through ordinary email, chat, or ticket text.

### Generate and represent secrets safely

Use a cryptographically secure random generator and enough entropy for online/offline attack model and lifetime. Human-readable prefixes may identify credential type/environment for inventory, but the secret portion remains random. Avoid sequential IDs, UUID variants not intended as secrets, timestamps, names, or shared default values.

Store an API-key verifier rather than plaintext when the protocol needs only equality verification. A slow password hash is appropriate for human passwords; a high-entropy API key can use a cryptographic keyed hash with a separately protected server key to resist database-only compromise and support indexed lookup through a non-secret prefix. Design lookup, collision, rotation, and key-encryption-key change deliberately.

Private keys should be generated and used in hardware-backed or non-exportable OS/cloud keystores where feasible. Restrict signing/decryption operations by identity and purpose; audit them; back up only under explicit recovery policy. Copying a private key into environment variables on hundreds of hosts expands the compromise surface.

JWTs are encodings, not secrecy. JWS-signed claims are normally readable by any holder. Do not put passwords, private keys, unnecessary personal data, or internal policy details in them. Encryption adds key and composition complexity and still does not justify excessive claims. Minimize data and lifetime.

### Deliver without creating uncontrolled copies

Prefer protocol-defined secure channels and one-time retrieval for issued secrets. Authenticate both destination and operator/client enrollment. Display a static key once; afterward show only safe prefix, creation/use metadata, owner, scope, and status. Recovery means rotate/re-enroll, not reveal stored plaintext.

Avoid credentials in URLs. Query strings enter browser history, referrers, proxy/access logs, caches, analytics, screenshots, and support transcripts. RFC 6750 defines the `Authorization: Bearer` request header as the normal bearer-token method and warns about token protection. Do not place tokens in path parameters or response redirects.

Treat deep links, QR codes, copy/paste, shell history, process listings, CI output, and command examples as delivery channels. CLI tools accept tokens from protected files, OS credential stores, or standard input rather than command-line arguments when process inspection/history can expose them. Documentation uses unmistakably invalid examples.

When a gateway forwards identity, prefer a newly protected internal context or validated original token according to architecture. Strip public copies of trusted internal headers. Authenticate the gateway-to-service hop and define which component revalidates what. A network route alone does not authenticate forwarded claims.

### Store according to client and attacker model

There is no universal safe storage location independent of platform. Ask which code can read it, which attacks can execute there, whether it survives restart, whether it syncs/backups, how it is erased, and whether sender constraint or re-authentication limits theft.

Server workloads use a managed secret/identity system with workload authentication, least-privilege access, audit, rotation, and memory/process isolation. Prefer short-lived injected identity over static secrets in source, images, repository variables, shared configuration, or baked artifacts. Environment variables can be convenient but may appear in dumps, diagnostics, child processes, or orchestration views; assess the platform rather than declaring them inherently safe.

Native clients use platform secure storage and hardware-backed keys where available, but a compromised device/process may still access tokens during use. Public clients cannot keep a distributed client secret. Browser JavaScript storage is exposed to successful script injection; architectures such as a backend-for-frontend can keep tokens server-side and give the browser a hardened session cookie, with CSRF and origin protections. The right choice follows the web threat model and current OAuth browser guidance.

Keep refresh tokens in a smaller, stronger boundary than access tokens. Resource APIs should never receive them. Cache access tokens only for their required lifetime; encrypt/protect caches, isolate tenants/users, and wipe on logout/revocation according to semantics. Crash dumps, swap, backups, observability agents, and support snapshots count as storage.

### Protect transport and endpoints

Use end-to-end TLS to the intended resource server with current transport guidance and correct hostname/peer verification. If TLS terminates at an edge, protect and authenticate every subsequent hop that carries credentials or authoritative context. Do not silently downgrade to plaintext inside a cluster.

Reject tokens over insecure origins. Constrain redirects and outbound calls so authorization headers are not forwarded to a different host. HTTP client libraries may automatically follow redirects; configure whether sensitive headers survive and test cross-origin redirects. Proxies and service meshes must not mirror credential-bearing traffic to untrusted destinations.

Bearer tokens are replayable by design. For higher-risk or exposed paths, RFC 9700 recommends sender-constraining access tokens using mechanisms such as mutual TLS (RFC 8705) or DPoP (RFC 9449). Sender constraint requires the resource server to verify the binding and proof, including method/target/time/nonce/replay rules applicable to the mechanism. It reduces value of token theft but does not repair a compromised authorized client that can use its key.

Do not invent request signing casually. Canonicalization, body streaming, proxies, replay windows, clock/nonce state, key discovery, rotation, and error behavior are protocol design. Use reviewed standards suited to the deployment; [Replay and Request Signing](../ROADMAP.md) treats this explicitly.

### Select a validation profile before parsing claims

The resource server configuration determines acceptable token kinds, issuers, algorithms, key sources, audiences, time policy, sender constraint, and required claims. Untrusted token headers and claims do not choose the security policy.

For a JWT access token profile:

1. enforce bounded token/header/claim size, segment/encoding syntax, and expected explicit type;
2. accept only a server-configured algorithm set and bind each key to its intended algorithm/use;
3. resolve `kid` only within a configured issuer/key set—never fetch an arbitrary header URL;
4. verify the cryptographic operation before trusting claims;
5. compare exact configured issuer and ensure the key belongs to it;
6. require the API's configured audience under defined single/multiple-audience rules;
7. validate expiry and not-before/issued-at policy with small documented clock skew and maximum lifetime;
8. validate subject/client/tenant claim types and required relationships for this profile;
9. verify token status and sender binding where the architecture requires them; and
10. construct a minimal immutable context, then perform requested object/action authorization.

Do not decode, inspect `scope`, choose a tenant, or log a subject as trusted before verification. It can be reasonable to read an untrusted issuer/key identifier for routing, but use it only as bounded input to a configured allowlist. Avoid network fetch on every request; cache issuer metadata/keys with bounded freshness and safe refresh. Key refresh failures need a policy that neither trusts arbitrary stale authority forever nor causes uncontrolled outage.

RFC 8725 requires algorithm verification, appropriate algorithms, issuer/subject and audience validation, explicit typing, and mutually exclusive rules. Signature validation alone is incomplete. Reject `none`, algorithm/key-type confusion, missing required claims, duplicate/ambiguous JSON interpretations, and tokens from the right issuer but wrong use.

For opaque access tokens, local syntax reveals no authority. Resolve them through an issuer-owned store or introspection interface over authenticated protected transport, verify that the response is active and intended for this resource/client/use, and cache no longer than safe revocation/lifetime rules. Introspection availability and cache staleness are part of the API availability/security model.

### Keep errors safe and clients interoperable

Return authentication failures using the applicable HTTP authentication scheme and stable public categories such as invalid/expired token or insufficient scope only where disclosure is safe and specified. Do not distinguish signature byte mismatch, unknown subject, revoked credential, or internal key-store outage with attacker-useful detail. Keep diagnostic specificity in protected logs.

Separate `401` (valid authentication credentials absent/invalid for the resource) from `403` (authenticated context lacks permission under the API's concealment policy). A valid token with wrong object authority is not fixed by refreshing it. An expired token may be renewed by the client according to its authorization protocol; the resource server does not accept a refresh token in its place.

Challenge fields and error bodies must not echo tokens. Avoid reflecting untrusted issuer, key ID, or claims without encoding and redaction. Bound token-parsing work and authentication-failure rates so invalid-token floods cannot exhaust cryptography/key retrieval or flood logs.

### Authorize after token validation

A validated token says that an accepted issuer made a cryptographically protected statement for this resource under a particular profile. The API must interpret that statement within local policy.

Bind token tenant/organization claims to path/resource scope. Combine token permissions with client identity, effective user, delegation, object ownership, relationship, state, environment, and risk controls. Do not treat a broad scope like `orders:write` as permission to mutate every order. Do not accept caller body fields that contradict authoritative context.

Claims become stale. Role removal, account suspension, tenant exit, and emergency revocation may need effect before a long-lived self-contained token expires. Options include short lifetimes, introspection/reference tokens, policy-version checks, revocation/deny lists for critical events, or narrower action tokens. Each adds availability, state, and privacy trade-offs. State the maximum authorization-staleness bound.

Record actor and client separately. A service acting for a user is not only the service or only the user. Delegation/audit should preserve issuer, subject/effective subject, client, tenant, token/session safe identifier, and assurance without logging raw credentials.

### Design rotation as a bounded state machine

Rotation is not “create a second key.” Define states: prepared, distributed/published, active for issuance, accepted for verification, retired from issuance, rejected, destroyed. Asymmetric signing rotation normally publishes the new public key before signing with it, waits for verifier refresh, switches issuance, permits old-token verification only through their bounded lifetime, then removes the old key. Emergency compromise can shorten this sequence and trade availability for containment.

For static API keys/client secrets, support two credential slots or an equivalent overlapping scheme: issue replacement, update callers, observe new use, stop issuing/using old, revoke old by deadline, verify no old use, then destroy it. Never leave both active indefinitely. Inventory owner, last use, scope, creation, expiry, and rotation state without retaining raw secrets.

Key identifiers aid selection but are not trust anchors. Prevent collisions across issuers/environments and bound lookup. A missing/unknown `kid` does not justify trying every untrusted algorithm/key without limits. Protect issuer signing keys more strongly than public verification keys and separate algorithms/purposes.

Test rotation under cached metadata, clock skew, partial rollout, regional partition, rollback, old clients, and issuer/key-service outage. Deployment must not depend on perfectly synchronized cache invalidation.

### Define revocation and expiry honestly

Expiry is local time-bounded invalidation; revocation is a state decision before expiry. Self-contained access tokens can remain valid at offline resource servers until expiry unless the API consults state or distributes revocation. Do not promise immediate revocation without a mechanism and tested latency.

Logout usually ends a client/browser session and may revoke refresh authority, but already issued access tokens may live until expiry. Document user/admin expectations. Credential compromise response may require revoking sessions, refresh tokens, API keys, client credentials, signing keys, and downstream derived credentials separately.

Refresh-token rotation can detect replay when an old token is reused and revoke the active family, under the selected OAuth profile. Sender constraint can further reduce theft. Those mechanisms require atomic state, client recovery rules, race handling, and monitoring.

Clock skew should be small, justified, and symmetric only where semantics require it. Large leeway silently extends token life and permits early use. Monitor clock health; use trusted time; test exact `exp`/`nbf` boundaries. After expiry/revocation, remove cached context and securely delete stored artifacts according to platform limits and retention law.

### Prevent leakage through observability and operations

Redact `Authorization`, cookies, API-key headers, token/code query fields, signed URLs, private keys, and secrets at the earliest collection point. Configure proxies, frameworks, APM, traces, exception reporters, packet capture, analytics, WAF samples, support bundles, and CI. Redaction at a dashboard after raw ingestion is too late.

Use a non-reversible safe identifier for correlation, such as a keyed digest of a stable token ID under a separate protected observability key, with rotation and access policy. Do not hash a low-entropy API key without a secret and assume safety. Metric labels use bounded issuer/client/outcome classes, never raw subjects, token IDs, or keys.

Detect unusual issuance, failed validation by bounded reason, expired/revoked use, sender-binding mismatch, token reuse from incompatible contexts, old credential use after migration, key fetch/rotation failure, high-privilege scope issuance, and credentials nearing expiry without owner. Signals need privacy review, response owner, and runbook.

Support tooling displays prefix/status/owner and performs revocation/rotation through approved workflows. Operators should not request customers paste tokens into tickets. Emergency “break glass” credentials are narrow, short-lived, strongly approved, isolated, audited, exercised, and revoked—not a shared permanent master key.

### Respond to compromise by artifact class

Prepare before leakage. Inventory affected credential, issuer, holders, resource audiences, authority, derived tokens, logs/stores where copied, last use, and rotation/revocation mechanisms. Classify whether only a public identifier, bearer secret, refresh authority, private key, or issuer signing key was exposed.

Contain in a dependency-aware order. Revoke/disable the artifact and derived sessions where feasible, block malicious use, rotate replacement through a separate trusted channel, prevent automatic reissuance from compromised refresh/client authority, and protect service availability. Signing-key compromise may require rejecting many tokens and publishing new metadata; preserving old acceptance can preserve attacker authority.

Search telemetry using safe identifiers, not by copying secrets. Determine exposure window, resources/actions accessed, persistence established, and downstream credentials minted. Notify owners and affected parties under policy. Recover by re-enrollment, least-privilege reissue, state repair, control verification, and removal of leaked copies where possible. Feed root cause into threat model, storage/delivery design, scanners, tests, and incident exercises.

The executable validator below models configured claim predicates and sender binding after cryptographic verification. It does not perform cryptography, parse JWTs, validate OAuth flows, or prove production security.

<!-- bijux-verify: {"id":"access-token-acceptance-profile","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"valid=accept\nwrong_audience=reject:audience\nexpired=reject:time\nwrong_algorithm=reject:algorithm\nunbound=reject:sender\n","stderr":""}} -->
```python
PROFILE = {
    "issuer": "https://issuer.example",
    "audience": "orders-api",
    "algorithms": {"ES256"},
    "type": "at+jwt",
    "require_sender": True,
}

def validate(claims, header, now, proof_thumbprint):
    if header.get("typ") != PROFILE["type"]:
        return "reject:type"
    if header.get("alg") not in PROFILE["algorithms"]:
        return "reject:algorithm"
    if claims.get("iss") != PROFILE["issuer"]:
        return "reject:issuer"
    if PROFILE["audience"] not in claims.get("aud", []):
        return "reject:audience"
    if not (claims.get("nbf", now) <= now < claims.get("exp", 0)):
        return "reject:time"
    if PROFILE["require_sender"] and claims.get("cnf") != proof_thumbprint:
        return "reject:sender"
    return "accept"

base_claims = {
    "iss": "https://issuer.example",
    "aud": ["orders-api"],
    "nbf": 900,
    "exp": 1100,
    "cnf": "key-thumbprint-7",
}
base_header = {"typ": "at+jwt", "alg": "ES256"}

print("valid=" + validate(base_claims, base_header, 1000, "key-thumbprint-7"))
print("wrong_audience=" + validate({**base_claims, "aud": ["billing-api"]}, base_header, 1000, "key-thumbprint-7"))
print("expired=" + validate(base_claims, base_header, 1100, "key-thumbprint-7"))
print("wrong_algorithm=" + validate(base_claims, {**base_header, "alg": "none"}, 1000, "key-thumbprint-7"))
print("unbound=" + validate(base_claims, base_header, 1000, "different-key"))
```

The model assumes signature verification succeeded with a configured issuer key; real code must perform that step before claims are trusted and must use maintained security libraries rather than handwritten token parsing.

### Verify the complete lifecycle

Build a credential matrix from issuance to destruction. Test entropy/format without exposing generated secrets; unauthorized issuance; wrong owner/scope/environment; delivery replay; storage permissions; accidental repository/image/log inclusion; URL/header/referrer/redirect leakage; plaintext hops; and client compromise assumptions.

For validation, test malformed/oversized encodings, wrong type, disallowed/`none` algorithm, wrong key/issuer/audience, missing/duplicate/wrong-type claims, exact time boundaries/skew, token substitution, unknown/hostile key IDs, configured key refresh, opaque-token inactivity, sender-proof absence/replay, and authorization after acceptance. Fuzz the real library boundary and keep dependency advisories current.

For lifecycle, test overlapping rotation, partial rollout, cache staleness, rollback, old-key rejection, revocation latency, logout semantics, refresh replay, clock failure, introspection/key-service outage, emergency containment, re-enrollment, and evidence. Scan logs, traces, errors, metrics, support bundles, backups, CI, and artifacts for seeded canary credentials. Exercise a realistic leak and measure containment time.

## Definitions and Notation

Let lifecycle $L=(G,I,D,S,T,V,U,R,X,E)$ cover generation, issuance, delivery, storage, transport, validation, use, rotation/revocation, expiry/destruction, and evidence/response. Let token $z$, resource server $r$, and evaluation time $t$ determine a configured acceptance predicate.

Let $iss(z)$ be issuer, $aud(z)$ audiences, $exp(z)$ expiry, $nbf(z)$ not-before, $typ(z)$ explicit token type, $alg(z)$ declared protected algorithm, and $cnf(z)$ sender confirmation binding where applicable. These claims are untrusted until the cryptographic operation and validation profile accept them.

A **validation profile** is the resource-server-owned set of accepted token kinds, algorithms, issuers, keys, audiences, claims, time, sender, and state rules. **Credential inventory** records safe metadata and lifecycle state, never raw reusable secret material. **Revocation latency** is the maximum time from authorized invalidation decision until all in-scope verifiers reject use under stated availability assumptions.

## Mechanisms, Invariants, or Proof Structure

1. Classify every credential/token by issuer, holder, presenter, verifier, audience, authority, and lifetime.
2. Generate secrets/keys with approved cryptography and minimize authority at issuance.
3. Deliver once through an authenticated protected channel and prevent uncontrolled copies.
4. Store according to client/workload threat model, preferring short-lived and non-exportable authority.
5. Protect every transport hop and prevent credential forwarding across unintended origins.
6. Select explicit mutually exclusive validation profiles before inspecting untrusted claims.
7. Verify cryptography, issuer/key ownership, audience, type, time, sender, and state; then authorize object/action.
8. Rotate through bounded observable states; revoke/expire with truthful latency and recovery semantics.
9. Redact at collection, maintain safe inventory/signals, and exercise compromise response.
10. Test negative predicates, substitution, replay, leakage, failure, rotation, revocation, and destruction.

The acceptance conjunction is only as strong as its cryptographic library, configured trust anchors, time, key distribution, sender proof, and calling coverage. A passing token validator cannot prove secure storage or correct object authorization; lifecycle evidence must cover both.

## Alternatives and Trade-Offs

Opaque tokens centralize current state, permit prompt revocation/introspection, and hide claims from clients, but add authorization-server dependency, latency, caching/staleness, and privacy-sensitive lookup. Self-contained tokens enable local validation and resilience but expose claims to holders and make early revocation/policy freshness harder. Hybrid designs still need explicit consistency bounds.

Bearer tokens maximize interoperability and simplicity but theft enables replay. Sender-constrained tokens reduce replay from copied artifacts but add client key management, proxy/method/URL canonical concerns, proof replay state, and recovery. They do not stop a compromised authorized client.

Static API keys are simple for controlled integrations but tend toward broad authority, poor user context, long lifetime, and difficult distribution. Short-lived workload identity improves containment and automation but depends on issuer/control-plane availability and correct federation.

Symmetric MAC validation can be fast but shares token-minting capability with every verifier holding the key. Asymmetric signatures separate issuance from verification at greater key-distribution and algorithm complexity. Choose from trust topology, not fashion.

Very short lifetimes reduce compromise window but raise renewal load and availability coupling. Long lifetimes improve continuity but require stronger sender/storage/revocation controls. Define a loss-and-outage budget rather than selecting a round number.

Immediate online revocation reduces staleness but makes every request depend on state. Offline validation improves availability but accepts revoked authority until expiry or state propagation. State the bound and design critical-action step-up/state checks where necessary.

## Failure Modes and Misconceptions

- **“An API key is only an identifier.”** If possession grants access, it is a bearer credential.
- **“JWT means encrypted.”** Signed JWT claims are typically readable to holders.
- **“We decoded the token successfully.”** Decoding is not cryptographic or semantic validation.
- **“A valid signature is enough.”** Type, issuer, audience, time, key ownership, sender, and state also matter.
- **“The token chooses its algorithm/key URL.”** The resource server owns trust policy; token metadata is bounded untrusted input.
- **“Any token from our issuer works.”** Access, ID, refresh, tenant, and audience purposes are not interchangeable.
- **“Scope authorizes the object.”** Local object/action/tenant policy remains.
- **“TLS solves token theft.”** Endpoints, stores, logs, redirects, dependencies, and authorized clients remain.
- **“Hashed API keys are always safe.”** Low entropy and unkeyed offline verification can still expose them.
- **“Logout revokes everything immediately.”** State the actual refresh/session/access-token behavior.
- **“Rotation means two keys forever.”** Overlap is bounded and retirement is verified.
- **“Revocation is instant.”** Measure propagation/cache/introspection latency and outage behavior.
- **“Log it, then redact later.”** Raw ingestion, replication, and backup have already leaked it.
- **“Sender constraint stops client compromise.”** A compromised holder with key access can still exercise authority.
- **“One credential can span every environment.”** Environment separation limits blast radius.

## Worked Examples

### Example 1

**Situation:** A partner's API key appears in a query string. **Reasoning:** Proxies, history, referrers, analytics, and tickets may copy it. **Conclusion:** revoke/rotate it, move authentication to a protected header/protocol, and scan every collection path.

### Example 2

**Situation:** The orders API accepts a correctly signed token whose audience is `billing-api`. **Reasoning:** Signature authenticates issuer output, not applicability to this resource. **Conclusion:** reject on exact configured audience and investigate token-substitution tests.

### Example 3

**Situation:** A JWT library accepts `HS256` using an RSA public key intended for `RS256`. **Reasoning:** Untrusted algorithm selection creates key-type confusion. **Conclusion:** bind configured algorithms to keys and profiles; reject all others before trust.

### Example 4

**Situation:** A resource API receives a refresh token and introspection says active. **Reasoning:** Active does not make the artifact an access token for this endpoint. **Conclusion:** enforce explicit token type/use and audience; refresh authority stays at the authorization server.

### Example 5

**Situation:** A bearer token is stolen from an APM trace. **Reasoning:** TLS was intact, but observability created a replayable copy. **Conclusion:** revoke within documented latency, rotate derived authority as needed, remove/redact copies at collection, and use safe token identifiers.

### Example 6

**Situation:** A high-value API uses DPoP-bound tokens. The token leaks without the private key. **Reasoning:** The attacker cannot produce the required proof, subject to correct binding/replay validation. **Conclusion:** sender constraint reduces stolen-token utility but client-key compromise and authorization abuse remain modeled.

### Example 7

**Situation:** A signing-key rotation switches issuance before verifiers fetch the new JWKS. **Reasoning:** Valid requests fail across stale caches. **Conclusion:** publish first, observe propagation, switch issuance, retain old verification through bounded token life, then retire.

### Example 8

**Situation:** An employee leaves a tenant, but a 24-hour self-contained token retains administrator claims. **Reasoning:** Offline verification accepts stale authority. **Conclusion:** shorten lifetime and/or consult state/policy version for critical actions, with an explicit staleness bound.

### Example 9

**Situation:** A CLI receives a secret as `--token ...`. **Reasoning:** Shell history and process inspection can expose it. **Conclusion:** read from a protected store/file or standard input, avoid debug echo, and document secure automation.

### Example 10

**Situation:** A production API key is reused in staging for convenience. **Reasoning:** Weaker staging access now compromises production, and signals cannot attribute environment correctly. **Conclusion:** use distinct issuers/keys/audiences and reject cross-environment artifacts.

## Cross-Program Connections

- **Security Engineering:** key management, capability security, least privilege, defense in depth, and incident containment determine credential strength.
- **Cryptography:** randomness, signatures/MACs, key separation, algorithm agility, and proof of possession underpin validation but do not replace authorization.
- **Distributed Systems:** caches, clock skew, key propagation, introspection availability, regional partitions, and partial rollout determine revocation/rotation truth.
- **Operating Systems and Platform Engineering:** process isolation, workload identity, secret stores, hardware-backed keys, dumps, and deployment permissions govern exposure.
- **Web Engineering:** cookies, script injection, CSRF, origins, redirects, browser storage, and backend-for-frontend patterns shape client handling.
- **Observability and Incident Response:** safe identifiers, early redaction, inventory, detection, revocation, evidence, and exercises bound compromise.
- **Data Governance:** token claims, logs, backups, retention, and support systems can contain personal or authorization-sensitive information.

## References

1. Lodderstedt, T., Bradley, J., Labunets, A., and Fett, D. [RFC 9700: Best Current Practice for OAuth 2.0 Security](https://www.rfc-editor.org/rfc/rfc9700.html). IETF BCP 240, January 2025. Checked 2026-09-01.
2. Jones, M., and Hardt, D. [RFC 6750: The OAuth 2.0 Authorization Framework: Bearer Token Usage](https://www.rfc-editor.org/rfc/rfc6750.html). IETF, October 2012. Checked 2026-09-01.
3. Sheffer, Y., Hardt, D., and Jones, M. [RFC 8725: JSON Web Token Best Current Practices](https://www.rfc-editor.org/rfc/rfc8725.html). IETF BCP 225, February 2020. Checked 2026-09-01.
4. Fett, D., Campbell, B., Bradley, J., Lodderstedt, T., Jones, M., and Waite, D. [RFC 9449: OAuth 2.0 Demonstrating Proof of Possession](https://www.rfc-editor.org/rfc/rfc9449.html). IETF, September 2023. Checked 2026-09-01.
5. Campbell, B., Bradley, J., Sakimura, N., and Lodderstedt, T. [RFC 8705: OAuth 2.0 Mutual-TLS Client Authentication and Certificate-Bound Access Tokens](https://www.rfc-editor.org/rfc/rfc8705.html). IETF, February 2020. Checked 2026-09-01.
6. Jones, M., Bradley, J., and Sakimura, N. [RFC 9068: JSON Web Token (JWT) Profile for OAuth 2.0 Access Tokens](https://www.rfc-editor.org/rfc/rfc9068.html). IETF, October 2021. Checked 2026-09-01.
7. OWASP Foundation. [Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html). Checked 2026-09-01.

## Exercises

### Exercise 1

Design a credential inventory for a public web client, backend-for-frontend, orders API, authorization server, worker, and partner integration. Classify every artifact and state issuer, holder, verifier, audience, storage, lifetime, rotation, revocation, and owner.

### Exercise 2

Write an explicit JWT access-token validation profile and negative test matrix for the orders API. Include token substitution, algorithms/keys, issuer, audience, type, time, sender binding, claims, key rotation, outages, and authorization handoff.

### Exercise 3

A production API key was printed by CI and copied into logs, chat, and a support ticket. Create a containment, investigation, recovery, and prevention plan that accounts for every copy and derived authority.

### Exercise 4

Compare opaque bearer access tokens, self-contained bearer JWT access tokens, and sender-constrained access tokens for a high-value multi-region API. Discuss availability, replay, revocation, privacy, key/state distribution, and client complexity.

### Exercise 5

Design and verify zero-downtime scheduled signing-key rotation, then explain how emergency compromise changes the sequence and accepted availability risk.

## Answers to the Exercises

### Answer 1

The browser holds only a hardened BFF session cookie under the chosen web architecture; the BFF holds short-lived user access tokens server-side and any refresh authority in a stricter store. The authorization server holds signing/private issuance keys and refresh/session state; APIs hold configured issuer metadata/public verification keys, not issuer private keys. The orders API receives only access tokens for its audience and may use a distinct short-lived workload identity to call dependencies. Workers receive narrow short-lived workload credentials and job context, not copied user refresh tokens. The partner gets its own scoped credential or asymmetric client identity, never a shared master key. Each row records environment, tenant/client/user binding, allowed use, store/access identity, issue/expiry, two-slot or key-publication rotation, actual revocation latency, safe ID/last use, owner, and response path. Browser session, access, refresh, signing, workload, and partner artifacts remain distinct.

### Answer 2

The profile fixes `at+jwt`, allowed algorithms and key types, exact trusted issuer/metadata/key source, orders audience, required subject/client/tenant claims and types, maximum lifetime, `exp`/`nbf`/`iat` with small skew, and DPoP/mTLS confirmation where required. The parser bounds size/segments/JSON and resolves bounded `kid` only inside the issuer set. Tests cover malformed/duplicate claims; `none` and key confusion; bad signature/key; attacker key URL; wrong/missing issuer, audience, type, time, or claims; ID/refresh token substitution; multiple audiences; clock edges; missing/mismatched/replayed sender proof; old/new keys across cache rotation; metadata/key-service failure; and generic safe errors. After acceptance, tests prove immutable context, tenant/path binding, permissions, object/action authorization, concealment, and no raw token in telemetry.

### Answer 3

Treat the key as compromised immediately: identify owner/scope/audience/environment and dependent automation; revoke or disable it, apply temporary blocking, and issue least-privilege replacement through a separate trusted channel without allowing the exposed key to authorize replacement. Search CI artifacts, raw log storage/replicas/backups, chat, ticket attachments, caches, and local copies using restricted incident procedures; remove where retention systems allow and restrict remaining access. Use safe inventory/usage evidence to determine exposure window, source identities, actions, data/effects, and derived credentials; preserve forensic evidence and notify under policy. Update callers, verify new use, prove old rejection everywhere, repair effects, and destroy replacement staging copies. Prevent recurrence through masked protected secret injection or workload identity, no shell echo/arguments, redaction before collection, secret scanning/canaries, scoped CI permissions, invalid examples, rotation drills, and owner/expiry alerts.

### Answer 4

Opaque bearer tokens hide claims and permit current-state introspection/revocation, but every region needs an authenticated highly available lookup or bounded cache whose staleness weakens revocation; the issuer learns resource use. Self-contained bearer JWTs validate locally across partitions and reduce lookup latency, but expose claims to holders and accept stale/revoked authority until expiry/state distribution; signing-key rotation must propagate. Both bearer forms are replayable when copied. Sender-constrained tokens add proof tied to a client key, reducing stolen-token utility, but add key storage, proof validation/replay handling, proxy/URL semantics, and recovery; compromised clients can still act. For a high-value API, use minimized short-lived audience-specific tokens, sender constraint where clients support it, current authorization checks for critical actions, and an explicit availability-versus-revocation bound; choose opaque/self-contained per regional state and privacy constraints rather than syntax preference.

### Answer 5

For scheduled rotation, generate the new private key in protected storage, assign a non-colliding identifier, publish the public key/metadata, verify every region/client can fetch and cache it, then begin signing new tokens. Continue accepting the old key only for tokens issued before the switch and within bounded maximum lifetime/skew. Observe issuance and verification by key ID, resolve stragglers, stop old issuance, wait the bounded acceptance window, remove old public acceptance, prove old-token rejection, then destroy/retire the private key and close inventory evidence. Test stale caches, partition, rollback, and overlapping deployments. On compromise, attacker authority makes long overlap unsafe: publish/activate replacement through a clean path, stop old issuance, revoke/reject the compromised key as quickly as risk requires, invalidate affected sessions/derived authority, and accept that valid old tokens may fail. Communicate, monitor abuse, recover clients, and document the explicit availability trade rather than retaining attacker access for zero downtime.

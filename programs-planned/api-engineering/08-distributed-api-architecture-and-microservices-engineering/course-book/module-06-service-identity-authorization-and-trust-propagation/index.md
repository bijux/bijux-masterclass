# Module 06 — Service Identity, Authorization, and Trust Propagation

> **Program stage:** Course 8 of 10 — Distribute ownership deliberately.

> **Central question:** How do services authenticate workloads, preserve end-user intent, and avoid confused-deputy failures without trusting caller-supplied identity headers?

## Where this module fits

Module 05 produced **Implement the artifact-publication and run-completion saga with durable step identity, semantic locks, compensation, timeout handling, and operator-visible reconciliation**. This module extends that result by asking: **How do services authenticate workloads, preserve end-user intent, and avoid confused-deputy failures without trusting caller-supplied identity headers?**

The new capstone increment is **Introduce workload identities, audience-bound service credentials, delegated user context, short-lived artifact capabilities, and explicit authorization at every trust boundary**. It becomes the prerequisite for **Discovery, Routing, Gateways, and Traffic Topology**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Separate workload identity, end-user identity, tenant context, and delegated authority.
- Design service-to-service authentication without treating network location as trust.
- Prevent confused-deputy and privilege-amplification failures.
- Mint and verify narrow, short-lived capability tokens for artifact transfer.
- Propagate only bounded non-sensitive context across services.
- Define network policy as defense in depth rather than application authorization.

## Capstone increment

Introduce workload identities, audience-bound service credentials, delegated user context, short-lived artifact capabilities, and explicit authorization at every trust boundary.

## Four identities cross a service boundary

A distributed request may carry several distinct identities:

1. **Workload identity** — the calling process or service instance.
2. **End-user identity** — the human or client application whose intent initiated the action.
3. **Tenant context** — the isolation domain in which the resource exists.
4. **Delegated authority** — the exact action the caller may perform on the user’s behalf.

Collapsing these into `X-User-Id` or one shared bearer token creates confused-deputy failures. Artifact Service must know that Analysis Control is an authenticated workload, but workload identity alone does not authorize access to every artifact. It also needs narrow authority tied to a tenant, run or artifact, action, and time.

## Network location is not trust

Private IP ranges, cluster DNS, and service meshes are routing and defense-in-depth mechanisms. A compromised pod or misrouted request can still reach a peer. Every service authenticates the caller and authorizes its owned resource.

A practical trust stack is:

```text
transport identity       mTLS or platform workload credential
service authorization    allowed caller service and audience
end-user delegation      subject, tenant, scopes, assurance
resource authorization   owner-specific policy in the target service
capability restriction   resource, action, checksum/size, expiry
```

No single layer replaces the others.

## Workload identity

Service credentials should be:

- unique to the workload or service account;
- audience-bound;
- short-lived or automatically rotated;
- unavailable to unrelated services;
- recorded in audit events without exposing secrets;
- mapped to allowed service actions.

A shared “internal-service” token destroys attribution and makes revocation broad and dangerous.

## End-user delegation

The gateway validates the public credential. Downstream services need enough user context to authorize their resources, but blindly forwarding the original bearer token may expose excessive audience and privilege.

Options include:

- token exchange into a downstream audience;
- a signed internal delegation token;
- a narrow capability minted by the authoritative policy service;
- a synchronous authorization decision, when latency and availability permit it.

The course uses narrow artifact capabilities because Artifact Service should not call Control synchronously on every upload or download.

## Artifact capabilities

An upload capability contains:

```json
{
  "issuer": "analysis-control",
  "audience": "artifact-service",
  "subject": "worker-17",
  "tenant": "tenant-a",
  "resource": "run-9",
  "action": "artifact:upload",
  "sha256": "...",
  "maxBytes": 1048576,
  "issuedAt": 100,
  "expiresAt": 400,
  "jti": "upload:run-9:attempt-3:<digest>"
}
```

Artifact Service verifies signature, issuer, audience, tenant, action, lifetime, checksum, and size. It still stores its own canonical artifact record. The capability grants one action; it does not transfer data ownership.

Capabilities reduce synchronous coupling, but they create new responsibilities: key rotation, clock discipline, replay policy, revocation boundaries, and safe logging. Short lifetime limits the harm of leakage.

## Confused deputy example

A worker is allowed to upload artifacts for `run-9`. If Artifact Service trusts only the worker workload identity and a caller-supplied `runId`, the worker can upload into another tenant’s run. If it trusts only an end-user token forwarded by the gateway, the worker may not have a legitimate user token and may receive excess authority.

The narrow capability binds the worker’s action to:

- one tenant;
- one run;
- one attempt;
- one checksum;
- one maximum size;
- one audience;
- one time window.

Analysis Control later rechecks the current attempt before attaching the artifact, preventing a stale capability from completing the run.

## Authorization remains local to the owner

Artifact Service authorizes artifact content. Notification Service authorizes subscription administration and destination changes. Analysis Control authorizes run transitions. The gateway may reject obvious unauthorized requests early, but the owner performs the decisive check.

This avoids a common failure: centralizing every policy in the gateway while allowing direct internal callers to bypass it.

## Context propagation

Trace identifiers, correlation identifiers, and limited tenant context may cross boundaries. Sensitive data should not be placed in tracing baggage because it may be propagated and logged broadly. Treat propagated context as input: validate size, format, and source.

Do not use telemetry baggage as authorization. It is observability context, not a signed authority channel.

## Network policy

The optional Kubernetes policy denies traffic by default and permits only required paths. This narrows attack surface and misconfiguration blast radius. It does not prove that the permitted caller is authorized for a specific run or artifact.

## Python and TypeScript implications

The reference tracks use the same canonical capability claims and HMAC verification rules. Python’s `hmac.compare_digest` and TypeScript’s `timingSafeEqual` avoid ordinary string comparison. The course token is an instructional profile, not a claim that a home-grown token format should replace an operated identity system.

## Evidence required before Module 7

Prove wrong audience, wrong tenant, expiry, tampering, excessive size, and checksum mismatch are rejected. Show that no service treats `X-User-Id`, `X-Tenant-Id`, private networking, or trace baggage as authority.

## Four identities must remain distinct

A distributed request can carry several identities:

| Identity | Question answered | Typical evidence |
|---|---|---|
| workload | Which deployed service instance is calling? | mTLS certificate or workload token |
| end user | On whose behalf did the original action begin? | validated access token or delegated claim set |
| tenant | Which isolation boundary applies? | owner-validated tenant claim and resource lookup |
| business effect | Which exact action is authorized? | capability or stable command identity |

Collapsing these into one header creates confused-deputy failures. A valid workload identity does not mean the workload may access every tenant. A valid user does not mean a worker should carry the user’s broad bearer token for thirty minutes. A tenant header from the network is not authority.

## Authentication at each hop

The receiving service authenticates the immediate caller. It does not assume that traffic from an internal network is trusted.

A workload credential should be:

- audience bound;
- short lived;
- issued to a named workload identity;
- rotated automatically where possible;
- mapped to allowed service operations;
- observable without logging secret material.

Mutual TLS can authenticate both channel endpoints and protect traffic. It does not decide whether the caller may read artifact `artifact-7` for tenant `tenant-a`. Resource authorization still belongs to Artifact Service.

## End-user delegation

Some downstream decisions need end-user context. Forwarding the original token unchanged is often excessive because it may have a broad audience and scopes.

A delegated context should contain only the claims required by the downstream operation and should preserve:

- original subject;
- actor or calling workload;
- tenant;
- allowed action;
- audience;
- expiry;
- authentication assurance or freshness when relevant;
- correlation to the originating request.

The downstream service validates issuer, audience, expiry, actor, and resource policy. It does not trust `X-User-Id` added by any caller.

## Capability design for artifact effects

The capstone’s artifact-upload capability is intentionally narrow:

```text
issuer       analysis-control
audience     artifact-service
tenant       tenant-a
resource     run-42
action       artifact:upload
attempt      attempt-3
sha256       expected digest
max_bytes    bounded size
expires_at   short lifetime
```

The capability answers “may this exact effect occur?” rather than “is this caller generally powerful?” Artifact Service verifies the capability locally, then applies its own constraints.

Capabilities introduce their own risks:

- theft before expiry;
- replay;
- overly broad resource patterns;
- weak audience validation;
- clock and rotation errors;
- logging of bearer material.

Use short lifetime, exact audience, narrow action, bounded resource, and stable effect identity. One-time consumption may be useful, but it must tolerate response loss and idempotent retry. The capstone therefore deduplicates the effect rather than simply rejecting every repeated token use.

## The confused deputy in concrete form

Suppose Gateway is allowed to call Artifact Service. A user asks Gateway for `artifact-foreign`. Gateway authenticates the user but fails to verify ownership, then calls Artifact with its workload credential. Artifact authorizes “Gateway may read artifacts” and returns the object.

Both authentications succeed. Authorization fails because Artifact trusted the deputy’s general power rather than the delegated resource context.

Correct designs include:

- Artifact verifies a user-delegated token and resource ownership;
- Control issues a narrow artifact-download capability after owner authorization;
- Gateway calls an owner endpoint that returns only authorized data.

The capstone uses capabilities for narrow artifact operations and keeps final resource authorization at the owner.

## Context propagation is not authority propagation

Trace context and baggage help correlate work. They are not security credentials. A caller can often supply trace headers. Receivers should validate syntax, generate safe replacements when invalid, and never authorize from a trace identifier.

Baggage may propagate across many services and even to external systems. Do not place access tokens, personal data, authorization decisions, or secrets in it. Use bounded identifiers whose disclosure is acceptable.

Useful propagated operational context includes:

```text
trace id
correlation id
request deadline
idempotency/effect id
sanitized tenant pseudonym
contract version
```

Each item still needs a size and trust policy.

## Network policy is defense in depth

A network policy can restrict which workloads may connect. It reduces attack surface and accidental dependencies. It does not replace application authentication or authorization.

Course 8’s example policy allows only declared paths in the course namespace. The service catalogue and dependency graph remain the source for intended communication. Runtime network evidence should be compared with that declaration.

A compromised allowed caller still needs least-privilege application credentials. A misconfigured policy must not turn the internal network into an administrative superuser.

## Service-to-service authorization matrix

For each operation, record:

```text
caller workload
downstream audience
end-user context required?
tenant context required?
resource capability required?
allowed scopes or roles
maximum credential lifetime
replay behavior
audit event
```

Example:

| Operation | Caller | User context | Capability | Owner decision |
|---|---|---:|---:|---|
| upload artifact | Worker | no broad token | upload capability | Artifact validates exact effect |
| download artifact | Gateway | delegated or narrow capability | download capability | Artifact validates tenant/resource |
| report completion | Worker | no | lease/attempt identity | Control validates current generation |
| consume completion | Notification | no | event authenticity | Notification applies subscription policy |

This matrix is more useful than “all internal calls use mTLS.”

## Key and certificate rotation

Independent services must tolerate overlapping trust material during rotation. A safe rotation sequence is:

1. publish or trust the new verification key/certificate chain;
2. keep the old verifier active;
3. begin issuing with the new key;
4. observe that all consumers accept it;
5. wait beyond the maximum credential lifetime;
6. retire the old verifier;
7. prove rejected-old-key behavior.

A simultaneous issuer/verifier switch recreates a coordinated release. Rotation is therefore another version-skew problem.

## Security evidence for a distributed boundary

The lab does not pass because a happy-path token verifies. Required negative evidence includes:

- wrong audience;
- wrong tenant;
- expired capability;
- altered checksum;
- stale worker attempt;
- untrusted identity header;
- valid workload with insufficient operation permission;
- cross-tenant artifact access;
- trace or baggage value presented as authority.

A boundary that cannot reject these cases is not ready for independent deployment.

## Module synthesis

You are ready to leave this module when you can **separate workload identity, end-user identity, tenant context, and delegated authority, design service-to-service authentication without treating network location as trust, and prevent confused-deputy and privilege-amplification failures** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Remove any authorization dependency on caller-supplied identity headers** and requiring the following oracle: **Only the intended workload and tenant can perform the bounded action; network location and unsigned headers never establish authority.**

The cumulative platform now includes **Introduce workload identities, audience-bound service credentials, delegated user context, short-lived artifact capabilities, and explicit authorization at every trust boundary**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Discovery, Routing, Gateways, and Traffic Topology](../module-07-discovery-routing-gateways-and-traffic-topology/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.

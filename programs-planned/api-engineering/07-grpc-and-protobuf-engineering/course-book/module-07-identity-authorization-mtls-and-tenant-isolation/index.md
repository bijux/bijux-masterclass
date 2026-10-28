# Module 07 — Identity, Authorization, mTLS, and Tenant Isolation

> **Program stage:** Course 7 of 10 — Engineer typed internal invocation and streaming.

> **Central question:** How do internal RPC peers establish workload and delegated user identity, enforce method and resource policy, and protect long-lived streams without treating a private network as trust?

## Where this module fits

Module 06 produced **Implement `WatchRun`, `UploadDataset`, `DownloadArtifact`, and the worker `Work` stream with shared schedule vectors, bounded buffers, resumable observation, and stale-attempt fencing**. This module extends that result by asking: **How do internal RPC peers establish workload and delegated user identity, enforce method and resource policy, and protect long-lived streams without treating a private network as trust?**

The new capstone increment is **Implement RPC security profile 1.0 with method policy, workload and user identity binding, tenant-isolation vectors, mTLS-ready configuration, and secure worker-stream authorization**. It becomes the prerequisite for **Channels, Health, Discovery, Load Balancing, and Lifecycle**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Distinguish server TLS, mutual TLS workload identity, bearer identity, and delegated end-user context.
- Authenticate callers without trusting arbitrary metadata or network location.
- Enforce method, tenant, resource, field, and attempt-level authorization.
- Bind worker sessions and completions to workload identity and lease generation.
- Protect credentials and authorization context on long-lived streams.
- Produce cross-language security vectors without leaking secrets in status, metadata, logs, reflection, or traces.

## Capstone increment

Implement RPC security profile 1.0 with method policy, workload and user identity binding, tenant-isolation vectors, mTLS-ready configuration, and secure worker-stream authorization.

## Private is not trusted

An RPC endpoint reachable only inside a cluster still accepts traffic from compromised workloads, misconfigured jobs, debugging tools, and future services. Network location is an input to defense, not an identity. Every call needs an authenticated peer appropriate to the deployment and an authorization decision appropriate to the method and resource.

The course distinguishes four contexts. Server TLS authenticates the server and protects transport. Mutual TLS can authenticate a workload certificate to the server. A bearer access token can identify an end user or client. A delegated context links a workload invocation to the external principal on whose behalf it acts. None is automatically interchangeable.

The dependency-light profile uses deterministic fixture identities and signatures. The full profile provides certificate and JWKS configuration routes. Fixture credentials are explicitly non-production and cannot satisfy operated identity claims.

## Workload identity and user delegation

The HTTP gateway may call Analysis Control as a workload while acting for an authenticated user. If it sends only its service identity, downstream policy loses the user and may over-authorize. If it forwards the external bearer token blindly, it may expose a token to services outside its intended audience. Use an audience-restricted delegated token or a signed internal identity envelope according to the security profile.

The downstream receives two identities: the authenticated calling workload and the delegated principal. Policy can require that a trusted gateway workload is allowed to delegate, that the delegated token targets the RPC audience, and that tenant and subject claims are bound. The service records both identities in bounded audit evidence.

Do not accept `x-user-id` or `x-tenant-id` metadata as authority. Untrusted metadata is rejected or ignored; authoritative identity comes from verified credentials.

## Method policy begins with default deny

The RPC catalogue declares every method, allowed caller workloads, required user scopes or service roles, tenant source, resource action, and whether delegation is allowed. A method absent from policy is denied. Adding a method therefore requires a security review rather than inheriting permissive defaults.

`CreateRun` requires a trusted gateway or approved internal client, delegated run-write authority, and access to the project/dataset tenant. `GetRun` and `WatchRun` require read authority and resource visibility. `UploadDataset` requires write authority plus upload budgets. Worker `Work` permits registered worker identities, not user tokens. Reflection and health have separate exposure policy.

Interceptors can establish identities and method-level prerequisites. Resource ownership and state-dependent decisions remain in the application transaction or use case.

## Tenant isolation must reach the query and mutation

Checking a tenant claim before loading a run is not enough if the repository later queries by resource name alone. Authorization-aware access constrains the data operation by tenant and permitted relationship. A foreign resource should be absent from the caller's result population according to concealment policy.

Mutations bind tenant, resource, expected revision, and principal within the same authoritative transaction. A request cannot swap the dataset name after a separate authorization check. Stream subscriptions bind tenant at creation and validate every resumed resource. Cache, channel, and client pools must not reuse authorization context across tenants.

Shared vectors include cross-tenant resource names, nested identifiers, mismatched delegated claims, and valid scopes with wrong ownership.

## Transport security and mTLS profile

TLS protects confidentiality and integrity in transit and authenticates the server certificate. Mutual TLS additionally authenticates the client certificate, but the certificate subject must be mapped to a governed workload identity. Trusting any certificate from a broad internal CA can grant too much authority.

The profile defines trusted roots, expected server name, permitted workload identity patterns, certificate validity, revocation or rotation approach, and behavior during overlapping rotations. Clients validate names rather than disabling verification. Servers do not rely on a forwarded certificate header unless it comes from a specifically trusted terminator with a protected channel.

Local development can use fixture certificates. The proof checks configuration and identity mapping; it does not claim a production public-key infrastructure.

## Worker identity is attempt-scoped in effect

A worker workload may be authorized to open `Work`, but it is not authorized to complete every run. Analysis Control assigns work with an assignment identifier, tenant, lease generation, and expiry. Results are accepted only from the bound worker identity and current generation. This combines transport/workload identity with durable attempt authority.

A stolen or replayed progress frame from another stream fails. A reconnected worker must re-establish identity and receive or reconcile assignments. Certificate rotation may change the connection identity material without changing the governed worker identity; the mapping and session policy state how.

Do not place secret dataset credentials in assignment messages. Use scoped references or short-lived access grants with a narrower audience and lifetime.

## Long-lived streams and credential freshness

A stream may outlive a short-lived access token or certificate rotation window. Decide whether authentication is evaluated only at stream establishment, periodically refreshed, or bounded by a maximum stream age. A public user watch stream should not remain authorized indefinitely after revocation. Worker streams need certificate/key rotation and session renewal behavior.

The course profile sets maximum stream age and requires reconnect before credential expiry where practical. Authorization-sensitive resource changes may terminate a stream or filter future messages. A stream cannot accept a midstream identity swap through arbitrary metadata frames.

Tests use an injected clock to expire credentials, revoke scopes, rotate keys, and change tenant membership while streams are active.

## Metadata, status, and telemetry privacy

Authorization metadata, delegated tokens, certificate details, and internal principal identifiers are sensitive. Redact values recursively in logs and traces. Record stable pseudonymous identifiers where correlation is required. Do not echo failed token claims in status details. `PERMISSION_DENIED` and `UNAUTHENTICATED` messages remain generic while internal audit evidence captures the reason.

Trace baggage is not a security channel. It is caller-controlled unless explicitly validated. Do not place scopes, roles, or tenant authority in trace attributes and then consume them for policy. Metrics use bounded method and outcome dimensions, never user IDs or raw tenant IDs.

Reflection and descriptor access can expose internal service and field names. Course 9 governs it as an authenticated diagnostic capability.

## Cross-language security conformance

Python and TypeScript TLS libraries, metadata APIs, and interceptor models differ. Shared conformance compares accepted identity, rejected reason class, method policy, resource visibility, stream termination, and durable effect. It does not require identical exception classes or certificate object layouts.

Vectors cover wrong issuer/audience, expired or future tokens, untrusted gateway delegation, tenant mismatch, missing scope, wrong worker identity, stale lease generation, certificate-name mismatch, and overlapping key rotation. Secret values are fixture-only and scanned from reports.

A dependency-light proof validates deterministic credentials and policy. Live TLS and mTLS evidence remains a separate environment-backed route.

## Worked authorization review: gateway delegation

A user authenticates to the public gateway and requests `GetRun` for a tenant-owned resource. The gateway then calls internal Analysis Control. Two identities matter. The gateway workload proves which software component opened the channel. The delegated user identity proves on whose behalf the request is made. If Analysis Control sees only the gateway, every user may inherit gateway-wide authority. If it accepts a raw `x-user-id`, any compromised workload can impersonate a user.

The profile therefore requires a verified workload identity plus an audience-restricted delegated principal. In a full deployment, mTLS can establish the workload and a signed internal token can carry subject, tenant, scopes, issuer, audience, issued/expiry time, and delegation authority. The deterministic course fixture models the same fields without claiming an operated PKI or identity provider.

Method policy first checks that the gateway workload may call `GetRun` with delegation. It then checks delegated read scope. Resource authorization is not complete until the repository constrains the run lookup by tenant or relationship. Querying by globally unique name and checking tenant afterward risks existence leaks and time-of-check/time-of-use defects. Under concealment policy, a foreign run is returned as not found.

A worker stream follows a different path. The caller presents a worker workload identity and no end-user token. Opening `Work` grants permission to establish a session, not to complete any assignment. Each assignment binds worker identity, tenant, assignment identifier, lease generation, and expiry in durable state. A result from the wrong worker or stale generation fails even when sent over the original authenticated channel.

Long-lived streams create freshness questions. A WatchRun token can expire while the stream is open. The profile sets a maximum stream age and reconnect requirement. A worker certificate may rotate; the governed workload identity can remain stable across overlapping certificates. Arbitrary midstream identity replacement is forbidden. Revocation and membership changes can terminate or filter streams according to policy.

The evidence deliberately avoids credential leakage. Client-facing status says unauthenticated or permission denied without echoing claims. Audit evidence records pseudonymous workload and user identities, tenant, method, resource action, and stable denial reason. Metrics use method and outcome, never raw subject identifiers. Trace baggage is propagated context, not authority.

The final vector matrix crosses workload, user, tenant, scope, resource, stream age, and lease generation. Python and TypeScript can implement interceptors differently, but both must deny before durable effect, conceal the same information, and produce equivalent safe audit semantics.

## Implementation reading

Read `capstone/security/method-policy.yaml`, `capstone/shared/vectors/security.json`, and both tracks' identity/policy modules. The live server accepts fixture bearer metadata for local proof; `capstone/security/tls/` and the full-proof route show the mTLS configuration boundary without claiming an operated PKI.

## Failure checklist

- Is internal network reachability being treated as identity?
- Can arbitrary metadata assert user, tenant, role, or scope?
- Does method authorization default deny new RPCs?
- Is tenant ownership enforced inside the authoritative query or transaction?
- Can a worker identity complete an assignment it was not leased?
- Can long-lived streams outlive credential or policy validity indefinitely?

## Transition

After preserving the checkpoint evidence, continue to **Channels, Health, Discovery, Load Balancing, and Lifecycle**. Do not progress while the non-compensable gate remains unresolved.

## Module synthesis

You are ready to leave this module when you can **distinguish server TLS, mutual TLS workload identity, bearer identity, and delegated end-user context, authenticate callers without trusting arbitrary metadata or network location, and enforce method, tenant, resource, field, and attempt-level authorization** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Expire and revoke credentials during WatchRun and Work sessions** and requiring the following oracle: **Only explicitly allowed workload/delegation/method/resource combinations reach application effects. Cross-tenant and stale-attempt calls reveal no protected data. Long-lived streams obey freshness policy, and no report or status leaks credentials.**

The cumulative platform now includes **Implement RPC security profile 1.0 with method policy, workload and user identity binding, tenant-isolation vectors, mTLS-ready configuration, and secure worker-stream authorization**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Channels, Health, Discovery, Load Balancing, and Lifecycle](../module-08-channels-health-discovery-load-balancing-and-lifecycle/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.

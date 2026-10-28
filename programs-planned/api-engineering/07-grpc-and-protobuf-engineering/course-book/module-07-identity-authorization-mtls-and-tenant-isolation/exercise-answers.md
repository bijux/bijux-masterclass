# Worked Answers — Module 07: Identity, Authorization, mTLS, and Tenant Isolation

Use these solutions to audit your reasoning for **Identity, Authorization, mTLS, and Tenant Isolation**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Differentiate server TLS, mTLS workload identity, and delegated user identity.

Server TLS authenticates the server and protects the channel; mTLS authenticates the calling workload; delegated identity represents the end user/client on whose behalf that workload acts. Each has a different audience and policy role.

**Decisive evidence:** identity-layer diagram

The chapter’s decisive distinction is this: TLS protects confidentiality and integrity in transit and authenticates the server certificate. Mutual TLS additionally authenticates the client certificate, but the certificate subject must be mapped to a governed workload identity. Trusting any certificate from a broad internal CA can grant too much authority.

## 2. Why should a gateway not forward arbitrary `x-user-id` metadata?

The value is caller-controlled and unverified. A compromised peer can impersonate any principal or tenant. Use a verified audience-restricted token or signed internal delegation envelope.

**Decisive evidence:** metadata forgery test

In the cumulative capstone, the rule becomes concrete: The HTTP gateway may call Analysis Control as a workload while acting for an authenticated user. If it sends only its service identity, downstream policy loses the user and may over-authorize. If it forwards the external bearer token blindly, it may expose a token to services outside its intended audience. Use an audience-restricted delegated token or a signed internal identity envelope according to the security profile.

## 3. What policy should apply to a newly added RPC method?

Default deny until the RPC catalogue names allowed workloads, delegation, user/service permissions, tenant source, resource action, and evidence.

**Decisive evidence:** method catalogue gate

A useful way to reason about the boundary is: The RPC catalogue declares every method, allowed caller workloads, required user scopes or service roles, tenant source, resource action, and whether delegation is allowed. A method absent from policy is denied. Adding a method therefore requires a security review rather than inheriting permissive defaults.

## 4. Where must tenant isolation be enforced for GetRun?

Inside the repository query or transaction, constraining resource name by authorized tenant/relationship. A separate pre-check can race or be bypassed.

**Decisive evidence:** authorized query test

The implementation consequence is: Mutations bind tenant, resource, expected revision, and principal within the same authoritative transaction. A request cannot swap the dataset name after a separate authorization check. Stream subscriptions bind tenant at creation and validate every resumed resource. Cache, channel, and client pools must not reuse authorization context across tenants.

## 5. Why is a valid worker certificate insufficient to accept WorkResult?

Completion also requires the assignment to be bound to that worker and the current durable lease generation. Workload identity alone grants session eligibility, not attempt authority.

**Decisive evidence:** worker lease vector

The important nuance is: A worker workload may be authorized to open Work, but it is not authorized to complete every run. Analysis Control assigns work with an assignment identifier, tenant, lease generation, and expiry. Results are accepted only from the bound worker identity and current generation. This combines transport/workload identity with durable attempt authority.

## 6. How should a user WatchRun stream behave after token expiry?

Terminate or require bounded renewal according to maximum stream age and credential freshness policy. It must not continue indefinitely under stale authority.

**Decisive evidence:** stream expiry test

Under concurrency or failure, the distinction becomes: A stream may outlive a short-lived access token or certificate rotation window. Decide whether authentication is evaluated only at stream establishment, periodically refreshed, or bounded by a maximum stream age. A public user watch stream should not remain authorized indefinitely after revocation. Worker streams need certificate/key rotation and session renewal behavior.

## 7. What risk exists when any certificate from an internal CA is trusted as any workload?

A broadly trusted CA can let one compromised workload authenticate as another unless certificate identity is mapped and authorized narrowly.

**Decisive evidence:** certificate mapping policy

The design remains honest only if: The profile defines trusted roots, expected server name, permitted workload identity patterns, certificate validity, revocation or rotation approach, and behavior during overlapping rotations. Clients validate names rather than disabling verification. Servers do not rely on a forwarded certificate header unless it comes from a specifically trusted terminator with a protected channel.

## 8. Why must trace baggage never become an authorization source?

Baggage is propagated caller data and can be forged. It is for observability context, not trusted scopes, roles, or tenant authority.

**Decisive evidence:** baggage rejection test

The consumer-facing consequence is: The evidence deliberately avoids credential leakage. Client-facing status says unauthenticated or permission denied without echoing claims. Audit evidence records pseudonymous workload and user identities, tenant, method, resource action, and stable denial reason. Metrics use method and outcome, never raw subject identifiers. Trace baggage is propagated context, not authority.

## 9. How should wrong-tenant resources appear under concealment policy?

As `NOT_FOUND` or an empty authorized collection according to the documented concealment policy, while internal audit records the denial.

**Decisive evidence:** concealment vector

The operational consequence is: Checking a tenant claim before loading a run is not enough if the repository later queries by resource name alone. Authorization-aware access constrains the data operation by tenant and permitted relationship. A foreign resource should be absent from the caller's result population according to concealment policy.

## 10. Which identities should an audit record capture for a delegated call?

Capture the calling workload, delegated principal, tenant scope, method, resource/action, decision, and stable reason without raw credentials.

**Decisive evidence:** audit schema

The strongest engineering interpretation is: The downstream receives two identities: the authenticated calling workload and the delegated principal. Policy can require that a trusted gateway workload is allowed to delegate, that the delegated token targets the RPC audience, and that tenant and subject claims are bound. The service records both identities in bounded audit evidence.

## 11. What must be tested during signing-key or certificate rotation overlap?

Both old and new valid keys/certificates work during the bounded overlap, unknown material fails, expiry/revocation takes effect, and reports contain no secret material.

**Decisive evidence:** rotation overlap vectors

The defect-oriented view is: A stolen or replayed progress frame from another stream fails. A reconnected worker must re-establish identity and receive or reconcile assignments. Certificate rotation may change the connection identity material without changing the governed worker identity; the mapping and session policy state how.

## 12. Define cross-language security equivalence for one denied mutation.

Both tracks deny before durable mutation, expose the same status and safe reason class, produce equivalent audit semantics, and reveal no extra resource information.

**Decisive evidence:** cross-language denial report

Across the Python and TypeScript tracks, the invariant is: Vectors cover wrong issuer/audience, expired or future tokens, untrusted gateway delegation, tenant mismatch, missing scope, wrong worker identity, stale lease generation, certificate-name mismatch, and overlapping key rotation. Secret values are fixture-only and scanned from reports.

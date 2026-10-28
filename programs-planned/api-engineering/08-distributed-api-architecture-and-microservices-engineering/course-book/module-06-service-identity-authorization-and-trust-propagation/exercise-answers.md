# Worked Answers — Module 06: Service Identity, Authorization, and Trust Propagation

Use these solutions to audit your reasoning for **Service Identity, Authorization, and Trust Propagation**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why is workload identity insufficient to authorize an artifact upload?

It proves which service or worker is calling, not which tenant, run, attempt, checksum, and action are allowed. Resource authority must be narrower.

**Decisive evidence:** capability authorization vector

The chapter’s decisive distinction is this: A worker is allowed to upload artifacts for run-9. If Artifact Service trusts only the worker workload identity and a caller-supplied runId, the worker can upload into another tenant’s run. If it trusts only an end-user token forwarded by the gateway, the worker may not have a legitimate user token and may receive excess authority.

## 2. What is the confused-deputy risk when Artifact Service trusts `X-User-Id`?

A caller can forge or overstate user authority, and Artifact Service cannot prove who validated it or for which audience. Signed delegation or capability is required.

**Decisive evidence:** forged-header rejection test

In the cumulative capstone, the rule becomes concrete: Collapsing these into X-User-Id or one shared bearer token creates confused-deputy failures. Artifact Service must know that Analysis Control is an authenticated workload, but workload identity alone does not authorize access to every artifact. It also needs narrow authority tied to a tenant, run or artifact, action, and time.

## 3. Why does a capability include audience?

A token minted for Artifact Service must not be replayed to Analysis Control or another service. Audience limits where the authority is meaningful.

**Decisive evidence:** wrong-audience test

A useful way to reason about the boundary is: Artifact Service authorizes artifact content. Notification Service authorizes subscription administration and destination changes. Analysis Control authorizes run transitions. The gateway may reject obvious unauthorized requests early, but the owner performs the decisive check.

**Evidence.** Test workload identity, delegated tenant/user context, audience-bound capability, expiry, tampering, cross-tenant use, and owner-side authorization.

## 4. Why bind an upload capability to checksum and maximum size?

It limits what bytes and resource cost the holder may create, preventing substitution and unbounded upload under an otherwise valid token.

**Decisive evidence:** checksum and size proof

The implementation consequence is: Operation Caller User context Capability Owner decision --- --- ---: ---: --- upload artifact Worker no broad token upload capability Artifact validates exact effect download artifact Gateway delegated or narrow capability download capability Artifact validates tenant/resource report completion Worker no lease/attempt identity Control validates current generation consume completion Notification no event authenticity Notification applies subscription policy

## 5. Can mTLS replace resource authorization?

No. It authenticates the workload channel, not whether that workload may act on a specific tenant resource for a user.

**Decisive evidence:** workload-versus-resource policy matrix

The important nuance is: Collapsing these into one header creates confused-deputy failures. A valid workload identity does not mean the workload may access every tenant. A valid user does not mean a worker should carry the user’s broad bearer token for thirty minutes. A tenant header from the network is not authority.

## 6. Why should the original public bearer token not automatically be forwarded to every service?

It may have the wrong audience, excessive scope, long lifetime, and exposure surface. Downstream delegation should be purpose- and audience-bound.

**Decisive evidence:** token propagation review

Under concurrency or failure, the distinction becomes: Use short lifetime, exact audience, narrow action, bounded resource, and stable effect identity. One-time consumption may be useful, but it must tolerate response loss and idempotent retry. The capstone therefore deduplicates the effect rather than simply rejecting every repeated token use.

## 7. What context is safe to put in trace baggage?

Only bounded non-sensitive diagnostic context. Credentials, API keys, PII, and authorization decisions must not be placed there.

**Decisive evidence:** baggage redaction test

The design remains honest only if: Course 8’s example policy allows only declared paths in the course namespace. The service catalogue and dependency graph remain the source for intended communication. Runtime network evidence should be compared with that declaration.

**Evidence.** Apply the boundary scorecard and ownership catalogue, then reject duplicate writers, shared private data, cyclic dependencies, and capabilities lacking reversal criteria.

## 8. Who performs the decisive artifact authorization?

Artifact Service, because it owns the artifact. Gateway and Control may reject early or mint authority, but the owner validates the capability and resource.

**Decisive evidence:** owner-side authorization proof

The consumer-facing consequence is: Artifact Service authorizes artifact content. Notification Service authorizes subscription administration and destination changes. Analysis Control authorizes run transitions. The gateway may reject obvious unauthorized requests early, but the owner performs the decisive check.

**Evidence.** Test workload identity, delegated tenant/user context, audience-bound capability, expiry, tampering, cross-tenant use, and owner-side authorization.

## 9. Why must Control reauthorize completion after artifact upload?

The run attempt or tenant policy may change during transfer. Storage authority does not imply completion authority.

**Decisive evidence:** stale capability schedule

The operational consequence is: The optional Kubernetes policy denies traffic by default and permits only required paths. This narrows attack surface and misconfiguration blast radius. It does not prove that the permitted caller is authorized for a specific run or artifact.

**Evidence.** Require a remote-process fault experiment, ownership/reconciliation evidence, operational responsibility, and a quantified benefit exceeding distribution cost.

## 10. What does network policy contribute?

It restricts reachable paths and reduces blast radius. It is defense in depth, not a substitute for service authentication or business authorization.

**Decisive evidence:** network-policy and application-policy comparison

The strongest engineering interpretation is: Course 8’s example policy allows only declared paths in the course namespace. The service catalogue and dependency graph remain the source for intended communication. Runtime network evidence should be compared with that declaration.

**Evidence.** Require a remote-process fault experiment, ownership/reconciliation evidence, operational responsibility, and a quantified benefit exceeding distribution cost.

## 11. How does short capability lifetime reduce coupling and risk?

Artifact Service can verify locally without a synchronous Control call, while the brief lifetime limits leakage and stale-policy exposure.

**Decisive evidence:** capability lifetime analysis

The defect-oriented view is: Suppose Gateway is allowed to call Artifact Service. A user asks Gateway for artifact-foreign. Gateway authenticates the user but fails to verify ownership, then calls Artifact with its workload credential. Artifact authorizes “Gateway may read artifacts” and returns the object.

**Evidence.** Test workload identity, delegated tenant/user context, audience-bound capability, expiry, tampering, cross-tenant use, and owner-side authorization.

## 12. Why is a shared internal superuser token unacceptable?

It erases service attribution, grants excessive authority, makes revocation broad, and turns one credential compromise into platform-wide access.

**Decisive evidence:** credential inventory and compromise scenario

Across the Python and TypeScript tracks, the invariant is: The reference tracks use the same canonical capability claims and HMAC verification rules. Python’s hmac.compare digest and TypeScript’s timingSafeEqual avoid ordinary string comparison. The course token is an instructional profile, not a claim that a home-grown token format should replace an operated identity system.

# Worked answers — Identity, Authorization, mTLS, and Tenant Isolation

These are reference answers, not scripts to memorize. Compare the decision rule and evidence, then revise your answer.

## 1. Differentiate server TLS, mTLS workload identity, and delegated user identity.

Server TLS authenticates the server and protects the channel; mTLS authenticates the calling workload; delegated identity represents the end user/client on whose behalf that workload acts. Each has a different audience and policy role.

**Decisive evidence:** identity-layer diagram

## 2. Why should a gateway not forward arbitrary `x-user-id` metadata?

The value is caller-controlled and unverified. A compromised peer can impersonate any principal or tenant. Use a verified audience-restricted token or signed internal delegation envelope.

**Decisive evidence:** metadata forgery test

## 3. What policy should apply to a newly added RPC method?

Default deny until the RPC catalogue names allowed workloads, delegation, user/service permissions, tenant source, resource action, and evidence.

**Decisive evidence:** method catalogue gate

## 4. Where must tenant isolation be enforced for GetRun?

Inside the repository query or transaction, constraining resource name by authorized tenant/relationship. A separate pre-check can race or be bypassed.

**Decisive evidence:** authorized query test

## 5. Why is a valid worker certificate insufficient to accept WorkResult?

Completion also requires the assignment to be bound to that worker and the current durable lease generation. Workload identity alone grants session eligibility, not attempt authority.

**Decisive evidence:** worker lease vector

## 6. How should a user WatchRun stream behave after token expiry?

Terminate or require bounded renewal according to maximum stream age and credential freshness policy. It must not continue indefinitely under stale authority.

**Decisive evidence:** stream expiry test

## 7. What risk exists when any certificate from an internal CA is trusted as any workload?

A broadly trusted CA can let one compromised workload authenticate as another unless certificate identity is mapped and authorized narrowly.

**Decisive evidence:** certificate mapping policy

## 8. Why must trace baggage never become an authorization source?

Baggage is propagated caller data and can be forged. It is for observability context, not trusted scopes, roles, or tenant authority.

**Decisive evidence:** baggage rejection test

## 9. How should wrong-tenant resources appear under concealment policy?

As `NOT_FOUND` or an empty authorized collection according to the documented concealment policy, while internal audit records the denial.

**Decisive evidence:** concealment vector

## 10. Which identities should an audit record capture for a delegated call?

Capture the calling workload, delegated principal, tenant scope, method, resource/action, decision, and stable reason without raw credentials.

**Decisive evidence:** audit schema

## 11. What must be tested during signing-key or certificate rotation overlap?

Both old and new valid keys/certificates work during the bounded overlap, unknown material fails, expiry/revocation takes effect, and reports contain no secret material.

**Decisive evidence:** rotation overlap vectors

## 12. Define cross-language security equivalence for one denied mutation.

Both tracks deny before durable mutation, expose the same status and safe reason class, produce equivalent audit semantics, and reveal no extra resource information.

**Decisive evidence:** cross-language denial report

# Exercises — Identity, Authorization, mTLS, and Tenant Isolation

Answer before opening the reference answers. For every answer, state the governing rule, one failure example, and the evidence that decides the case.

## 1. Differentiate server TLS, mTLS workload identity, and delegated user identity.

Write a concise engineering answer and name the decisive proof.

## 2. Why should a gateway not forward arbitrary `x-user-id` metadata?

Write a concise engineering answer and name the decisive proof.

## 3. What policy should apply to a newly added RPC method?

Write a concise engineering answer and name the decisive proof.

## 4. Where must tenant isolation be enforced for GetRun?

Write a concise engineering answer and name the decisive proof.

## 5. Why is a valid worker certificate insufficient to accept WorkResult?

Write a concise engineering answer and name the decisive proof.

## 6. How should a user WatchRun stream behave after token expiry?

Write a concise engineering answer and name the decisive proof.

## 7. What risk exists when any certificate from an internal CA is trusted as any workload?

Write a concise engineering answer and name the decisive proof.

## 8. Why must trace baggage never become an authorization source?

Write a concise engineering answer and name the decisive proof.

## 9. How should wrong-tenant resources appear under concealment policy?

Write a concise engineering answer and name the decisive proof.

## 10. Which identities should an audit record capture for a delegated call?

Write a concise engineering answer and name the decisive proof.

## 11. What must be tested during signing-key or certificate rotation overlap?

Write a concise engineering answer and name the decisive proof.

## 12. Define cross-language security equivalence for one denied mutation.

Write a concise engineering answer and name the decisive proof.

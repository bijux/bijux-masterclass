# Worked answers — Secrets, credentials, artifact trust, and policy gates

These answers are reference reasoning, not phrases to memorize. A different answer is acceptable only when it preserves the same ownership, compatibility, and evidence constraints.

## 1. Why is a Kubernetes Secret not necessarily the source of secret truth?

It may be a projection created from encrypted Git, an external secret manager, or runtime retrieval. The source authority, rotation owner, decryption key, and workload consumption path may live elsewhere. Treating the Kubernetes object as the complete lifecycle hides important failure and recovery boundaries.

## 2. What is the main authority trade-off of decrypting SOPS data inside the GitOps controller?

Plaintext remains close to the target cluster and CI need not see it, but the controller gains access to the decryption key and plaintext for every scoped document. Its compromise blast radius, caches, logs, and multi-tenant boundary therefore require careful design.

## 3. Why can an ExternalSecret be Ready while the application still uses an old credential?

Ready may prove that the operator reconciled the target Secret. The workload may read environment variables only at process start, cache the credential, or fail to reload projected files. Rotation evidence must include workload adoption and successful use of the new version.

## 4. Why should image automation write credentials differ from source read credentials?

Read-only reconciliation should not be able to alter history. Automation that proposes updates needs write access only to bounded paths or branches. Separating credentials reduces the impact of controller compromise and prevents an application reader from becoming a release author.

## 5. What does a valid artifact signature fail to prove?

It does not prove the signer is an authorized builder, the source and workflow are expected, the artifact passed tests, vulnerabilities are accepted, or the subject is not revoked. Signature verification is one input to a broader trust policy.

## 6. Why are policy gates needed at more than one layer?

Review-time gates see source and evidence before change; admission sees the actual object submitted; runtime observation detects drift and outcome. No layer has every fact. Layering is justified when each gate owns a distinct observation, not when logic is copied inconsistently.

## 7. What does `not-executed` communicate?

The required tool or environment was unavailable, so the claim lacks evidence. It is not equivalent to pass or fail. Environment policy decides whether missing evidence blocks promotion. Recording it honestly prevents synthetic success.

## 8. Why is secret rotation a release process?

It changes authority across the secret provider, delivery controller, Kubernetes projection, workload process, and external service. Overlap, adoption, revocation, rollback, and recovery must be ordered. Merely updating a manifest does not establish completion.

## 9. How can rendered-manifest caching leak secrets?

If decryption occurs before caching, the cache, diff, UI, logs, or support bundle may store plaintext. The system must avoid caching plaintext where possible, scope access, encrypt storage, and redact structurally. A simple string replacement is not sufficient.

## 10. Why should a migration Job not receive the database owner credential?

Its task is narrower than database administration. A dedicated role can permit only the required schema or data operation and can be revoked afterward. Owner credentials increase blast radius and make compromise or accidental destructive behavior much worse.

## 11. How can admission mutation create a GitOps loop?

Admission changes a field after the controller applies it; the controller compares live state with source and writes the original value again; admission mutates again. Align field ownership or configure a precise ignore rule so the mutation has one authoritative owner.

## 12. Design a policy result for a candidate whose artifact signature passes but native cluster admission was unavailable.

The signature sub-gate passes. The cluster-admission evidence is `not-executed`. The overall production result should be blocked or review-required according to policy, not pass. The report must preserve both component outcomes and the reason the environment-backed check was unavailable.

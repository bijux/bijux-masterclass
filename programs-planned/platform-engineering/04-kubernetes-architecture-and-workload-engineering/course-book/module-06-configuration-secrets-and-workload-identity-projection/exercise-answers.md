# Worked answers

## 1. Why is a Secret not secure merely because it is a Secret object?

Secret data is base64-encoded, not encrypted by that representation. Security depends on API/RBAC access, etcd encryption, audit/log handling, node projection, transport, and application use. Course 4 verifies projection contracts and non-leakage; Course 8 owns enforcement and rotation. The object kind alone is not a confidentiality proof.

## 2. Which configuration delivery forms update without restarting a container?

Projected ConfigMap/Secret volume content can update eventually, except subPath mounts; environment variables and command arguments are fixed at container start. Even when a file changes, the application may not reload it. Evidence must separate source-object update, kubelet projection, and process adoption.

## 3. Why use immutable content-addressed ConfigMap names?

They make configuration identity stable and force an explicit Pod-template change for adoption. This avoids hidden in-place mutation and simplifies rollback. The cost is object lifecycle management and rollout. The content digest is an identity aid, not a security signature.

## 4. Why set automountServiceAccountToken false?

Most application containers do not need the Kubernetes API. Avoiding default token projection reduces credential exposure and accidental authority. Workloads that need API access should receive a separate ServiceAccount, least-privilege RBAC, and an explicit short-lived audience-bound token.

## 5. What must a service-account token consumer validate?

Issuer, signature, audience, expiry, not-before if present, and subject/identity mapping. It must not accept a token minted for another audience. The consumer also needs a key-rotation strategy. Possessing a syntactically valid JWT is not sufficient authorization.

## 6. Why is Downward API data not a remote authorization credential?

Pod name, UID, labels, and namespace are local context projected by kubelet. A process can report them, but a remote system needs cryptographic workload identity and policy. Downward API is useful for logs, metrics, and configuration, not as proof to another trust domain.

## 7. What is the danger of mounting a registry pull secret into the application?

It transfers image-distribution authority into the workload, allowing the application or an attacker to pull/push registry content beyond its runtime need. The kubelet/runtime should use image-pull credentials; application runtime identity and registry authority remain separate.

## 8. How can a projected directory still expose a mixed configuration version?

Kubelet manages projection updates, but the application may read several files across an update boundary or cache some old values. Use a version marker, validate the whole set, and adopt atomically in memory. Do not assume filesystem projection creates an application-level transaction.

## 9. Why should secret checksums not be placed in visible annotations?

A checksum may enable offline guessing for low-entropy secrets and creates a durable correlator. It also encourages release systems to read secret values broadly. Use secret version/reference identity and rotation policy; if a checksum is unavoidable, assess entropy and exposure carefully.

## 10. What proves a secret rotation completed?

The source version changed, the projected value changed, the process adopted the new version, dependent authentication succeeded, old credentials were retired after overlap, and no stale replicas remain. A changed Secret resourceVersion proves only the first stage.

## 11. Why must the controller reopen a projected token?

Projected service-account tokens rotate. A client that reads once and caches forever eventually sends an expired token. Libraries should reload from the file or use an in-cluster client that supports rotation. The proof should cross a rotation boundary, not only authenticate immediately after startup.

## 12. Who owns configuration reload failure?

Kubernetes owns object storage and projection according to its semantics; the application owns validation and adoption. A platform may trigger restart or signal. The incident report should identify the failed transition rather than saying broadly “ConfigMap update failed.”

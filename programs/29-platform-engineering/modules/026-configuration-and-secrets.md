---
module_id: PLAT-026
program: Platform Engineering
level: 1
module_number: 26
title: Configuration and Secrets
status: complete
last_verified: 2026-09-02
---

# Configuration and Secrets

## One-Page Review

### Governing question

How should a platform deliver configuration and credentials to workloads so that ownership, confidentiality, validation, propagation, rotation, rollback, revocation, and evidence remain explicit from source to running process?

### Essential definitions

- **configuration** is non-secret input that selects an application's behavior without changing its executable artifact.
- A **ConfigMap** is a namespaced Kubernetes API object for small non-confidential UTF-8 or binary key-value data.
- A **Secret** is a namespaced Kubernetes API object intended for small confidential values; base64 representation is encoding, not encryption.
- A **binding** connects a named configuration or credential source and version to a workload, container, key, delivery mechanism, path or variable, reload behavior, and owner.
- **projection** is kubelet delivery of ConfigMap, Secret, downward API, service-account token, trust-bundle, or certificate material as files in a pod volume.
- **materialization** copies a value from an authority into another store or runtime surface, creating an additional copy with its own policy and lifecycle.
- **rotation** issues or selects replacement credential material; **reload** makes a consumer use it; **revocation** causes old material to stop authorizing access.
- An **immutable configuration object** forbids data mutation and is replaced under a new identity when content changes.
- **secret zero** is the initial trust mechanism by which a workload authenticates to a credential authority without already possessing the target credential.
- **blast radius** is the set of identities, workloads, namespaces, systems, environments, and time intervals exposed by compromise or erroneous configuration.

### Central model, mechanism, or theorem

Model a binding as $B=(S,V,K,C,D,T,R,A,O,L,X)$: authoritative source $S$, version $V$, selected keys $K$, consumer/container $C$, delivery surface $D$, transformation $T$, refresh and reload contract $R$, access and confidentiality controls $A$, observations $O$, lifecycle $L$, and declared exceptions $X$. The process-effective value at time $t$, $E(t)$, may differ from the source value $S(t)$ because reconciliation, projection, polling, process reload, and connection renewal introduce separate transitions. A safe change requires source authenticity, schema validity, authorized delivery, bounded propagation, successful activation, observable use, reversible rollout, and retirement or revocation of the previous value.

### Critical invariants

- Every datum is classified before storage: public configuration, internal configuration, confidential value, credential, private key, trust anchor, or regulated material.
- Images and workload specifications contain references and defaults, never live credentials or environment-specific secret values.
- ConfigMap never carries confidential data; Secret data is not considered protected merely because it is base64-encoded or stored in the Secret API.
- Each workload receives only selected keys in only the containers that need them; pod-creation authority and interactive debug paths are included in the access model.
- The delivery mechanism matches change semantics: environment variables require pod replacement, projected files require application reload, and `subPath` projections do not receive source updates.
- Mutable in-place change is never the only rollback mechanism; immutable content-addressed or versioned bindings make rollout identity and rollback explicit.
- Rotation is complete only when new material is issued, distributed, loaded, verified, and old material is revoked after a bounded overlap.
- At-rest encryption, transport protection, RBAC, admission policy, audit, node/runtime protection, application memory/logging discipline, and downstream authorization are separate controls.
- External secret stores reduce some persistence but do not remove node, pod, provider, CSI driver, application, telemetry, or availability risks.
- Missing, malformed, stale, unauthorized, expired, and revoked values fail according to an intentional startup and runtime policy with non-secret evidence.

### Common failures

Committing base64 secrets; building environment configuration into images; putting credentials in ConfigMaps, command arguments, annotations, or logs; granting broad `get`, `list`, or pod-creation rights; using `envFrom` for oversized secret scope; expecting environment variables or `subPath` mounts to update; mutating shared ConfigMaps without coordinated reload; rotating a source without reloading clients; deleting an old key before overlap verification; syncing an external secret into Kubernetes without accounting for the extra copy; treating encryption at rest as end-to-end protection; exposing secrets in shell history or CI output; making every dependency optional; and debugging by printing live values.

### Compact example

A payments worker uses an immutable, version-named ConfigMap for validated routing policy and a projected external-store volume for a short-lived database credential. The Deployment template records the configuration digest, so policy changes create a visible rollout and can return to the previous object. Workload identity is the secret zero; the provider authorizes only the exact path. The process watches the credential file, opens and validates the atomically replaced content, establishes new connections, reports the credential version as a one-way identifier, and drains old connections. Rotation metrics distinguish provider issuance, node projection, process reload, downstream acceptance, and old-version use; revocation occurs only after the maximum overlap and an emergency path can revoke immediately.

### Connections

Retrieve declarative ownership and conditions from [PLAT-023](023-kubernetes-declarative-resources.md), pod/container and rollout behavior from [PLAT-024](024-pods-workloads-and-controllers.md), network paths from [PLAT-025](025-services-and-ingress.md), runtime isolation from [PLAT-022](022-runtime-isolation-and-resource-controls.md), image provenance from [PLAT-021](021-container-images-as-platform-artifacts.md), and cryptography, identity, delivery pipelines, and reliability from their specialist programs.

## Governing Question

What is the authoritative source for each setting or credential, who may change and consume it, how does it reach a particular process, when does that process begin using a new version, and what evidence proves activation, rollback, rotation, and revocation without disclosing the value?

Kubernetes provides useful transport objects, not a complete configuration or secrets-management system. A value commonly moves through authoring, review, storage, API admission, reconciliation, node projection, container namespace, process parsing, connection establishment, telemetry, backups, and incident tooling. Each surface can preserve, transform, cache, leak, or reject it.

The platform contract must therefore cover both control-plane objects and process behavior. “The Secret was updated” states only that one API write succeeded. It does not prove that a node observed the write, a volume changed, the application reopened the file, a connection adopted the credential, or the relying system accepted it.

## Why This Matters

Separating an immutable application artifact from deployment configuration enables one reviewed image to run in many environments. Poor separation instead produces environment-specific images, manual edits, divergent rollbacks, and credentials embedded in layers that remain recoverable after deletion.

Configuration failures can be as severe as code failures. A malformed rate limit can deny every request. A wrong endpoint can send regulated data to the wrong system. A feature gate can activate incomplete behavior globally. A stale trust bundle can cause a regional outage. These are typed, governed changes, not harmless strings.

Secrets add adversarial pressure. Copies can appear in Git history, CI logs, terminal history, API audit bodies, etcd backups, controller caches, node storage, crash dumps, environment inspection, support bundles, application logs, traces, and downstream databases. Confidentiality depends on minimizing materialization and authority, not on naming an object `Secret`.

Rotation also changes availability. A replacement password is useless until clients load it; immediate invalidation can break old connections, while excessive overlap preserves stolen credentials. The platform must make the rotation state machine and its evidence routine before an incident requires it.

## Prerequisites and Retrieval

Retrieve process environments, files, permissions, symbolic links, atomic rename, polling and file notification, serialization, schema validation, hashes, encryption, keys, certificates, identity, authentication, authorization, RBAC, namespaces, service accounts, pods, volumes, controllers, rollouts, eventual consistency, caching, connections, logs, metrics, tracing, backups, and incident response.

You should distinguish encoding, encryption, hashing, signing, and redaction; data at rest, in transit, and in use; desired, observed, and process-effective state; an identifier from a secret value; and credential issuance from authorization at the relying service.

## Learning Objectives

After completing this module, you should be able to:

1. classify configuration and secret material by confidentiality, authority, scope, lifetime, and impact;
2. design ConfigMap and Secret resources with explicit keys, immutability, ownership, and size boundaries;
3. choose environment, argument, volume, projected-volume, API, sidecar, or external-store delivery from application semantics;
4. explain propagation behavior for environment variables, ordinary projected files, `subPath`, caches, and application reload;
5. design least-privilege RBAC, pod authority, namespace, node, admission, audit, and encryption-at-rest controls;
6. distinguish external secret-store mounting from synchronization and analyze each materialized copy;
7. implement rotation, overlap, reload, verification, revocation, rollback, and emergency recovery; and
8. diagnose configuration and credential failures without printing confidential data.

## Core Exposition

### Inventory and classify before choosing an object

Begin with a data-flow inventory. For every input, record the authority, human and machine writers, consumers, environments, data classification, schema, legal constraints, expected size, change rate, required freshness, failure behavior, rollback unit, retention, and deletion obligations.

Do not infer confidentiality from familiar names. An endpoint may reveal internal topology. A feature flag may expose a security control. A CA bundle is normally public trust material, while a private key is secret. A database username may be internal configuration, yet a combined connection URI contains a password. Split fields so each gets the narrowest suitable control.

Credentials deserve additional fields: subject, audience, privileges, issuer, issue time, expiry, rotation interval, revocation mechanism, maximum overlap, and compromise response. Prefer identity-based, short-lived credentials over static shared strings where the relying system supports them.

### Separate artifact, deployment configuration, and live control

An image should contain executable code, static assets, parsers, safe defaults, and documentation of its configuration schema. Deployment configuration selects environment-specific endpoints, limits, policies, and integrations. Live control changes high-frequency operational decisions through a purpose-built API or controller with validation and audit.

Not every value belongs in a ConfigMap. Large datasets, rapidly changing coordination state, durable business data, or values requiring transactional updates need an appropriate service or database. Kubernetes documents a 1 MiB limit for an individual ConfigMap; practical watch, API, and memory costs argue for much smaller objects.

Command-line arguments are visible in workload specifications and commonly in process inspection, so they are unsuitable for credentials. Environment variables are simple and portable but form a process-start snapshot and may be included by debugging or crash tooling. Files support structured documents and controlled permissions, and can change, but only applications designed to reopen them benefit.

### Model ConfigMaps precisely

A ConfigMap has `data` for UTF-8 strings and `binaryData` for base64-represented arbitrary bytes; keys cannot overlap. It is namespaced, and ordinary pod references require the ConfigMap in the pod's namespace. It has no secrecy property.

Use explicit keys with stable meaning. A single file-like key can preserve the native syntax of a validated application document; individual keys enable narrow references. Avoid one global ConfigMap shared across unrelated workloads because its ownership, rollout, and blast radius become inseparable.

Set `immutable: true` for configuration released as a versioned artifact. A content change then creates a new object name, such as `checkout-policy-<digest>`, and a workload-template change selects it. This prevents silent in-place drift, reduces watches, supplies rollout identity, and retains a direct rollback target. Garbage collection must keep every version referenced by live or rollbackable workloads.

Mutable ConfigMaps suit explicitly reloadable, bounded-scope settings. Their schema, propagation bound, partial-update behavior, reload failure, last-known-good state, and rollback must still be defined. The API accepting bytes does not prove the application can parse them.

### Treat Kubernetes Secrets as a transport boundary, not a vault claim

A Secret separates confidential bytes from a pod specification and supports selective delivery, but its data is base64-represented and Kubernetes warns that backing storage is unencrypted by default unless operators configure encryption at rest. API readers, etcd access, backups, node/runtime authority, and consuming processes remain important.

Use a specific Secret type when it adds validation or communicates intent, such as TLS, Docker registry, basic authentication, SSH authentication, or bootstrap token. `Opaque` remains appropriate for application-defined material. `stringData` is a write convenience that the API merges into encoded `data`; it is not safer storage.

Never commit a live Secret manifest. Declarative workflows can commit encrypted ciphertext or an external reference only when key custody, decryption identity, review metadata, recovery, and rotation are designed. Repository deletion does not erase history or replicas.

Secret objects also have a size limit of 1 MiB, but security argues against using them as archives. Keep keys narrow, avoid credential bundles shared by many applications, and separate lifecycles that rotate independently.

### Make every workload binding explicit

A binding should name source object and key rather than importing everything with `envFrom`. Explicit `configMapKeyRef`, `secretKeyRef`, and projected `items` document the actual dependency and limit accidental exposure when a source later gains another key.

Mount a volume only into containers that need it. Containers in one pod share important trust boundaries, but volume mounts can still prevent an unrelated sidecar from directly reading a credential. Account for privileged sidecars, ephemeral containers, process tracing, shared process namespaces, and node-level access in the threat model.

Mark secret and configuration mounts read-only, choose paths that do not obscure image content, and set the narrowest usable file mode. File mode is not authorization against a process with sufficient pod or node privilege. Never copy projected material to a writable shared volume merely for convenience without governing that additional copy.

Missing required inputs should normally prevent startup with a clear non-secret condition. The `optional` flag is correct only when the application has a safe, tested fallback. Optional credentials can silently disable authentication or route traffic to an unintended default.

### Understand snapshot and projection semantics

Environment variables and container arguments are resolved when the container starts. Updating the ConfigMap or Secret does not mutate the environment of a running process. A controller must replace pods, usually through a workload-template change such as a source digest annotation.

ConfigMap and Secret volumes are projected by kubelet. Mutable source updates eventually appear after watch/cache propagation and kubelet synchronization. The application must reopen the path; a process holding an old file descriptor or reading once at startup retains old content. Kubernetes uses atomic projection structures, so watching only the underlying inode can miss replacement; watch the directory or poll and reopen according to the application contract.

A volume mounted with `subPath` does not receive projected updates. Treat it as startup-only input or change the mount layout. Projected volumes can combine sources into one directory, but all sources must share the pod namespace and path collisions or overly broad aggregation should be avoided.

The effective state chain is:

$$
S(t) \rightarrow A(t) \rightarrow K_n(t) \rightarrow F_p(t) \rightarrow E_p(t) \rightarrow U_p(t)
$$

where $S$ is authoritative source, $A$ admitted API state, $K_n$ node-observed state, $F_p$ projected file or startup snapshot, $E_p$ parsed process state, and $U_p$ downstream use. Each arrow has independent latency and failure.

### Choose reload or rollout intentionally

Rollout on change is simple and makes a new ReplicaSet or equivalent controller revision observable. It is appropriate for startup-only libraries, environment injection, structural configuration, or applications without reliable reload. It consumes surge capacity and can amplify a bad global change, so validate first and stage promotion.

In-process reload reduces disruption and supports fast rotation. Implement parse-then-validate-then-swap: read a coherent replacement, validate schema and semantics, build dependent state, atomically publish it to new operations, preserve old state for in-flight work, and report success. On failure, continue with last-known-good content where safe and expose a redacted condition.

Do not mix reloadable and restart-only keys in one mutable object without defining which action wins. The binding inventory below makes lifecycle decisions visible.

<!-- bijux-verify: {"id":"configuration-binding-inventory","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"bindings=7\nconfidential=4\nrestart_required=3\nreload_capable=4\nshort_lived=2\nimmutable=2\nowners=4\n","stderr":""}} -->
```python
bindings = [
    {"name": "ui-settings", "confidential": False, "delivery": "volume", "reload": True, "short": False, "immutable": False, "owner": "web"},
    {"name": "routing-policy", "confidential": False, "delivery": "environment", "reload": False, "short": False, "immutable": True, "owner": "payments"},
    {"name": "database-password", "confidential": True, "delivery": "csi-volume", "reload": True, "short": True, "immutable": False, "owner": "payments"},
    {"name": "partner-api-key", "confidential": True, "delivery": "environment", "reload": False, "short": False, "immutable": True, "owner": "integrations"},
    {"name": "tls-certificate", "confidential": True, "delivery": "volume", "reload": True, "short": False, "immutable": False, "owner": "edge"},
    {"name": "service-token", "confidential": True, "delivery": "projected", "reload": True, "short": True, "immutable": False, "owner": "payments"},
    {"name": "region", "confidential": False, "delivery": "environment", "reload": False, "short": False, "immutable": False, "owner": "web"},
]
print(f"bindings={len(bindings)}")
print(f"confidential={sum(item['confidential'] for item in bindings)}")
print(f"restart_required={sum(not item['reload'] for item in bindings)}")
print(f"reload_capable={sum(item['reload'] for item in bindings)}")
print(f"short_lived={sum(item['short'] for item in bindings)}")
print(f"immutable={sum(item['immutable'] for item in bindings)}")
print(f"owners={len({item['owner'] for item in bindings})}")
```

The fixture is a design inventory, not evidence that delivery, confidentiality, reload, expiry, ownership, or downstream acceptance works in a real cluster.

### Design a complete secret control set

Protect API storage with an encryption-at-rest configuration whose first matching provider actually encrypts. Envelope encryption can keep key-encryption operations in an external KMS and reduce key material in the API server. Disk encryption alone and API-layer encryption address different threats.

Enabling encryption affects new writes; existing objects must be rewritten or migrated and verified in backing storage. Encryption keys themselves need restricted custody, backup, availability, rotation, and disaster recovery. Losing a decryption key can make every protected object unavailable.

Use least-privilege RBAC. `list` and `watch` reveal Secret content, not merely names. A subject able to create a pod in a namespace can often cause that pod to mount namespace Secrets even without direct `get`, so pod creation, workload-controller creation, exec, debug/ephemeral containers, and service-account impersonation belong in the same authorization analysis.

Separate tenants and trust domains with namespaces and dedicated service accounts. Admission policy can reject plaintext-looking secret manifests from unsuitable paths, privileged consumers, mutable high-risk bindings, wildcard imports, or prohibited credential types. Audit metadata and access patterns, but configure request/response auditing so it does not become a secret archive.

Protect etcd transport and backups, control node access, disable unnecessary service-account token automounting, use bounded-audience projected tokens, and constrain egress. After delivery, the application must avoid logs, metrics labels, traces, errors, crash reports, heap dumps, and support bundles containing values.

### Use workload identity as secret zero

Prefer a platform-issued workload identity that is bound to pod, service account, audience, and lifetime. Kubernetes projected service-account tokens expire and are rotated by kubelet; an explicit projection can set the intended audience and requested lifetime. Long-lived service-account token Secrets are discouraged.

The target secret system validates the token and maps the authenticated workload identity to narrow policy. This avoids distributing one static bootstrap password to every workload. It does not eliminate trust: token issuer, admission, service-account assignment, provider integration, node, and network path must be protected.

Disable automatic API tokens for workloads that do not call an identity-aware service. Where a token is needed, mount it only into the consumer, validate audience at the recipient, and ensure the application reopens the rotated file.

### Compare external-store delivery patterns

An application can call an external secret API directly, an agent/sidecar can render files, a CSI driver can mount provider content, or an operator can synchronize provider values into Kubernetes Secrets. Each changes availability, portability, application complexity, policy, and copies.

Direct API retrieval offers explicit leases and renewal but couples application code and startup to the provider. An agent separates provider logic but shares pod resources and becomes a lifecycle dependency. The Secrets Store CSI Driver asks a provider through node-local components and mounts content as a volume when a pod starts; optional auto-rotation can update the mount when both driver and provider support it.

Synchronizing as a Kubernetes Secret enables environment variables and APIs that require native Secret objects, but deliberately creates a Kubernetes copy. In the CSI driver's sync mode, the volume mount is required, synchronization begins only with a consuming pod, and the synced Secret is removed when no consuming pods remain. Treat those semantics as part of availability and ownership, not as a universal secret controller.

External storage does not automatically protect the final file, process memory, logs, provider credentials, or compromised node. It also adds provider, plugin, network, quota, and regional failure modes. Decide whether workloads may start from cached material, remain on last-known-good values, or fail closed during provider outage.

### Make rotation a state machine

Represent rotation as:

$$
q_0\ \text{old active} \rightarrow q_1\ \text{new issued} \rightarrow q_2\ \text{both accepted} \rightarrow q_3\ \text{new distributed} \rightarrow q_4\ \text{new loaded} \rightarrow q_5\ \text{new verified} \rightarrow q_6\ \text{old revoked}.
$$

The overlap interval satisfies

$$
T_{overlap} \ge T_{reconcile}+T_{project}+T_{reload}+T_{connection}+T_{verify}+M,
$$

where $M$ is an uncertainty margin. Shorten each component with bounded automation rather than pretending overlap is zero. Some systems cannot accept two passwords; rotate through new users, keys, certificates, or trust bundles where possible.

Measure versions using safe identifiers such as resource versions, certificate serials, key IDs, or hashes that cannot feasibly reveal low-entropy values. Never publish a raw secret or a reversible transformation. Verify downstream authorization with a real bounded operation, not merely a successful file read.

Emergency compromise may skip graceful overlap: revoke immediately, accept controlled availability loss, replace secret zero if affected, investigate access, and issue new credentials. Practice both routine and emergency procedures.

### Coordinate trust-anchor and certificate changes

Trust anchors are configuration, not private secrets, but integrity is critical. Rotate trust before identity: distribute a bundle containing old and new issuers, verify consumers load both, issue identities from the new issuer, migrate use, then remove the old trust anchor after all legitimate old identities expire or are revoked.

Certificates and private keys must be loaded as a coherent pair. Prefer a single atomically projected credential bundle when supported, or ensure separate reads cannot straddle a rotation. TLS servers and clients must rebuild contexts and connections; file replacement alone leaves existing processes or sessions on old material.

Observe certificate identity, issuer, serial, validity window, reload success, handshake failures, and old-version connections without exporting private keys. Namespace-readable public trust does not imply that private signing material should share the same object or authority.

### Validate configuration before and during rollout

Define a machine-readable schema plus semantic checks for ranges, mutually exclusive fields, references, protocols, and environment policy. Validate at authoring and CI, at API admission where appropriate, and again in the application because consumers remain the final interpreter.

Render and diff references, not secret values. A change report can state source identity, key names, schema version, digest, consumers, risk class, rollout policy, and approvals. For confidential content, validate shape and provider metadata without exposing bytes to reviewers who do not need them.

Promote configuration through the same environments and workload revisions used in production. Canary high-risk changes, observe process-effective version and outcomes, then expand. Rollback selects a known-good immutable source or restores last-known-good parsed state; it must not depend on reconstructing unknown prior bytes from memory.

### Observe without disclosure

Useful signals include desired reference, admitted resource version, projected version, process-effective digest or key ID, age, expiry horizon, reload attempts and failures, stale-consumer count, provider latency/errors, denied access, rotation state, old-version use, and downstream authentication results.

Keep cardinality bounded and exclude secret values from labels and messages. Redaction must cover structured logs, nested errors, HTTP headers, URLs, database connection strings, environment dumps, command traces, and controller events. Test redaction with seeded canary values that are not real credentials.

Expose status at the binding level: `SourceReady`, `Projected`, `Loaded`, `Accepted`, `Fresh`, and `RevokedOld` should not collapse into one green indicator. Alert on imminent expiry, persistent version skew, failed reload, unexpected access volume, synchronization absence, and use after revocation.

### Diagnose by walking the binding chain

Start with symptoms, affected revisions, nodes, tenants, and time. Identify the expected source/version and delivery mechanism without retrieving the value. Check source existence and provider health, authorization, admission, controller/CSI status, pod events, node placement, mount metadata, safe file owner/mode/mtime/size, process-effective identifier, reload errors, and downstream rejection reason.

For environment injection, compare pod creation time and template digest with source version; do not wait for an update that cannot occur. For volume injection, check ordinary mount versus `subPath`, kubelet/driver propagation, file replacement, and whether the process reopened it. For external providers, distinguish identity denial, provider/network outage, missing object/version, mount failure, rotation poll failure, and application rejection.

Never begin with `kubectl get secret -o yaml`, `env`, `set -x`, `cat`, or copying a production credential into a ticket. Use metadata, hashes only when safe against brute force, and purpose-built probes. If value inspection is unavoidable, use an approved break-glass path with minimal audience, no durable output, immediate rotation, and audit.

### Govern the platform product

Offer supported binding classes rather than unlimited mechanisms: immutable rollout configuration, reloadable file configuration, native Secret projection for bounded legacy use, short-lived workload identity, external-store file projection, and certificate/trust-bundle delivery. Each class specifies owners, threat model, namespaces, policies, reload interface, freshness objective, observability, limits, and recovery.

Provide libraries or sidecars only when their lifecycle and security burden is lower than every team implementing reload independently. Standardize a safe readiness contract: a workload should not become ready until required configuration parses and required credentials can establish their intended dependency, while transient provider outage should not unnecessarily evict a process using valid cached material.

Maintain inventories from sources to consumers and from consumers back to sources. This enables impact analysis, rotation campaigns, orphan cleanup, breach response, and expiry forecasting. Ownership must persist when teams change; unowned credentials and configuration are production defects.

## Definitions and Notation

Let $S_i(t)$ be authoritative source version $i$ at time $t$, $A_i(t)$ its admitted representation, $F_{i,p}(t)$ the bytes projected or snapshotted for pod $p$, and $E_{i,p}(t)$ the value effectively used by its process. Generally,

$$
S_i(t)=A_i(t) \not\Rightarrow F_{i,p}(t)=E_{i,p}(t)=S_i(t).
$$

For binding $b$, define principals with direct read authority $R_b$, principals able to cause a consuming workload $W_b$, containers receiving material $C_b$, persistent copies $P_b$, and valid-use interval $I_b$. Its access blast radius can be reasoned about as

$$
\mathcal{B}_b=R_b\cup W_b\cup C_b\cup P_b,
$$

with time exposure bounded by $I_b$ only when expiry or revocation is enforced by the relying system.

Define the rollout-ready predicate

$$
Ready_b=SourceReady_b\land Authorized_b\land Projected_b\land Parsed_b\land Accepted_b\land Fresh_b.
$$

No one conjunct proves the others. `Projected` means bytes reached a runtime surface; `Accepted` means the intended dependency accepted use; `Fresh` means policy permits the age/version.

For routine rotation, old and new credentials coexist during $[t_a,t_r)$, where $t_a$ is new acceptance and $t_r$ old revocation. A consumer is migrated only after $E_{new,p}$ is observed and a relying operation succeeds.

## Mechanisms, Invariants, or Proof Structure

The mechanism is a reconciled binding chain. An authority publishes a version; policy admits a reference or encrypted representation; a controller or kubelet delivers it; the application validates and atomically activates it; downstream systems accept its use; observers compare desired and effective version; lifecycle automation retires the former version.

The **classification invariant** maps each datum to a storage and delivery class before it exists in deployment state. The **least-materialization invariant** creates no copy without a named purpose, controller, access policy, retention, and deletion behavior. The **least-authority invariant** includes indirect pod/workload creation as well as direct reads.

The **activation invariant** requires parse and semantic validation before a new value affects work. The **coherence invariant** activates related values as one unit, preventing key/certificate or endpoint/credential mismatches. The **freshness invariant** bounds how long effective state may trail desired state.

The **rotation invariant** keeps the old credential valid until all intended consumers demonstrate new use, except during explicit emergency revocation. The **rollback invariant** retains a known-good identity and application state. The **non-disclosure invariant** permits lifecycle evidence without exporting secret bytes.

This is an assurance argument, not a proof that an implementation is secure. It depends on the cluster, provider, node, runtime, application, relying service, identity, cryptography, policies, and operations satisfying their stated assumptions.

## Alternatives and Trade-Offs

Environment variables maximize compatibility and simplicity but are startup snapshots, flat strings, and common debug surfaces. Projected files support structured data and rotation but require correct watch/reopen logic. Direct API reads offer immediate watch semantics and cross-namespace possibilities under authorization, but couple applications to Kubernetes and expand API credentials.

Mutable sources reduce object churn and enable reload, but weaken rollout identity and can change many consumers simultaneously. Immutable versioned sources improve audit, canary, rollback, and cache behavior at the cost of object lifecycle and explicit workload changes.

Native Secrets are portable and integrate with workloads, image pulls, and controllers, but persist through the Kubernetes API and its backups. External stores centralize issuance, lease, policy, and rotation, but add provider integrations and runtime availability dependencies. Synchronization improves compatibility while recreating native persistence; mounting avoids that copy but cannot satisfy every API consumer.

Static credentials are broadly supported and tolerate issuer outages until expiry, but have long compromise windows and difficult attribution. Dynamic credentials narrow lifetime and subject but require reliable identity, issuance, renewal, reload, and revocation. Certificates support strong identity and rotation but add trust-bundle and connection-lifecycle complexity.

Fail-closed startup protects against unsafe defaults but can amplify provider outages. Last-known-good operation preserves availability while a still-valid credential/configuration exists, but must bound staleness. The correct choice depends on whether stale use or absence causes greater harm, and it must be explicit per binding.

## Failure Modes and Misconceptions

- **“A Kubernetes Secret is encrypted.”** Its API representation uses base64; configure and verify encryption at rest and protect every other surface.
- **“RBAC denies `get`, so the user cannot read it.”** Workload creation in the namespace may provide indirect mounting authority; `list`, `watch`, exec, debug, and impersonation also matter.
- **“The source changed, so applications rotated.”** Environment variables never update in place; files require projection and reload; existing connections may still use old state.
- **“A file watcher guarantees reload.”** Atomic symlink replacement, inode watches, partial reads, parse failures, and application state swaps must be handled deliberately.
- **“`subPath` gives one clean file and still updates.”** Kubernetes projected `subPath` mounts do not receive source updates.
- **“External storage means the secret is not in the cluster.”** It reaches node/plugin memory, a pod volume, and application memory; sync mode also creates a Kubernetes Secret.
- **“Short expiry automatically reduces risk.”** A recipient that ignores expiry, a renewal loop that never reloads, or an always-valid bootstrap identity defeats the intended bound.
- **“Rotation means overwriting a value.”** Safe rotation coordinates dual acceptance, distribution, activation, verification, connection transition, and revocation.
- **“All configuration belongs in Git.”** Live credentials, high-frequency control state, large data, and regulated material need purpose-built authorities; Git may hold reviewed references or encrypted forms under policy.
- **“Optional input improves resilience.”** It may select unsafe defaults or unauthenticated behavior; use it only with a defined fallback.
- **“A checksum is always safe telemetry.”** Hashes of low-entropy secrets can enable guessing; prefer provider key IDs or keyed/non-reversible identifiers designed for observation.
- **“Printing the value is the fastest diagnosis.”** It spreads the incident into logs, chat, tickets, shell history, and support systems while rarely locating the failed lifecycle stage.

## Worked Examples

### Example 1

A web application imports forty ConfigMap keys with `envFrom` but needs six. The platform replaces it with explicit references, validates types, records the digest in the pod template, and rolls out only when those six change.

### Example 2

A team updates a database password Secret and waits, but pods use environment variables. The rotation stalls at distribution. A staged pod rollout proves new authentication before the old password is revoked.

### Example 3

A proxy mounts `policy.yaml` with `subPath` and never sees mutable ConfigMap changes. The team mounts the containing directory, watches it correctly, parses to last-known-good state, and exposes the effective digest.

### Example 4

A Secret is encrypted in new etcd writes, yet old backups contain plaintext objects. Operators migrate existing resources, verify backing representation, rotate and protect encryption keys, and update backup retention.

### Example 5

A namespace role denies Secret reads but permits Deployments with arbitrary service accounts and mounts. The security review treats workload creation as indirect read authority and narrows both permissions and admission policy.

### Example 6

A CSI-mounted API key changes at the provider and on disk, but a client library cached it. The application rebuilds its client, shifts new calls, drains old connections, verifies acceptance, and only then revokes the former key.

### Example 7

An operator syncs an external certificate into a native TLS Secret for an Ingress controller. The design records the intentional Kubernetes copy, encryption, RBAC, owner, sync dependency, reload evidence, and cleanup semantics.

### Example 8

A malformed global feature policy passes YAML parsing and disables checkout. Schema and semantic validation, canary binding, process-effective status, business-task probes, and immutable rollback contain the next change.

### Example 9

A credential provider is unavailable during node replacement. Existing pods retain valid material, while new pods cannot mount it. Capacity planning, provider objectives, cached-valid policy, and controlled rollout prevent simultaneous loss.

### Example 10

A signing key is suspected compromised. Operators use the emergency path: stop issuance, revoke the key, disable affected identity, deploy replacement trust/material, accept bounded failure, inspect access evidence, and rotate any bootstrap authority.

## Cross-Program Connections

Security engineering contributes classification, threat modeling, cryptography, identity, least privilege, audit, redaction, key custody, and incident response. Distributed systems contributes reconciliation, eventual propagation, caching, leases, consistency, and partial failure. Software engineering contributes typed schemas, validation, immutable values, dependency injection, and reload-safe state management.

Site reliability contributes objectives for freshness and issuance, staged rollout, last-known-good operation, expiry alerts, disaster recovery, and incident diagnostics. Delivery engineering contributes Git history, CI log protection, encrypted declarative workflows, promotion, and provenance. Networking contributes provider reachability, TLS sessions, and egress policy.

Data engineering contributes classification, retention, deletion, lineage, and regulated copies. API engineering contributes authentication tokens, audiences, keys, certificates, and downstream acceptance. Platform product engineering turns these into supported binding classes with safe defaults and consumer-visible status.

## References

- Kubernetes Project, [*ConfigMaps*](https://kubernetes.io/docs/concepts/configuration/configmap/), current documentation retrieved September 2, 2026. Non-confidential purpose, `data`/`binaryData`, namespace and size boundaries, consumption methods, immutable objects, volume propagation, environment snapshots, and `subPath` behavior.
- Kubernetes Project, [*Secrets*](https://kubernetes.io/docs/concepts/configuration/secret/), current documentation retrieved September 2, 2026. Secret purpose and types, data representation, limits, information-security caveats, immutable objects, pod delivery, and alternatives.
- Kubernetes Project, [*Good Practices for Kubernetes Secrets*](https://kubernetes.io/docs/concepts/security/secrets-good-practices/), current documentation retrieved September 2, 2026. Encryption at rest, least-privilege RBAC, indirect pod authority, namespace isolation, external stores, container scope, logging, and manifest handling.
- Kubernetes Project, [*Distribute Credentials Securely Using Secrets*](https://kubernetes.io/docs/tasks/inject-data-application/distribute-credentials-secure/), current documentation retrieved September 2, 2026. Key selection, file paths and modes, volume delivery, environment variables, and restart semantics.
- Kubernetes Project, [*Updating Configuration via a ConfigMap*](https://kubernetes.io/docs/tutorials/configuration/updating-configuration-via-a-configmap/), current documentation retrieved September 2, 2026. Environment, volume, sidecar, immutable ConfigMap, kubelet synchronization, and rollout behavior.
- Kubernetes Project, [*Projected Volumes*](https://kubernetes.io/docs/concepts/storage/projected-volumes/), current documentation retrieved September 2, 2026. Combined projections, namespace constraint, selected keys, file modes, service-account tokens, trust bundles, certificates, atomic projection, and `subPath` exception.
- Kubernetes Project, [*Encrypting Confidential Data at Rest*](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/), current documentation retrieved September 2, 2026. Encryption providers, provider order, KMS integration, verification, migration of existing data, key rotation, and automatic reload.
- Kubernetes Project, [*Service Accounts*](https://kubernetes.io/docs/concepts/security/service-accounts/), current documentation retrieved September 2, 2026. Workload identity, bounded token projection, audience, expiry, rotation, and risks of long-lived token Secrets.
- Kubernetes Project, [*RBAC Good Practices*](https://kubernetes.io/docs/concepts/security/rbac-good-practices/), current documentation retrieved September 2, 2026. Least privilege, namespace boundaries, privilege escalation, workload creation, token and Secret access, and impersonation.
- Secrets Store CSI Driver, [*Introduction*](https://secrets-store-csi-driver.sigs.k8s.io/), current project documentation retrieved September 2, 2026. CSI volume lifecycle, provider integration, pod mount flow, architecture, and security considerations.
- Secrets Store CSI Driver, [*Secret Auto Rotation*](https://secrets-store-csi-driver.sigs.k8s.io/topics/secret-auto-rotation), current project documentation retrieved September 2, 2026. Rotation reconciliation, mounted content, synchronized Secrets, environment restart limitation, and application reload responsibility.
- Secrets Store CSI Driver, [*Sync as Kubernetes Secret*](https://secrets-store-csi-driver.sigs.k8s.io/topics/sync-as-kubernetes-secret), current project documentation retrieved September 2, 2026. Optional native-Secret materialization, required volume consumer, supported Secret types, and lifecycle when consumers disappear.

## Exercises

### Exercise 1

Classify and design bindings for a public UI theme, internal endpoint, database password, partner API key, TLS private key/certificate, CA trust bundle, feature policy, and high-frequency traffic weight. State authority, storage, delivery, reload, rollback, evidence, and why rejected mechanisms do not fit.

### Exercise 2

Audit a namespace where developers cannot `get` Secrets but can create Deployments, use any service account, exec into pods, import `envFrom`, and mount one shared mutable Secret. The cluster uses unverified default etcd storage and verbose request auditing.

### Exercise 3

Design a zero-downtime database credential rotation for 200 pods across three regions. The application uses connection pools, the database can accept two users, and provider, projection, rollout, network, and clock delays are variable.

### Exercise 4

Diagnose a workload whose external provider shows a new credential, CSI status is healthy, the mounted path has a recent timestamp, half the requests receive authentication failures, and restarting pods temporarily repairs them. Give a value-safe evidence sequence and durable correction.

### Exercise 5

Transfer the binding model to configuration and cryptographic keys on a fleet of intermittently connected medical devices. Address authority, signed configuration, confidentiality, staged activation, expiry, offline operation, rollback, revocation, evidence, patient safety, and human control.

## Answers to the Exercises

### Answer 1

The UI theme is public configuration in a validated ConfigMap file, reloadable or immutable-rollout according to the app. The internal endpoint is configuration, but its topology sensitivity may warrant a service-discovery reference rather than copied addresses. The database password and partner API key are confidential credentials from a secret authority, preferably short-lived and identity-bound; mount files for reload-capable clients or use explicit rollout when legacy libraries require environment snapshots. The TLS private key is secret and the certificate is public identity material, delivered coherently to the exact TLS container; the CA bundle is integrity-critical public trust configuration and rotates trust-first. Feature policy is typed, immutable, canaried configuration with business-task evidence. High-frequency traffic weight belongs in a routing control API, not a ConfigMap mutation loop. Every binding records source version/key ID, consumer, owner, schema, activation, last-known-good target, freshness, and downstream outcome. Images, command arguments, unscoped `envFrom`, shared Secrets, and Git plaintext are rejected because they expand copies, authority, or lifecycle ambiguity.

### Answer 2

The direct `get` denial is ineffective as a confidentiality boundary. Deployment creation plus arbitrary service-account and volume selection permits indirect Secret consumption; exec exposes runtime material; broad `envFrom` expands every pod's copy; and a shared mutable Secret couples unrelated blast radii and rotations. Restrict workload creation to approved templates, service-account assignment, exec/debug, and Secret references; separate namespaces and service accounts; select exact keys and containers; split credentials by owner and lifecycle; and use admission to enforce binding classes. Determine whether encryption at rest is configured, then inspect backing representation and migrate existing objects rather than assuming defaults. Protect encryption keys and backups. Change audit policy to retain useful metadata and access events without request/response secret bodies, secure prior logs, and rotate any possibly recorded values. Validate node/runtime access, external delivery where suitable, redaction, expiry, rotation drills, and break-glass procedures.

### Answer 3

Issue a new database user with equivalent narrow privileges while the old user remains valid. Bind the new provider version, reconcile and project it, then have each process parse it and create a new connection pool. New requests use the new pool; old transactions finish on the former pool under a maximum connection age. Observe desired, projected, process-effective, and database-authenticated key/user identifiers by pod, region, and revision without values. Canary one region/pod set, verify real bounded reads and writes, then expand with surge and provider capacity. Choose overlap greater than worst-case provider, network, reconciliation, projection, reload, connection, verification, and clock uncertainty. Stop and roll back to the old binding on errors. After every intended consumer and long transaction has migrated, deny new old-user sessions, drain remaining sessions, revoke the old user, and alert on any subsequent use. Predefine emergency immediate revocation, compromised bootstrap rotation, and regional/provider outage behavior.

### Answer 4

The evidence suggests source issuance and file projection succeed but process activation or connection transition is incomplete. Compare provider version/key ID, CSI object/version and rotation time, mount directory target and safe metadata, process-effective identifier, reload events, client-library state, connection creation time, request failure by pod and connection, and downstream rejection of old versus new identity. Do not print or hash a guessable credential. Check whether the application reads once, watches an inode replaced atomically, fails parse silently, swaps only some workers, or retains old pooled connections. Restart repairs it because startup reads the new file. Correct the application to watch the directory or poll, reopen and validate coherent content, atomically replace the client/pool, drain old connections within bounded overlap, expose reload/effective-version status, and prove a downstream operation before revocation. Add an expiry/old-use alert and a conformance test that rotates the provider while traffic continues.

### Answer 5

An authorized clinical/device authority signs versioned configuration and issues device-unique keys through protected manufacturing or enrollment identity. Public configuration is integrity-protected; patient or private credential material is encrypted for the intended device or hardware-backed key. Devices verify signer, model, region, schema, monotonic version, activation window, dependency compatibility, and available power before staging. Activation is canaried by model and clinical setting, atomic, and followed by self-tests whose results reveal versions and outcomes but no patient data or keys. Offline devices retain a bounded last-known-good configuration and valid credential sufficient for safe essential operation; expiry policy distinguishes care continuity from network privilege. Rollback uses a signed known-good version and anti-rollback rules allow only authorized emergency exceptions. Revocation lists or short-lived credentials reconcile when connected, while urgent compromised-device isolation can deny server access immediately. Clinicians retain safe local override for patient care under audit; automation cannot silently change therapy authority. Fleet status, delayed devices, failed signature/activation, expiry, safety alarms, and human acknowledgements drive rollout and recall decisions.

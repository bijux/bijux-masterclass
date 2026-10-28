---
module_id: PLAT-036
program: Platform Engineering
level: 1
module_number: 36
title: Secret Delivery
status: complete
last_verified: 2026-09-02
---

# Secret Delivery

## One-Page Review

### Governing question

How should a platform authorize, obtain, deliver, load, rotate, revoke, observe, and retire secret material so that a workload receives only what it needs, for only as long as it needs it, without turning storage encryption, orchestration objects, logs, or bootstrap credentials into false assurances?

### Essential definitions

- A **secret** is data whose unauthorized disclosure or use can cross a security boundary, such as a password, private key, bearer token, signing key, or recovery code.
- A **secret reference** is a non-secret identifier and requested contract for material; it must not contain the payload it names.
- A **workload identity** is an attested, short-lived identity assigned to a running workload rather than copied into it as a permanent bootstrap secret.
- A **secret authority** authenticates a workload, authorizes a request, issues or retrieves material, records access, rotates versions, and revokes capability.
- A **static secret** is stored material reused until replaced; a **dynamic secret** is created on demand with bounded scope and lifetime.
- A **bearer credential** can be used by any possessor; a **proof-of-possession credential** additionally requires control of bound key material.
- **delivery** moves authorized material to a workload consumption boundary; **loading** is the application's successful adoption of that material.
- A **lease** is a renewable or expiring authorization for secret material; its expiry is not proof that every downstream session or copy disappeared.
- **rotation** introduces replacement material and migrates consumers; **revocation** makes prior capability unusable at its enforcing authority.
- A **break-glass secret** is exceptional recovery capability with independent custody, bounded activation, strong recording, and post-use replacement.

### Central model, mechanism, or theorem

Let workload $w$ present attested identity $i_w$ to secret authority $A$. For reference $r$, purpose/audience $u$, target $t$, and policy revision $p$, authorization returns secret instance $s=(k,v,\ell,e)$: kind $k$, version $v$, lease $\ell$, and expiry $e$. Safe use requires authenticated identity, least-privilege authorization, confidential and integrity-protected transport/storage, delivery to only the intended process boundary, successful load acknowledgement, redacted evidence, and a tested rotation/revocation path. Control-plane issuance is necessary evidence; it does not prove the application loaded the credential or that the old credential stopped working.

### Critical invariants

- Secret payloads never enter source control, ordinary configuration, image layers, build arguments, manifests, tickets, chat, telemetry, shell history, or durable review artifacts.
- Every reference has a secret kind, purpose, audience, target scope, owner, consumer, lifetime, rotation method, revocation authority, and retirement condition.
- Workloads authenticate with attested, short-lived identity; one reusable bootstrap credential is not copied across a fleet.
- Authorization binds exact workload identity, secret path/role, operation, target, audience, and policy revision with deny-by-default least privilege.
- Encryption at rest, in transit, and in process are separate boundaries; base64 encoding provides none of them.
- Delivery narrows exposure to required containers/processes, uses restrictive permissions, avoids argv/environment when disclosure surfaces are unacceptable, and never logs payloads.
- Desired, issued, delivered, loaded, accepted, and revoked versions are observed separately; no control-plane state substitutes for runtime proof.
- Rotation preserves an overlap window only when protocol semantics require it, proves replacement use, then revokes old capability and removes old copies.
- Expiry, renewal failure, authority outage, partial write, stale cache, and rollback have explicit fail-open/fail-closed/degraded behavior per secret purpose.
- Audit records actor/workload, reference, version metadata, policy, decision, time, target, and outcome without recording secret material.

### Common failures

Committing secrets and later deleting only the latest revision; treating base64 as encryption; granting namespace-wide Secret `list` or `watch`; mounting every secret into every container; using one cloud access key across services; placing secrets in image layers, command lines, environment dumps, exception text, or metrics labels; assuming encrypted storage protects an authorized API read; copying a secret from an external authority into additional stores without modeling exposure; rotating the source but not applications or connection pools; overwriting files non-atomically; watching an inode that projections replace; issuing short TTL credentials to applications that cannot renew; failing open on signing-key loss; revoking before replacement acceptance; retaining old keys indefinitely; and recording secret values in audit trails.

### Compact example

A payments pod is admitted with service account identity bound to namespace, account, image provenance, and production cell. It requests database role `payments-writer` for audience `orders-prod`; policy permits only that role and returns a leased credential. A local agent writes a versioned file to memory-backed storage with mode `0400`, atomically swaps the current link, and emits metadata—not values. The application opens the path, creates a new connection, proves authentication, reports loaded version, shifts new connections, drains old sessions, and acknowledges replacement. The authority then revokes the previous lease and a negative probe confirms rejection. Deployment records reference, policy, lease/version, loaded acknowledgement, and revocation evidence while no payload reaches manifests or telemetry.

### Connections

This capability separates confidential material from [PLAT-035](035-configuration-management.md), binds secret references into [PLAT-034](034-deployment-capability.md), and uses environment/workload identity boundaries from [PLAT-033](033-environment-provisioning.md). It deepens the Kubernetes primitives introduced in [PLAT-026](026-configuration-and-secrets.md) and feeds later connectivity, policy, observability, reliability, and incident-response capabilities.

## Governing Question

What durable platform contract can deliver secret capability to an authorized workload while minimizing disclosure, replay, lifetime, fan-out, and recovery risk—and while proving the application actually changed what it uses?

Secret delivery is not a file-copy problem. It is an end-to-end authorization and lifecycle protocol crossing identity, policy, authority, network, orchestrator, node, process, downstream service, observability, and human administration.

The secret's value is only one risk. A broadly reusable credential has greater blast radius than a target-bound credential. A credential valid for a year is harder to contain than one valid for minutes. A credential readable by ten components has more disclosure paths than one delivered to a single process.

The platform should make the safe route easier: references instead of values, workload identity instead of fleet bootstrap keys, narrow delivery, automatic renewal, runtime acknowledgement, redaction by construction, and complete rotation/revocation evidence.

## Why This Matters

Secrets bridge identity to authority. Disclosure can allow data access, impersonation, signing, decryption, infrastructure mutation, supply-chain compromise, or denial of service. Their protection must match the capability they unlock, not the apparent length or format of the string.

Central storage improves policy and audit but can centralize blast radius. Replicating material closer to workloads improves availability but creates more durable copies and authorities. Short lifetimes reduce the usefulness of stolen material but increase dependence on renewal and time. Every design trades exposure, availability, latency, operational complexity, and recovery.

Rotation is often falsely declared complete when a vault contains a new version. Long-lived processes may retain environment snapshots, files may update without reload, pools may preserve authenticated sessions, and a downstream system may still accept the old credential. Runtime and negative evidence are essential.

Secret incidents are also observability incidents. Logs, traces, crash dumps, support bundles, shell history, CI output, and dashboards can become secondary secret stores. Redaction should occur before emission, while response must assume any copied value is compromised.

## Prerequisites and Retrieval

Retrieve cryptographic hashes and authenticated encryption, TLS, PKI, identity and attestation, authentication versus authorization, bearer versus proof-of-possession tokens, RBAC/ABAC, namespaces and service accounts, Kubernetes Secrets and projected volumes, KMS/envelope encryption, filesystem permissions and atomic rename, process environments, leases/TTL, connection pools, certificate chains and trust bundles, audit, backup/restore, deployment rollout, telemetry redaction, incident response, and disaster recovery.

You should distinguish a secret payload from its reference and metadata; encoding from encryption; encryption at rest from access control; human identity from workload identity; identity issuance from secret authorization; storage from delivery from loading; desired version from accepted version; renewal from rotation from revocation; key rotation from data re-encryption; short lifetime from low privilege; and audit metadata from secret material.

## Learning Objectives

After completing this module, you should be able to:

1. classify confidential values and define complete secret-delivery contracts;
2. design workload authentication and least-privilege authorization without reusable fleet bootstrap secrets;
3. evaluate Kubernetes objects, environment variables, projected files, CSI, agents, APIs, and dynamic credentials;
4. protect material at storage, transport, node, process, logging, backup, and human boundaries;
5. implement atomic delivery, load acknowledgement, caching, renewal, and authority-outage behavior;
6. design overlap-safe rotation and evidence-backed revocation for passwords, tokens, certificates, and signing keys;
7. observe delivery freshness and failures without exposing values or sensitive metadata;
8. respond to disclosure by containing capability rather than merely deleting one copy; and
9. migrate and retire secrets, trust roots, policies, exceptions, and legacy bootstrap mechanisms.

## Core Exposition

### Classify the capability before storing a value

Inventory passwords, API keys, bearer tokens, private keys, encryption keys, signing keys, certificate key pairs, recovery codes, webhook secrets, connection strings, and bootstrap credentials. Classify by capability, issuer, verifier, audience, scope, lifetime, rotation, revocation, derivation, and recovery.

Not every sensitive value is a credential. Personal data, regulated records, and proprietary model/data assets need data-governance controls beyond a secret store. Public certificates and trust roots are integrity-critical configuration but not confidential; their private keys are secrets.

Avoid compound blobs. A connection URI containing host, username, and password forces public routing data and secret material through the same lifecycle. Deliver non-secret configuration separately and assemble only inside the consumer boundary.

Prefer eliminations over better storage. Workload federation can replace cloud access keys; managed identity can replace copied passwords; short-lived certificates can replace static mutual-TLS keys. A secret that does not exist cannot leak.

### Write the secret-delivery contract

Define logical reference, secret kind, issuer/authority, authorized workload selectors, operation, purpose, target/audience, scope, maximum lifetime, renewal window, version semantics, delivery mechanism, consumer path/API, file ownership/mode, reload behavior, cache policy, outage behavior, owner, rotation SLO, revocation mechanism, audit fields, recovery, and retirement.

Treat reference existence and metadata as potentially sensitive. A path may reveal customer names, account structure, privileged roles, or incident state. Limit catalog/list access separately from value retrieval.

State non-guarantees. A store does not prove safe delivery; encryption does not deny an authorized reader; TTL does not terminate established sessions; deleting an orchestrator object does not erase process memory or backups; and masking one known value does not catch transformed encodings.

Version the contract independently of payload versions. An application may migrate from a password to a certificate while retaining the same business purpose. Compatibility includes consumer parsing, reload, protocol behavior, and rollback.

### Bootstrap from workload identity

A workload must authenticate before obtaining a secret, creating the bootstrap problem. Do not solve it by placing an identical root token in every image or node. Use platform-attested identity derived from bounded runtime facts such as trust domain, cluster, namespace, service account, workload digest, node attestation, or cloud workload federation.

SPIFFE's Workload API models local attestation and delivery of short-lived X.509-SVIDs/JWT-SVIDs and trust bundles. Kubernetes projected service account tokens can bind audience and expiration. Cloud federation can exchange a platform token for scoped cloud credentials. Each mechanism still needs issuer trust, selector integrity, audience validation, time, revocation, and compromise analysis.

Separate human administration from workload access. Humans manage policy and exceptional recovery through strongly authenticated, time-bounded workflows; applications use non-human identities. CI source access must not automatically imply production secret read.

Identity itself is a high-value dependency. Monitor issuance, renewal, attestation, trust-bundle freshness, clock error, and policy selection. A healthy application endpoint does not prove identity renewal remains possible.

### Authorize least privilege at request time

Policy should bind workload identity to a precise role/reference, operation, target, audience, environment, and constraints. Prefer generated database role `orders-read` over permission to read an arbitrary key-value hierarchy.

Avoid `list` and `watch` where `get` is sufficient. Kubernetes notes that Secret `list` or `watch` effectively reveals all returned contents. Creation permissions may also enable privilege escalation when a controller or workload later consumes the created object.

Evaluate policy at issuance and re-evaluate on renewal according to authority semantics. Record policy revision and decision reason. Cache authorization only for a bounded interval compatible with revocation objectives.

Tenant and environment boundaries need independent policy, keys, and audit partitions where compromise must not cross them. A namespace is useful organization but not automatically a complete security boundary.

### Protect storage with layers

Kubernetes Secret values are base64-encoded for representation, not encrypted by that encoding. API data may be stored unencrypted in etcd unless encryption at rest is configured. KMS v2 uses envelope encryption so data keys are protected by an external key-encryption key, but API authorization remains necessary.

Encryption at rest protects selected storage-theft scenarios. It does not protect a principal allowed to call the API, a compromised API server after decryption, a process that loaded plaintext, or a log that copied it. Local encryption keys on the same control-plane host have a different threat boundary from external KMS/HSM keys.

Backups, snapshots, replicas, queues, caches, search indexes, and disaster-recovery copies are secret stores too. Record encryption, key dependency, access, restoration testing, retention, deletion, and geographic constraints for each.

Key rotation and data re-encryption are different. Changing the first encryption provider/key affects new writes; existing ciphertext may require rewriting. Preserve old decryption capability until all governed data is migrated and verified.

### Choose a delivery boundary

**Orchestrator Secret objects** integrate with workload scheduling and references. They are operationally simple but replicate material through the API/control plane, node delivery, and possibly more readers. Configure encryption, narrow RBAC, immutable/versioned objects where suitable, and explicit rollout/reload.

**Environment variables** suit legacy startup-only consumers but are string snapshots inherited by child processes and commonly exposed by debugging, crash, support, and process tooling. Updates require process replacement. Never assume changing the source updates an existing process.

**Projected files/CSI volumes** can narrow mounting to selected containers, support structured material, and update without embedding values in Pod specifications. They add node plugins, provider calls, mount semantics, permissions, projection delay, and application reload obligations. `subPath` and inode-following behavior can defeat update expectations.

**Local agents/sidecars** can authenticate, renew leases, cache, template, and write to memory-backed shared volumes. They increase per-workload components and shared-process/volume trust. The application must still signal successful adoption.

**Direct APIs/SDKs** give applications precise lease, error, and renewal control and can avoid intermediary stores. They couple application code to authority availability and require safe caching, backoff, redaction, and renewal state machines.

**Dynamic credentials** reduce sharing and lifetime by generating database, cloud, or PKI credentials per workload. They improve attribution and revocation granularity but require issuer capacity, downstream support, renewal, connection/session migration, and outage planning.

### Deliver files atomically and narrowly

Render into a new file or directory with restrictive ownership and mode, validate format/metadata, `fsync` where durability matters, then atomically rename or switch a symlink within one filesystem. Never truncate the live credential file in place while readers operate.

Use memory-backed ephemeral storage when it fits the threat and availability model, but recognize that memory, swap, core dumps, privileged host access, and sidecars remain exposure surfaces. Mount only into the consuming container, not every Pod container by default.

Applications should reopen the path rather than retain an outdated inode, parse a complete snapshot, verify certificate/key pairs and expected audience/metadata, construct new clients, test authentication, then atomically swap in-memory state. Preserve last-known-good only within declared expiry and compromise constraints.

Filesystem notification is a hint, not proof. Debounce events, tolerate duplicates and missed events, periodically reconcile version metadata, and report delivered versus loaded version. Secrets Store CSI rotation updates mounts according to driver/provider behavior, but environment variables sourced through a synchronized Kubernetes Secret still require restart.

### Treat environment injection as immutable per process

Environment delivery puts plaintext inside the process environment before application code starts. It cannot support live rotation unless a supervisor creates a replacement process with new variables. Writing `export` in a sidecar cannot alter another running process environment.

Map individual keys rather than importing a whole object. Reject startup if required material is absent or malformed without echoing the value. Avoid exposing environments in diagnostics, admin endpoints, process listings, test snapshots, or crash reports.

For rotation, use a controlled rollout that proves new processes authenticate before terminating old ones. Keep old material valid only for the minimum overlap and revoke it after every supported rollback path uses replacement material.

Environment injection remains an explicit legacy choice when file/API consumption is infeasible; it is not a neutral default.

### Manage leases, caches, and renewal

For secret issued at time $t_0$ with expiry $e$, schedule renewal before expiry with margin for retries, jitter, clock error, authority failover, application reload, and downstream validation. Do not synchronize an entire fleet at one fixed fraction without jitter or capacity analysis.

Separate agent/authority lease state from application-loaded state. An agent may renew a token while an application holds a derivative client or previous password. Emit only version/lease identifiers, remaining lifetime buckets, and transition status.

Cache only when the outage and theft trade-off permits it. Encrypt durable caches, bind them to workload/node identity where feasible, restrict permissions, set maximum staleness, and erase on retirement. A cache improves authority-outage tolerance while extending availability to an attacker who steals it.

Define startup and runtime behavior separately. A payment signer may fail closed without a current key. A read-only service might continue established connections for a bounded interval. There is no universal “fail open” for secrets.

### Rotate as a compatibility protocol

Rotation has prepare, distribute, accept, migrate, revoke, and clean-up stages. First create replacement material and make the verifier/downstream accept it. Deliver it to consumers and prove load/use. Shift new operations or connections. Revoke old capability, prove rejection, remove copies, and close exceptions.

Passwords often require dual users or dual accepted passwords because overwriting one value can strand consumers. Database pools retain authenticated sessions; force new connections and decide whether old sessions must be terminated.

Certificates require new key generation, issuance, chain and SAN/audience validation, trust-bundle compatibility, delivery, hot reload or restart, peer observation, old certificate revocation/expiry, and private-key removal. Rotate trust roots with overlapping bundles and cross-signing/dual trust where protocol permits; removing the old root too early partitions systems.

Signing keys require verifiers to accept the new public key before signers use it. Key IDs select candidates but do not establish trust. Retain old public verification material for artifacts/tokens that remain valid while protecting or destroying obsolete private signing material.

Encryption-key rotation requires decrypt-old/encrypt-new capability and often bulk or lazy re-encryption. Never destroy an old key until every required ciphertext and backup is migrated or intentionally expired.

### Revoke and prove containment

Revocation acts at the enforcing authority: disable a database principal, revoke a lease, invalidate a token/session, remove a public key, disable a cloud role binding, or reject a certificate. Deleting the file delivered to one pod is only copy removal.

Negative proof matters. After revocation, test that the old credential is rejected at representative enforcement points without putting its value into logs. Confirm cached authorizers, proxies, gateways, sessions, and replicas honor the decision within the objective.

Short expiry bounds bearer-token replay only if verifiers enforce time and cannot be induced to accept stale state. Established TLS, database, or application sessions may live beyond credential expiry. Define whether revocation terminates them.

For compromise, rotate related derivatives and investigate all copies. A disclosed root, signing key, or shared bootstrap credential may require trust-domain recovery rather than one version update.

### Observe without disclosing

Useful metadata includes reference ID, secret kind, non-sensitive version/lease ID, workload identity, target, policy revision, issue/renew/deliver/load/revoke times, remaining lifetime bucket, decision, error class, and correlation ID. Protect metadata access because relationships and timing can be sensitive.

Never log payloads, authorization headers, private keys, full connection strings, unredacted environment, template output, or decrypted responses. Apply structured allowlists before serialization rather than regex-only masking after emission. Test encodings, multiline keys, URLs, exception chains, HTTP middleware, tracing attributes, and support bundles.

Hashing a low-entropy secret is not safe redaction because it can be guessed offline. A keyed, access-controlled correlation token can sometimes support incident matching, but it becomes sensitive metadata and needs rotation.

Alert on unusual identities/paths, denied access, list/watch, high read rate, policy changes, expiring leases, renewal errors, loaded-version lag, excessive overlap, revocation failure, use after revocation, unowned references, and expired exceptions.

### Design outage and disaster recovery

Model secret authority, identity issuer, KMS, network, DNS, node plugin, webhook, agent, filesystem, clock, downstream verifier, and audit pipeline failures independently. Admission-time injection can block new pods while existing pods run; direct fetch can block startup; renewal failure can create delayed fleet expiry.

Do not let secret availability depend circularly on the same secret service. Authorities need separately protected bootstrap, unseal, storage, TLS, audit, and recovery mechanisms with tested quorum and custody.

Backups must preserve ciphertext plus the keys and policy/metadata necessary for restoration—or deliberately use independent recovery keys. A backup that cannot be decrypted is not recovery; a backup whose decryption key is stored beside it provides weak separation.

Break-glass access uses multi-party or independently monitored custody where warranted, explicit incident authorization, minimal scope, brief lifetime, immutable audit, and immediate post-use rotation. Test it without exposing production payloads.

### Govern platform tenancy and administration

Separate policy authors, secret writers/issuers, application deployers, platform operators, auditors, and emergency administrators. Prevent one role from silently creating material, granting itself read access, and erasing evidence.

Admission policy can reject inline secret-looking fields, privileged mounts, broad imports, missing references, unsafe service accounts, and unapproved providers. Detection is probabilistic; it complements clear APIs and repository scanning rather than proving absence.

External secret synchronization copies material into another authority. Document source, destination, refresh/rotation latency, deletion behavior, metadata, encryption, RBAC, backups, and which version is authoritative. More automation does not mean fewer copies.

Control provider/plugin upgrades, images, signatures, RBAC, host access, sockets, and network egress. A node-level CSI provider or mutating injector can affect many workloads and belongs in the platform threat model.

### Respond to disclosure

Treat an exposed value as compromised even if the message, commit, or log is deleted. Identify capability, issuer, audience, scope, copies, use, dependents, and revocation mechanism. Revoke or fence it, issue replacement, migrate consumers, and verify old rejection.

Preserve incident evidence without reproducing payloads. Search repository history, build logs, artifacts, images, registries, tickets, chat, observability, backups, endpoints, caches, and downstream access records using protected methods.

If a secret entered Git history, history rewriting may reduce future discovery but cannot retract clones, caches, forks, or logs. Rotation/revocation is the security action; rewriting is copy reduction.

After containment, repair the delivery path: eliminate the secret where possible, narrow policy, shorten lifetime, add prevention/detection, retest rotation, and document remaining risk.

### Retire secrets and delivery debt

Inventory consumers through policy, issuance, mounts, code search, loaded acknowledgements, and downstream use. Absence of telemetry alone is not proof because consumers or audit paths may be broken.

Migrate consumer code and delivery mechanisms before deleting references. Remove obsolete policy, aliases, synchronized copies, templates, environment variables, mounts, caches, backup retention, alerts, dashboards, exceptions, and bootstrap credentials after evidence windows.

Retain only non-secret audit metadata and public verification material needed for accountability or validation. Destroy private material using the guarantees available from the store/KMS/HSM and document limitations of backups and media.

### Operate the capability

Measure authorization and delivery latency/errors, identity and lease renewal, time-to-expiry, loaded-version lag, stale cache age, rotation completion, overlap duration, revocation latency, negative-probe results, secret-caused deployment failures, broad policies, list/watch grants, unowned/expired references, redaction test coverage, and secret incidents.

Capacity includes issuance/renewal rate, burst after outages, watch/mount fan-out, provider/KMS latency, audit volume, policy evaluation, node plugin resources, downstream credential creation, and re-encryption throughput. Add jitter and staged recovery to prevent renewal storms.

The following synthetic inventory demonstrates control coverage without containing secret values.

<!-- bijux-verify: {"id":"secret-delivery-control-inventory","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"references=10\nworkload_identity=9\nnarrow_delivery=8\nrotation_tested=7\nrevocation_tested=6\nloaded_evidence=7\nredaction_tested=8\nowner_expiry=9\n","stderr":""}} -->
```python
references = [
    {"name":"orders-db",      "workload_identity":True,  "narrow_delivery":True,  "rotation_tested":True,  "revocation_tested":True,  "loaded_evidence":True,  "redaction_tested":True,  "owner_expiry":True},
    {"name":"payments-mtls",  "workload_identity":True,  "narrow_delivery":True,  "rotation_tested":True,  "revocation_tested":True,  "loaded_evidence":True,  "redaction_tested":True,  "owner_expiry":True},
    {"name":"events-signing", "workload_identity":True,  "narrow_delivery":True,  "rotation_tested":True,  "revocation_tested":True,  "loaded_evidence":True,  "redaction_tested":True,  "owner_expiry":True},
    {"name":"search-cloud",   "workload_identity":True,  "narrow_delivery":True,  "rotation_tested":True,  "revocation_tested":True,  "loaded_evidence":True,  "redaction_tested":True,  "owner_expiry":True},
    {"name":"billing-api",    "workload_identity":True,  "narrow_delivery":True,  "rotation_tested":True,  "revocation_tested":True,  "loaded_evidence":True,  "redaction_tested":True,  "owner_expiry":True},
    {"name":"webhook-hmac",   "workload_identity":True,  "narrow_delivery":True,  "rotation_tested":True,  "revocation_tested":True,  "loaded_evidence":True,  "redaction_tested":True,  "owner_expiry":True},
    {"name":"backup-key",     "workload_identity":True,  "narrow_delivery":True,  "rotation_tested":True,  "revocation_tested":False, "loaded_evidence":False, "redaction_tested":True,  "owner_expiry":True},
    {"name":"monitor-token",  "workload_identity":True,  "narrow_delivery":True,  "rotation_tested":False, "revocation_tested":False, "loaded_evidence":True,  "redaction_tested":True,  "owner_expiry":True},
    {"name":"legacy-sftp",    "workload_identity":True,  "narrow_delivery":False, "rotation_tested":False, "revocation_tested":False, "loaded_evidence":False, "redaction_tested":False, "owner_expiry":True},
    {"name":"shared-legacy",  "workload_identity":False, "narrow_delivery":False, "rotation_tested":False, "revocation_tested":False, "loaded_evidence":False, "redaction_tested":False, "owner_expiry":False},
]

print(f"references={len(references)}")
for field in ("workload_identity", "narrow_delivery", "rotation_tested", "revocation_tested", "loaded_evidence", "redaction_tested", "owner_expiry"):
    print(f"{field}={sum(reference[field] for reference in references)}")
```

The counts reveal lifecycle gaps; they do not prove identity integrity, least privilege, confidentiality, correct loading, complete revocation, or absence of leaked copies.

## Definitions and Notation

Let workload $w$ have attested identity $i_w$ and request secret reference $r$ from authority $A$ for purpose/audience $u$ in target $t$ under policy revision $p$. Authorization predicate is $Z(i_w,r,u,t,p)$.

If authorized, issuance returns $s=(k,v,\ell,e,m)$: secret kind $k$, non-payload version identifier $v$, lease $\ell$, expiry $e$, and protected metadata $m$. It does not imply delivery or adoption.

Let $S_i(w,t)$, $S_d(w,t)$, $S_l(w,t)$, and $S_a(w,t)$ denote issued, delivered, loaded, and accepted-at-downstream secret versions. Let $R(v,t)$ state whether version $v$ is rejected by the enforcing authority at time $t$.

For old version $v_o$ and replacement $v_n$, rotation completes only when intended consumers have accepted $v_n$, new operations use it, $R(v_o,t)$ holds within scope, obsolete sessions/copies are handled, and recovery remains viable. Equality of control-plane desired version and $v_n$ is insufficient.

Risk is not a scalar guarantee, but exposure generally grows with privilege, audience breadth, validity duration, number of readable copies, and detect/revoke latency. Short TTL alone cannot compensate for broad privilege or replayable copies.

## Mechanisms, Invariants, or Proof Structure

The secret-delivery assurance chain is:

1. classify the secret capability and eliminate static material where possible;
2. define purpose, audience, owner, lifetime, consumer, delivery, renewal, revocation, and retirement;
3. attest workload identity without a fleet-shared root credential;
4. authorize the exact reference/role, operation, target, and policy revision;
5. issue or retrieve bounded material through protected transport and storage;
6. deliver narrowly and atomically without entering broad manifests or telemetry;
7. validate and load in the application, then prove downstream acceptance;
8. renew or rotate with compatibility, overlap, runtime acknowledgement, and outcome evidence;
9. revoke old capability at enforcement points and prove rejection; and
10. remove copies, policy, exceptions, caches, and obsolete trust while retaining safe audit metadata.

This is not proof of secrecy. Identity selectors, policy, cryptography, authorities, nodes, plugins, processes, dependencies, clocks, telemetry, humans, backups, and incident evidence can fail. The chain makes each trust boundary and non-guarantee reviewable.

The invariants are payload exclusion, complete ownership, attested workload identity, exact authorization, layered protection, narrow delivery, state-separated runtime evidence, complete rotation/revocation, explicit failure behavior, and payload-free audit.

## Alternatives and Trade-Offs

**Static versus dynamic credentials:** static material is widely compatible and tolerates issuer outage but increases sharing and rotation burden. Dynamic credentials improve attribution, scope, and lifetime while increasing renewal and issuer dependency.

**Environment versus file:** environment values serve legacy startup-only consumers but have broad diagnostic/inheritance surfaces and need restart. Files support permissions and rotation but require atomic projection, reopen, reload, and acknowledgement.

**CSI projection versus sidecar agent:** CSI centralizes node/provider integration and avoids a sidecar per workload. Agents offer rich authentication, templating, caching, and renewal but add containers, resources, and shared-volume/process trust.

**Direct API versus synchronized orchestrator object:** direct APIs reduce copied stores and expose lease semantics but couple applications to the authority. Synchronization improves native integration but duplicates payloads into another RBAC, encryption, backup, and rotation domain.

**Short TTL versus cached availability:** short lifetimes reduce stolen-credential utility but make issuer/clock/renewal availability critical. Durable caches survive outages while extending theft and revocation exposure.

**Bearer versus proof of possession:** bearer tokens are simple and interoperable; possession equals capability. Certificate/key-bound tokens reduce replay by requiring the private key, at PKI, key-storage, and protocol complexity.

**Fail closed versus bounded degraded operation:** fail closed protects authorization but can cause outage or prevent recovery. Bounded last-known-good may preserve service but accepts stale or compromised capability. Choose per operation, not platform-wide.

**Shared secret versus asymmetric identity:** shared secrets can authenticate both directions poorly and complicate attribution. Asymmetric credentials separate signing/private material from verification/public material but introduce trust chains and key lifecycle.

## Failure Modes and Misconceptions

- **“Base64 means the Secret is encrypted.”** it is reversible representation without confidentiality.
- **“Encryption at rest solves secret access.”** authorized APIs and compromised runtime components receive plaintext.
- **“The vault is the security boundary.”** identity, policy, delivery, node, process, verifier, logs, and humans also are.
- **“A reference cannot be sensitive.”** names and metadata can reveal systems, tenants, roles, or incidents.
- **“Short-lived means least privilege.”** a brief credential can still be globally destructive.
- **“The mounted file rotated.”** the application may retain the old inode, parser state, client, connection, or session.
- **“Expiry revokes every use.”** established sessions or cached authorization may continue.
- **“Deleting a Secret revokes it.”** downstream credentials and copies remain until their authority rejects them.
- **“Sidecars make applications rotation-aware.”** the sidecar can update material while the application ignores it.
- **“One secret per namespace is isolated.”** RBAC, nodes, controllers, backups, and privileged workloads can cross that assumption.
- **“Redaction catches leaks.”** alternate encodings, structured fields, multiline keys, dumps, and derived tokens escape naive regexes.
- **“Hashing the value is safe telemetry.”** low-entropy secrets can be guessed, and stable hashes enable correlation.
- **“Rotation should overwrite immediately.”** incompatible consumers may fail before replacement is accepted.
- **“Keeping old keys enables rollback.”** indefinite overlap preserves attacker capability and growing ambiguity.
- **“Removing a leaked commit fixes exposure.”** clones, caches, artifacts, and logs may retain it; revoke first.

## Worked Examples

### Example 1

A manifest stores `password: cGFzc3dvcmQ=`. Anyone who can read it can decode it. The platform replaces inline values with a reference and encrypts governed storage while narrowing API authorization. Conclusion: encoding, storage protection, and access control are distinct.

### Example 2

A controller needs one Secret but receives namespace-wide `list`. A compromised controller extracts every returned value. Policy grants resource-name-scoped `get` and isolates controller duties. Conclusion: collection operations expand payload exposure.

### Example 3

All services use one static cloud key. A single log leak enables cross-service mutation with no workload attribution. Workload federation issues target/audience-scoped, short-lived credentials. Conclusion: identity can eliminate distributable bootstrap secrets.

### Example 4

A CSI-mounted certificate changes, but the server retains the original key pair in memory. Loaded-version telemetry remains old. The server reopens, validates pair/chain/SAN, swaps listener state, and reports acceptance. Conclusion: projected update is not application rotation.

### Example 5

A database password is overwritten before old pods load replacement. Half the fleet cannot reconnect. Dual principals allow new credential delivery and authenticated new connections before the old principal is revoked. Conclusion: rotation is a compatibility sequence.

### Example 6

A five-minute token expires, yet a WebSocket authenticated earlier remains open for hours. The service defines session reauthentication and forced closure on compromise. Conclusion: credential expiry and session revocation are separate.

### Example 7

A local agent renews a lease successfully, but a connection pool uses old sessions. Metrics distinguish agent lease version, application-loaded version, and downstream-accepted version. Conclusion: observe each state boundary.

### Example 8

A secret-authority outage starts one minute before fleet-wide renewal. Jitter, renewal margin, cached bounded leases, staged recovery, and issuer capacity prevent simultaneous expiry. Conclusion: short lifetime requires availability engineering.

### Example 9

A signing service emits with key `new` before verifiers receive its public key. Verification fails globally. The safe sequence distributes/observes verification material first, then signs new, then retires the old private key after old artifacts expire. Conclusion: producers and verifiers rotate in order.

### Example 10

An API token appears in CI logs. The team deletes the log but keeps the token. The correct response revokes it, replaces consumers, verifies rejection, searches derivative copies, and repairs masking and delivery. Conclusion: deletion reduces copies; revocation contains capability.

## Cross-Program Connections

- **Computer Security:** threat models, identity, least privilege, key custody, side channels, and incident containment define the trust boundaries.
- **Cryptography:** authenticated encryption, key derivation, PKI, signatures, proof of possession, and key destruction constrain mechanisms.
- **Distributed Systems:** leases, clocks, caches, partial failure, reconciliation, fan-out, and convergence shape renewal and rotation.
- **Operating Systems:** environments, process memory, permissions, files, inodes, core dumps, namespaces, and privileged access shape exposure.
- **API Engineering:** audience, scopes, tokens, compatibility, versioning, error semantics, and deprecation apply to secret contracts.
- **Database Engineering:** users, grants, pools, sessions, replication, backups, and dual-principal rotation determine actual revocation.
- **Reliability Engineering:** renewal margins, authority outages, degraded modes, staged recovery, and rotation SLOs bound availability risk.
- **Governance and Compliance:** separation of duties, custody, audit, retention, residency, and evidence govern administrative use.

## References

1. Kubernetes, “Secrets,” official documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/configuration/secret/
2. Kubernetes, “Good Practices for Kubernetes Secrets,” official documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/security/secrets-good-practices/
3. Kubernetes, “Encrypting Confidential Data at Rest,” official documentation, retrieved 2026-09-02. https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/
4. Kubernetes, “Using a KMS Provider for Data Encryption,” official documentation, retrieved 2026-09-02. https://kubernetes.io/docs/tasks/administer-cluster/kms-provider/
5. Kubernetes, “Service Accounts,” official documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/security/service-accounts/
6. Secrets Store CSI Driver, “Secret Auto Rotation,” project documentation, retrieved 2026-09-02. https://secrets-store-csi-driver.sigs.k8s.io/topics/secret-auto-rotation
7. Secrets Store CSI Driver, “Concepts,” project documentation, retrieved 2026-09-02. https://secrets-store-csi-driver.sigs.k8s.io/concepts
8. HashiCorp, “Vault Agent Injector,” official documentation, retrieved 2026-09-02. https://developer.hashicorp.com/vault/docs/deploy/kubernetes/injector
9. HashiCorp, “Use Vault Agent Templates,” official documentation, retrieved 2026-09-02. https://developer.hashicorp.com/vault/docs/agent-and-proxy/agent/template
10. SPIFFE, “SPIFFE Workload API,” specification, retrieved 2026-09-02. https://github.com/spiffe/spiffe/blob/main/standards/SPIFFE_Workload_API.md
11. SPIFFE, “Working with SVIDs,” project documentation, retrieved 2026-09-02. https://spiffe.io/docs/latest/deploying/svids/
12. IETF, “OAuth 2.0 Mutual-TLS Client Authentication and Certificate-Bound Access Tokens,” RFC 8705, February 2020. https://www.rfc-editor.org/rfc/rfc8705
13. NIST, “Recommendation for Key Management: Part 1—General,” SP 800-57 Part 1 Rev. 5, May 2020. https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final

## Exercises

### Exercise 1

Define secret, reference, workload identity, authority, static secret, dynamic secret, bearer credential, proof-of-possession credential, lease, rotation, revocation, and break-glass access. State one non-guarantee for each.

### Exercise 2

Trace one dynamic database credential from workload attestation through authorization, issue, delivery, application load, connection acceptance, renewal, rotation, old-session handling, revocation, negative proof, audit, and retirement.

### Exercise 3

A platform base64-encodes secrets in Git, copies one administrator cloud key to every pod through environment variables, grants controllers `list` across namespaces, logs environment dumps, updates a mounted password in place, treats vault renewal as application acknowledgement, and deletes old objects without downstream revocation. Diagnose at least twelve failures and correct them.

### Exercise 4

Design secret delivery for a multi-region payment API needing database credentials, mutual-TLS identities, a transaction-signing key, intermittent authority connectivity, 24-hour regional isolation, ten-minute credential-revocation objective, and no plaintext secret in Kubernetes API storage. State which objectives conflict and how you resolve them.

### Exercise 5

A fleet must migrate from a shared static API key in environment variables to workload-bound proof-of-possession tokens without downtime. Design identity bootstrap, verifier compatibility, application rollout, telemetry, rollback, revocation, copy cleanup, and evidence for removing the old key.

## Answers to the Exercises

### Answer 1

A secret is disclosure-sensitive capability data, but classification does not protect it. A reference identifies desired material but its metadata can remain sensitive. Workload identity authenticates runtime claims but depends on attestation and issuer trust. An authority issues/retrieves and governs material but can be unavailable or compromised. A static secret is stored/reused material but not necessarily long-lived; a dynamic secret is issued on demand but not automatically least-privileged. A bearer credential authorizes any possessor; transport encryption cannot prevent later replay after theft. A proof-of-possession credential requires a bound key but does not prove the endpoint is benign. A lease bounds renewable authorization but may not close sessions. Rotation introduces replacement but does not revoke old capability. Revocation rejects prior capability at an authority but does not erase copies. Break-glass access enables recovery but creates exceptional high-value authority.

### Answer 2

The runtime obtains attested identity bound to environment, namespace/service, and intended workload. It requests a named database role and audience; policy revision authorizes only required operations and returns a unique leased principal/version. A protected agent/API delivers material to one consumer boundary. The application validates format, opens a new database connection, reports accepted non-secret version metadata, and serves. Renewal starts with margin/jitter and rechecks policy. Rotation creates replacement, proves new connections, shifts pool acquisition, drains or terminates old sessions according to compromise policy, and revokes the old database principal/lease. A protected negative probe verifies rejection across replicas/proxies. Audit records identity, role, policy, lease/version, decisions, and times without values. Retirement proves no policy/issuance/load/use, removes reference/templates/cache/alerts, and retains only governed metadata.

### Answer 3

Base64 provides no confidentiality, and Git preserves history/copies; use references and revoke exposed values. One administrator key violates per-workload identity, least privilege, audience, scope, attribution, and blast-radius controls; use federation/dynamic roles. Environment variables create startup snapshots and diagnostic/inheritance exposure; prefer narrow files/APIs or controlled restart for legacy use. Cross-namespace `list` reveals every returned secret and breaks tenancy; grant exact resource/operation and separate controllers. Environment dumps are a secondary secret store; allowlist diagnostic fields and test redaction before emission. In-place writes permit partial reads; render privately and atomically swap. File update still needs application reopen, validation, new-client creation, downstream proof, and loaded acknowledgement. Authority renewal is not that proof. Deleting an object neither revokes a database/cloud credential nor erases processes, sessions, backups, logs, and caches. Further corrections include encryption at rest/in transit, owner/expiry, audit without payload, rotation overlap, negative revocation tests, outage behavior, and copy retirement.

### Answer 4

Use attested workload identity per trust domain/region. Database authority issues per-service/per-region dynamic roles through a local agent; applications load atomic memory-backed files and prove new connections. SPIFFE-style short-lived X.509 identities and overlapping trust bundles provide mutual TLS. A signing service uses a KMS/HSM so private signing material is non-exportable; workloads receive authorization to sign, not the key. Keep secret payloads out of Kubernetes API storage by using direct/agent or CSI provider delivery without syncing Kubernetes Secret objects. Regional agents/authorities and bounded encrypted caches support isolation. However, 24-hour disconnected operation conflicts with a ten-minute revocation objective: an offline region cannot learn global revocation, and 24-hour offline credentials remain usable. Resolve by requiring a regional enforcing authority/control channel capable of local revocation within ten minutes, or explicitly weaken one objective. Use proof-of-possession, narrow scopes, ten-minute session reauthorization, staged renewal, protected audit buffering, and tested regional recovery. Signing may fail closed if current authorization cannot be proved.

### Answer 5

Establish attested workload identity and local key generation so private proof keys do not travel. Update the verifier first to accept both the legacy key and new issuer/audience/certificate-bound tokens, while attributing method, workload, token expiry, and result without credentials. Release applications capable of obtaining/renewing new tokens and falling back to the old key only under explicit bounded rollback policy. Progress by cell, prove identity issuance, new-method authentication, renewal, user outcomes, and absence of legacy use; exercise issuer outage and clock boundaries. A rollback retains verifier dual support and application capability without reintroducing copied keys. After all supported workloads use the new method for the evidence window, disable legacy issuance/use, revoke the shared key at the API, and negatively test every enforcement replica/cache. Remove environment mappings, orchestrator objects, CI variables, templates, images/artifacts, documentation examples, backups under retention, and broad policies. Only after rejection and copy cleanup should verifier compatibility code and legacy alerts be retired.

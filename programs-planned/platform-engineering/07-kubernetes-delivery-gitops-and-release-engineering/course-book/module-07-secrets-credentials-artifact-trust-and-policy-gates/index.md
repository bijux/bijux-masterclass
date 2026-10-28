# Module 7 — Secrets, credentials, artifact trust, and policy gates

## Central question

**How can the delivery plane obtain enough authority to reconcile workloads without becoming a universal credential broker or a path that bypasses artifact and policy trust?**

GitOps changes the credential topology. CI no longer needs broad cluster credentials, but controllers now need repository access, artifact access, Kubernetes write authority, and sometimes secret decryption. A careless design concentrates all of those powers in one namespace and one ServiceAccount.

## Secret material versus secret references

A Kubernetes Secret object is a delivery target, not necessarily the source of secret truth. Atlas distinguishes:

- secret value authority;
- encryption-key authority;
- delivery-controller authority;
- workload read authority;
- rotation authority;
- audit and recovery authority.

The desired-state repository should generally contain references, policies, or ciphertext—not plaintext. The fact that a manifest uses `stringData` or base64 does not protect it.

## Three common strategies

### Encrypted secrets in Git

Tools such as SOPS encrypt selected values while preserving document structure. The repository stores ciphertext and metadata; an authorized controller or CI process decrypts during rendering or reconciliation.

Strengths include reviewable encrypted revisions, offline history, and tight linkage between configuration and secret version. Risks include decryption-key concentration, plaintext exposure in process memory or rendered artifacts, key rotation complexity, and repository readers learning secret names and structure.

Atlas uses a synthetic SOPS lane to teach identity and rotation, but does not claim that encrypted Git is always the preferred production strategy.

### External secret authority

An operator reads a cloud secret manager or vault and writes Kubernetes Secret objects or mounts material through a provider-specific path. Git contains an `ExternalSecret` or equivalent reference.

This separates secret value from Git and can use workload identity. It introduces a new controller, provider API, availability dependency, refresh policy, and caching behavior. A synchronized ExternalSecret object is not proof that the target Secret contains current material or that the workload reloaded it.

### Runtime retrieval

The workload retrieves the secret directly from an external authority. This reduces Kubernetes Secret persistence but moves availability, authentication, caching, rotation, and retry concerns into the application or sidecar. The choice belongs to the platform and workload contract, not to a universal slogan.

## Decryption location matters

Decrypting in CI means plaintext may appear in runner memory, logs, workspace, artifacts, or caches. Decrypting in the GitOps controller keeps plaintext closer to the cluster but grants the controller decryption authority. Decrypting in an external-secrets controller separates responsibilities but adds another privileged reconciler.

Atlas records:

```text
who can decrypt
where plaintext can exist
how long it exists
which namespace receives it
how rotation is detected
how revocation is performed
what evidence is retained without plaintext
```

A secret strategy is incomplete without these answers.

## Repository credentials

GitOps controllers need repository or OCI access. Use separate credentials for:

- public versus private sources;
- platform versus tenant repositories;
- read-only source access;
- image automation write access;
- break-glass maintenance.

Read credentials should not automatically permit push. Image automation write credentials should not access unrelated repositories. Repository credentials should be rotated without requiring an application redeploy and should not be embedded in Application or Kustomization manifests.

## Cluster credentials and impersonation

The controller's Kubernetes identity determines its maximum authority. Application-level or Kustomization-level impersonation can reduce effective permissions, but only if the shared controller cannot bypass the restriction through another path.

Atlas separates:

- controller installation authority;
- repository observation authority;
- namespace reconciliation authority;
- cluster-scoped platform authority;
- secret decryption authority.

Course 8 will develop the full multi-tenant security model. Course 7 ensures the delivery design does not make least privilege impossible.

## Artifact trust belongs before reconciliation

Course 3 produced image, chart, SBOM, provenance, signature, and policy evidence. Course 7 must preserve that subject binding. The desired state should reference the exact approved digest. A controller or admission policy should reject untrusted or mismatched subjects before workloads run.

Trust questions include:

- Is the registry approved?
- Is the digest immutable and present?
- Does the signature identity match an authorized builder?
- Does provenance bind the digest to the expected source and build workflow?
- Is the vulnerability disposition current?
- Is the chart digest the one reviewed?
- Has the artifact been revoked?

A valid signature from an unauthorized builder is not sufficient. An allowed registry with an unverified digest is not sufficient.

## Policy locations

Delivery policy can run in several places:

- pull-request checks;
- renderer validation;
- GitOps pre-sync policy;
- Kubernetes admission;
- runtime observation;
- promotion decision.

No single location sees every fact. Pull-request policy sees source and evidence but not live admission mutations. Admission sees the submitted object but may not see complete promotion history. Runtime policy observes live state but acts after some change occurred.

Atlas uses layered policy and records which gate owns each decision. The same rule should not be duplicated with subtly different logic in five systems without a common policy definition and test corpus.

## Policy outcomes

A binary pass/fail model encourages teams to turn missing evidence into failure or, worse, into success. Atlas uses:

- `pass` — required evidence is present and policy accepts it;
- `review` — policy needs human judgment or an approved exception;
- `fail` — evidence proves the candidate violates a blocker;
- `not-executed` — the required environment or tool was unavailable.

`not-executed` is not `pass`. Whether it blocks a particular environment depends on the environment policy.

## Secret rotation as a release

Rotation affects several states:

```text
new secret version exists
controller can retrieve or decrypt it
Kubernetes projection updates
workload observes or reloads it
old credential remains valid during overlap
old credential is revoked
recovery path retains required authority
```

A Secret object becoming synchronized proves only part of the sequence. Atlas rotation records version identity without recording plaintext, tests both old and new credentials during the overlap, verifies workload adoption, then revokes the old version.

## Generated and decrypted artifacts

Controllers and CI systems may cache rendered manifests. If those manifests contain plaintext secrets, the cache becomes a secret store. Logs, diffs, UI views, notifications, and support bundles can leak values.

Atlas render evidence records secret object identity and ciphertext or external version metadata, not plaintext. Diff systems redact sensitive paths structurally. A redaction string applied after serialization is not reliable because values may appear in annotations, error messages, or nested objects.

## Protected data and delivery credentials

The Course 6 handoff explicitly prohibits delivery objects from containing backend credentials. A GitOps controller may deploy a backup job reference; it should not hold the object-store recovery key merely because it applies the job manifest. The backup workload obtains its credential through a dedicated identity or secret authority.

Similarly, a migration hook should use a narrowly scoped database role and operation ID, not the database owner credential.

## Secret and policy failure patterns

### Ciphertext committed with the private key

Encryption is meaningless if the decryption identity is stored beside the ciphertext.

### Controller can decrypt every tenant

One compromised controller exposes unrelated tenants and environments. Separate key groups, namespaces, controller instances, or external authorities as required by the threat model.

### Secret rotation changes Git but not workload state

The Secret object updates, but the process reads only at startup. A rollout or application reload is required and must be evidenced.

### Policy validates a tag, not a digest

The tag moves after approval and the controller retrieves different bytes.

### Admission and GitOps fight

Admission mutates a field that the GitOps controller owns, causing endless drift. Ownership and mutation policy must be aligned.

## Atlas trust profile

Atlas adopts these rules:

1. plaintext secrets are prohibited in Git and release evidence;
2. repository read and automation write credentials are separate;
3. decryption authority is scoped by environment and tenant;
4. rendered caches and diffs are treated as sensitive when decryption occurs;
5. workload artifacts are pinned by digest and bound to Course 3 evidence;
6. policy outcomes distinguish fail, review, and not-executed;
7. secret rotation proves workload adoption before revocation;
8. delivery controllers do not receive backend data-owner credentials;
9. admission and GitOps field ownership are tested together;
10. policy definitions have shared fixtures across review, admission, and release gates.

Module 8 uses these trust boundaries while exposing a candidate gradually. Progressive delivery is valuable only when analysis signals are meaningful and rollback boundaries are honest.

## Deep-dive practicum

### Secret delivery has four different success points

Teams often say a secret “rotated” after updating a vault or committing encrypted YAML. That describes only source state. A complete rotation records:

1. a new source version exists;
2. the delivery controller materialized the intended Kubernetes Secret version;
3. the workload adopted the new value;
4. the predecessor credential was revoked after adoption.

A controller can report the ExternalSecret Ready while a process still uses an old environment snapshot. A projected volume can update while the application never reloads. Revoking the old credential too early causes outage; leaving it valid indefinitely defeats rotation.

### SOPS and External Secrets solve different custody problems

SOPS keeps encrypted values in Git. Reviewers can see that ciphertext changed, and Git history records versions. The controller or plugin needs decryption identity, and ciphertext metadata must be stable enough for review. Repository compromise exposes ciphertext and history but not necessarily plaintext.

External Secrets keeps values outside Git. The repository stores references and templates. The controller needs read authority to the external source and write authority to Kubernetes Secrets. The platform must observe source version, refresh state, and target adoption.

Neither design is automatically superior. Choose according to key custody, offline recovery, repository trust, source availability, tenant boundaries, audit, and incident procedures.

### Controller credentials are high-value supply-chain identities

A GitOps controller may hold repository read credentials, cluster write authority, chart registry credentials, and secret decryption keys. Combining all environments and tenants in one identity creates a broad compromise path. Atlas separates controller scope by environment and requires repository and decryption identities to be independently reviewable.

A read-only source credential does not justify write access for image automation. A decryption identity for one namespace does not justify cluster-wide Secret reads. The practical standard is not “least privilege” as a slogan; it is an enumerated set of actions, subjects, and destinations tested against real controller behavior.

### Artifact trust at admission and delivery

Course 3 produced image digests, SBOMs, provenance, and release policy. Course 7 must preserve those subjects during promotion. Verifying an image signature at admission is useful, but the delivery record also needs to show that the selected digest is the reviewed digest. Otherwise admission can verify a trusted builder while CD selects the wrong trusted artifact.

Chart packages, Git commits, Kustomize remote bases, controller plugins, and rendered manifests are also supply-chain inputs. The trust policy should name each subject and verification mechanism rather than reducing everything to “signed images.”

### Policy gate outcomes

Atlas gates use four outcomes:

- `pass` — the required evidence supports the claim;
- `fail` — evidence contradicts the policy;
- `review` — bounded ambiguity requires an authorized decision;
- `not-executed` — required evidence was not produced.

Do not average a failed blocker with several passing checks. A missing restore test or unverified secret adoption remains a blocker even if rendering and health pass.

### Recovery design

A repository outage, key loss, or secret-source outage can prevent new reconciliation. Existing workloads may continue using materialized credentials. Recovery procedures must decide whether to preserve the last-known-good Secret, rotate to emergency credentials, or suspend reconciliation. Deleting an undecryptable Secret and hoping the controller recreates it is not a recovery plan.

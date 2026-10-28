# Module 10 — Release promotion, revocation, rollback, and Kubernetes handoff

The previous modules produced evidence. This module makes a decision.

A release is not the image, tag, signature, SBOM, scan, provenance, or runtime profile individually. It is a governed record that selects exact immutable subjects, evaluates required evidence for a target environment, publishes convenience references, and preserves rollback and incident options.

The final result is **Atlas Workload Release 1.0**, ready to become an input to Kubernetes Course 4.

## Learning outcomes

By the end of the module you can:

- define a release object distinct from build and registry records;
- implement ordered, non-compensable promotion gates;
- separate build, candidate, staging, and production trust domains;
- promote by digest while managing tags as mutable views;
- design rollback around configuration, state, and compatibility rather than old-image nostalgia;
- revoke compromised artifacts, keys, evidence, or tags with the correct scope;
- retain evidence and content for recovery and forensics;
- publish a Kubernetes handoff that exposes image/runtime requirements without inventing orchestration policy;
- defend every release claim and mark unexecuted evidence honestly.

## The release object

A release record should identify:

```text
product and semantic version
exact OCI index digests
platform child manifest digests
registry/repository locations
evidence artifact digests
runtime-profile version
source and builder identity
policy version and result
target environment
approval and time
known risks and unexecuted checks
rollback/revocation references
```

The object is immutable after approval. Corrections create a new record. Tags may change, scan databases may update, and new evidence may be attached, but the original decision remains auditable.

Atlas stores the accepted record under `capstone/releases/accepted/release.json` and verifies every referenced digest.

## Promotion is evidence re-evaluation

Promotion from candidate to staging or production is not copying bytes and adding a tag. The target environment may have stronger requirements:

```text
candidate: structural + unit + subject evidence
staging:   runtime integration + platform tests
production: authorized builder + complete evidence + rollback + target policy
```

If the exact digest has already passed target-equivalent evidence, promotion can reuse it. If a registry copy changes media representation or a tool rebuilds the image, the digest changes and the candidate is new.

The safest model promotes the same immutable digest through environments while environment-specific configuration is supplied separately.

## Gate ordering prevents evidence laundering

Atlas uses this order:

1. **Subject integrity** — OCI graph, media types, sizes, digests.
2. **Platform truth** — labels, executables, per-platform evidence.
3. **Runtime contract** — non-root, mounts, shutdown, bounds.
4. **Inventory** — SBOM subject/completeness/license.
5. **Risk disposition** — vulnerability/VEX and exceptions.
6. **Origin** — provenance source, materials, builder, parameters.
7. **Authenticity** — signature/identity and validity.
8. **Rebuild/test class** — controlled, native, target integration.
9. **Operational readiness** — retention, rollback, ownership, known risks.
10. **Environment authorization** — target-specific policy/approval.

A later success cannot compensate for an earlier non-compensable failure. A signed image with a secret layer fails at gate 1/4 regardless of signer. A clean SBOM for the wrong subject fails at gate 1.

## Exceptions need scope and expiry

An exception record includes:

- exact subject;
- failed rule;
- reason;
- risk owner;
- compensating control;
- target environments;
- creation and expiry;
- remediation issue;
- revocation trigger.

Do not write “temporarily accepted” without a clock and owner. Do not reuse an exception for a new digest unless its assumptions are re-evaluated.

Some failures should be non-exceptionable: subject mismatch, invalid signature under required policy, secret disclosure, untrusted builder for production, or missing platform evidence may be absolute blockers.

## Rollback is not simply pulling the old tag

An old image may no longer be compatible with:

- database/schema changes;
- message formats;
- external configuration;
- secret/key rotation;
- persisted state;
- operating-system/kernel changes;
- security policy;
- revoked credentials.

Course 3 can ensure the previous digest and evidence remain available. Course 4 will coordinate workload rollout/rollback. The handoff must state compatibility assumptions and whether old/new instances may coexist.

For Atlas Workload Release 1.0, application state schema remains unchanged from Course 2, so image rollback is expected to be compatible within the release exercise. That is a documented property, not a universal guarantee.

## Revocation has multiple subjects

### Image revocation

The digest is known unsafe. Admission/deployment policy blocks it, tags move away, active deployments are remediated, mirrors/caches are considered, and forensic evidence is retained.

### Signature-key revocation

The key/identity is no longer trusted. Previously signed digests must be reevaluated using signing time, provenance, independent rebuild, and incident evidence.

### Evidence revocation

An SBOM, VEX, or provenance statement was wrong. Remove it from accepted evidence, publish corrected evidence, and reevaluate dependent releases.

### Tag revocation

A convenience name should no longer point to the object. This does not revoke digest access.

Use precise language so incident actions match the compromised object.

## Registry retention and rollback inventory

Retain:

- current approved index and platform manifests;
- at least the supported rollback set;
- all referenced blobs;
- SBOM, VEX, provenance, signatures, and decision records;
- revoked releases for an investigation period;
- key and policy history;
- source/material references needed for rebuild.

Garbage collection must understand referrers and release holds. A clean tag list is not a safe GC root set.

## Kubernetes handoff: capabilities, not manifests

Course 3 does not guess the final Pod or Deployment YAML. It publishes a contract Course 4 can map deliberately.

### Image release

- exact API/worker index digests;
- available platforms;
- entrypoint/default args;
- ports;
- stop signal;
- SBOM/provenance/signature references.

### Runtime contract

- UID/GID 65532;
- no required capabilities;
- no privilege escalation;
- read-only root;
- writable durable and ephemeral paths;
- resource hypotheses;
- health endpoints;
- thirty-second termination contract.

### Configuration and secrets

- runtime injection only;
- required keys/paths;
- restart/reload behavior;
- no secret values.

### Storage

- spool/results persistence requirements;
- ownership/modes;
- backup/restore owner;
- ephemeral runtime state.

### Networking

- API listens on 8080;
- worker has no public listener;
- outbound dependencies and DNS/TLS assumptions;
- no host networking requirement.

### Supply chain

- digest-only deployment;
- accepted evidence artifact types;
- admission verification expectations;
- known unexecuted native/cloud evidence.

Kubernetes Course 4 will decide Pods, controllers, Services, volumes, probes, scheduling, and admission. The handoff prevents it from silently weakening the release contract.

## Final defense: one release, many proof classes

The defense must separate:

### Executed dependency-light evidence

- deterministic image graph;
- digest and DiffID checks;
- cross-compiled platform inspection;
- local registry/referrers;
- runtime probe;
- SBOM/VEX fixture evaluation;
- signed provenance and policy.

### Native-tool evidence

- actual BuildKit/Podman build;
- independent OCI inspection;
- native SBOM/vulnerability tools;
- Cosign/Sigstore verification;
- OCI conformance tools where available.

### Environment-backed evidence

- target architecture native execution;
- production registry policy/retention;
- hardened runtime/LSM/seccomp;
- Kubernetes admission and scheduling;
- cloud identity and secret injection.

The release record marks unavailable lanes `not-executed`. It never rebrands semantic fixtures as production proof.

## Worked case: urgent rollback after key compromise

A signing key is compromised after Atlas 1.0 deployment. The image digest has a complete SBOM, trusted provenance, and independent controlled rebuild. The signature is now suspect.

Possible response:

1. revoke old key in verifier policy;
2. stop promotions relying solely on it;
3. identify all signed subjects;
4. verify source/provenance/rebuild records;
5. re-sign trusted digests with a newly provisioned key only if policy permits and the original artifact is independently established;
6. redeploy or reaffirm exact digests under new policy;
7. retain old signature evidence for incident chronology;
8. rotate affected automation credentials;
9. document whether bytes or only authorization were compromised.

Blindly rebuilding can produce a new digest and complicate rollback during an incident. Blindly trusting the old signature ignores compromise. The response depends on independent evidence.

## Atlas capstone completion

The final capstone performs:

```text
source + build profile
→ deterministic multi-platform OCI layouts
→ local registry distribution
→ SBOM/VEX artifacts
→ provenance + signature
→ runtime-profile proof
→ release-policy evaluation
→ accepted release record
→ Course 4 handoff
```

It also rejects:

- root-user candidate;
- tag-only candidate;
- secret-layer candidate;
- architecture mislabel;
- writable-root candidate;
- incomplete SBOM;
- untrusted builder;
- evidence subject mismatch;
- unsigned promotion;
- false reproducibility claim.

## Graduate capability

After Course 3, you should be able to take a host/cloud workload contract and produce a release that another platform can consume without asking:

- which tag was reviewed;
- what user it should run as;
- where it writes;
- whether the architecture label is real;
- what components it contains;
- where its bytes came from;
- who authorized it;
- which evidence was actually executed.

Course 4 can now focus on Kubernetes reconciliation instead of rediscovering container fundamentals.


## Operational release walkthrough

A candidate reaches the promotion service with an index digest and evidence graph. The release process should:

1. resolve and verify the candidate by digest;
2. enumerate every platform child and content blob;
3. discover and verify required referrers;
4. evaluate the policy for the target environment;
5. ensure target registry retention and availability;
6. copy or authorize the same immutable graph without rebuilding;
7. verify the target graph by digest after transfer;
8. assign protected discovery tags only after digest verification;
9. write an immutable release record;
10. publish deployment and rollback authorization separately.

If any transfer changes bytes or media representation such that a digest changes, the target contains a new artifact and needs a new subject decision.

## Debugging from the earliest failed phase

Use this phase model:

```text
reference resolution
→ authentication/authorization
→ manifest/index retrieval
→ platform selection
→ blob retrieval
→ unpack/rootfs construction
→ runtime create
→ exec/startup
→ readiness
→ request/work
→ shutdown/cleanup
```

Capture the exact digest before debugging. Avoid modifying the running rootfs or installing tools into the application container; that destroys correspondence with the released artifact.

Examples:

- `manifest unknown` belongs before platform selection;
- `exec format error` belongs to platform/executable truth;
- missing dynamic loader belongs to rootfs/runtime closure;
- permission denied on spool belongs to runtime identity/mount ownership;
- SIGTERM timeout belongs to PID 1/application lifecycle;
- tag movement belongs to release/reference governance.

Purpose-built, digest-pinned probes are preferable to an all-powerful toolbox image. Debug access should be time-bounded and audited.

## Rollback decision tree

Before authorizing a prior digest, ask:

1. Is the full image and evidence graph retained?
2. Is the old artifact still authorized under current signer/vulnerability policy?
3. Can the current runtime execute its platform and kernel requirements?
4. Are configuration and secret interfaces compatible?
5. Is durable data backward compatible?
6. Will rollback replay or duplicate work?
7. Is the old release observable and supportable?

If data or external contracts are incompatible, rolling back only the image can increase damage. Course 4 will add orchestrated rollout mechanics; storage migration and recovery are addressed later in the platform program.

## Emergency compromise handling

If the release key is suspected compromised:

- freeze new promotions under that identity;
- preserve evidence and transparency/audit records;
- determine affected signatures, releases, environments, and deployment state;
- distribute revocation or policy denial;
- assess whether running workloads must be replaced immediately;
- establish a new signing identity through an independently authorized process;
- rebuild/re-sign only when policy requires new artifact or trusted provenance;
- document exceptions and residual exposure.

Re-signing the same digest with a new key can restore authorization only if the artifact and provenance remain trusted. If the builder or source may be compromised, rebuild in a known-good environment.

## Kubernetes handoff design review

Course 4 needs workload facts, not prewritten YAML. The handoff must be sufficient to derive:

- image references by digest and supported platforms;
- commands, ports, and process identities;
- startup, liveness, readiness, and shutdown semantics;
- immutable root and writable mount contracts;
- configuration and secret injection interfaces;
- network ingress/egress expectations;
- resource hypotheses and evidence classes;
- security requirements and forbidden authorities;
- SBOM/provenance/signature policy;
- rollback/revocation constraints.

It must not decide Deployment versus StatefulSet, replica count, probe periods, StorageClass, Service type, Gateway, or admission implementation. Those are orchestration decisions made with new evidence.

## Graduation test

A graduate can take an unfamiliar image reference and answer, from exact evidence:

```text
What bytes will run?
On which platforms?
How was the subject built?
What does it contain?
Which findings and exceptions apply?
Who authorized it under which policy?
What runtime authority does it require?
Can it be promoted, rolled back, or revoked safely?
What must the orchestrator preserve?
```

That is the skill this course is designed to produce—not fluency in one container CLI.

## Promotion changes authorization, not artifact bytes

Build once, verify once, and promote the same digest. Copying between registries may duplicate storage, but the destination digest must remain identical. Rebuilding for each environment creates different subjects and invalidates earlier evidence.

Model release states explicitly:

```text
built
→ evidence-complete
→ approved
→ promoted
→ deployed
→ superseded
→ revoked or retired
```

The transitions have different owners. A builder should not approve itself. A registry tag movement should not silently change deployment authorization. A runtime should not accept a digest solely because it exists in the production repository.

### Revocation has multiple targets

Distinguish:

- **tag rollback** — move a discovery tag;
- **deployment rollback** — select a previous approved digest;
- **release revocation** — prohibit a particular digest;
- **signer revocation** — distrust a key or identity for a time range;
- **builder revocation** — distrust outputs from a compromised builder;
- **evidence withdrawal** — invalidate an incorrect SBOM/VEX/provenance decision.

Deleting a tag does not revoke a digest already deployed. Deleting a blob can destroy forensic evidence without removing running copies. Incident response needs an admission deny rule, deployment inventory, replacement plan, and preserved evidence.

### Rollback compatibility is broader than image startup

Before selecting an older image, check database/data format, event schemas, configuration keys, secret versions, external API assumptions, and storage contents. Course 3 inherits an unchanged Atlas data model, so rollback within this exercise is expected to be compatible. That bounded fact must not become a universal platform rule.

### The Course 4 handoff is an interface, not a dump

Kubernetes receives:

- API and worker repository-plus-digest identities;
- supported platform tuples;
- entrypoints and ports;
- UID/GID, read-only root, capabilities, and privilege rules;
- health and termination semantics;
- durable, ephemeral, and configuration mount classes;
- resource hypotheses with evidence labels;
- SBOM/provenance/signer policy;
- unresolved risks.

It does not receive signing private keys, registry backend state, build caches, or mutable source workspaces. Kubernetes may reconcile the declared release. It may not rebuild at startup, replace digests with tags, or weaken runtime policy to make a pod schedule.

### Final self-review

A release is ready for the next course only when you can answer, using evidence:

1. Which exact bytes are selected for each platform?
2. Which build and source produced them?
3. Which runtime behavior is requested and observed?
4. Which dependencies and risks are known?
5. Which signer and builder identities are trusted?
6. Which proof lanes were not executed?
7. How is the digest promoted, revoked, rolled back, and handed off?

If any answer depends on “the tag,” “the Dockerfile,” or “the scanner was green,” the release model is incomplete.

## Continue

- [Exercises](exercises.md)
- [Worked answers](exercise-answers.md)
- [Laboratory](lab.md)
- [Checkpoint](checkpoint.md)
- [Previous stage](../module-09-provenance-signatures-attestations-and-verification-policy/index.md)
- [Next stage](../assessment/final-defense.md)

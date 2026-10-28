# Module 1 — Delivery systems, GitOps authority, and reconciliation

## Central question

**Who is authorized to change desired state, who is authorized to realize it, and which observation proves that the change became safe?**

A deployment system is not a file copier. It is a chain of authorities and control loops. Most delivery incidents occur because one link is granted authority that belongs to another link, or because a signal from one link is treated as proof about the entire chain.

## From pipeline thinking to control-system thinking

A traditional pipeline is usually described as a sequence:

```text
build → test → deploy → verify
```

That picture is useful for one execution, but it hides what happens afterward. The cluster continues changing. Controllers replace Pods. admission mutates objects. operators update status and child resources. humans perform emergency edits. cloud controllers create load balancers. secrets rotate. nodes fail. A pipeline that finished successfully yesterday is not observing those changes today.

GitOps introduces a continuously operating reconciler. The important shift is not that YAML is stored in Git. The shift is that an explicitly versioned desired state is compared repeatedly with observed state, and divergence is corrected or reported according to policy.

A useful model is:

```text
versioned desired state
        ↓ observation
reconciliation decision
        ↓ authorized writes
observed system
        ↓ status and evidence
feedback to humans and automation
```

The controller is not the source of truth for business data. It is the actor authorized to make selected Kubernetes resources converge on selected desired state. This distinction prevents a GitOps repository from becoming an accidental database for facts that belong elsewhere.

## The four principles and their limits

The OpenGitOps principles can be summarized as declarative, versioned and immutable, pulled automatically, and continuously reconciled. Each principle prevents a class of failure, but none is sufficient alone.

### Declarative

The desired state describes what should exist, not the series of shell commands that once created it. Declarative state enables comparison and repeated reconciliation. It does not guarantee that every operation is naturally reversible. A schema contraction, destructive migration, certificate revocation, or external payment cannot be undone by applying an older YAML file.

### Versioned and immutable

A release decision must refer to immutable identities. A branch name is mutable. A tag can move. A Helm repository index can change. A remote Kustomize base at `main` can render new resources without a change in the consuming repository. Immutable Git commits, OCI digests, chart digests, and image digests create stable review subjects.

Versioning also supplies causality: who proposed the change, which evidence was attached, which predecessor it replaced, and which revert followed an incident. Git history is valuable because it preserves this decision record, not because Git is a magical source of correctness.

### Pulled automatically

A controller inside or near the target environment pulls desired state. This reduces the need to distribute broad cluster credentials to every CI runner. It does not remove credential risk. The controller now holds repository credentials and Kubernetes write authority. Its ServiceAccount, repository scope, destination scope, and decryption keys require deliberate boundaries.

### Continuously reconciled

Continuous observation detects drift and repairs selected differences. It does not mean “force every observed field to equal local YAML.” Kubernetes objects have multiple managers. defaulting and admission add fields. controllers own status and child objects. a cloud provider owns load-balancer status. A correct reconciler must compare the fields and resources it legitimately owns, not erase all other managers.

## CI and CD own different transitions

Continuous integration turns source into tested, immutable artifacts. Continuous delivery selects which already-built artifacts and configuration revisions should become desired state for an environment. Mixing these transitions creates an evidence problem.

Suppose staging tests `registry.example/atlas-api@sha256:aaa`. A production job rebuilds the same source and pushes `sha256:bbb` under the same semantic version. Production did not receive the staging candidate. It received a different artifact. The correct promotion changes only the production reference to `sha256:aaa`, accompanied by the evidence collected for that subject.

CI may publish:

- image and chart digests;
- SBOM and provenance subjects;
- test results;
- compatibility evidence;
- vulnerability dispositions.

CD may publish:

- environment revision;
- rendered-set digest;
- promotion evidence;
- sync and health observations;
- progressive-exposure results;
- release decision.

Neither system should silently regenerate the other's evidence.

## Desired-state authority

Atlas separates four repositories and authorities conceptually:

| Authority | Owns | Must not own |
|---|---|---|
| application team | application source and tests | production cluster credentials |
| build system | immutable workload artifacts and build evidence | environment promotion decisions |
| environment owners | desired revisions and promotion approvals | artifact rebuilding |
| GitOps controller | authorized Kubernetes fields and inventory | application business data or recovery approval |

The same organization may operate several authorities, but the records and credentials should remain distinguishable. Separation makes incident analysis possible. If the wrong image ran, you can ask whether the artifact was built incorrectly, selected incorrectly, rendered incorrectly, or reconciled incorrectly.

## Source, render, live, and health are separate populations

A mature delivery dashboard never reduces the system to one green icon. It records at least:

1. **source state** — commit, chart digest, image digests, renderer configuration;
2. **rendered state** — exact objects and a canonical digest;
3. **sync state** — whether owned live fields match the rendered set;
4. **health state** — whether resource-specific conditions indicate readiness or progression;
5. **journey state** — whether users and dependent systems receive correct service;
6. **data state** — whether migrations, fencing, backups, and recovery gates remain valid.

An application can be synchronized and unhealthy. It can be synchronized and Kubernetes-healthy while returning incorrect results. It can be healthy while a backup is stale. It can be degraded because a dependency is intentionally withheld during an incident. Every signal answers a narrower question.

## Drift is not one thing

Drift can be classified before remediation:

- **unauthorized drift** — a human changed a controller-owned field;
- **shared-field conflict** — another field manager legitimately owns the field;
- **defaulting drift** — the API server added a default absent from source;
- **admission drift** — a policy or mutating webhook changed the object;
- **controller drift** — an operator changed a child or status field;
- **emergency drift** — an audited break-glass change intentionally diverges from Git;
- **unmanaged state** — a resource exists outside the application's inventory.

Self-heal is appropriate for some classes and dangerous for others. Repeatedly overwriting a break-glass mitigation can extend an incident. Ignoring unauthorized drift can leave the environment compromised. The delivery policy needs classification and escalation, not one global boolean.

## Prune is an authority decision

Prune is often explained as deleting resources removed from Git. That description omits the crucial question: who is authorized to declare the resource's lifecycle complete?

Course 6 identifies retained volumes, claims, snapshot contents, backup manifests, and recovery keys as protected. Removing their YAML from an application repository does not transfer deletion authority to the GitOps controller. Atlas requires a data-owner approval and a separate retirement record before such resources become prune-eligible.

The same reasoning applies to shared namespaces, cluster-scoped controllers, CRDs, and resources consumed by other applications. Inventory must be explicit. A controller should not prune resources merely because they were returned by an old renderer invocation if ownership is ambiguous.

## Pull, push, and the false binary

Pull-based reconciliation is a strong default because the controller observes continuously and cluster credentials need not be copied into each CI job. Yet real systems still contain pushes:

- developers push commits;
- CI pushes OCI artifacts;
- image automation may push a configuration update;
- webhooks push source-change notifications;
- operators may push emergency configuration;
- controllers push desired state to the Kubernetes API.

The useful question is not “Is this pull or push?” It is “Which actor can change which state, through which authenticated interface, with which review and recovery path?”

## Break glass without creating a second truth

An emergency path is necessary because the ordinary delivery system can itself fail. A repository outage, controller defect, credential compromise, or unsafe desired revision may require direct intervention.

A responsible break-glass procedure has:

- explicit activation authority;
- short-lived credentials;
- a bounded resource and field scope;
- an incident identifier;
- durable audit evidence;
- a plan to reconcile the emergency change back into reviewed desired state;
- protection against the controller immediately undoing the mitigation.

The correct recovery is not to normalize permanent manual administration. It is to suspend the affected reconciliation scope, perform the minimal safe change, review the resulting state, commit the intended long-term state, and resume reconciliation.

## Atlas delivery contract

By the end of this module, Atlas Delivery Plane adopts these invariants:

1. every environment selects immutable source and artifact identities;
2. every render records the renderer version and input digest;
3. every delivery application owns an explicit inventory and destination scope;
4. protected resources require authority beyond ordinary prune;
5. sync, health, journey, and data gates are reported separately;
6. promotion reuses artifacts instead of rebuilding them;
7. emergency drift is time-bounded, audited, and reconciled back to reviewed state;
8. release status records evidence limitations rather than converting missing evidence into success.

These invariants will be implemented progressively in the capstone. Module 2 begins with the first difficult transformation: turning reusable Kubernetes configuration into a deterministic rendered set without hiding environment-specific behavior.

## Deep-dive practicum

### Reconstructing one failed release without a single “deployment status”

Assume production runs image digest `A`. A reviewed environment commit selects digest `B`. The controller fetches the commit, renders the same object set as CI, applies it, and reports the Application synchronized. Five minutes later, clients receive incorrect artifact metadata.

A shallow incident report says “the deployment succeeded and the app was broken.” A useful report separates the chain:

| Transition | Question | Decisive evidence |
|---|---|---|
| source to artifact | was `B` the tested subject? | provenance, build record, digest |
| source to render | did production render the reviewed set? | renderer version, input digests, canonical render digest |
| render to live | did the controller apply the fields it owns? | inventory, diff, managed fields, sync revision |
| live to healthy | did Kubernetes observe the current generation? | conditions, endpoint eligibility, rollout state |
| healthy to correct | did the user journey preserve semantics? | domain assertions and request/result correlation |
| release to data | could both revisions interpret current data? | compatibility matrix, writer phase, migration ledger |

This decomposition may show that delivery performed exactly as authorized while the release decision was wrong. That is not an excuse for the delivery system. It means the release system lacked a blocker gate for semantic correctness or data compatibility. Conversely, if the render digest differs from CI, then user-journey failure is downstream evidence; the earliest broken transition is render integrity.

### Authority is narrower than access

A controller ServiceAccount may technically have permission to delete a PVC. That permission does not establish organizational authority to decide that the data is no longer needed. Technical authorization, lifecycle ownership, and decision accountability are separate. Atlas therefore uses three layers:

1. Kubernetes RBAC limits what the controller can attempt.
2. inventory and prune policy limit what ordinary reconciliation may treat as owned.
3. retirement evidence records who decided that a protected object may leave the recovery set.

The same distinction applies to image automation. A bot may write a candidate branch. Branch protection and promotion policy determine whether that write can affect production. The platform should prefer credentials whose technical scope approximates the actor’s decision authority, but it must still record the human or policy decision.

### Break glass as a controlled fork

During an incident, an operator may patch replicas, routing, or a feature flag directly. Treat this as a temporary fork of desired state. The incident record needs the fork point, exact field changes, expiration, controller behavior, and merge strategy. Three recovery choices exist:

- commit the emergency state because it is the new intended state;
- revert the live change because the repository was correct;
- replace both with a third reviewed state because neither is safe.

Simply re-enabling self-heal answers none of these questions. It only chooses the repository branch of the fork. The decision must be based on evidence about the failure, not on loyalty to automation.

### Design review

For every automated write path in your organization, write a sentence in this form:

> Actor **X** may change state **Y** for scope **Z** when evidence **E** satisfies policy **P**; recovery is owned by **R**.

If you cannot complete the sentence, the write path is not governable. This exercise usually reveals hidden authorities in CI credentials, image automation, chart repositories, admission mutation, feature-flag systems, and emergency scripts.

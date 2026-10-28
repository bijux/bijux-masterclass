# Module 10 — Release operations, incidents, final defense, and security handoff

## Central question

**Can the delivery plane make a categorical release decision, explain every transition, survive failure of its own control path, and hand Course 8 an authority model that can actually be secured?**

A mature delivery system is not judged by how quickly it applies a good commit. It is judged by whether it rejects unsafe changes, preserves evidence, limits authority, communicates uncertainty, and recovers when Git, registries, controllers, metrics, credentials, or humans fail.

## The release dossier

Atlas requires one immutable dossier per environment release. It contains:

- release ID and predecessor;
- source commit and signature status;
- image, chart, and OCI source digests;
- renderer and plugin versions;
- canonical rendered-set digest;
- source and rendered diffs;
- policy and compatibility results;
- protected-resource and prune report;
- secret and credential version identities;
- migration and recovery gates;
- target cluster compatibility;
- sync and health observations;
- progressive-delivery evidence;
- user-journey evidence;
- approvals, exceptions, and expiry;
- rollback frontier and incident owner;
- evidence-class limitations.

The dossier should be reproducible from machine-readable records. A narrative summary helps reviewers; it must not replace the raw subjects and decisions.

## Categorical release decisions

Atlas uses four top-level outcomes:

### Accepted

All blocker evidence is present and passes for the target environment. Review-required items have approved, current exceptions.

### Rejected

Evidence proves a blocker: mutable artifact, incompatible schema, untrusted identity, protected-resource deletion, failed canary, unsafe rollback, or unauthorized destination.

### Review required

The candidate may be acceptable, but policy needs a human decision with owner, reason, compensating control, and expiry. Review is not a way to ignore a hard blocker.

### Not executed

A required environment or tool was unavailable. The candidate has no positive result for that gate. Production policy commonly blocks; a development environment may permit bounded progress.

An average score is deliberately avoided. Ten minor passes cannot compensate for one protected-data deletion.

## Release freeze and sync windows

A freeze controls change timing, not correctness. Emergency security or reliability work may require an exception. Atlas records:

- scope;
- start and end;
- authority;
- allowed emergency classes;
- review path;
- reconciliation behavior during the window.

Argo CD sync windows or controller suspension can enforce part of the rule. Repository merges, image automation, and secret rotation may need coordinated controls. A freeze that stops deployment but allows automation to mutate production desired state merely accumulates unobserved risk.

## Suspension

Suspending reconciliation can be safe when:

- the desired revision is suspected unsafe;
- a controller defect causes destructive behavior;
- emergency drift must remain temporarily;
- a data migration requires an explicit hold.

Suspension also stops drift correction and new fixes. It should be scoped, owned, time-bounded, visible, and paired with resumption criteria. The release dossier records the exact suspended applications or Flux resources and the last-known-good revision.

## Incident command for delivery failures

Delivery incidents need clear roles:

- incident commander coordinates decisions and communication;
- delivery operator controls reconciliation and promotion;
- application owner assesses behavior and compatibility;
- data owner controls migration, restore, and protected resources;
- security owner controls credentials and artifact trust;
- observability owner validates signals;
- scribe preserves timeline and evidence.

One person may hold several roles in a small team, but the responsibilities remain distinct. The GitOps controller is not the incident commander.

## Incident sequence

A disciplined response is:

1. **detect** the earliest failed transition;
2. **bound** affected environments, clusters, revisions, and users;
3. **stabilize** by pausing promotion, suspending harmful reconciliation, or routing traffic to stable;
4. **preserve evidence** before deleting Jobs, caches, or controller state;
5. **decide** rollback, forward fix, compensation, or data recovery using the rollback frontier;
6. **reconcile** emergency state back into reviewed desired state;
7. **restore** ordinary credentials and controller behavior;
8. **verify** user journeys, data gates, and no-op steady state;
9. **learn** by updating policy, tests, runbooks, and ownership.

The sequence may overlap, but skipping evidence preservation and authority cleanup creates repeated incidents.

## Common incident classes

### Unsafe desired revision

Source and render are known, controller behaves correctly, and the candidate is harmful. Stop promotion, abort exposure, select a compatible stable revision or forward fix, and retain the candidate evidence.

### Renderer regression

Same source produces different output under a new renderer. Freeze the renderer version, compare canonical sets, and treat the tool upgrade as the release cause.

### Prune incident

A resource is marked for deletion unexpectedly. Suspend prune for the affected application, preserve the resource, determine inventory and authority, and require explicit retirement evidence.

### Secret or repository credential compromise

Suspend affected controllers or sources, rotate credentials, verify unauthorized commits or fetches, and restore scoped identities. Do not rotate all unrelated credentials blindly if that obscures causality and expands downtime.

### Controller defect

Pin or roll back the controller release using the external recovery path. Preserve CRD compatibility and avoid running old binaries against unsupported stored objects.

### Git outage

Hold last-known-good state, report staleness, and stop new promotion. Do not treat fetch errors as deletions.

## Reconciliation after manual intervention

Before resuming, calculate the diff between emergency live state and the intended reviewed revision. Decide for each difference:

- commit it because it is the desired long-term state;
- remove it because it was temporary;
- transfer ownership because another controller now owns it;
- retain it as protected or externally managed;
- investigate because ownership is unknown.

Resuming without this review can undo a mitigation or make an accidental edit permanent.

## Delivery-plane SLOs

Course 9 will develop platform SLOs deeply, but Course 7 defines minimum delivery indicators:

- source observation age;
- reconciliation success and duration;
- drift age;
- promotion lead time;
- rollback/abort duration;
- controller availability;
- release rejection causes;
- protected-prune attempts;
- evidence completeness;
- stale suspension count.

Fast deployment is not the only objective. A controller that applies unsafe changes quickly is not performing well.

## Final defense scenarios

The learner must defend Atlas Delivery Plane against five combined scenarios.

### Scenario 1 — mutable artifact after staging

A tag resolves to a new digest before production. The release must reject the candidate and show which identity changed.

### Scenario 2 — data resource removed from Git

A retained snapshot content disappears from the render. Prune is blocked until data-owner retirement evidence exists.

### Scenario 3 — canary aggregate passes, one tenant fails

Segment and sample policy abort the candidate. Git and cluster return to a consistent stable revision.

### Scenario 4 — repository outage during controller restart

Running workloads persist. Recovered controller waits for trustworthy source rather than constructing empty desired state.

### Scenario 5 — delivery credential compromise

Affected repository and cluster authority is revoked, controller scope is contained, unauthorized revisions are identified, and ordinary operation resumes with narrower credentials.

## Course 8 handoff

Platform Security, Identity, Policy, and Multi-Tenancy Engineering needs a concrete authority map, not a generic statement that GitOps is secure. Course 7 publishes:

- delivery controller identities and ServiceAccounts;
- repository and OCI credential scopes;
- environment and tenant boundaries;
- decryption and external-secret authority;
- artifact verification requirements;
- policy enforcement points;
- admission/GitOps field ownership;
- break-glass roles and expiry;
- fleet bootstrap authority;
- known unresolved security evidence.

Course 8 will test and harden these boundaries. It may change credentials and policy, but it should not destroy the delivery lineage and evidence model.

## Atlas Delivery Plane 1.0 completion criteria

The course is complete only when:

1. the Course 6 handoff verifies exactly;
2. Kustomize and Helm sources render deterministically in the mandatory model;
3. source, artifact, render, release, and live identities remain distinct;
4. environment promotion reuses immutable artifacts;
5. Argo CD and Flux lanes preserve the same safety invariants;
6. protected resources cannot be pruned by ordinary reconciliation;
7. secrets and credentials have scoped authority and no plaintext evidence leak;
8. progressive delivery has meaningful analysis and tested abort;
9. fleet bootstrap and controller recovery avoid universal credentials;
10. release candidates receive categorical, explainable decisions;
11. incident intervention returns to reviewed desired state;
12. the Course 8 handoff verifies exactly.

The final goal is not tool familiarity. It is the ability to answer, for every production change: **what revision was intended, what exact resources were produced, who was authorized to apply them, what actually happened, what evidence justified promotion, and how the system can return to a trustworthy state?**

## Deep-dive practicum

### A release decision is a categorical argument

Atlas does not compute an average “release score.” Some properties are non-compensable: immutable subject identity, protected-data safety, required restore evidence, authorization, and rollback compatibility. Ten lint passes cannot compensate for a failed data gate.

The final dossier contains the candidate, predecessor, artifact set, render digest, controller versions, inventory diff, policy outcomes, health, actual exposure, journey results, data phase, secret adoption, fleet compatibility, approvals, limitations, and decision. Each evidence record names its subject and timestamp. Stale evidence is not silently reused.

### Incident diagnosis starts at the earliest broken transition

Suppose users fail after a release. Start with the release ledger rather than opening random dashboards:

1. Did the intended immutable candidate exist?
2. Did the target revision select it?
3. Did the pinned renderer produce the reviewed set?
4. Did the controller fetch and apply that set?
5. Did owned resources converge without destructive prune?
6. Did health observe the current generation?
7. Did actual traffic reach the candidate as intended?
8. Did journeys and data invariants hold?

The earliest negative answer narrows the owner and recovery action. Later symptoms remain useful for impact, but they should not obscure causality.

### Controller outage versus unsafe desired state

These incidents require opposite instincts. If the controller is unavailable while live state is safe, preserve workloads and restore the controller without changing desired state. If desired state is unsafe while the controller is healthy, suspend the smallest reconciliation scope and correct the source. Treating both as “GitOps down” causes unnecessary changes.

### Release recovery modes

Atlas names four recovery modes:

- **reconcile** — restore the intended current state after transient drift;
- **revert** — select a prior compatible desired revision;
- **forward fix** — publish a new candidate because rollback frontier was crossed;
- **retire** — remove a resource through explicit lifecycle completion.

The incident commander chooses the mode with the relevant owner. The controller executes only the Kubernetes portion.

### Final defense prompts

In the final defense, be prepared to answer:

- Why is the production revision immutable and reproducible?
- Which fields and resources may each controller change?
- Which resources can never be pruned by ordinary application reconciliation?
- How does promotion prove artifact identity rather than source similarity?
- What happens if source, secret provider, metrics, or one cluster is unavailable?
- Where is the rollback frontier, and when is forward repair required?
- How does a release candidate move through fleet waves?
- Which security decisions remain for Course 8?

A complete answer uses evidence from the capstone rather than product slogans.

### Security handoff

Course 8 receives a working delivery plane and must harden its identities, tenant boundaries, admission policy, key custody, artifact verification, and exception process. It may not centralize business-data authority in policy controllers or grant a global GitOps identity merely for convenience. The handoff freezes these boundaries so security work strengthens the platform instead of silently changing its ownership model.

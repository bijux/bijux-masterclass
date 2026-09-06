---
module_id: SDRE-022
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 22
title: Environment Promotion
status: complete
last_verified: 2026-09-06
---

# Environment Promotion

## One-Page Review

### Governing question

How can a delivery system advance an exact artifact through environments while preserving identity and re-establishing every claim that depends on the target environment?

### Essential definitions

- an **environment** is a bounded deployment context comprising runtime, infrastructure, configuration, secrets, dependencies, data, network policy, and operating controls;
- **promotion** authorizes an exact subject to advance to a target environment after required evidence is evaluated;
- an **artifact** is immutable build output identified by digest;
- **build once, promote** reuses the same artifact bytes across environments rather than rebuilding per environment;
- **environment-specific evidence** establishes a claim only in a named target context;
- **parity** means deliberately matching relevant properties, not cloning all production scale or data;
- **configuration drift** is divergence between declared, approved, and effective state;
- an **overlay** supplies controlled environment-specific values over a shared base declaration;
- a **promotion record** binds subject, source, origin, target, configuration, evidence, policy, actor, and time;
- a **soak** observes a deployed subject for a justified duration and hypothesis;
- a **promotion graph** permits controlled paths among environments; it need not be a single linear ladder;
- **demotion** moves an environment to an earlier known subject, usually through the same deployment mechanism;
- a **compatibility window** is the interval during which old and new components or schemas must interoperate.

### Central model, mechanism, or theorem

Represent a deployment subject as $s=(a,c,m)$ for artifact digest $a$, effective configuration digest $c$, and migration set $m$. For target environment $e$ at time $t$, promotion is allowed only when

$$
Promote(s,e,t)=I(s)\land G(s,e)\land E_s(s,t)\land E_e(s,e,t)\land P(s,e,t)\land R(s,e,t),
$$

where identity, graph permission, subject-wide evidence, environment-specific evidence, policy, and recoverability all hold. Passing in staging can contribute $E_s$ but cannot by itself establish $E_e$ for production because dependencies, data, scale, access, and failure conditions differ.

### Critical invariants

- promote immutable artifact bytes; do not rebuild after evidence or approval;
- bind effective configuration and migrations with the artifact as one deployment subject;
- verify artifact provenance and policy at every trust boundary;
- declare allowed origin-to-target edges and reject path skipping by default;
- distinguish reusable subject evidence from target-specific evidence;
- define parity by required properties, not environment names;
- keep secrets as target-resolved references, never copied values in artifacts;
- reconcile declared and running state and surface drift;
- preserve exact promotion, approval, deployment, and observation records;
- invalidate evidence when subject, target, configuration, policy, or time changes;
- rehearse recovery through the same controller and compatibility model;
- promote small subjects and stop expansion on missing or adverse signals.

### Common failures

Common failures include rebuilding for production, retagging `latest`, copying staging secrets, assuming staging success proves production, maintaining hand-edited snowflake environments, hiding overlay differences, promoting configuration separately without identity, skipping graph edges, using production data unsafely in test, arbitrary soak time, approving a mutable release name, ignoring running-state drift, and rolling back code across an incompatible schema.

### Compact example

Artifact digest `A7`, configuration digest `C-prod-4`, and migration set `M2` form the production subject. Staging evidence verifies the artifact's package and API behavior. Production promotion separately checks the target's identity policy, capacity, dependency versions, data compatibility, secrets references, rollout signals, and recovery plan. Rebuilding `A7` or changing `C-prod-4` creates a different subject and requires re-evaluation.

### Connections

[SDRE-021](021-continuous-delivery-versus-continuous-deployment.md) separates readiness from deployment policy. [SDRE-023](../ROADMAP.md) next deepens configuration and secret separation, while [SDRE-024](../ROADMAP.md) owns database change delivery.

## Governing Question

Teams often draw development, test, staging, and production as boxes connected by arrows. The picture is useful only if each arrow has exact semantics. What moves? Which prior evidence remains applicable? Which target differences require new evidence? Who authorizes the transition, and how can it be reversed?

Environment promotion is not copying a branch or declaring that “staging passed.” It is a policy decision over an immutable deployment subject, a target, and current evidence. Good promotion preserves artifact identity while making environmental differences explicit.

## Why This Matters

Rebuilding per environment changes compilers, dependencies, timestamps, or inputs and breaks the connection between tested and deployed bytes. Humble and Farley make build-once and deployment-pipeline discipline central to continuous delivery [1]. Google SRE release-engineering guidance likewise emphasizes reproducible builds, unique artifact versions, recorded release contents, and controlled rollout [2].

Identity is necessary but not sufficient. SLSA 1.2 defines provenance as verifiable information about where, when, and how an artifact was produced and describes verification against expectations [3]. Provenance can support artifact admission, but it does not prove that production configuration, capacity, dependencies, data, or access policy are suitable.

Environment state is security-relevant configuration. NIST SP 800-128 treats configuration management and monitoring as part of managing system security and organizational risk [4]. A delivery system therefore records, reviews, deploys, and reconciles configuration rather than treating it as invisible operator knowledge.

## Prerequisites and Retrieval

Retrieve artifact, digest, provenance, environment, configuration, secret, dependency, data schema, migration, version, compatibility, deployment, release, canary, rollback, policy, approval, drift, reconciliation, and audit.

From SDRE-001 through SDRE-010 retrieve artifacts, repositories, metadata, provenance, signing, and supply-chain verification. From SDRE-017 retrieve complete gate states, from SDRE-019 trust separation, from SDRE-020 evidence latency, and from SDRE-021 readiness and deployment policy. Platform and Cloud Engineering own environment mechanisms; Security Engineering owns secrets and authorization; Database Engineering owns schema and data correctness.

## Learning Objectives

After completing this module, you should be able to:

1. define an environment by relevant properties rather than a label;
2. construct an immutable deployment subject from artifact, configuration, and migrations;
3. explain why build-once preserves tested identity;
4. separate reusable subject evidence from target-specific evidence;
5. design promotion graphs, gates, records, and invalidation rules;
6. select intentional parity and safe production-data substitutes;
7. detect and respond to configuration drift;
8. govern overlays and target-resolved secret references;
9. plan observation, soak, rollback, and compatibility windows;
10. test the promotion controller under failure and concurrency.

## Core Exposition

**Define environments by properties.** An environment includes compute architecture, operating system, orchestrator, network routes, identity, policy, configuration, secret references, dependencies, data shape and volume, quotas, traffic, observability, ownership, and recovery controls. “Staging” is a name, not a guarantee.

Inventory which properties affect each claim. A CPU-specific binary needs architecture parity. A latency claim needs representative load and dependency behavior. An authorization claim needs production-like identity and policy. A migration claim needs representative schema history and adversarial data shapes.

Exact production duplication is usually impossible and undesirable. Copying personal data or production credentials into test creates risk. Match relevant interfaces and constraints, synthesize or transform data under governance, and use bounded production exposure for properties pre-production cannot reproduce.

**Promote a complete subject.** Artifact bytes alone do not define running behavior. Bind artifact digest, effective configuration digest, migration set, deployment definition, and target. If any changes, the subject changes. This prevents a tested image from being paired silently with untested configuration.

Build once in a controlled environment, publish immutable content, verify provenance and signature, and promote by digest. Movable labels can aid human navigation but resolve them to immutable identity before policy. Never approve `latest`.

Some outputs cannot be identical across targets, such as platform-specific binaries. Build the declared matrix once, identify every member, test the relevant member, and promote its exact digest. Do not rebuild a production member after staging evidence.

**Classify evidence by scope.** Subject-wide evidence may include signature, provenance, static analysis, unit tests, package structure, and deterministic contract tests. Environment-specific evidence includes target access policy, dependency reachability, configuration validity, capacity, data compatibility, deployment health, and runtime behavior.

Evidence is not automatically transitive. A staging pass establishes only its stated assumptions. Production may use different scale, accounts, network, data, feature state, regional services, and quotas. Record assumptions so policy can decide what carries forward and what must be reacquired.

Evidence also expires. A new vulnerability, dependency incident, policy version, target drift, or elapsed approval window can invalidate a waiting promotion. Re-evaluate at the edge rather than copying a green badge.

**Design the promotion graph.** A simple graph might permit integration to staging, staging to canary, and canary to production. Hotfixes may use a separate reviewed edge from trusted build to canary. Regional deployments may branch after common evidence.

Each edge declares allowed origins, targets, subject classes, required evidence, approvers, credentials, observation, and recovery. Reject unlisted edges and path skipping. A graph is not proof that each environment is safer; it makes transitions explicit.

Promotion should be idempotent. Repeating the same request converges on the same declared subject or reports completion. Two competing requests require serialization, compare-and-swap, or a controller policy that prevents stale completion from overwriting a newer subject.

**Keep configuration visible.** Use a shared schema and base declaration with small explicit overlays. Render effective configuration deterministically, validate it, hash it, and include that digest in the promotion record. Review differences between environments rather than only individual files.

Avoid environment forks containing copied application definitions that drift independently. A production-only safety value can be legitimate; its rationale and owner belong in policy. Hidden manual edits are not an overlay.

Resolve secrets at the target through narrow identity. The promotion record contains secret identifiers and versions where safe, not values. Never bake environment credentials into the artifact or copy staging secrets to production. SDRE-023 develops this boundary further.

**Reconcile declared and running state.** Deployment success means the controller reports desired state; verification must also inspect actual running versions, configuration, replicas, dependencies, and health. Compare declared digest to observed state continuously or at governed intervals.

Drift may arise from emergency changes, failed rollouts, external controllers, mutable dependencies, or manual access. Classify it, stop promotion when it invalidates assumptions, and either reconcile through the controlled path or record a temporary exception with expiry. Do not silently overwrite forensic evidence.

Declarative, versioned, automatically reconciled state makes divergence observable. The OpenGitOps principles describe declarative, versioned and immutable, pulled automatically, continuously reconciled desired state [5]. These principles are an implementation model, not a requirement to use a particular product.

**Promote data changes compatibly.** Code, schema, and data may have different reversibility. During rolling deployment, old and new instances coexist. Expand schema first, deploy tolerant readers and writers, migrate or backfill, observe, then contract only after the rollback window.

Bind migration identity and status to the subject. Prevent the same non-idempotent migration from running twice. Record checkpoints and partial completion. Never treat code rollback as data rollback without explicit proof.

Production data in lower environments requires minimization, authorization, transformation, retention, access control, and leak analysis. Synthetic data should reproduce relevant distributions and pathological shapes, not merely look realistic.

**Use observation as an edge condition.** Promotion to canary begins a new evidence stage. Define metrics, invariants, baseline, cohort, threshold, missing-data behavior, duration, and decision before rollout. Version-tag telemetry so observations bind to subject.

A soak has value only with a time-dependent hypothesis: memory growth, delayed jobs, compaction, lease renewal, certificate rotation, or workload cycle. “Wait 24 hours” without a hypothesis creates delay without defined evidence.

Stop expansion on adverse or unavailable signals. A halt protects scope but does not prove the candidate caused the problem. Preserve evidence for causal analysis.

**Recover through the graph.** Demotion promotes a previous known subject through the same controller and current target policy. Verify that configuration, secrets, schema, and dependencies remain compatible. Sometimes roll forward or disable a feature is safer than old code.

Keep recent artifacts immutable and retrievable. Rehearse recovery, including unavailable artifact storage, partial region change, telemetry loss, and stuck migrations. Record recovery time from decision through verified service restoration.

Break-glass changes enter declared state afterward, receive review, and expire. If emergency state remains outside the model, future promotions are evaluated against fiction.

**Record and test promotion.** A promotion record includes request and attempt identity, actor, source and target, artifact and provenance digest, configuration digest, migration set, evidence, policy version, approval, timestamps, observed rollout, and final state. Protect the record from the deployment subject.

Test wrong artifact, invalid signature, stale evidence, disallowed edge, changed overlay, missing secret reference, target drift, concurrent request, partial rollout, failed migration, missing telemetry, cancellation, rollback incompatibility, and audit failure. Safe failure is hold or deny, never implicit promotion.

## Definitions and Notation

Let environments be vertices $V$ and allowed promotion edges $E\subseteq V\times V$. Let deployment subject $s=(a,c,m)$ contain artifact digest, effective configuration digest, and migration set. For target $e$ and time $t$,

$$
Promote(s,e,t)=I(s)\land G(s,e)\land E_s(s,t)\land E_e(s,e,t)\land P(s,e,t)\land R(s,e,t).
$$

$G$ checks the declared origin-to-target edge; $E_s$ is reusable subject evidence; $E_e$ is target-specific evidence; $P$ is policy and approval; $R$ is recovery readiness.

Let $D(e,t)$ be declared state and $O(e,t)$ observed running state. Drift exists when

$$
D(e,t)\ne O(e,t).
$$

Equality must compare relevant immutable identities and normalized effective configuration, not human labels.

## Mechanisms, Invariants, or Proof Structure

**Identity preservation.** If the promoted artifact digest equals the verified digest, byte identity is preserved under the hash assumptions. Rebuilding can produce a different digest, so previous artifact evidence does not automatically apply.

**Non-transitivity counterexample.** A candidate passes staging with a mock payment service and ten requests per second, then fails production authorization or saturation. Therefore staging pass does not imply production suitability unless those target-specific assumptions are separately established.

**Configuration binding.** If artifact $a$ is tested with $c_1$ but deployed with $c_2$, the subject changed from $(a,c_1,m)$ to $(a,c_2,m)$. Evidence scoped to the former cannot silently authorize the latter.

**Graph safety.** A transition not in $E$ has no declared evidence or authority contract and is denied. Adding an edge is a policy change requiring review, not an ad hoc runtime flag.

**Executable promotion model.** The model checks exact subject identity, graph edge, evidence, policy, recovery, and drift. It does not deploy a system.

<!-- bijux-verify: {"id":"environment-promotion-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"staging_to_canary=allowed\nrebuild_to_production=denied:subject-changed\nskip_to_production=denied:edge\nmissing_target_evidence=denied:target-evidence\nconfiguration_change_invalidates=True\ndrift_detected=True\nrollback_uses_promotion=True\n","stderr":""}} -->
```python
edges = {("staging", "canary"), ("canary", "production")}
approved = ("sha256:A7", "sha256:C4", "migration:M2")

def decide(origin, target, subject, subject_evidence=True, target_evidence=True,
           policy=True, recoverable=True):
    if subject != approved:
        return "denied:subject-changed"
    if (origin, target) not in edges:
        return "denied:edge"
    if not subject_evidence:
        return "denied:subject-evidence"
    if not target_evidence:
        return "denied:target-evidence"
    if not policy:
        return "denied:policy"
    if not recoverable:
        return "denied:recovery"
    return "allowed"

print(f"staging_to_canary={decide('staging', 'canary', approved)}")
rebuilt = ("sha256:A8", "sha256:C4", "migration:M2")
print(f"rebuild_to_production={decide('canary', 'production', rebuilt)}")
print(f"skip_to_production={decide('staging', 'production', approved)}")
print(f"missing_target_evidence={decide('canary', 'production', approved, target_evidence=False)}")
changed_config = ("sha256:A7", "sha256:C5", "migration:M2")
print(f"configuration_change_invalidates={changed_config != approved}")
declared = {"artifact": "A7", "config": "C4"}
observed = {"artifact": "A7", "config": "C3"}
print(f"drift_detected={declared != observed}")
rollback = {"mechanism": "promotion", "artifact": "A6"}
print(f"rollback_uses_promotion={rollback['mechanism'] == 'promotion'}")
```

## Alternatives and Trade-Offs

**Build once versus rebuild per environment.** Promotion preserves tested bytes. Rebuild may target different platforms but creates new subjects; build a declared matrix up front instead.

**Linear ladder versus promotion graph.** A ladder is simple. A graph supports regions and hotfixes but every edge needs its own contract.

**High parity versus safe abstraction.** Parity improves environmental evidence. Exact copies can expose data and credentials or cost too much. Match relevant properties deliberately.

**Shared base versus environment forks.** A shared base reduces drift. Explicit overlays support legitimate differences but require rendered-diff review.

**Push versus reconciliation.** Push gives immediate orchestration. Pull reconciliation continuously corrects drift but introduces controller authority and convergence delay.

**Rollback versus roll forward.** Old artifacts recover quickly when schemas remain compatible. Irreversible state often requires correction or disablement.

**Fixed soak versus hypothesis-driven observation.** Fixed waits are simple but weak. A hypothesis ties duration to mechanisms and measurable outcomes.

**Automatic versus human promotion.** Automation is consistent for machine-readable policy. Humans handle accountable judgment; both bind the exact subject.

## Failure Modes and Misconceptions

- **“Same version label means same bytes.”** movable labels can resolve differently.
- **“Rebuild from the same source is identical.”** tool, dependency, and environment inputs can differ.
- **“Artifact alone defines deployment.”** configuration and migrations change behavior.
- **“Staging passed, so production will.”** target-specific assumptions remain.
- **“Parity means copy production.”** sensitive data and credentials should not be duplicated casually.
- **“Environment names define trust.”** properties and controls do.
- **“Overlay differences are harmless.”** one value can change security or data behavior.
- **“Secrets belong in environment files.”** use target-resolved references and narrow identity.
- **“Declarative state prevents drift.”** observation and reconciliation are still required.
- **“A promotion graph guarantees order.”** controllers must enforce edges and concurrency.
- **“Waiting creates evidence.”** only a defined time-dependent hypothesis does.
- **“Canary pass proves production.”** exposure and observation are bounded.
- **“Rollback only changes code.”** configuration, schema, and data compatibility matter.
- **“Emergency edits need not be reconciled.”** hidden state corrupts future decisions.
- **“Digest proves suitability.”** it proves identity, not target behavior.
- **“Approval transfers across configuration.”** changed subject requires re-evaluation.
- **“Production data makes staging realistic.”** it may create privacy and security harm.
- **“Deployment success means promotion complete.”** target observation and recorded final state remain.

## Worked Examples

### Example 1

**Situation.** Staging builds from source and production builds again later. **Reasoning.** The builds may differ, so production lacks the artifact identity that passed staging. Publish once, promote by digest, and verify provenance at each edge. **Conclusion.** Build-once connects evidence to deployed bytes.

### Example 2

**Situation.** Image `A7` passes with staging configuration `C2`, then production uses unrecorded `C9`. **Reasoning.** The subject changed. Render, validate, hash, review, and bind `C9` before promotion. **Conclusion.** Configuration identity is part of deployment identity.

### Example 3

**Situation.** Staging uses a mock payment service and production uses a rate-limited external provider. **Reasoning.** Staging contract evidence carries forward, but production reachability, identity, quota, latency, and failure handling require target evidence and bounded rollout. **Conclusion.** Evidence scope is assumption-dependent.

### Example 4

**Situation.** An operator promotes directly from integration to production using a hidden flag. **Reasoning.** No declared edge defines authority or evidence. Deny, or review a durable hotfix edge with minimum checks, canary, and recovery. **Conclusion.** Path exceptions are policy changes.

### Example 5

**Situation.** Production differs only by an overlay setting `AUTH_REQUIRED=false`. **Reasoning.** Small textual size does not imply low impact. Render and compare effective configurations, apply policy constraints, and test authorization. **Conclusion.** Review differences by semantics, not file size.

### Example 6

**Situation.** Desired state says `A7/C4`, while one region runs `A6/C3`. **Reasoning.** Mark drift, preserve evidence, stop dependent promotion, identify controller or manual cause, and reconcile through the governed path. **Conclusion.** Promotion requires observed-state verification.

### Example 7

**Situation.** A 24-hour soak has no stated risk. **Reasoning.** Replace it with hypotheses such as a daily compaction or memory-growth bound, select metrics and workload, and set duration accordingly. If no time mechanism exists, the wait adds latency without defined evidence. **Conclusion.** Soak duration follows a mechanism.

### Example 8

**Situation.** A rolling deployment changes readers before an additive schema exists. **Reasoning.** Old and new processes will coexist. Expand schema, deploy tolerant code, migrate, observe, then contract after the rollback window. **Conclusion.** Promotion order includes compatibility state.

### Example 9

**Situation.** A canary metric disappears midway through rollout. **Reasoning.** Missing evidence is not healthy. Halt expansion, retain current bounded exposure if safe, restore telemetry, and decide rollback or continuation under explicit policy. **Conclusion.** Unavailable observation blocks automatic promotion.

### Example 10

**Situation.** An emergency manual edit restores service but is absent from declarations. **Reasoning.** Preserve incident evidence, record the exception, encode and review the desired state, reconcile, and expire break-glass access. **Conclusion.** Recovery is incomplete until actual and declared state rejoin.

## Cross-Program Connections

- Platform Engineering owns deployment controllers, environment services, reconciliation, and fleet policy.
- Cloud Engineering owns infrastructure identity, accounts, regions, quotas, and managed-service differences.
- Security Engineering owns provenance verification, secrets, target identity, authorization, and drift response.
- Database Engineering owns migration order, compatibility, checkpointing, and data recovery.
- Distributed Systems owns controller convergence, concurrent requests, partial rollout, and uncertain completion.
- Software Architecture owns environment-sensitive boundaries and independently deployable units.
- Data Architecture owns governed production-like datasets and privacy-preserving test representations.
- Testing & Quality Engineering owns evidence scopes, parity assumptions, and environment-specific test design.

## References

1. Jez Humble and David Farley, *Continuous Delivery*, Addison-Wesley, 2010, build-once and deployment-pipeline foundations.
2. Dinah McNutt, [Release Engineering](https://sre.google/sre-book/release-engineering/), *Site Reliability Engineering*, 2016, reproducible builds, artifact identity, policy, and rollout.
3. SLSA, [Provenance](https://slsa.dev/spec/v1.2/provenance) and [Verifying artifacts](https://slsa.dev/spec/v1.2/verifying-artifacts), Specification v1.2, current approved provenance and expectation-verification guidance. Retrieved 2026-09-06.
4. NIST, [SP 800-128: Guide for Security-Focused Configuration Management of Information Systems](https://csrc.nist.gov/pubs/sp/800/128/upd1/final), 2011 with 2019 updates.
5. OpenGitOps, [Principles](https://opengitops.dev/), Version 1.0, declarative, versioned, pulled, and reconciled state model. Retrieved 2026-09-06.
6. Martin Fowler, [Continuous Delivery](https://martinfowler.com/bliki/ContinuousDelivery.html), 2013, updated 2014, deployability and environment-pipeline foundations.
7. Carlos Arilla, Nand Kishore, and Brendan McAdams, [Canarying Releases](https://sre.google/workbook/canarying-releases/), *The Site Reliability Workbook*, 2018.
8. Kief Morris, *Infrastructure as Code*, 2nd ed., O'Reilly, 2020, environment, configuration, and delivery-system foundations.

## Exercises

### Exercise 1

Define environment, promotion, deployment subject, parity, environment-specific evidence, overlay, drift, promotion graph, soak, and compatibility window.

### Exercise 2

Artifact `A3` passed staging with configuration `C1` and migration `M4`. Production requests `A3/C2/M4`. Evaluate subject identity and list evidence that may carry forward versus evidence that must be reacquired.

### Exercise 3

A pipeline permits dev-to-staging and staging-to-production, uses mutable tags, and allows two concurrent promotions. Diagnose identity, graph, and race failures and design controls.

### Exercise 4

Design an environment-parity matrix for an authentication service. Cover runtime, identity, network, configuration, secrets, dependencies, data, scale, observability, and safe substitutes.

### Exercise 5

A region received a break-glass configuration change during an incident, its database migration partially completed, and the next release is ready. Design the safe resume path.

## Answers to the Exercises

### Answer 1

An environment is a deployment context of runtime, infrastructure, configuration, identity, dependencies, data, networks, and controls. Promotion authorizes an exact subject to a target. A deployment subject binds artifact, effective configuration, and migrations. Parity matches relevant properties intentionally. Environment-specific evidence applies only to a named target context. An overlay supplies controlled differences over a shared base. Drift is divergence between declared and observed state. A promotion graph lists allowed environment transitions. A soak observes a time-dependent hypothesis. A compatibility window is the period old and new versions or schemas must interoperate.

### Answer 2

`A3/C2/M4` differs from the tested `A3/C1/M4`; it is a new subject even though artifact and migration match. Artifact provenance, signature, package structure, static analysis, unit tests, and configuration-independent contract evidence can carry forward if current and explicitly scoped. Render and validate `C2`; reacquire policy, secret-reference, identity, dependency, data compatibility, capacity, target access, deployment, health, and rollback evidence for production. Any staging evidence dependent on `C1` does not transfer. Bind the resulting production evidence and approval to the complete new tuple.

### Answer 3

Mutable tags can resolve to different bytes between evidence and deployment. Resolve and record immutable digests. The graph should explicitly enforce only dev-to-staging and staging-to-production, with source environment evidence and no hidden skip. Two concurrent promotions can finish out of order and let a stale request overwrite a newer subject. Serialize per target or use compare-and-swap against observed generation; give each request and attempt identity; make execution idempotent; reject completion if target generation changed. Bind configuration, migrations, evidence, policy, and approval alongside the artifact digest.

### Answer 4

Match runtime version, architecture, identity protocol and policy rules, network segmentation and dependency endpoints, configuration schema and safety constraints, secret identifiers with non-production values, dependency contracts and failure modes, schema histories and adversarial data shapes, resource limits and representative load, and version-linked logs, metrics, and traces. Do not copy production credentials or unrestricted personal data. Use synthetic or governed transformed data, service simulators plus bounded contract tests, scaled load models plus production canary, and test identities with equivalent permissions structure but separate resources. Record every mismatch, affected claim, compensating evidence, owner, and review date.

### Answer 5

Freeze promotion and preserve incident and controller evidence. Read actual artifact, configuration, schema, migration checkpoint, traffic, and health; compare them with declared state. Encode the break-glass configuration as a reviewed time-bounded declaration or reverse it through the controller, then expire emergency access. Determine whether the partial migration is idempotently resumable, reversible, or requires roll-forward repair; do not rerun blindly. Re-establish compatibility for current and candidate code, verify backups or recovery, restore telemetry, and reconcile the region. Re-evaluate all target evidence and approval for the next release against the actual recovered generation. Resume with a bounded canary and explicit halt criteria only after drift and migration uncertainty are resolved.

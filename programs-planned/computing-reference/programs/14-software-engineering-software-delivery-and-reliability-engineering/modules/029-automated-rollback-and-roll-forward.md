---
module_id: SDRE-029
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 29
title: Automated Rollback and Roll Forward
status: complete
last_verified: 2026-09-06
---

# Automated Rollback and Roll Forward

## One-Page Review

### Governing question

When a release produces adverse or uncertain evidence, how can automation limit harm and select rollback, roll forward, or containment without restoring an incompatible subject, oscillating on noisy signals, or pretending durable effects disappeared?

### Essential definitions

- **rollback** deploys a previously accepted subject as a new recovery transition;
- **roll forward** deploys a new corrective subject that preserves or repairs current state;
- **containment** stops impact expansion without yet selecting a binary target;
- a **recovery subject** binds application, infrastructure, configuration, dependencies, migrations, and required policy by immutable identity;
- **rollback eligibility** means the recovery subject can safely operate on current state and dependencies;
- a **trigger** maps observed evidence to a recovery decision;
- a **guardrail** is an absolute condition whose breach stops or reverses exposure;
- **hysteresis** requires stronger or sustained evidence to change direction than to maintain the current state;
- a **cooldown** prevents immediate repeated direction changes while observations settle;
- **false rollback** is an unnecessary reversal caused by misleading evidence;
- **missed rollback** allows harmful exposure to continue;
- a **one-way effect** cannot be reliably undone by redeploying code, such as a sent payment or disclosed secret;
- **recovery verification** proves the chosen transition restored its declared service properties.

### Central model, mechanism, or theorem

Let $s_c$ be the current subject, $s_r$ a prior recovery subject, and $S_t$ current persistent and external-effect state. Automatic rollback is eligible only when

$$
Eligible(s_r,S_t)=Available(s_r)\land Compatible(s_r,S_t)\land Configured(s_r)\land Capacity(s_r)\land Deployable(s_r)\land Observable(s_r).
$$

If eligibility is false, reversal is not a valid automatic action even when the candidate is harmful. Contain impact and choose a compatible roll-forward repair.

Recovery latency is more than actuation:

$$
T_{recover}=T_{detect}+T_{decide}+T_{actuate}+T_{verify}.
$$

Automation must minimize user harm across all four intervals rather than optimize only a fast rollback command.

### Critical invariants

- every action names the exact source, target, generation, evidence, policy, and current state assumptions;
- guardrail breach halts further exposure before diagnosis or target selection;
- rollback eligibility is proved before the release, rechecked at decision time, and invalidated by incompatible state change;
- recovery uses the normal authenticated, idempotent, observable deployment mechanism;
- triggers bind to version-attributed user and service outcomes, not ambiguous fleet averages;
- missing, delayed, or contaminated telemetry never counts as health;
- hysteresis and cooldown prevent noisy direction changes while hard safety invariants still react immediately;
- database changes, messages, caches, credentials, dependencies, and external effects are evaluated separately from compute revision;
- stale controllers cannot act on a newer rollout generation;
- recovery completes only after service-level verification, not when orchestration reports a target version.

### Common failures

Failures include equating a previous image with a previous system, rolling back across a destructive migration, undoing a security fix, triggering on one noisy sample, using fleet-wide signals that old replicas mask, sharing one alarm for unrelated releases, interpreting missing metrics as zero errors, retrying an uncertain rollback blindly, oscillating between versions, keeping no recovery artifact, rolling back only code while configuration remains new, assuming feature-flag reversal undoes writes, and marking recovery complete before traffic and state converge.

### Compact example

A checkout canary breaches a predeclared duplicate-charge invariant. The controller immediately freezes exposure and disables new candidate admissions. It reconciles rollout generation 44, preserves evidence, and checks the previous complete subject. Because the candidate wrote only backward-compatible rows and payment calls use idempotency keys, rollback remains eligible. The same rolling controller deploys the prior application and configuration digests, drains candidate work, and verifies charge uniqueness, error rate, latency, capacity, and running identity. If incompatible rows had already been written, it would keep the safe admission stop and deploy a forward-compatible reader instead.

### Connections

[SDRE-028](028-feature-flags.md) supplies fast behavioral containment but cannot reverse data or external effects. [SDRE-030](../ROADMAP.md) composes these mechanisms into a safe release pipeline. Database Engineering owns state repair; Distributed Systems owns generations, retries, and convergence.

## Governing Question

“If the release fails, roll it back” is not a recovery design. It omits which evidence establishes failure, which version is safe, whether that version remains deployable, what state the candidate already changed, how partial rollout is reconciled, and how restoration is verified. Automating the slogan can accelerate a second failure.

The governing problem has two stages. First, stop increasing harm when evidence becomes unacceptable or unavailable. Second, select and execute a recovery transition whose preconditions still hold. Rollback, roll forward, and containment are distinct outcomes; good automation does not force every incident into reversal.

## Why This Matters

Small progressive releases bound exposure, while automation reduces detection and actuation delay. Google SRE's canary guidance treats evaluation and rollback as parts of controlled release engineering and stresses that production evidence should decide whether expansion continues [1]. AWS delivery guidance describes alarm-driven rollback using the same pipeline mechanism and immutable release artifacts [2, 3]. These are operational patterns, not proof that every alarm or older artifact is safe.

Current Kubernetes Deployment documentation illustrates a narrower mechanism: rollout history permits restoring a prior Deployment revision, but the revision covers the Pod template; scaling changes do not create revisions, and external state is outside that rollback [4]. This distinction prevents a common overclaim: an orchestrator can restore desired compute configuration without restoring databases, queues, secrets, dependencies, or already completed side effects.

Current AWS rollback-safety guidance emphasizes upgrade–downgrade testing, mixed-version compatibility, two-stage changes, and backfill before old representations are removed [5]. Its named platform examples are vendor-specific; the underlying rule is durable. Reversal must be designed into the change before production state crosses a one-way boundary.

## Prerequisites and Retrieval

Retrieve deployment subject, immutable artifact, configuration, rollout generation, canary, guardrail, baseline, SLO, error budget, false positive, false negative, hysteresis, idempotency, state compatibility, schema migration, message version, side effect, fencing, reconciliation, rollback, recovery time, and incident containment.

From SDRE-022 retrieve complete subject identity and target evidence. From SDRE-024 retrieve expand–migrate–contract. From SDRE-026 retrieve attributable canary decisions. From SDRE-027 retrieve mixed-version rolling behavior. From SDRE-028 retrieve reversible behavior switches and their limits.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish halt, containment, rollback, roll forward, and recovery verification;
2. define an exact recovery subject rather than a version label;
3. construct and invalidate a rollback-eligibility predicate;
4. design triggers using absolute guardrails, relative evidence, hysteresis, and missing-data policy;
5. compare false rollback and missed-rollback costs;
6. identify state, protocol, security, dependency, and side-effect barriers to reversal;
7. choose a compatible roll-forward repair when rollback is unsafe;
8. build an idempotent generation-checked recovery controller;
9. measure detection, decision, actuation, and verification latency separately;
10. exercise upgrade, partial rollout, downgrade, and restoration before release.

## Core Exposition

**Separate impact control from diagnosis.** A hard correctness, security, or safety breach should stop exposure even before causality is known. Pause the rollout, stop new candidate admissions, disable a reversible hazardous path, or isolate affected work. This containment action limits future harm and preserves a stable system for investigation.

A halt does not prove the candidate caused the signal. A shared dependency may fail; telemetry may be corrupt; the control may also regress. Preserve subject, cohort, route, state, dependency, and metric evidence. Target selection comes after immediate impact control unless an already-proved rollback policy safely couples them.

Use explicit controller states: `advancing`, `holding`, `contained`, `rolling_back`, `rolling_forward`, `verifying`, `recovered`, and `failed_recovery`. “Failed” alone hides whether users are still exposed or which action is in progress. Each transition records expected generation and is idempotent.

**Define the complete recovery subject.** A last-known-good application image paired with new configuration or infrastructure may never have run. A recovery subject binds exact application artifact, infrastructure declaration, runtime configuration, secret references, dependency constraints, feature state, and schema assumptions. It is immutable and retrievable.

The “previous version” may not be the right target. It might contain a severe vulnerability, depend on an expired certificate, call a retired API, or reject current data. Select from a compatibility graph, not a linear list of version numbers. The safest target can be a prepared forward patch based on the current subject.

Retain recovery artifacts and provenance according to a declared horizon. Periodically prove they remain accessible and admissible. Artifact existence alone does not establish capacity, credentials, dependency compatibility, or state compatibility.

**Prove rollback eligibility before release.** For candidate $s_c$ and recovery target $s_r$, enumerate every boundary crossed during the rollout. Can $s_r$ read records, messages, cache entries, tokens, and configuration produced by $s_c$? Can it tolerate candidate instances during a rolling downgrade? Are old dependencies still available? Can it serve current load? Can the normal controller deploy it?

Use upgrade–downgrade testing: begin with old subjects, introduce a mixed old/new population, complete upgrade, generate representative work, then deploy old subjects through the same mixed stages and verify outcomes [5]. Cover scheduled, batch, and delayed work, not only immediate APIs. This is evidence under the test environment, not a universal guarantee.

Maintain a machine-readable eligibility record bound to both subjects, configuration, schema generation, dependency set, evidence, and expiry. Recheck it immediately before rollback. A migration, feature activation, credential revocation, or dependency removal can invalidate an earlier pass.

**Design reversible state evolution.** Expand–migrate–contract keeps rollback possible through a declared window. First deploy readers that understand old and new forms. Add representations without removing old ones. Activate new writers only while old readers remain safe. Backfill idempotently. Contract after recovery policy deliberately closes the old target.

Some state changes are logically reversible but operationally too slow. Restoring a multi-terabyte backup may take hours and lose newer accepted writes; it is disaster recovery, not an automatic binary rollback. Model recovery point and recovery time separately.

Messages and caches count as state. A new poison message can repeatedly crash old consumers. Discarding an incompatible cache may create a dependency stampede. Version formats, preserve tolerant readers, bound retention, and test mixed producers and consumers.

External effects such as payments, emails, shipments, actuator commands, or disclosed data cannot be erased by code deployment. Use idempotency, authorization, reconciliation, compensating workflows, and containment. Compensation is a new business action with its own failure modes; it is not time reversal.

**Construct triggers from user harm.** Use absolute invariants and SLO guardrails first: duplicated payments, data corruption, authorization failure, severe error rate, latency beyond objective, or saturation threatening collapse. Relative candidate-versus-control metrics improve attribution but cannot excuse an unhealthy service when both fail.

Tag every observation with subject, cohort, operation, region, dependency state, time, and rollout generation. Fleet averages let old healthy replicas hide a candidate defect. A trigger using data from generation 51 cannot govern generation 52.

Define metric query, aggregation, comparison, threshold, minimum sample, maximum lag, required duration, missing-data behavior, and action before rollout. Alarm configuration is part of the release policy and needs review. An alert intended for human investigation may be too noisy or ambiguous for automatic reversal.

**Control noise and delay.** Metrics fluctuate. Triggering rollback on one latency sample creates false actions; averaging too long allows harm. Apply consecutive-window requirements, confidence bounds, minimum counts, or change-point methods appropriate to the signal. Hard invariants can react to one proven event.

Hysteresis separates the threshold for entering recovery from the threshold for declaring health. For example, rollback after error rate exceeds 3% for two complete windows, but require error rate below 1% for three windows before recovery. A cooldown prevents new rollout immediately after restoration while telemetry and caches settle.

Missing metrics are not zero. If telemetry completeness drops below policy, stop expansion. Whether to roll back depends on eligibility and the hazard of acting blind. An independent external probe can supply a different failure channel, but no single observer proves system health.

Consider false rollback and missed rollback explicitly. False rollback consumes capacity, may reintroduce defects, and can itself disrupt service. Missed rollback extends candidate harm. Security, financial, and safety invariants usually weight missed action heavily; low-impact latency noise may require more evidence.

**Choose among rollback, roll forward, and containment.** Roll back when a prior complete subject is eligible, reversal is faster than a tested forward repair, and the old subject does not reintroduce greater risk. Roll forward when current state is incompatible with old code, a small prepared correction exists, or reverting would remove critical fixes. Contain when neither target is yet safe or evidence is insufficient.

A feature flag can quickly disable new behavior while compute stays current. Traffic routing can remove a candidate cohort. A circuit breaker can isolate a dependency. These are containment or behavioral reversal mechanisms, not complete rollback. They may be exactly the safest immediate action.

Do not improvise forward fixes directly in production. Build, identify, test, and deploy the correction through an expedited but controlled path. The emergency policy can reduce breadth or waiting time while retaining identity, authorization, evidence, and audit.

**Execute recovery as an ordinary deployment.** Use the same controller, credentials, health gates, surge limits, draining, and version telemetry as forward rollout. Special rollback scripts exercised only during incidents rot. An immutable environment prevents newer files or configuration fragments from contaminating the restored subject [2].

Rollback creates another mixed-version window. Check compatibility in the downgrade direction. Start small enough to observe recovery but fast enough to meet harm bounds. If the candidate is catastrophically unsafe and rollback eligibility is strong, policy may authorize a larger first recovery batch.

Reconcile commands. A timeout after submitting rollback yields unknown state. Read actual desired and running subjects before retrying. Every actuation compares expected rollout generation, recovery attempt, and route state. A stale rollback process cannot overwrite a newer roll-forward fix.

Serialize release and recovery transitions. New feature releases are blocked while recovery is active. Infrastructure autoscaling and failover continue only under a tested interaction policy. Do not let an unrelated deployment contaminate evidence or remove the target being restored.

**Verify restoration end to end.** Orchestration completion proves only its declared state. Verify exact subject identity, configuration, schema compatibility, traffic distribution, serving capacity, correctness invariants, latency, saturation, dependency behavior, queue progress, business outcomes, and telemetry completeness.

Recovery verification uses both current absolute health and version-attributed comparison. Returning to yesterday's error rate is insufficient if yesterday already violated the SLO. Inspect residual candidate processes, long connections, messages, jobs, and writes.

Declare recovery only after a stable observation interval derived from relevant mechanisms. Keep the incident contained through that interval. If signals do not recover, transition to `failed_recovery`, preserve evidence, and choose the next compatible action rather than oscillate automatically.

**Measure the whole response.** Detection time includes metric production, aggregation, transport, and evaluation. Decision time includes required persistence or analysis. Actuation time includes scheduling, startup, routing, draining, and state repair. Verification time covers telemetry lag and a meaningful stability window.

Record each component. A two-second command with ten-minute telemetry aggregation is not a two-second recovery. Reduce the dominant interval without weakening the claim: faster external probes, smaller release stages, precomputed eligibility, warm recovery capacity, and rehearsed controllers often matter more than command execution.

Estimate harm as exposure rate multiplied by excess failure probability and time only when effects are request-local and homogeneous. Shared saturation, corrupt state, security compromise, or safety effects violate that simple model and need scenario bounds.

**Govern automation.** Policy names owners, eligible actions, evidence, thresholds, recovery targets, state assumptions, maximum scope, cooldown, override authority, and audit retention. High-confidence repeatable failures can fully automate. Ambiguous causality can automate containment and page a human for target selection.

Break-glass authority remains narrow, authenticated, time-bounded, and recorded. An operator can stop automation, but manual commands still reconcile through declared state. Afterward, review false actions, escaped defects, detection delay, restoration time, and whether eligibility evidence matched reality.

**Test adversarially.** Exercise an unavailable target artifact, invalid signature, expired secret, dependency removal, wrong configuration, insufficient capacity, incompatible database row, poison message, cache stampede, partial region rollout, missing metrics, false alarm, shared dependency failure, controller restart, stale generation, concurrent feature flag, failed rollback, failed forward patch, and recovery that restores compute but not business outcomes.

## Definitions and Notation

Let current deployment subject be $s_c$, candidate recovery subject $s_r$, and current durable state $S_t$. Let $g$ be rollout generation and $e$ observed evidence. Define action set

$$
\mathcal{A}=\{advance,hold,contain,rollback,rollforward\}.
$$

Rollback eligibility is

$$
R(s_r,S_t)=A(s_r)\land C(s_r,S_t)\land K(s_r)\land Q(s_r)\land D(s_r)\land O(s_r),
$$

for availability, compatibility, complete configuration, capacity, deployability, and observability. Each predicate is evidence-scoped and time-sensitive.

Let $T_d,T_q,T_a,T_v$ be detection, decision, actuation, and verification intervals. Then

$$
T_{recover}=T_d+T_q+T_a+T_v.
$$

For request-local homogeneous excess failure probability $\Delta p$, request rate $\lambda$, exposed fraction $f$, and interval $T$, expected incremental failed requests are approximately $f\lambda T\Delta p$. State corruption and shared effects are not bounded by this expression.

## Mechanisms, Invariants, or Proof Structure

**Eligibility necessity.** If the prior subject cannot read current reachable state, deploying it can add failure rather than restore service. Therefore “candidate harmful” does not imply “rollback safe”; compatibility is an independent necessary condition.

**Version identity argument.** Reusing an old application with different configuration constructs a new subject. Evidence for the original pair does not automatically apply. Recovery must identify and evaluate the complete subject.

**Hysteresis argument.** If rollback and recovery use the same threshold, noise around that value can alternate actions. Separated entry and exit thresholds plus a cooldown create a deadband, reducing oscillation. This does not correct a biased or irrelevant metric.

**Recovery-time decomposition.** The four intervals are sequential prerequisites for a verified result. Optimizing actuation cannot remove time already spent detecting or time still needed to verify, so reporting only actuation understates restoration latency.

**Executable recovery policy.** The model distinguishes halt, rollback, roll forward, and containment using generation, telemetry, sustained breach, eligibility, security, and irreversible effects. It is not an incident controller.

<!-- bijux-verify: {"id":"automated-recovery-policy","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"healthy=advance\nfirst_breach=hold:hysteresis\nsustained_breach=rollback\nstate_incompatible=roll_forward\nmissing_telemetry=contain\nstale_generation=denied:generation\nsecurity_regression=roll_forward\nirreversible_effect=contain\nrecovery_seconds=270\nrollback_is_deployment=True\n","stderr":""}} -->
```python
def decide(*, healthy=False, breach_windows=0, telemetry=True,
           rollback_eligible=True, generation=12, expected_generation=12,
           old_has_security_bug=False, irreversible_effect=False):
    if generation != expected_generation:
        return "denied:generation"
    if not telemetry:
        return "contain"
    if healthy and breach_windows == 0:
        return "advance"
    if breach_windows < 2:
        return "hold:hysteresis"
    if irreversible_effect:
        return "contain"
    if old_has_security_bug or not rollback_eligible:
        return "roll_forward"
    return "rollback"

print(f"healthy={decide(healthy=True)}")
print(f"first_breach={decide(breach_windows=1)}")
print(f"sustained_breach={decide(breach_windows=2)}")
print(f"state_incompatible={decide(breach_windows=2, rollback_eligible=False)}")
print(f"missing_telemetry={decide(breach_windows=2, telemetry=False)}")
print(f"stale_generation={decide(breach_windows=2, generation=11)}")
print(f"security_regression={decide(breach_windows=2, old_has_security_bug=True)}")
print(f"irreversible_effect={decide(breach_windows=2, irreversible_effect=True)}")
detect, decision, actuate, verify = 60, 30, 90, 90
print(f"recovery_seconds={detect + decision + actuate + verify}")
print("rollback_is_deployment=True")
```

## Alternatives and Trade-Offs

**Rollback versus roll forward.** Rollback reuses a known subject and can be fast when compatibility holds. Roll forward preserves current state and fixes one defect but requires a newly built and tested subject.

**Automatic reversal versus automatic containment.** Reversal reduces response time when target eligibility is strong. Containment is safer when causality or state is uncertain and can still cap harm while humans select a target.

**Absolute versus relative triggers.** Absolute guardrails protect users during shared failure. Relative comparison improves candidate attribution. Use both rather than choose one.

**Fast threshold versus sustained evidence.** A fast trigger bounds catastrophic harm but increases false action. Consecutive windows and confidence reduce noise while extending exposure. Match policy to effect severity.

**Binary rollback versus feature disable.** Binary rollback removes an entire subject and dependencies slowly. A flag can disable a bounded path quickly, but leaves code present and cannot undo state.

**Warm recovery capacity versus provisioning on demand.** Warm capacity reduces actuation time and proves readiness, at cost and with drift risk. On-demand recovery costs less but makes restoration depend on scheduling, quotas, and artifact retrieval.

**Linear version history versus compatibility graph.** Linear history is simple but assumes the immediate predecessor is safe. A graph represents security patches, schema boundaries, and prepared recovery variants more honestly.

**Human selection versus policy selection.** Humans handle ambiguous context but respond slowly and inconsistently under stress. Policy acts quickly for tested cases. Hybrid automation contains immediately and escalates uncertain target choice.

## Failure Modes and Misconceptions

- **“Rollback means undo.”** code replacement cannot erase durable state or effects.
- **“Yesterday's image is known good.”** current data, secrets, dependencies, and load may differ.
- **“The previous revision is the whole system.”** orchestrator history may cover only one configuration surface.
- **“Any alarm should roll back.”** noisy or shared signals can trigger a harmful false action.
- **“No alarm means healthy.”** telemetry may be missing, delayed, or masked.
- **“One bad point proves regression.”** use severity-appropriate persistence unless one proven event violates a hard invariant.
- **“Rollback is safer than waiting.”** an incompatible target can amplify failure.
- **“Feature off restores state.”** writes and external effects remain.
- **“Database backup is instant rollback.”** restore time and accepted-write loss change the recovery objective.
- **“Old code can always read new messages.”** poison messages can keep failure alive after compute rollback.
- **“Automation needs no generation check.”** stale recovery can overwrite a newer fix.
- **“A fast command means fast recovery.”** detection and verification often dominate.
- **“Controller success means users recovered.”** serving and business outcomes require separate verification.
- **“Retry rollback after timeout.”** reconcile unknown state before another actuation.
- **“Keep flipping until metrics improve.”** oscillation destroys attribution and capacity.
- **“Roll forward means patch live.”** forward recovery still requires immutable identity and controlled evidence.

## Worked Examples

### Example 1

**Decompose recovery time.** Detection takes 60 seconds, policy evaluation 30, rolling actuation 90, and stable verification 90. Total verified recovery is $60+30+90+90=270$ seconds. Conclusion: optimizing a five-second API call would barely change the dominant latency.

### Example 2

**Reject an incomplete target.** Version A was healthy with configuration C1; candidate B uses C2. Automation deploys A but leaves C2, a combination never tested. Conclusion: recovery targets the complete subject `(A,C1)`, not the application label alone.

### Example 3

**Use hysteresis.** Candidate error rates across one-minute windows are 2.8%, 3.2%, 2.9%, and 3.3%. Policy requires two consecutive windows above 3%, so it holds rather than oscillates. A duplicate-payment invariant would contain on one confirmed event. Conclusion: persistence belongs to the signal's harm model.

### Example 4

**Select rollback.** Candidate latency and errors breach guardrails in two windows. The prior subject is retrievable, patched, capacity-tested, and accepts all current rows and messages; no irreversible effects occurred. Conclusion: rollback through the normal deployment controller is eligible.

### Example 5

**Select roll forward.** Candidate writers stored a new enum that the prior reader rejects. Turning traffic back would increase failures. A prepared reader patch accepts both values. Conclusion: stop candidate expansion and roll forward to the compatible reader.

### Example 6

**Contain uncertain evidence.** Candidate metrics disappear while external probes show rising failures. The cause might be telemetry or service failure. Automation stops new candidate traffic but does not declare rollback success or candidate guilt. Conclusion: missing evidence justifies containment, followed by reconciliation and target selection.

### Example 7

**Avoid security regression.** Release B has a performance defect but also removes a remotely exploitable flaw in A. Reintroducing A creates higher security risk. The system disables the expensive B feature and deploys a forward performance patch. Conclusion: “known good” must include current security state.

### Example 8

**Reconcile an uncertain command.** A rollback request times out. The new controller observes half the fleet already on recovery generation 73. It adopts that state, verifies target digests, and continues within budget. Conclusion: retry from observed generation, not from the caller's timeout assumption.

### Example 9

**Detect partial restoration.** Compute returns to A and HTTP errors fall, but queue age continues growing because B emitted messages A cannot parse. Recovery verification fails. Conclusion: inspect asynchronous state and business progress, not only web health.

### Example 10

**Handle a one-way effect.** A flawed release emailed incorrect invoices. Rolling back stops new generation but cannot recall messages. The team disables sending, restores compatible calculation, identifies affected recipients, and runs an approved correction workflow. Conclusion: containment, code recovery, and business compensation are separate actions.

## Cross-Program Connections

- **Database Engineering:** schema domains, logs, backups, and repair determine downgrade eligibility.
- **Distributed Systems:** generations, idempotency, leases, retries, and reconciliation govern recovery under uncertainty.
- **Platform Engineering:** deployment controllers, immutable subjects, routing, and capacity execute recovery.
- **Testing and Quality Engineering:** upgrade–downgrade tests, trigger calibration, and fault injection establish evidence.
- **Security Engineering:** vulnerability state, credentials, audit, and containment can forbid an old target.
- **API and Service Engineering:** wire compatibility, deadlines, idempotency, and versioned messages preserve mixed operation.
- **Data Engineering:** backfills, lineage, replay, and correction workflows handle persistent effects.
- **Systems Engineering:** hazard severity, recovery objectives, and degraded modes shape decision policy.
- **Software Architecture:** state ownership and dependency boundaries determine reversibility.
- **Operating Systems:** process replacement and signals are only one layer of end-to-end restoration.

## References

1. Alec Warner et al., [“Canarying Releases”](https://sre.google/workbook/canarying-releases/), *The Site Reliability Workbook*, O'Reilly, 2018; retrieved 2026-09-06.
2. Clare Liguori, [“Automating safe, hands-off deployments”](https://aws.amazon.com/builders-library/automating-safe-hands-off-deployments/), Amazon Builders' Library, 2020; retrieved 2026-09-06. Used as documented AWS practice, not a universal platform guarantee.
3. AWS Builder Center, [“My CI/CD pipeline is my release captain”](https://builder.aws.com/content/3Ev3XnnYuuBhlgnywbbVFzwibm1/my-cicd-pipeline-is-my-release-captain), current article retrieved 2026-09-06. Used for immutable rollback deployment and alarm-driven pipeline examples.
4. Kubernetes Authors, [“Deployments”](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/), current documentation retrieved 2026-09-06. Used only for current Kubernetes revision and Pod-template rollback semantics.
5. Sandeep Pokkunuri, [“Ensuring rollback safety during deployments”](https://builder.aws.com/content/3F04j2yRAAMBuPSPs50xwXZqg01/ensuring-rollback-safety-during-deployments), Amazon Builders' Library, published June 2026; retrieved 2026-09-06. Used for upgrade–downgrade testing, two-stage format change, and backfill practices.
6. Jez Humble and David Farley, *Continuous Delivery*, Addison-Wesley, 2010, Chapters 10, 12, and 13.
7. Michael Nygard, *Release It!*, second edition, Pragmatic Bookshelf, 2018. Used for stability, recovery, timeouts, and cascading-failure reasoning.
8. Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly, 2017. Used for encoding evolution, compatibility, logs, and distributed-state reasoning.
9. NIST, [SP 800-34 Rev. 1: *Contingency Planning Guide for Federal Information Systems*](https://csrc.nist.gov/pubs/sp/800/34/r1/final), May 2010. Used for recovery planning vocabulary; not used to claim compliance.

## Exercises

### Exercise 1

Define rollback, roll forward, containment, recovery subject, rollback eligibility, guardrail, hysteresis, cooldown, and recovery verification. Explain why a harmful candidate does not logically imply a safe rollback.

### Exercise 2

A rollout detects failure in 45 seconds, waits two 30-second decision windows, actuates recovery in 150 seconds, and verifies for 180 seconds. Compute total verified recovery time. At 2,000 requests/s, 10% exposure, and 4% excess request-local failure probability, estimate incremental failures during that interval and state the model limitations.

### Exercise 3

A candidate has changed application code, configuration, database rows, queue messages, and a third-party payment call. Construct a rollback-eligibility checklist for the prior subject and identify which effects require compensation rather than rollback.

### Exercise 4

Design an automated trigger for a checkout canary using duplicate-charge invariants, error rate, latency, control comparison, telemetry completeness, hysteresis, cooldown, and rollout generation. Specify actions for hard breach, sustained regression, and missing evidence.

### Exercise 5

A release fixes a critical vulnerability but corrupts a new optional search index format. The prior application is vulnerable, the authoritative database is intact, and search can be disabled. Choose containment, rollback, or roll forward and design verification.

## Answers to the Exercises

### Answer 1

Rollback deploys a prior subject; roll forward deploys a new corrective subject; containment stops impact expansion; a recovery subject binds all required application and environment identities; rollback eligibility proves that subject can safely operate now; a guardrail is an absolute stop condition; hysteresis separates action and recovery thresholds; cooldown delays repeated direction change; and recovery verification establishes service outcomes after actuation. Candidate harm establishes a need to limit exposure, not compatibility of old code with current state. If old code rejects new rows, messages, credentials, or dependencies, rollback can worsen the incident.

### Answer 2

Decision time is $2(30)=60$ seconds, so total time is $45+60+150+180=435$ seconds. Under the homogeneous request-local model, expected incremental failures are $0.10\cdot2000\cdot435\cdot0.04=3480$. This estimate assumes stationary rate, correct exposure, homogeneous independent request effects, immediate attribution, and no shared or persistent harm. It does not bound corruption, security compromise, saturation, retries, or external effects.

### Answer 3

Verify the exact prior application, configuration, infrastructure, secrets, dependencies, capacity, provenance, and deployability. Confirm it can coexist with candidate instances and read every current database row, queue message, cache value, token, and API form. Check migration checkpoints, running backfills, lease ownership, and telemetry. Confirm the payment provider and credentials still accept the old integration. Database or message state may need a compatible reader, translation, or forward repair. A completed third-party payment cannot be undone by redeployment; idempotency prevents duplication, while refund or correction is a separately authorized compensating business action.

### Answer 4

Bind queries to candidate/control subjects and current rollout generation. One confirmed duplicate charge immediately contains: stop expansion, block new candidate payment admissions, preserve evidence, and select an eligible recovery action. For error or latency, require minimum samples and two complete windows beyond absolute SLO and declared candidate-control regression bounds; then contain and roll back only if eligibility is current. Require three healthy windows below a stricter recovery threshold before declaring recovery, followed by cooldown. If telemetry completeness or lag violates policy, halt expansion and use independent probes; do not treat missing points as health. Every action uses compare-and-swap on generation and records query, evidence, target, and outcome.

### Answer 5

Do not restore the vulnerable application. Immediately contain by disabling search through a rehearsed server-side operational control and stop release expansion if needed. Preserve the authoritative database, isolate or discard only the derived index under a bounded rebuild plan, and roll forward with a patch that writes and reads a corrected versioned index format while retaining the security fix. Verify application identity and vulnerability remediation, database correctness, disabled-search fallback, index rebuild progress, query correctness on sampled and adversarial data, error and latency objectives, dependency load, and absence of stale vulnerable instances. Re-enable search progressively only after those checks pass.
